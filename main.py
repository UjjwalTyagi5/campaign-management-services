import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from loguru import logger
from core.logger import setup_logger
from core.config import PROJECT_NAME, VERSION, API_PREFIX, ORIGINS
from api.routes import router
from db.models import Base
from db.database import engine

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def create_app() -> FastAPI:
    setup_logger()
    app = FastAPI(title=PROJECT_NAME, version=VERSION)
    app.include_router(router, prefix=API_PREFIX)
    
    # cors
    origins = []

    if ORIGINS:
        origins_raw = list(ORIGINS)
        for origin in origins_raw:
            use_origins = origin.strip()
            origins.append(use_origins)
        logger.debug(f"origins : {origins}")
        app = CORSMiddleware(
            app=app,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




