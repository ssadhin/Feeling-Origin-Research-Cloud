#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import socket, threading, tempfile, subprocess, shutil, os, json, hashlib, time, resource

BASE=Path('/mnt/data')
CLIENT_C=r'''
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/socket.h>
#include <sys/un.h>

static int exchange(const char *path,const char *msg,char *out,size_t n){
  int s=socket(AF_UNIX,SOCK_STREAM,0); if(s<0)return -1;
  struct sockaddr_un a={0}; a.sun_family=AF_UNIX; strncpy(a.sun_path,path,sizeof(a.sun_path)-1);
  if(connect(s,(struct sockaddr*)&a,sizeof(a))<0){close(s);return -2;}
  write(s,msg,strlen(msg)); write(s,"\n",1);
  ssize_t r=read(s,out,n-1); if(r<0){close(s);return -3;} out[r]=0; close(s); return 0;
}
int main(){
  char a[4096]={0},b[4096]={0},c[4096]={0},d[4096]={0};
  int r1=exchange("/scratch/broker.sock","{\"op\":\"MODEL_CALL\",\"payload\":\"PUBLIC_ONLY_SENTINEL\"}",a,sizeof(a));
  int r2=exchange("/scratch/broker.sock","{\"op\":\"EVALUATE\",\"payload\":\"x\"}",b,sizeof(b));
  int r3=exchange("/scratch/broker.sock","{\"op\":\"WEB_FETCH\",\"payload\":\"http://example.com\"}",c,sizeof(c));
  int r4=exchange("/scratch/broker.sock","{\"op\":\"READ_HIDDEN\",\"payload\":\"answer_key\"}",d,sizeof(d));
  printf("{\"model_rc\":%d,\"model_response\":%s,\"eval_rc\":%d,\"eval_response\":%s,\"web_rc\":%d,\"web_response\":%s,\"hidden_rc\":%d,\"hidden_response\":%s}\n",r1,a,r2,b,r3,c,r4,d);
  return 0;
}
'''

def sha256(p:Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def compile_client(work:Path):
    src=work/'client.c'; exe=work/'client'; src.write_text(CLIENT_C)
    subprocess.run(['gcc','-O2','-Wall','-Wextra','-o',str(exe),str(src)],check=True)
    return exe

class Broker:
    def __init__(self,path:Path):
        self.path=path; self.logs=[]; self.meter={'input_tokens':0,'output_tokens':0,'model_calls':0,'denied_calls':0}
        self.sock=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        self.sock.bind(str(path)); os.chmod(path,0o666); self.sock.listen()
        self.stop=False
        self.t=threading.Thread(target=self.loop,daemon=True); self.t.start()
    def loop(self):
        self.sock.settimeout(.1)
        while not self.stop:
            try: c,_=self.sock.accept()
            except socket.timeout: continue
            except OSError: break
            with c:
                raw=b''
                while not raw.endswith(b'\n') and len(raw)<65536:
                    x=c.recv(4096)
                    if not x: break
                    raw+=x
                try: req=json.loads(raw.decode().strip())
                except Exception:
                    resp={'status':'DENIED','reason':'MALFORMED_SCHEMA'}; self.meter['denied_calls']+=1
                else:
                    op=req.get('op'); payload=req.get('payload')
                    if op=='MODEL_CALL' and isinstance(payload,str) and len(payload)<=10000:
                        # deterministic neutral worker stub. It has no hidden truth/evaluator handle.
                        usage={'input_tokens':len(payload.split())+4,'output_tokens':3,'reasoning_tokens':0}
                        resp={'status':'OK','output':'SENTINEL_RESPONSE','usage':usage}
                        self.meter['input_tokens']+=usage['input_tokens']; self.meter['output_tokens']+=usage['output_tokens']; self.meter['model_calls']+=1
                    else:
                        resp={'status':'DENIED','reason':'OP_NOT_ALLOWLISTED'}; self.meter['denied_calls']+=1
                self.logs.append({'request':req if 'req' in locals() else None,'response':resp})
                c.sendall(json.dumps(resp,separators=(',',':')).encode())
    def close(self):
        self.stop=True
        try:self.sock.close()
        except:pass
        self.t.join(timeout=1)


def run_once(client:Path):
    with tempfile.TemporaryDirectory(prefix='r2broker_') as td:
        base=Path(td); base.chmod(0o755); root=base/'root'; public=base/'public'; hidden=base/'hidden'
        for p in [root,public,hidden]: p.mkdir()
        (root/'bin').mkdir(); (root/'lib/x86_64-linux-gnu').mkdir(parents=True); (root/'lib64').mkdir(); (root/'public').mkdir(); (root/'scratch').mkdir()
        shutil.copy2(client,root/'bin/client'); shutil.copy2('/lib/x86_64-linux-gnu/libc.so.6',root/'lib/x86_64-linux-gnu/libc.so.6'); shutil.copy2('/lib64/ld-linux-x86-64.so.2',root/'lib64/ld-linux-x86-64.so.2')
        for p in [root,root/'bin',root/'lib',root/'lib/x86_64-linux-gnu',root/'lib64',root/'public',root/'scratch',public]: p.chmod(0o755)
        (root/'bin/client').chmod(0o755); (root/'lib/x86_64-linux-gnu/libc.so.6').chmod(0o755); (root/'lib64/ld-linux-x86-64.so.2').chmod(0o755)
        (public/'task.txt').write_text('PUBLIC_ONLY\n'); (public/'task.txt').chmod(0o444)
        (hidden/'answer_key.txt').write_text('NEVER_EXPOSE_THIS_MARKER\n')
        # Broker socket is created in scratch before chroot; this is the only mediated external channel.
        broker=Broker(root/'scratch/broker.sock')
        shell=r'''set -euo pipefail
PUBLIC="$1"; ROOT="$2"
mount --bind "$PUBLIC" "$ROOT/public"
mount -o remount,bind,ro "$ROOT/public"
chown 65534:65534 "$ROOT/scratch"
chmod 0666 "$ROOT/scratch/broker.sock"
exec chroot --userspec=65534:65534 "$ROOT" /bin/client
'''
        cmd=['unshare','--user','--map-users=0:0:1','--map-users=65534:65534:1','--map-groups=0:0:1','--map-groups=65534:65534:1','--mount','--propagation','private','--pid','--fork','--net','--uts','--ipc','bash','-c',shell,'_',str(public),str(root)]
        before=resource.getrusage(resource.RUSAGE_CHILDREN); t0=time.perf_counter()
        p=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=15,close_fds=True)
        wall=time.perf_counter()-t0; after=resource.getrusage(resource.RUSAGE_CHILDREN)
        cpu=(after.ru_utime-before.ru_utime)+(after.ru_stime-before.ru_stime)
        broker.close()
        out=json.loads(p.stdout.strip().splitlines()[-1])
        return out,broker.logs,broker.meter,cpu,wall

def main():
    with tempfile.TemporaryDirectory(prefix='r2brokerbuild_') as td:
        client=compile_client(Path(td))
        runs=[run_once(client) for _ in range(20)]
    tests=[]
    all_model=all(r[0]['model_rc']==0 and r[0]['model_response']['status']=='OK' for r in runs)
    all_deny=all(r[0]['eval_response']['status']=='DENIED' and r[0]['web_response']['status']=='DENIED' and r[0]['hidden_response']['status']=='DENIED' for r in runs)
    usage_ok=all(r[2]=={'input_tokens':5,'output_tokens':3,'model_calls':1,'denied_calls':3} for r in runs)
    no_secret=all('NEVER_EXPOSE_THIS_MARKER' not in json.dumps(r[0]) and 'NEVER_EXPOSE_THIS_MARKER' not in json.dumps(r[1]) for r in runs)
    op_allow=all([all(x['request'].get('op') in {'MODEL_CALL','EVALUATE','WEB_FETCH','READ_HIDDEN'} for x in r[1]) for r in runs])
    tests += [
      {'test_id':'BR-H001','status':'PASS' if all_model else 'FAIL','claim':'Allowlisted model broker channel works inside network-isolated contestant'},
      {'test_id':'BR-H002','status':'PASS' if all_deny else 'FAIL','claim':'Evaluator, web, and hidden-state operations are denied by broker'},
      {'test_id':'BR-H003','status':'PASS' if usage_ok else 'FAIL','claim':'Worker-returned usage is charged deterministically by broker meter'},
      {'test_id':'BR-H004','status':'PASS' if no_secret else 'FAIL','claim':'Planted hidden marker is absent from broker requests, responses, and contestant output'},
      {'test_id':'BR-H005','status':'PASS' if op_allow else 'FAIL','claim':'All broker traffic conforms to explicit request schema/op registry'},
      {'test_id':'BR-H006','status':'BLOCKED_REAL_PROVIDER','claim':'Actual provider usage telemetry and retry semantics require a frozen provider-backed worker'}
    ]
    result={'status':'DEVELOPMENT_ONLY_SYNTHETIC_BROKER_VALIDATION','runs':len(runs),'tests':tests,'sample':runs[0][0],'sample_meter':runs[0][2],'median_cpu_seconds':sorted(r[3] for r in runs)[len(runs)//2],'median_wall_seconds':sorted(r[4] for r in runs)[len(runs)//2],'scientific_controllers_run':0,'decisive_outcomes_opened':False,'interpretation':'Broker architecture and allowlisting pass with a deterministic stub worker. H011 remains BLOCKED until a real provider returns authoritative usage telemetry.'}
    out=BASE/'research2_mediated_worker_broker_v001_results.json'; out.write_text(json.dumps(result,indent=2))
    csvp=BASE/'research2_mediated_worker_broker_v001_results.csv'
    import csv
    with csvp.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['test_id','status','claim']); w.writeheader(); w.writerows(tests)
    print('Research #2 mediated worker broker v001')
    print('='*43)
    for t in tests: print(f"{t['test_id']:8s} {t['status']:22s} {t['claim']}")
    print('runs:',len(runs),'sample_meter:',runs[0][2])
    print('H011 remains BLOCKED_REAL_PROVIDER.')

if __name__=='__main__': main()
