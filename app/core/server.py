import traceback
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.models import Response
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.common import custom_exc
from app.common.logger import logger
from app.router import api_router

from app.schemas.response import response_code
from setting import settings


def create_app() -> FastAPI:
    """
    generate FastAPI object
    :return:
    """
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        redoc_url=settings.REDOC_URL
    )

    # settings of cross-domain
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://www.yuzuhi.xyz", "http://localhost:8080", "http://127.0.0.1:8080"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # register router
    register_router(app)

    # catch global exceptions
    register_exception(app)

    # request reject
    register_hook(app)

    if settings.DEBUG:
        # 注册静态文件
        register_static_file(app)

    return app


def register_static_file(app: FastAPI) -> None:
    """
    静态文件交互开发模式使用
    生产使用 nginx 静态资源服务
    这里是开发是方便本地
    :param app:
    :return:
    """
    import os
    from fastapi.staticfiles import StaticFiles
    if not os.path.exists("./static"):
        os.mkdir("./static")
    app.mount("/static", StaticFiles(directory="static"), name="static")


def register_router(app: FastAPI) -> None:
    """
    register router
    """
    # 项目API
    app.include_router(
        api_router,
    )


def register_exception(app: FastAPI) -> None:
    """
    全局异常捕获
    注意 别手误多敲一个s
    exception_handler
    exception_handlers
    两者有区别
        如果只捕获一个异常 启动会报错
        @exception_handlers(UserNotFound)
    TypeError: 'dict' object is not callable
    :param app:
    :return:
    """

    # 自定义异常 捕获
    @app.exception_handler(custom_exc.TokenExpired)
    async def user_not_found_exception_handler(request: Request, exc: custom_exc.TokenExpired):
        """
        token过期
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"token未知用户\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

        return response_code.response_4002(message=exc.err_desc)

    @app.exception_handler(custom_exc.TokenAuthError)
    async def user_token_exception_handler(request: Request, exc: custom_exc.TokenAuthError):
        """
        用户token异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"用户认证异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

        return response_code.response_4003(message=exc.err_desc)

    @app.exception_handler(custom_exc.AuthenticationError)
    async def user_not_found_exception_handler(request: Request, exc: custom_exc.AuthenticationError):
        """
        用户权限不足
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"用户权限不足 \nURL:{request.method}{request.url}")
        return response_code.response_4003(message=exc.err_desc)

    @app.exception_handler(ValidationError)
    async def inner_validation_exception_handler(request: Request, exc: ValidationError):
        """
        内部参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"内部参数验证错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return response_code.response_5002(message=exc.errors())

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        请求参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"请求参数格式错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        # return response_code.resp_4001(message='; '.join([f"{e['loc'][1]}: {e['msg']}" for e in exc.errors()]))
        return response_code.response_4001(message=exc.errors())

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        catch all exceptions
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"全局异常\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return response_code.response_500()


def register_hook(app: FastAPI) -> None:
    """
    请求响应拦截 hook
    https://fastapi.tiangolo.com/tutorial/middleware/
    :param app:
    :return:
    """

    @app.middleware("http")
    async def logger_request(request: Request, call_next) -> Response:
        # https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip
        # logger.info(f"访问记录:{request.method} url:{request.url}\nheaders:{request.headers}\nIP:{request.client.host}")
        response = await call_next(request)
        return response
