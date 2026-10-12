"""Read-only source identity verifier, NOT full behavioral runner or decisive test."""
import hashlib
import urllib.request
BASE = "https://raw.githubusercontent.com/SakanaAI/AI-Scientist-v2/"
PIN = "96bd51617cfdbb494a9fc283af00fe090edfae48"
SOURCES = {
 "callback": ("ai_scientist/treesearch/perform_experiments_bfts_with_agentmanager.py",
              "7779630b31b5d20f87da35bf13ead89e0953a4ac", 2065, "0735cc2c"),
 "save": ("ai_scientist/treesearch/utils/config.py",
          "aaeba6780fb978ddfa3f8cf7101ec28740821f51", 1510, "475aee27")
}
def fnv(s):
    h=2166136261
    for ch in s:
        h=((h ^ ord(ch))*16777619)&0xffffffff
    return f"{h:08x}"
for name,(path,blob,n,expected) in SOURCES.items():
    raw=urllib.request.urlopen(BASE+PIN+"/"+path,timeout=15).read()
    actual_blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\\0"+raw).hexdigest()
    assert actual_blob==blob,(name,"blob mismatch")
    s=raw.decode().replace("\\r\\n","\\n")
    if name=="callback":
        s=s[s.index("    def step_callback(stage, journal):"):s.index("    def generate_live(manager):")]
        s="\\n".join(line[4:] if line.startswith("    ") else line for line in s.split("\\n")).rstrip()
    else:
        s=s[s.index("def save_run(cfg: Config, journal, stage_name: str = None):"):].rstrip()
    assert len(s)==n and fnv(s)==expected,(name,len(s),fnv(s))
    print(name,"source identity PASS",blob)
print("Static source identity verified; this does not replay dynamic fault injection.")
