from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, phones, captcha, info_square, recycle
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="天韵手机账务系统API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
logger.info("Registering routes...")
app.include_router(auth.router, prefix="/api", tags=["认证"])
app.include_router(captcha.router, prefix="/api/captcha", tags=["验证码"])  # 注意这里改变了路由的顺序
app.include_router(phones.router, prefix="/api/phones", tags=["手机管理"])
app.include_router(info_square.router, prefix="/api/info-square", tags=["信息广场"])
app.include_router(recycle.router, prefix="/api/recycle", tags=["回收管理"])

@app.on_event("startup")
async def startup_event():
    logger.info("Server starting up...")
    logger.info("Routes registered:")
    for route in app.routes:
        logger.info(f"  {route.path}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)