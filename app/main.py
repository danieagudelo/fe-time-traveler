import uvicorn
from fastapi import FastAPI
from controllers import user
from controllers import location
from controllers import comments
from fastapi.middleware.cors import CORSMiddleware

# settings
from settings import Settings

settings = Settings()


description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""


app = FastAPI(
    title="Teusaquillo Time Traveler",
    description=description,
    summary="Backend API",
    version="0.0.1",
    root_path=settings.ROOT_PATH,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

app.include_router(user.router)
app.include_router(location.router)
app.include_router(comments.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
