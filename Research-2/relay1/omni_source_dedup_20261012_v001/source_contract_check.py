"""Bounded source-contract check, pinned OmniScientist-V2 1cbb9f6f6d793290326ca29df4d389fb64832f91.
store.py Git blob 01fd379c4e109e5652014516c3c204837be8ec58.
NOT full native ResearchStore/19C certification.
"""
import re, hashlib, json
def source_dedup_key(meta):
    for field in ("arxiv_id","doi"):
        val=str(meta.get(field) or "").strip().lower()
        if val: return f"{field}:{val}"
    url=str(meta.get("url") or meta.get("abs_url") or "").strip().lower()
    if url: return f"url:{url}"
    return "title:"+re.sub(r"\\s+"," ",str(meta.get("title") or "").strip().lower())
a={"title":"Introduction to Agent Evaluation","authors":["A. One"],"year":"2024","summary":"Positive effect."}
b={"title":"Introduction to Agent Evaluation","authors":["B. Two"],"year":"2026","summary":"Negative effect."}
assert source_dedup_key(a)==source_dedup_key(b)
assert source_dedup_key({"doi":"10.1/a"})!=source_dedup_key({"doi":"10.1/b"})
assert source_dedup_key({"url":"https://a.example"})!=source_dedup_key({"url":"https://b.example"})
assert source_dedup_key({"arxiv_id":"1"})!=source_dedup_key({"arxiv_id":"2"})
key=source_dedup_key(a)
print(json.dumps({"same_title_key":key,"would_collide":True,"hash_formula":hashlib.sha256((a["title"]+key).encode()).hexdigest()[:16]},sort_keys=True))
