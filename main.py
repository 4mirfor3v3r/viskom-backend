import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=str(os.environ.get("HOST", "0.0.0.0")),
        port=int(os.environ.get("PORT", 8888)),
        reload=False,
        log_level="info",
        workers=1
    )