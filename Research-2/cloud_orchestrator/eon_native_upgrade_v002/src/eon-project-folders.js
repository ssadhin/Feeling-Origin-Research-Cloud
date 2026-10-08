/**
 * Eon MCP native per-project output folder registry.
 * One workspace has many projects; each project owns one configurable output folder.
 * Project context must be explicit (project_id or a bound chat_id); never guess it
 * from a stable OpenAI subject or from the workspace alone.
 * This is an advisory policy, not filesystem interception or silent relocation.
 */
const VALID_ID=/^[a-zA-Z0-9][a-zA-Z0-9._-]{1,79}$/;
const WINDOWS_PATH=/^[A-Za-z]:\\/;
const PROTECTED=/^[A-Za-z]:\\(?:Windows|Program Files(?: \(x86\))?|ProgramData|Users\\[^\\]+\\AppData)(?:\\|$)/i;
const VALID_ACTIONS=[
 ["list","List all configured project output folders in this authenticated Eon workspace."],
 ["get","Show a configured project's preferred output folder."],
 ["add","Add a new project with an initial folder, requiring explicit user confirmation."],
 ["set","Change an existing project's output folder, requiring explicit user confirmation."],
 ["remove","Remove a project's saved folder mapping, never delete physical files."],
 ["check","Check a candidate file output path for the named project; advise asking before moving."],
 ["bind","Bind a named Eon project to a SPECIFIC chat_id; no automatic assumption across new chats."],
 ["unbind","Clear a previously bound chat_id project selection."],
 ["current","Read the project selection for a SPECIFIC chat_id; otherwise display all projects."]
];
const now=()=>Date.now();
const asString=v=>typeof v==="string"?v.trim():"";
export function projectId(v) {
  const s=asString(v);
  if(!VALID_ID.test(s)||s===".."||s.startsWith("."))throw Error("INVALID_PROJECT_ID");
  return s.toLowerCase();
}
export function folderPath(v) {
  if(typeof v!=="string"||v.length<5||v.length>550)throw Error("INVALID_FOLDER_LENGTH");
  if(!WINDOWS_PATH.test(v)||/[\u0000-\u001f<>"|?*]/.test(v))throw Error("ABSOLUTE_WINDOWS_PATH_REQUIRED");
  const p=v.replaceAll("/","\\").replace(/\\+/g,"\\").replace(/\\$/,"");
  const parts=p.split("\\");
  if(parts.length<2||!parts[1]||parts.some((seg,i)=>i>0&&(!seg||seg==="."||seg===".."||seg.endsWith(".")||seg.endsWith(" "))))throw Error("INVALID_DIRECTORY_SEGMENT");
  if(PROTECTED.test(p))throw Error("SYSTEM_DIRECTORY_NOT_ALLOWED");
  return p;
}
export function insideFolder(path,folder){
  if(typeof path!=="string"||!/^[A-Za-z]:\\/.test(path)||/[\u0000-\u001f]/.test(path))return false;
  const s=path.replaceAll("/","\\").replace(/\\+/g,"\\").replace(/\\$/,"");
  if(s.split("\\").some(v=>v==="."||v===".."))return false;
  const a=s.toLowerCase(),b=folder.toLowerCase();
  return a===b||a.startsWith(b+"\\");
}
export function outputCandidate(args){
  const operation=String(args?.arguments?.mode||args?.arguments?.operation||"").toLowerCase();
  const action=String(args?.action||"").toLowerCase();
  if(!/write|save|create|export|download|copy|move|upload|render|publish|edit/.test(action+" "+operation))return null;
  const x=args?.arguments||{};
  for(const k of ["output_path","destination_path","save_path","filepath","file_path","path","destination","target"]){
    if(typeof x[k]==="string"&&x[k].length>3)return {key:k,path:x[k]};
  }
  return null;
}
function reply(body,status=200){return {status,body}}
function safeLabel(s){
  if(typeof s!=="string")return "";
  const x=s.trim();if(x.length>100||/[\u0000-\u001f]/.test(x))throw Error("INVALID_PROJECT_LABEL");
  return x;
}
function safeChat(s) {
  if(typeof s!=="string"||s.length<8||s.length>160||!/^[a-zA-Z0-9._:-]+$/.test(s))throw Error("EXPLICIT_CHAT_ID_REQUIRED");
  return s;
}
async function tables(env){
  await env.EON_DB.prepare("CREATE TABLE IF NOT EXISTS eon_project_folders (workspace_id TEXT NOT NULL, project_id TEXT NOT NULL, project_name TEXT NOT NULL, folder TEXT NOT NULL, updated_at INTEGER NOT NULL, PRIMARY KEY(workspace_id,project_id))").run();
  await env.EON_DB.prepare("CREATE TABLE IF NOT EXISTS eon_chat_project_folder_bindings (workspace_id TEXT NOT NULL, chat_id TEXT NOT NULL, project_id TEXT NOT NULL, updated_at INTEGER NOT NULL, PRIMARY KEY(workspace_id,chat_id))").run();
}
async function get(env,ws,id){
  await tables(env);
  return await env.EON_DB.prepare("SELECT project_id,project_name,folder,updated_at FROM eon_project_folders WHERE workspace_id=?1 AND project_id=?2").bind(ws,id).first();
}
async function list(env,ws){
  await tables(env);
  const data=await env.EON_DB.prepare("SELECT project_id,project_name,folder,updated_at FROM eon_project_folders WHERE workspace_id=?1 ORDER BY project_id ASC LIMIT 100").bind(ws).all();
  return data.results||[];
}
async function binding(env,ws,chatId){
  await tables(env);
  const b=await env.EON_DB.prepare("SELECT project_id FROM eon_chat_project_folder_bindings WHERE workspace_id=?1 AND chat_id=?2").bind(ws,chatId).first();
  if(!b)return null;
  // A deleted project cannot remain selected.
  return await get(env,ws,b.project_id);
}
function noteFor(rows){
  return rows.length?
    "Preferred folders by project: "+rows.map(r=>r.project_id+" => "+JSON.stringify(r.folder)).join("; ")+". Identify the CURRENT project explicitly; do not assume that the Eon workspace is one ChatGPT project. Never silently move/overwrite files.":
    "No Eon project output folders configured. Ask user to add one using eon_run(engine=file_policy,action=add).";
}
export function policyHelp(){
  return {
    engine:"file_policy",store:"Cloudflare EON_DB, isolated by authenticated Eon workspace",
    description:"Manage one output directory for each project; available across chats and Eon-connected devices.",
    actions:VALID_ACTIONS.map(([action,description])=>({action,description})),
    examples:[
      {engine:"file_policy",action:"add",arguments:{project_id:"research-2",project_name:"Research #2",folder:"G:\\My Drive\\Research #2",confirmed_by_user:true}},
      {engine:"file_policy",action:"set",arguments:{project_id:"research-2",folder:"D:\\Research\\Research-2",confirmed_by_user:true}},
      {engine:"file_policy",action:"remove",arguments:{project_id:"research-2",confirmed_by_user:true}},
      {engine:"file_policy",action:"list"},
      {engine:"file_policy",action:"check",arguments:{project_id:"research-2",path:"D:\\Outputs\\results.json"}}
    ],
    limitations:"Folder preference is an instruction/reminder, not a monitor of ALL filesystem writes. Eon cannot automatically determine the ChatGPT project from its stable MCP workspace identity; pass project_id or bind a unique chat_id. No automatic file moves."
  };
}
export function catalogPolicy(workspaceId){
  if(!workspaceId)return reply({error:"WORKSPACE_AUTH_REQUIRED"},403);
  return reply(policyHelp());
}
export async function handlePolicy(env,workspaceId,request){
  if(!workspaceId)return reply({error:"WORKSPACE_AUTH_REQUIRED"},403);
  const a=String(request.action||"list").toLowerCase();
  const x=request.arguments||{};
  let id=null;
  try{if(["add","set","remove","get","check","bind"].includes(a))id=projectId(x.project_id)}catch(err){return reply({error:String(err.message)},400)}
  if(a==="list"){
    const rows=await list(env,workspaceId);
    return reply({projects:rows,count:rows.length,reminder:noteFor(rows),scope:"Eon workspace across chat sessions"});
  }
  if(a==="get"){
    const found=await get(env,workspaceId,id);
    return found?reply({project:found,reminder:"Use "+JSON.stringify(found.folder)+" for "+id+" outputs. Ask user before any relocation."}):reply({error:"PROJECT_FOLDER_NOT_CONFIGURED",project_id:id},404);
  }
  if(a==="add"||a==="set"){
    if(x.confirmed_by_user!==true)return reply({error:"EXPLICIT_USER_CONFIRMATION_REQUIRED"},409);
    let folder,project_name;
    try{folder=folderPath(x.folder);project_name=safeLabel(x.project_name??id)}catch(err){return reply({error:String(err.message)},400)}
    const old=await get(env,workspaceId,id);
    if(a==="add"&&old)return reply({error:"PROJECT_ALREADY_EXISTS_USE_SET",project:old},409);
    if(a==="set"&&!old)return reply({error:"PROJECT_NOT_FOUND_USE_ADD"},404);
    const name=project_name||old?.project_name||id;
    const stamp=now();
    if(a==="add"){
      await env.EON_DB.prepare("INSERT INTO eon_project_folders(workspace_id,project_id,project_name,folder,updated_at) VALUES(?1,?2,?3,?4,?5)").bind(workspaceId,id,name,folder,stamp).run();
    }else{
      await env.EON_DB.prepare("UPDATE eon_project_folders SET project_name=?3, folder=?4,updated_at=?5 WHERE workspace_id=?1 AND project_id=?2").bind(workspaceId,id,name,folder,stamp).run();
    }
    return reply({ok:true,action:a,project:{project_id:id,project_name:name,folder,updated_at:stamp},
      reminder:"Project "+id+" now uses "+JSON.stringify(folder)+". On other PCs verify the drive/path exists; ask before moving old files."});
  }
  if(a==="remove"){
    if(x.confirmed_by_user!==true)return reply({error:"EXPLICIT_USER_CONFIRMATION_REQUIRED"},409);
    const prior=await get(env,workspaceId,id);
    if(!prior)return reply({error:"PROJECT_NOT_FOUND"},404);
    await env.EON_DB.prepare("DELETE FROM eon_project_folders WHERE workspace_id=?1 AND project_id=?2").bind(workspaceId,id).run();
    await env.EON_DB.prepare("DELETE FROM eon_chat_project_folder_bindings WHERE workspace_id=?1 AND project_id=?2").bind(workspaceId,id).run();
    return reply({ok:true,removed_project_id:id,physical_files_deleted:false,reminder:"The stored destination mapping was removed; no files were touched."});
  }
  if(a==="check"){
    const row=await get(env,workspaceId,id);
    if(!row)return reply({error:"PROJECT_FOLDER_NOT_CONFIGURED",project_id:id},404);
    const path=String(x.path||"");
    if(path.length<4||path.length>1200)return reply({error:"INVALID_OUTPUT_PATH"},400);
    const inside=insideFolder(path,row.folder);
    return reply({project_id:id,preferred_folder:row.folder,path,inside,needs_move_permission:!inside,
      reminder:inside?"This output follows the saved project folder.":
        "File is outside "+JSON.stringify(row.folder)+". Verify the source and destination, and ask the user whether to move it. Never overwrite."});
  }
  if(a==="bind"){
    if(x.confirmed_by_user!==true)return reply({error:"EXPLICIT_CHAT_BINDING_CONFIRMATION_REQUIRED"},409);
    let chat;
    try{chat=safeChat(x.chat_id)}catch(e){return reply({error:String(e.message)},400)}
    const row=await get(env,workspaceId,id);
    if(!row)return reply({error:"PROJECT_NOT_FOUND"},404);
    await env.EON_DB.prepare("INSERT INTO eon_chat_project_folder_bindings(workspace_id,chat_id,project_id,updated_at) VALUES(?1,?2,?3,?4) ON CONFLICT(workspace_id,chat_id) DO UPDATE SET project_id=excluded.project_id, updated_at=excluded.updated_at").bind(workspaceId,chat,id,now()).run();
    return reply({ok:true,chat_id:chat,project:row,reminder:"Only this exact chat_id is bound; new chats must explicitly select their project."});
  }
  if(a==="unbind"||a==="current"){
    let chat;try{chat=safeChat(x.chat_id)}catch(e){return reply({error:String(e.message)},400)}
    if(a==="current")return reply({chat_id:chat,project:await binding(env,workspaceId,chat),note:"Null means no explicit binding. Ask for project; do not guess."});
    await tables(env);
    await env.EON_DB.prepare("DELETE FROM eon_chat_project_folder_bindings WHERE workspace_id=?1 AND chat_id=?2").bind(workspaceId,chat).run();
    return reply({ok:true,chat_id:chat,binding_cleared:true});
  }
  return reply({error:"UNKNOWN_FILE_POLICY_ACTION",supported:VALID_ACTIONS.map(([x])=>x)},400);
}
export async function contextHint(env,workspaceId,request){
  if(!workspaceId)return null;
  try{
    let id;
    if(typeof request.project_id==="string"&&request.project_id.trim()){
      try{id=projectId(request.project_id)}catch{return {status:"INVALID_PROJECT_HINT",advice:"Use a configured project_id; do not guess the folder."}}
    }else if(typeof request.chat_id==="string"&&request.chat_id.trim()){
      try{const row=await binding(env,workspaceId,safeChat(request.chat_id));if(row)id=row.project_id}catch{}
    }
    const rows=await list(env,workspaceId);
    if(!id){
      return {status:rows.length?"PROJECT_NOT_SELECTED":"NO_PROJECTS_CONFIGURED",
        projects:rows.map(({project_id,project_name,folder})=>({project_id,project_name,folder})),
        reminder:noteFor(rows),current_project_inferred:false};
    }
    const r=rows.find(x=>x.project_id===id);
    if(!r)return {status:"PROJECT_NOT_CONFIGURED",project_id:id,reminder:"Ask user to add project folder. Do not select a different project's folder."};
    const candidate=outputCandidate(request);
    const isInside=candidate?insideFolder(candidate.path,r.folder):null;
    return {status:"PROJECT_SELECTED",project_id:id,preferred_folder:r.folder,
      checked_output_path:candidate?.path||null,inside_folder:isInside,
      needs_move_permission:isInside===false,
      arbitrary_process_commands_not_observable:/eonstartprocess|powershell|cmd|exec/.test(String(request.action||"").toLowerCase()),
      reminder:isInside===false?
        "The output differs from this project's saved folder; ask user before any move and never overwrite.":
        "Use this project's preferred directory for new files. Verify availability on target PC. Ask before moving earlier outputs."};
  }catch{
    return {status:"POLICY_LOOKUP_FAILED",reminder:"Do not infer a folder; ask user to verify."};
  }
}
export async function enhancedTools(env,workspaceId,tools){
  if(!workspaceId)return tools;
  const hint=await contextHint(env,workspaceId,{});
  const brief=hint?.status==="NO_PROJECTS_CONFIGURED"?
      " Eon per-project file folders: NONE. Use eon_run(engine=file_policy,action=add,arguments={project_id,folder,confirmed_by_user:true}) after user authorization.":
      " Eon per-project file destinations: "+JSON.stringify(hint?.projects||[]).slice(0,2600)+". Identify CURRENT project explicitly via project_id; do not guess. Move files only with user approval.";
  return tools.map(t=>t.name==="eon_run"?{...t,
    description:t.description+brief,
    inputSchema:{...t.inputSchema,properties:{...t.inputSchema.properties,project_id:{type:"string",description:"Optional explicit Eon project identifier used to select the correct output-folder reminder."}}}
  }:t);
}
