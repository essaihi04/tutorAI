from app.supabase_client import get_supabase

s = get_supabase()
r = s.table("lesson_resources").select("id,title,resource_type,file_path,metadata").eq(
    "lesson_id", "19d32f48-f627-4c4f-b329-cf7697e3a9d3"
).execute()

for x in r.data:
    title = x.get("title", "?")
    rtype = x.get("resource_type", "?")
    fp = str(x.get("file_path", ""))[:80]
    meta = x.get("metadata", {})
    meta_keys = list(meta.keys()) if isinstance(meta, dict) else type(meta).__name__
    meta_size = len(str(meta)) if meta else 0
    print(f"  {title}")
    print(f"    type={rtype}  file_path={fp}")
    print(f"    metadata_keys={meta_keys}  metadata_size={meta_size}")
    if rtype == "simulation" and isinstance(meta, dict):
        for k in meta:
            val = str(meta[k])[:100]
            print(f"    metadata[{k}] = {val}")
    print()
