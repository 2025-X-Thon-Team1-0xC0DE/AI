from fastapi import FastAPI
app = FastAPI(title="gAIde Model Server")

from src.routes import router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["src"])