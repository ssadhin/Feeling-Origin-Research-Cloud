from pathlib import Path
from datetime import datetime, timezone
import urllib.request, urllib.error, json, hashlib, time, os, sys

SECRET = Path.home() / "AppData" / "Local" / "Research2_gemini_authkey.tmp"
OUTDIR = Path.home() / "Research2" / "provider_sentinels"
BASE = "https://generativelanguage.googleapis.com/v1beta"
PROMPT = "Reply with exactly R2_SENTINEL_OK."
MODELS = ("gemini-3.5-flash-lite","gemini-3.1-flash-lite")
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()
def request(method, path, key, body=None):
    raw = json.dumps(body,sort_keys=True,separators=(',',':')).encode() if body is not None else None
    headers={"x-goog-api-key":key,"Content-Type":"application/json"}
    req=urllib.request.Request(BASE+path, data=raw, headers=headers,method=method)
    started=time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=75) as res:
            payload=json.loads(res.read(1000000).decode())
            return res.status, payload, {"x-request-id":res.headers.get("x-request-id"),"elapsed_ms":round((time.perf_counter()-started)*1000,1)}
    except urllib.error.HTTPError as ex:
        try:
            err=json.loads(ex.read(20000).decode())
            info={"error_status":err.get("error",{}).get("status")}
        except Exception: info={}
        return ex.code, {}, {"elapsed_ms":round((time.perf_counter()-started)*1000,1),**info}
    except Exception as ex:
        return None, {}, {"transport_error_type":type(ex).__name__}
def main():
    rec={"type":"R2_H011_GEMINI_REAL_PROVIDER_SENTINEL_RETRY_V002","utc":utc(),
      "secret_recorded":False,"decisive_runs":0,"max_successful_model_calls":1}
    key=None
    try:
        key=SECRET.read_text(encoding="utf8").strip()
        if not key: raise ValueError("EMPTY_AUTH_FILE")
        code,models,meta=request("GET","/models?pageSize=100",key)
        rec["model_listing_http"]=code
        rec["model_listing_meta"]=meta
        if code!=200:
            rec["status"]="BLOCKED_MODEL_LISTING"
            return rec
        available={m.get("name","").split("/")[-1] for m in models.get("models",[])
                   if "generateContent" in m.get("supportedGenerationMethods",[])}
        rec["available_model_count"]=len(available)
        chosen=next((m for m in MODELS if m in available),None)
        rec["selected_development_model"]=chosen
        if not chosen:
            rec["status"]="BLOCKED_NO_LISTED_STABLE_MODEL"
            return rec
        body={"contents":[{"role":"user","parts":[{"text":PROMPT}]}],
              "generationConfig":{"maxOutputTokens":32}}
        rec["public_request_sha256"]=sha(json.dumps(body,sort_keys=True,separators=(',',':')).encode())
        code,res,meta=request("POST",f"/models/{chosen}:generateContent",key,body)
        rec["generation_http"]=code
        rec["generation_meta"]=meta
        if code!=200:
            rec["status"]="GENERATION_TRANSPORT_ERROR" if code is None else "BLOCKED_GENERATION_HTTP"
            return rec
        rec["model_version_returned"]=res.get("modelVersion")
        rec["response_id"]=res.get("responseId")
        rec["usage_metadata_raw"]=res.get("usageMetadata")
        rec["finish_reasons"]=[c.get("finishReason") for c in res.get("candidates",[])]
        rec["output_is_expected_sentinel"]=any(
            PROMPT.split()[-1].rstrip('.') in p.get("text","")
            for c in res.get("candidates",[])
            for p in c.get("content",{}).get("parts",[]))
        rec["raw_response_sha256"]=sha(json.dumps(res,sort_keys=True).encode())
        usage=rec["usage_metadata_raw"]
        valid=isinstance(usage,dict) and all(isinstance(usage.get(x),int) and usage[x]>=0 for x in ("promptTokenCount","candidatesTokenCount","totalTokenCount"))
        rec["status"]="REAL_PROVIDER_USAGE_OBSERVED" if valid and rec["model_version_returned"] else "PARTIAL_PROVIDER_METADATA"
        return rec
    except Exception as ex:
        rec["status"]="LOCAL_PROBE_ERROR"
        rec["exception_type"]=type(ex).__name__
        return rec
    finally:
        if SECRET.exists():
            try:SECRET.unlink()
            except OSError:rec["key_file_cleanup_failed"]=True
        rec["key_file_deleted"]=not SECRET.exists()
        rec["utc_completed"]=utc()
        rec["metadata_sha256"]=sha(json.dumps(rec,sort_keys=True).encode())
        OUTDIR.mkdir(parents=True,exist_ok=True)
        outfile=OUTDIR/("h011_gemini_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+".json")
        outfile.write_text(json.dumps(rec,indent=2,sort_keys=True)+"\n",encoding="utf8")
        summary={k:rec.get(k) for k in ("status","model_listing_http","generation_http","selected_development_model","model_version_returned","usage_metadata_raw","finish_reasons","key_file_deleted","metadata_sha256")}
        print(json.dumps(summary,indent=2))
        print("EVIDENCE_PATH:",str(outfile))
if __name__=="__main__":main()
