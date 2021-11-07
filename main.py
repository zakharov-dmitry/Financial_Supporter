import fastapi
import uvicorn
import fastapi_chameleon
from fastapi.staticfiles import StaticFiles

from models.db_session import global_init_db
from views import home

app = fastapi.FastAPI()


def configure_templates():
    fastapi_chameleon.global_init('templates')


def configure_routes():
    app.include_router(home.router)
    app.mount("/static", StaticFiles(directory="static"), name="static")


def configure_db():
    global_init_db()


def configure():
    configure_templates()
    configure_routes()
    configure_db()


def main():
    configure()
    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
else:
    configure()
