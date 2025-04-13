import time
from logging import getLogger

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

log_request_logger = getLogger('project.log_request_logger')

class LogginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()

        try:
            body = await request.body()
            body_str = body.decode('utf-8') if body else None
        except Exception:
            body_str = "<unable to read body>"

        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        log_request_logger.info(
            f"{request.client.host} - {request.method} {request.url.path} "
            f"Status: {response.status_code} | Time: {process_time:.4f}s | Body: {body_str}"
        )

        response.headers["X-Process-Time"] = str(process_time)
        return response