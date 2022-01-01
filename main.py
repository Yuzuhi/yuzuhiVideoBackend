
from app.core.server import create_app
from setting import settings

app = create_app()

if __name__ == "__main__":
    import uvicorn

    # print all router
    for route in app.routes:
        if hasattr(route, "methods"):
            print({'path': route.path, 'name': route.name, 'methods': route.methods})

    uvicorn.run(app='main:app', host=settings.HOST, port=settings.PORT, reload=settings.RELOAD, debug=settings.DEBUG)
