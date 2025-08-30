from fastapi import FastAPI
import os


app = FastAPI(title="SEO Assistant API", version="0.1.0")


@app.get("/", tags=["system"])  # type: ignore[no-untyped-def]
def read_root():
    return {"service": "seo-assistant-api", "version": "0.1.0"}


@app.get("/health", tags=["system"])  # type: ignore[no-untyped-def]
def health_check():
    return {"status": "ok"}

# Optional remote debugger, enabled via env var

    try:
        import debugpy  # type: ignore

        debugpy.listen(("0.0.0.0", int(os.getenv("DEBUGPY_PORT", "5678"))))
        print("debugpy listening on 0.0.0.0:" + os.getenv("DEBUGPY_PORT", "5678"))
        if os.getenv("DEBUGPY_WAIT_FOR_CLIENT", "1") == "1":
            debugpy.wait_for_client()
    except Exception as exc:  # pragma: no cover
        print(f"Failed to start debugpy: {exc}")
