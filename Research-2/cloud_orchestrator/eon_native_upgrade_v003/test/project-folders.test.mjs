import test from "node:test";
import assert from "node:assert/strict";
import {projectId,folderPath,insideFolder,outputCandidate,handlePolicy,contextHint,enhancedTools,catalogPolicy} from "../src/eon-project-folders.js";

class D1Mock {
 constructor(){this.projects=new Map();this.chats=new Map();}
 prepare(query){
  const db=this;
  function bound(...params){
   const ws=params[0],id=params[1];const key=ws+"|"+id;
   return {
    async run(){
      if(query.startsWith("CREATE TABLE"))return {};
      if(query.startsWith("INSERT INTO eon_project_folders")){ db.projects.set(key,{project_id:id,project_name:params[2],folder:params[3],updated_at:params[4]});return {}; }
      if(query.startsWith("UPDATE eon_project_folders")){db.projects.set(key,{project_id:id,project_name:params[2],folder:params[3],updated_at:params[4]});return {};}
      if(query.startsWith("DELETE FROM eon_project_folders")){db.projects.delete(key);return {};}
      if(query.startsWith("DELETE FROM eon_chat_project_folder_bindings WHERE workspace_id=?1 AND project_id=?2")){
        for(const [cid,value] of db.chats.entries())if(cid.startsWith(ws+"|")&&value.project_id===id)db.chats.delete(cid);
        return {};
      }
      if(query.startsWith("INSERT INTO eon_chat_project_folder_bindings")){db.chats.set(key,{project_id:params[2]});return {};}
      if(query.startsWith("DELETE FROM eon_chat_project_folder_bindings")){db.chats.delete(key);return {};}
      throw Error("Unknown mock SQL: "+query);
    },
    async first(){
      if(query.includes("FROM eon_project_folders WHERE"))return db.projects.get(key)||null;
      if(query.includes("FROM eon_chat_project_folder_bindings WHERE"))return db.chats.get(key)||null;
      throw Error("Unknown mock first: "+query);
    },
    async all(){
      if(query.includes("FROM eon_project_folders WHERE workspace_id"))return {results:[...db.projects.entries()].filter(([k])=>k.startsWith(ws+"|")).map(([,row])=>row).sort((a,b)=>a.project_id.localeCompare(b.project_id))};
      throw Error("Unknown mock all: "+query);
    }
   };
  }
  return {bind:bound,run:()=>bound().run()};
 }
}
const env=()=>({EON_DB:new D1Mock()});
const call=(e,ws,action,arguments_={})=>handlePolicy(e,ws,{action,arguments:arguments_});
const set=(id,folder)=>({project_id:id,project_name:id.toUpperCase(),folder,confirmed_by_user:true});

test("project identifiers and folders normalized securely",()=>{
 assert.equal(projectId("Research-2"),"research-2");
 assert.equal(folderPath("G:\\My Drive\\Project A"),"G:\\My Drive\\Project A");
 assert.throws(()=>projectId("x"));
 for(const f of ["G:\\","relative","C:\\Windows\\System32","G:\\A\\..\\B","G:\\A\nB","C:\\Users\\bob\\AppData\\X"])
  assert.throws(()=>folderPath(f),undefined,f);
 assert.equal(insideFolder("G:\\My Drive\\Project A\\results.json","G:\\My Drive\\Project A"),true);
 assert.equal(insideFolder("G:\\My Drive\\Project AA\\results.json","G:\\My Drive\\Project A"),false);
 assert.equal(insideFolder("G:\\My Drive\\Project A\\..\\Others\\x","G:\\My Drive\\Project A"),false);
});

test("two projects coexist and are isolated between workspaces",async()=>{
 const e=env();
 assert.equal((await call(e,"ws1","add",set("research-2","G:\\My Drive\\Research-2"))).status,200);
 assert.equal((await call(e,"ws1","add",set("client-a","D:\\Clients\\A"))).status,200);
 assert.equal((await call(e,"ws2","list")).body.count,0);
 const rows=(await call(e,"ws1","list")).body.projects;
 assert.deepEqual(rows.map(x=>x.project_id),["client-a","research-2"]);
 assert.equal((await call(e,"ws2","get",{project_id:"research-2"})).status,404);
 assert.equal((await call(e,"ws1","add",set("research-2","D:\\Wrong"))).status,409);
});

test("changing a project path does not mutate another project's path",async()=>{
 const e=env();await call(e,"ws1","add",set("research-2","G:\\My Drive\\Research-2"));await call(e,"ws1","add",set("project-b","D:\\ProjectB"));
 assert.equal((await call(e,"ws1","set",{project_id:"research-2",folder:"G:\\My Drive\\Research2New",confirmed_by_user:true})).status,200);
 assert.equal((await call(e,"ws1","get",{project_id:"research-2"})).body.project.project_name,"RESEARCH-2");
 assert.equal((await call(e,"ws1","get",{project_id:"project-b"})).body.project.folder,"D:\\ProjectB");
 assert.equal((await call(e,"ws1","remove",{project_id:"research-2",confirmed_by_user:true})).body.physical_files_deleted,false);
 assert.equal((await call(e,"ws1","list")).body.count,1);
});

test("unconfirmed additions/removals are rejected",async()=>{
 const e=env();
 assert.equal((await call(e,"ws1","add",{project_id:"research-2",folder:"G:\\Research"})).status,409);
 assert.equal((await call(e,"ws1","remove",{project_id:"research-2"})).status,409);
 assert.equal((await call(e,null,"list")).status,403);
 assert.equal(catalogPolicy(null).status,403);
});

test("outside folder checker advises permission rather than moving",async()=>{
 const e=env();await call(e,"ws1","add",set("research-2","G:\\My Drive\\Research-2"));
 const r=(await call(e,"ws1","check",{project_id:"research-2",path:"D:\\Temp\\answer.txt"})).body;
 assert.equal(r.inside,false);assert.equal(r.needs_move_permission,true);assert.match(r.reminder,/ask/i);
 assert.equal((await call(e,"ws1","check",{project_id:"research-2",path:"G:\\My Drive\\Research-2\\data.csv"})).body.inside,true);
});

test("chat bindings require explicit IDs and do not bleed between chats",async()=>{
 const e=env();
 await call(e,"ws1","add",set("research-2","G:\\My Drive\\Research-2"));
 await call(e,"ws1","add",set("project-b","G:\\Clients\\B"));
 assert.equal((await call(e,"ws1","bind",{project_id:"research-2",chat_id:"chat-0001"})).status,409);
 assert.equal((await call(e,"ws1","bind",{project_id:"research-2",chat_id:"chat-0001",confirmed_by_user:true})).status,200);
 const chosen=await contextHint(e,"ws1",{chat_id:"chat-0001",action:"FileSystem",arguments:{mode:"write",path:"D:\\Temp\\data.txt"}});
 assert.equal(chosen.project_id,"research-2");assert.equal(chosen.needs_move_permission,true);
 const newChat=await contextHint(e,"ws1",{chat_id:"chat-0002",action:"FileSystem",arguments:{mode:"write",path:"D:\\Temp\\data.txt"}});
 assert.equal(newChat.status,"PROJECT_NOT_SELECTED");
 assert.equal((await call(e,"ws1","current",{chat_id:"chat-0002"})).body.project,null);
 await call(e,"ws1","unbind",{chat_id:"chat-0001"});
 assert.equal((await call(e,"ws1","current",{chat_id:"chat-0001"})).body.project,null);
});

test("hints contain project mappings and decorated Eon descriptions",async()=>{
 const e=env();await call(e,"ws1","add",set("r2","G:\\My Drive\\R2"));
 const result=await contextHint(e,"ws1",{});
 assert.equal(result.status,"PROJECT_NOT_SELECTED");
 assert.equal(result.projects[0].project_id,"r2");
 const tools=await enhancedTools(e,"ws1",[{name:"eon_run",description:"Do work",inputSchema:{type:"object",properties:{engine:{type:"string"}}}}]);
 assert.match(tools[0].description,/r2/);
 assert.equal(tools[0].inputSchema.properties.project_id.type,"string");
 assert.equal(outputCandidate({action:"FileSystem",arguments:{mode:"write",path:"G:\\Somewhere\\a"}}).path,"G:\\Somewhere\\a");
});
