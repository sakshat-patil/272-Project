import os, sys
try:
    import uvicorn
except Exception as e:
    print(f"[startup] uvicorn not importable: {e}", file=sys.stderr)
    raise

port = int(os.environ.get("PORT", "8080"))
print(f"[startup] Starting app on 0.0.0.0:{port}")
uvicorn.run("app.main:app", host="0.0.0.0", port=port)
