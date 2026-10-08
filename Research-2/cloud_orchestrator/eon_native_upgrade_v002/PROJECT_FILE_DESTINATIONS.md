# Eon per-project output folders

One Eon MCP connection; no added plugin. User can manage one preferred output directory for each of many projects. Cloudflare EON_DB persists mappings across conversations and connected PCs.

## Manage project mappings
Discover: eon_catalog(engine=file_policy)
List: eon_run(engine=file_policy, action=list)
Add: eon_run(engine=file_policy, action=add, arguments={project_id: research-2, project_name: Research #2, folder: G:\My Drive\Research #2, confirmed_by_user: true})
Change: eon_run(engine=file_policy, action=set, arguments={project_id: research-2, folder: D:\Research\Research2, confirmed_by_user: true})
Remove: eon_run(engine=file_policy, action=remove, arguments={project_id: research-2, confirmed_by_user: true})
Check: eon_run(engine=file_policy, action=check, arguments={project_id: research-2, path: C:\Temp\report.csv})
Show one: eon_run(engine=file_policy, action=get, arguments={project_id: research-2})

Bind a specific chat: eon_run(engine=file_policy, action=bind, arguments={project_id: research-2, chat_id: chat-00001, confirmed_by_user: true})
Read binding: eon_run(engine=file_policy, action=current, arguments={chat_id: chat-00001})
Unbind: eon_run(engine=file_policy, action=unbind, arguments={chat_id: chat-00001})

## Operation
- Before any output, choose correct project explicitly using project_id or a specific chat binding. Eon cannot infer the current ChatGPT project from its stable workspace auth identity.
- The default list and tool descriptions remind the assistant of all mappings.
- For file actions Eon attaches guidance, warns if an explicit output path differs and tells AI to ask before moving.
- A folder preference does not automatically move, delete, or overwrite files. User can change/remove mapping without touching files on disk.
- Eon only sees file operations made through Eon's tools. Files made by unrelated tools/apps require separate checks.
- Paths may exist on only one device; verify availability before output.
- Scientific canonical Drive/GitHub/frozen records retain precedence; folder choice does not authorize changing them.
