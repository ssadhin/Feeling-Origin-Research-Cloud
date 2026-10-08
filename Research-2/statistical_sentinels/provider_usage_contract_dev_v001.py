"""Research #2 provider-usage contract DEV sentinel (no network/API calls).

Validates only the structure of *claimed* provider response usage.
An untrusted caller can fabricate a payload; this NEVER closes H011 by itself.
"""
from __future__ import annotations
import hashlib,json,math,unittest

def observed_usage(event):
    if not isinstance(event,dict) or event.get("usage_origin")!="provider_response":
        return {"status":"BLOCKED_NONAUTHORITATIVE_USAGE"}
    if event.get("model_source")!="provider_response":
        return {"status":"BLOCKED_MODEL_ID_NOT_RETURNED"}
    model=event.get("returned_model")
    if not isinstance(model,str) or not model.strip():
        return {"status":"BLOCKED_MISSING_RETURNED_MODEL"}
    if event.get("synthetic") is True or event.get("locally_estimated") is True:
        return {"status":"BLOCKED_SYNTHETIC_OR_ESTIMATED"}
    provider=event.get("provider")
    raw=event.get("raw_usage")
    if not isinstance(raw,dict):
        return {"status":"BLOCKED_MISSING_RAW_USAGE"}
    if provider=="openai":
        necessary=("input_tokens","output_tokens","total_tokens")
        if not all(k in raw for k in necessary):
            return {"status":"BLOCKED_MISSING_USAGE_FIELDS"}
        i,o,t=[raw[k] for k in necessary]
        if not all(type(x)==int and x>=0 for x in (i,o,t)):
            return {"status":"BLOCKED_INVALID_USAGE_VALUES"}
        if t!=i+o:
            return {"status":"BLOCKED_INCONSISTENT_TOTAL"}
        for group,key,parent in [("input_tokens_details","cached_tokens",i),
                                 ("output_tokens_details","reasoning_tokens",o)]:
            if group in raw and isinstance(raw[group],dict) and key in raw[group]:
                x=raw[group][key]
                if type(x)!=int or not 0<=x<=parent:
                    return {"status":"BLOCKED_INVALID_USAGE_BREAKDOWN"}
    elif provider=="anthropic":
        necessary=("input_tokens","output_tokens")
        if not all(k in raw for k in necessary):
            return {"status":"BLOCKED_MISSING_USAGE_FIELDS"}
        if any(type(raw[k])!=int or raw[k]<0 for k in necessary):
            return {"status":"BLOCKED_INVALID_USAGE_VALUES"}
        for k in ("cache_creation_input_tokens","cache_read_input_tokens"):
            if k in raw and (type(raw[k])!=int or raw[k]<0):
                return {"status":"BLOCKED_INVALID_CACHE_USAGE"}
        # Deliberately do NOT synthesize total tokens from Anthropic native usage.
    else:
        return {"status":"BLOCKED_UNFROZEN_PROVIDER_SCHEMA"}
    clean={"provider":provider,"returned_model":model,"raw_usage":raw,
           "provider_request_id":event.get("provider_request_id"),
           "attempt":event.get("attempt"),"finish_metadata":event.get("finish_metadata")}
    blob=json.dumps(clean,sort_keys=True,separators=(",",":"),ensure_ascii=False)
    return {"status":"STRUCTURE_PASS_PROVIDER_ORIGIN_UNVERIFIED",
            "commitment_sha256":hashlib.sha256(blob.encode("utf-8")).hexdigest(),
            "record":clean}

class ProviderContractTests(unittest.TestCase):
    def openai(self,**u):
        d={"provider":"openai","usage_origin":"provider_response","model_source":"provider_response",
           "returned_model":"fictional-development-model","raw_usage":{"input_tokens":12,"output_tokens":8,"total_tokens":20},
           "synthetic":False,"locally_estimated":False}
        d.update(u);return observed_usage(d)
    def test_structural_valid(self):
        self.assertEqual(self.openai()["status"],"STRUCTURE_PASS_PROVIDER_ORIGIN_UNVERIFIED")
    def test_missing_usage(self):
        self.assertEqual(self.openai(raw_usage={})["status"],"BLOCKED_MISSING_USAGE_FIELDS")
    def test_missing_model(self):
        self.assertEqual(self.openai(returned_model="")["status"],"BLOCKED_MISSING_RETURNED_MODEL")
    def test_configured_not_returned_model(self):
        self.assertEqual(self.openai(model_source="configured_request")["status"],"BLOCKED_MODEL_ID_NOT_RETURNED")
    def test_locally_estimated(self):
        self.assertEqual(self.openai(usage_origin="estimated")["status"],"BLOCKED_NONAUTHORITATIVE_USAGE")
    def test_fake_flag(self):
        self.assertEqual(self.openai(synthetic=True)["status"],"BLOCKED_SYNTHETIC_OR_ESTIMATED")
    def test_negative_usage(self):
        self.assertEqual(self.openai(raw_usage={"input_tokens":-1,"output_tokens":3,"total_tokens":2})["status"],"BLOCKED_INVALID_USAGE_VALUES")
    def test_mismatch_total(self):
        self.assertEqual(self.openai(raw_usage={"input_tokens":12,"output_tokens":8,"total_tokens":21})["status"],"BLOCKED_INCONSISTENT_TOTAL")
    def test_reasoning_exceeds_output(self):
        x={"input_tokens":12,"output_tokens":8,"total_tokens":20,"output_tokens_details":{"reasoning_tokens":10}}
        self.assertEqual(self.openai(raw_usage=x)["status"],"BLOCKED_INVALID_USAGE_BREAKDOWN")
    def test_cached_exceeds_input(self):
        x={"input_tokens":12,"output_tokens":8,"total_tokens":20,"input_tokens_details":{"cached_tokens":14}}
        self.assertEqual(self.openai(raw_usage=x)["status"],"BLOCKED_INVALID_USAGE_BREAKDOWN")
    def test_boolean_not_int(self):
        x={"input_tokens":True,"output_tokens":8,"total_tokens":9}
        self.assertEqual(self.openai(raw_usage=x)["status"],"BLOCKED_INVALID_USAGE_VALUES")
    def test_deterministic_commitment(self):
        self.assertEqual(self.openai()["commitment_sha256"],self.openai()["commitment_sha256"])
    def test_distinct_usage_changes_commitment(self):
        a=self.openai()["commitment_sha256"]
        b=self.openai(raw_usage={"input_tokens":10,"output_tokens":8,"total_tokens":18})["commitment_sha256"]
        self.assertNotEqual(a,b)
    def test_anthropic_usage_preserves_native_counter(self):
        d={"provider":"anthropic","usage_origin":"provider_response","model_source":"provider_response",
           "returned_model":"fictional-development-anthropic-model","raw_usage":{"input_tokens":3,"output_tokens":7,
               "cache_creation_input_tokens":10,"cache_read_input_tokens":5}}
        ans=observed_usage(d)
        self.assertEqual(ans["status"],"STRUCTURE_PASS_PROVIDER_ORIGIN_UNVERIFIED")
        self.assertNotIn("total_tokens",ans["record"]["raw_usage"])
    def test_unrecognized_provider_blocks(self):
        self.assertEqual(self.openai(provider="other")["status"],"BLOCKED_UNFROZEN_PROVIDER_SCHEMA")
if __name__=="__main__":
    unittest.main(verbosity=2)
