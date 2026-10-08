"""Research #2 NONDECISIVE Gemini provider-returned usage parser and guard tests.
No API access, no credentials, no frozen experiment policy. Native provider tokens
are NOT cross-provider-comparable and prompt cached tokens are not extra work.
Official schema: https://ai.google.dev/api/generate-content
"""
import json, unittest
from pathlib import Path

class UsageError(ValueError):pass

def require_token(value,name):
    if type(value) is not int or value < 0:
        raise UsageError(name + " must be a non-negative provider integer")
    return value

def parse_gemini_evidence(evidence):
    if not isinstance(evidence,dict):raise UsageError("No evidence object")
    if evidence.get("generation_http")!=200 or evidence.get("status")!="REAL_PROVIDER_USAGE_OBSERVED":
        raise UsageError("No successful generation")
    requested=evidence.get("selected_development_model")
    actual=evidence.get("model_version_returned")
    if not isinstance(requested,str) or not requested or not isinstance(actual,str) or not actual:
        raise UsageError("Missing exact model identity")
    if requested!=actual:
        raise UsageError("Model identity drift; no silent alias acceptance")
    if not isinstance(evidence.get("response_id"),str) or not evidence["response_id"]:
        raise UsageError("Missing provider response ID")
    raw=evidence.get("usage_metadata_raw")
    if not isinstance(raw,dict):raise UsageError("No provider usage")
    a=require_token(raw.get("promptTokenCount"),"promptTokenCount")
    b=require_token(raw.get("candidatesTokenCount"),"candidatesTokenCount")
    c=require_token(raw.get("totalTokenCount"),"totalTokenCount")
    thought=raw.get("thoughtsTokenCount")
    cached=raw.get("cachedContentTokenCount")
    tool=raw.get("toolUsePromptTokenCount")
    if thought is not None:thought=require_token(thought,"thoughtsTokenCount")
    if cached is not None:cached=require_token(cached,"cachedContentTokenCount")
    if tool is not None:tool=require_token(tool,"toolUsePromptTokenCount")
    if c<a+b+(thought if thought is not None else 0):
        raise UsageError("Provider total smaller than mandatory prompt/output/thought subtotal")
    if cached is not None and cached>a:raise UsageError("Cached tokens exceed prompt total")
    return {"provider":"gemini","model_requested":requested,"model_returned":actual,
        "response_id":evidence["response_id"],"input_tokens":a,"candidate_tokens":b,
        "total_tokens":c,"thought_tokens":thought,"cached_prompt_tokens":cached,
        "tool_use_prompt_tokens":tool,"native_usage":dict(raw),
        "accounting_source":"provider-reported","dollar_cost":None,
        "full_harness_resource_parity":False}

def fixture(**kwargs):
    item={"status":"REAL_PROVIDER_USAGE_OBSERVED","generation_http":200,
          "selected_development_model":"gemini-3.5-flash-lite",
          "model_version_returned":"gemini-3.5-flash-lite","response_id":"opaque-dev-id",
          "usage_metadata_raw":{"promptTokenCount":13,"candidatesTokenCount":8,"totalTokenCount":21}}
    item.update(kwargs)
    return item

class TestGeminiAccounting(unittest.TestCase):
    def test_accept_real_shape(self):
        self.assertEqual(parse_gemini_evidence(fixture())["total_tokens"],21)
    def test_missing_usage(self):
        with self.assertRaises(UsageError):parse_gemini_evidence(fixture(usage_metadata_raw=None))
    def test_missing_identity(self):
        with self.assertRaises(UsageError):parse_gemini_evidence(fixture(model_version_returned=None))
    def test_model_drift(self):
        with self.assertRaises(UsageError):parse_gemini_evidence(fixture(model_version_returned="different"))
    def test_missing_response_id(self):
        with self.assertRaises(UsageError):parse_gemini_evidence(fixture(response_id=None))
    def test_failed_http_no_interpolation(self):
        with self.assertRaises(UsageError):parse_gemini_evidence(fixture(generation_http=None))
    def test_negative_tokens(self):
        with self.assertRaises(UsageError):parse_gemini_evidence(fixture(usage_metadata_raw={"promptTokenCount":-1,"candidatesTokenCount":8,"totalTokenCount":21}))
    def test_bool_token_rejected(self):
        with self.assertRaises(UsageError):parse_gemini_evidence(fixture(usage_metadata_raw={"promptTokenCount":True,"candidatesTokenCount":8,"totalTokenCount":21}))
    def test_total_smaller_than_parts(self):
        with self.assertRaises(UsageError):parse_gemini_evidence(fixture(usage_metadata_raw={"promptTokenCount":13,"candidatesTokenCount":8,"totalTokenCount":20}))
    def test_thought_tokens_preserved(self):
        out=parse_gemini_evidence(fixture(usage_metadata_raw={"promptTokenCount":13,"candidatesTokenCount":8,"thoughtsTokenCount":5,"totalTokenCount":26}))
        self.assertEqual(out["thought_tokens"],5)
    def test_cache_included_in_input_not_added(self):
        out=parse_gemini_evidence(fixture(usage_metadata_raw={"promptTokenCount":13,"candidatesTokenCount":8,"totalTokenCount":21,"cachedContentTokenCount":7}))
        self.assertEqual((out["total_tokens"],out["cached_prompt_tokens"]),(21,7))
    def test_cache_gt_prompt_rejected(self):
        with self.assertRaises(UsageError):parse_gemini_evidence(fixture(usage_metadata_raw={"promptTokenCount":13,"candidatesTokenCount":8,"totalTokenCount":21,"cachedContentTokenCount":14}))
    def test_no_dollar_cost_invented(self):
        self.assertIsNone(parse_gemini_evidence(fixture())["dollar_cost"])
    def test_actual_eon_proof(self):
        path=Path.home()/"Research2"/"provider_sentinels"/"h011_gemini_20261008T052326Z.json"
        obj=json.loads(path.read_text(encoding="utf-8"))
        out=parse_gemini_evidence(obj)
        self.assertEqual((out["input_tokens"],out["candidate_tokens"],out["total_tokens"]),(13,8,21))
        self.assertEqual(out["model_returned"],"gemini-3.5-flash-lite")

if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(TestGeminiAccounting)
    res=unittest.TextTestRunner(verbosity=0).run(suite)
    print(json.dumps({"gate":"GEMINI_H011_NEUTRAL_USAGE_PARSER_DEVELOPMENT","tests_passed":res.testsRun-len(res.failures)-len(res.errors),"tests_run":res.testsRun,"real_eon_fixture":True,"freeze_status":"NOT_FROZEN","decisive_trials":0}))
    if not res.wasSuccessful():raise SystemExit(1)
