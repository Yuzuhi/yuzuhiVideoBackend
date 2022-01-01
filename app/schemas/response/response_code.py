"""

http status code

"""
from typing import Union
from fastapi.responses import Response, JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder


def response_200(*, data: Union[list, dict, str] = None, message: str = "success") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 200,
            'message': message,
            'data': data,
        })
    )


def response_500(*, data: Union[list, dict, str] = None, message: str = "Internal Server Error") -> Response:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({
            'code': 500,
            'message': message,
            'data': data,
        })
    )


# 请求参数格式错误
def response_4001(*, data: Union[list, dict, str] = None,
                  message: Union[list, dict, str] = "Request Validation Error") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 4001,
            'data': data,
            'message': message,
        })
    )


# 用户token过期
def response_4002(*, data: Union[list, dict, str] = None, message: str = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 4002,
            'data': data,
            'message': message,
        })
    )


# token认证失败
def response_4003(*, data: Union[list, dict, str] = None, message: str = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 4003,
            'data': data,
            'message': message,
        })
    )


# 未找到数据
def response_404(*, message: str = "Not Found") -> Response:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({
            'code': 404,
            'data': '',
            'message': message,
        })
    )


# 内部验证数据错误
def response_5002(*, data: Union[list, dict, str] = None, message: Union[list, dict, str] = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 5002,
            'data': data,
            'message': message,
        })
    )
