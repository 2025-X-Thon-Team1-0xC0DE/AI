from fastapi import FastAPI

app = FastAPI(title="gAIde Model Server")

# 엔드포인트는 src/routes.py에 정의되어 있습니다.
from src.routes import router

app.include_router(router)

if __name__ == "__main__":
    # uvicorn 실행
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["src"])
