from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.util import Util
from app.mapping import CodeStatus

app = FastAPI()
# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    headers = request.headers
    Authorization = headers.get("Authorization")
    if request.scope.get("path", "").startswith("/api") and not Authorization:
        return JSONResponse(Util.format_Resp(code_type=CodeStatus.Unauthorized))
    request.state.token = Authorization
    response = await call_next(request)
    if response.status_code == 422:
        return JSONResponse(Util.format_Resp(code_type=CodeStatus.BadRequest, message="Parameter type error"))
    return response

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     error_messages = []
#     for error in exc.errors():
#         error_messages.append({
#             'loc': error['loc'],
#             'msg': error['msg'],
#             'type': error['type']
#         })
#     raise HTTPException(status_code=422, detail={'errors': error_messages})
