#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import subprocess, tempfile, os, json, time, resource, statistics
import hashlib, platform, socket, threading, contextlib, shutil, csv

PROBE_C = r'''
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <signal.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mount.h>
#include <sys/syscall.h>
#include <linux/capability.h>

static int exists_read(const char *p){
    int fd=open(p,O_RDONLY);
    if(fd>=0){close(fd); return 1;}
    return 0;
}
static int can_write(const char *p){
    int fd=open(p,O_WRONLY|O_APPEND);
    if(fd>=0){write(fd,"X",1);close(fd);return 1;}
    return 0;
}
static int can_connect(const char *ip,int port,int *err){
    int s=socket(AF_INET,SOCK_STREAM,0);
    if(s<0){*err=errno;return 0;}
    struct sockaddr_in a={0};
    a.sin_family=AF_INET;
    a.sin_port=htons(port);
    inet_pton(AF_INET,ip,&a.sin_addr);
    int rc=connect(s,(struct sockaddr*)&a,sizeof(a));
    *err=(rc==0)?0:errno;
    close(s);
    return rc==0;
}
static unsigned long long caps_eff(){
    struct __user_cap_header_struct h={_LINUX_CAPABILITY_VERSION_3,0};
    struct __user_cap_data_struct d[2]={{0}};
    if(syscall(SYS_capget,&h,d)<0)return ~0ULL;
    return ((unsigned long long)d[1].effective<<32)|d[0].effective;
}
static unsigned long long burn(unsigned long long n){
    volatile unsigned long long x=0x9e3779b97f4a7c15ULL;
    for(unsigned long long i=0;i<n;i++){
        x ^= (i + 0x9e3779b97f4a7c15ULL + (x<<6) + (x>>2));
        x = x*6364136223846793005ULL + 1442695040888963407ULL;
    }
    return x;
}

int main(int argc,char **argv){
    int port=argc>1?atoi(argv[1]):9;
    int hostpid=argc>2?atoi(argv[2]):-1;
    unsigned long long iters=argc>3?strtoull(argv[3],NULL,10):0ULL;

    int e1=0,e2=0;
    int external=can_connect("1.1.1.1",80,&e1);
    int hostlocal=can_connect("127.0.0.1",port,&e2);

    int pub=exists_read("/public/task.txt");
    int secret=
        exists_read("/hidden/answer_key.txt") ||
        exists_read("/../hidden/answer_key.txt") ||
        exists_read("/mnt/data/answer_key.txt");
    int proc=exists_read("/proc/1/status");
    int wpub=can_write("/public/task.txt");

    int fd=open("/scratch/output.txt",O_WRONLY|O_CREAT|O_TRUNC,0644);
    int ws=0;
    if(fd>=0){ws=(write(fd,"ok\n",3)==3);close(fd);}

    errno=0;
    int host_pid_visible=(hostpid>0 && kill(hostpid,0)==0);
    int host_pid_errno=host_pid_visible?0:errno;

    errno=0;
    int su=(setuid(0)==0);
    int su_errno=su?0:errno;

    errno=0;
    int cr=(chroot("/scratch")==0);
    int cr_errno=cr?0:errno;

    mkdir("/scratch/m",0700);
    errno=0;
    int mo=(mount("tmpfs","/scratch/m","tmpfs",0,"size=4k")==0);
    int mo_errno=mo?0:errno;

    unsigned long long checksum=burn(iters);

    printf(
      "{\"uid\":%d,\"gid\":%d,\"pid\":%d,"
      "\"caps_eff\":%llu,"
      "\"public_read\":%s,\"hidden_read\":%s,\"proc_visible\":%s,"
      "\"public_write\":%s,\"scratch_write\":%s,"
      "\"external_connect\":%s,\"external_errno\":%d,"
      "\"hostlocal_connect\":%s,\"hostlocal_errno\":%d,"
      "\"host_pid_visible\":%s,\"host_pid_errno\":%d,"
      "\"setuid0\":%s,\"setuid0_errno\":%d,"
      "\"chroot_escape_capable\":%s,\"chroot_errno\":%d,"
      "\"mount_capable\":%s,\"mount_errno\":%d,"
      "\"burn_iters\":%llu,\"checksum\":%llu}\n",
      (int)getuid(),(int)getgid(),(int)getpid(),
      caps_eff(),
      pub?"true":"false",secret?"true":"false",proc?"true":"false",
      wpub?"true":"false",ws?"true":"false",
      external?"true":"false",e1,
      hostlocal?"true":"false",e2,
      host_pid_visible?"true":"false",host_pid_errno,
      su?"true":"false",su_errno,
      cr?"true":"false",cr_errno,
      mo?"true":"false",mo_errno,
      iters,checksum
    );
    return 0;
}
'''

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

@contextlib.contextmanager
def local_server():
    srv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    srv.bind(("127.0.0.1",0))
    srv.listen()
    port=srv.getsockname()[1]
    stop=threading.Event()
    def loop():
        srv.settimeout(.1)
        while not stop.is_set():
            try:
                c,_=srv.accept()
                c.sendall(b"EVALUATOR_ENDPOINT\n")
                c.close()
            except socket.timeout:
                pass
            except OSError:
                break
    t=threading.Thread(target=loop,daemon=True)
    t.start()
    try:
        yield port, os.getpid()
    finally:
        stop.set()
        srv.close()
        t.join(timeout=1)

def compile_probe(work: Path) -> Path:
    src=work/"sandbox_probe.c"
    exe=work/"sandbox_probe"
    src.write_text(PROBE_C)
    subprocess.run(["gcc","-O2","-Wall","-Wextra","-o",str(exe),str(src)],check=True)
    return exe

def copy_runtime(root: Path, probe: Path):
    (root/"bin").mkdir(parents=True)
    (root/"lib/x86_64-linux-gnu").mkdir(parents=True)
    (root/"lib64").mkdir(parents=True)
    (root/"public").mkdir()
    (root/"scratch").mkdir()
    shutil.copy2(probe,root/"bin/probe")
    shutil.copy2("/lib/x86_64-linux-gnu/libc.so.6",root/"lib/x86_64-linux-gnu/libc.so.6")
    shutil.copy2("/lib64/ld-linux-x86-64.so.2",root/"lib64/ld-linux-x86-64.so.2")
    for p in [root,root/"bin",root/"lib",root/"lib/x86_64-linux-gnu",root/"lib64",root/"public",root/"scratch"]:
        p.chmod(0o755)
    (root/"bin/probe").chmod(0o755)
    (root/"lib/x86_64-linux-gnu/libc.so.6").chmod(0o755)
    (root/"lib64/ld-linux-x86-64.so.2").chmod(0o755)

def run_sandbox(probe: Path, port: int, host_pid: int, burn_iters: int=0):
    with tempfile.TemporaryDirectory(prefix="r2sandbox_") as td:
        base=Path(td); base.chmod(0o755)
        root=base/"root"; public=base/"public_source"; hidden=base/"hidden"
        root.mkdir(); public.mkdir(); hidden.mkdir()
        public.chmod(0o755); hidden.chmod(0o700)
        copy_runtime(root,probe)

        (public/"task.txt").write_text("PUBLIC_TASK_ONLY\n")
        (public/"task.txt").chmod(0o666)
        (hidden/"answer_key.txt").write_text("TOP_SECRET_ANSWER_KEY\n")
        (hidden/"evaluator_private.txt").write_text("PRIVATE_EVALUATOR_STATE\n")

        shell = r'''
set -euo pipefail
PUBLIC="$1"
ROOT="$2"
PORT="$3"
HOSTPID="$4"
ITERS="$5"
mount --bind "$PUBLIC" "$ROOT/public"
mount -o remount,bind,ro "$ROOT/public"
chown 65534:65534 "$ROOT/scratch"
exec chroot --userspec=65534:65534 "$ROOT" /bin/probe "$PORT" "$HOSTPID" "$ITERS"
'''
        cmd=[
            "unshare",
            "--user",
            "--map-users=0:0:1",
            "--map-users=65534:65534:1",
            "--map-groups=0:0:1",
            "--map-groups=65534:65534:1",
            "--mount","--propagation","private",
            "--pid","--fork",
            "--net","--uts","--ipc",
            "bash","-c",shell,
            "_",str(public),str(root),str(port),str(host_pid),str(burn_iters)
        ]

        before=resource.getrusage(resource.RUSAGE_CHILDREN)
        t0=time.perf_counter()
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=15,check=True,close_fds=True)
        wall=time.perf_counter()-t0
        after=resource.getrusage(resource.RUSAGE_CHILDREN)
        cpu=(after.ru_utime-before.ru_utime)+(after.ru_stime-before.ru_stime)

        lines=[x.strip() for x in p.stdout.splitlines() if x.strip()]
        data=json.loads(lines[-1])
        data["metered_cpu_seconds"]=cpu
        data["metered_wall_seconds"]=wall
        data["host_public_unchanged"]=(public/"task.txt").read_text()=="PUBLIC_TASK_ONLY\n"
        data["scratch_roundtrip"]=(root/"scratch/output.txt").read_text()=="ok\n"
        data["stderr"]=p.stderr.strip()
        return data

def isolation_pass(d):
    return all([
        d["uid"]==65534,
        d["gid"]==65534,
        d["caps_eff"]==0,
        d["public_read"] is True,
        d["hidden_read"] is False,
        d["proc_visible"] is False,
        d["public_write"] is False,
        d["scratch_write"] is True,
        d["external_connect"] is False,
        d["hostlocal_connect"] is False,
        d["host_pid_visible"] is False,
        d["setuid0"] is False,
        d["chroot_escape_capable"] is False,
        d["mount_capable"] is False,
        d["host_public_unchanged"] is True,
        d["scratch_roundtrip"] is True,
    ])

def main():
    missing=[x for x in ["gcc","unshare","chroot","mount"] if shutil.which(x) is None]
    if missing:
        raise SystemExit(f"Missing required runtime tools: {missing}")

    with tempfile.TemporaryDirectory(prefix="r2build_") as bd:
        probe=compile_probe(Path(bd))
        with local_server() as (port,host_pid):
            stress=[run_sandbox(probe,port,host_pid,0) for _ in range(30)]
            low=[run_sandbox(probe,port,host_pid,5_000_000) for _ in range(5)]
            high=[run_sandbox(probe,port,host_pid,25_000_000) for _ in range(5)]

    isolation_ok=all(isolation_pass(x) for x in stress+low+high)
    low_cpu=statistics.median(x["metered_cpu_seconds"] for x in low)
    high_cpu=statistics.median(x["metered_cpu_seconds"] for x in high)
    cpu_ratio=high_cpu/max(low_cpu,1e-9)
    cpu_accounting_ok=(high_cpu>low_cpu and cpu_ratio>2.0)
    first=stress[0]

    tests=[
      {"test_id":"RT-H009","status":"PASS_LOCAL_RUNTIME" if isolation_ok else "FAIL",
       "claim":"Process/filesystem contestant isolation",
       "evidence":{"stress_runs":len(stress),"contestant_uid":first["uid"],"contestant_gid":first["gid"],
                   "effective_capabilities":first["caps_eff"],"host_pid_visible":first["host_pid_visible"],
                   "proc_visible":first["proc_visible"],"hidden_truth_readable":first["hidden_read"],
                   "public_read":first["public_read"],"public_write":first["public_write"],
                   "scratch_write":first["scratch_write"],"setuid0_succeeded":first["setuid0"],
                   "chroot_succeeded_from_contestant":first["chroot_escape_capable"],
                   "mount_succeeded_from_contestant":first["mount_capable"]}},
      {"test_id":"RT-H010","status":"PASS_LOCAL_RUNTIME" if isolation_ok else "FAIL",
       "claim":"Raw contestant network and host-local evaluator endpoint isolation",
       "evidence":{"external_connect":first["external_connect"],"external_errno":first["external_errno"],
                   "hostlocal_evaluator_connect":first["hostlocal_connect"],"hostlocal_errno":first["hostlocal_errno"],
                   "note":"Provider/model calls must be mediated by the harness outside this namespace."}},
      {"test_id":"RT-H011","status":"BLOCKED","claim":"Actual provider token/accounting telemetry",
       "evidence":{"reason":"No frozen provider-backed worker/API billing telemetry was invoked in this local sandbox test."}},
      {"test_id":"RT-H012A","status":"PASS_LOCAL_RUNTIME" if cpu_accounting_ok else "FAIL",
       "claim":"Subprocess CPU and wall-time accounting",
       "evidence":{"low_burn_iters":5_000_000,"high_burn_iters":25_000_000,
                   "low_median_cpu_s":low_cpu,"high_median_cpu_s":high_cpu,
                   "high_to_low_cpu_ratio":cpu_ratio,
                   "low_median_wall_s":statistics.median(x["metered_wall_seconds"] for x in low),
                   "high_median_wall_s":statistics.median(x["metered_wall_seconds"] for x in high)}},
      {"test_id":"RT-H012B","status":"BLOCKED_OR_NA","claim":"GPU accounting",
       "evidence":{"reason":"No GPU device/workload is exposed here. GPU accounting remains required if the frozen primary arm permits GPU use."}},
      {"test_id":"RT-H019","status":"PARTIAL_LOCAL_MANIFEST","claim":"Code/environment provenance",
       "evidence":{"reason":"Local executable/environment hashes are produced, but immutable Research 2 repository provenance remains unavailable."}},
      {"test_id":"RT-H023","status":"PASS_LOCAL_RUNTIME" if isolation_ok else "FAIL",
       "claim":"External answer-source blocking at contestant sandbox layer",
       "evidence":{"hidden_truth_readable":first["hidden_read"],"external_network_reachable":first["external_connect"],
                   "hostlocal_evaluator_reachable":first["hostlocal_connect"],"public_bundle_read_only":not first["public_write"],
                   "note":"End-to-end provider/tool broker allowlisting must still be validated when the real worker is attached."}},
    ]

    env={
      "development_only":True,
      "scientific_controllers_run":0,
      "aes_vs_comparator_outcomes_opened":False,
      "platform":platform.platform(),
      "python":platform.python_version(),
      "kernel":platform.release(),
      "sandbox_mechanisms":["user_namespace","mount_namespace","pid_namespace","network_namespace","uts_namespace",
                            "ipc_namespace","chroot","uid_gid_drop","capability_drop","read_only_public_bind",
                            "private_scratch","no_proc_mount"],
      "probe_source_sha256":hashlib.sha256(PROBE_C.encode()).hexdigest(),
      "this_script_sha256":sha256_file(Path(__file__).resolve()),
    }

    out={
      "status":"DEVELOPMENT_ONLY_LOCAL_RUNTIME_VALIDATION",
      "tests":tests,
      "stress_summary":{"total_isolation_runs":len(stress)+len(low)+len(high),
                        "all_isolation_invariants_pass":isolation_ok,
                        "sample_probe_output":{k:v for k,v in first.items() if k!="stderr"}},
      "environment":env,
      "remaining_decisive_blockers":["H011 actual frozen provider token/resource telemetry",
                                     "H012 GPU accounting if GPU use remains permitted",
                                     "H019 immutable Research 2 repository/container provenance",
                                     "end-to-end mediated provider/tool broker integration under the frozen worker architecture",
                                     "final comparator fidelity/resource/model/preregistration freezes"]
    }

    Path("research2_real_runtime_sandbox_v003_results.json").write_text(json.dumps(out,indent=2))
    Path("research2_real_runtime_environment_manifest_v003.json").write_text(json.dumps(env,indent=2))
    with open("research2_real_runtime_sandbox_v003_results.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["test_id","status","claim","evidence_json"])
        w.writeheader()
        for t in tests:
            w.writerow({"test_id":t["test_id"],"status":t["status"],"claim":t["claim"],
                        "evidence_json":json.dumps(t["evidence"],sort_keys=True)})

    print("Research #2 real-runtime sandbox v003")
    print("="*47)
    for t in tests:
        print(f"{t['test_id']:9s} {t['status']:23s} {t['claim']}")
    print()
    print(f"Isolation launches: {len(stress)+len(low)+len(high)}; all invariants pass: {isolation_ok}")
    print(f"Contestant UID/GID: {first['uid']}/{first['gid']}; effective capabilities: {first['caps_eff']}")
    print(f"Hidden truth readable: {first['hidden_read']}; /proc visible: {first['proc_visible']}; host PID visible: {first['host_pid_visible']}")
    print(f"External network reachable: {first['external_connect']}; host-local evaluator reachable: {first['hostlocal_connect']}")
    print(f"Public bundle writable: {first['public_write']}; private scratch writable: {first['scratch_write']}")
    print(f"CPU meter median low/high: {low_cpu:.4f}s / {high_cpu:.4f}s (ratio {cpu_ratio:.2f}x)")
    print()
    print("Decisive harness remains NOT READY: H011, immutable provenance, and real provider-broker integration are still open.")

if __name__=="__main__":
    main()
