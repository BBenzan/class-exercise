import logging
import time
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    request_id = uuid.uuid4().hex[:8]
    request.state.request_id = request_id
    started = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        logger.error(f"Unexpected failure: request_id={request_id}",exc_info=True)
        response = JSONResponse(status_code=500,content={"detail": "Internal server error"})
    

    duration_ms = (time.perf_counter() - started) * 1000
    message = (
        f"request_id={request_id} {request.method} {request.url.path} "
        f"status={response.status_code} duration={duration_ms:.1f}ms"
    )

    # TODO 2: Log message at INFO for status < 400 (e.g. logger.info(message)),
    if response.status_code < 400:
        logger.info(f"request_id={request_id} {request.method} {request.url.path} status={response.status_code} duration={duration_ms:.1f}ms")
    elif 400 <= response.status_code < 500:
        logger.warning(f"request_id={request_id} {request.method} {request.url.path} status={response.status_code} duration={duration_ms:.1f}ms")
    else:
        logger.error(f"request_id={request_id} {request.method} {request.url.path} status={response.status_code} duration={duration_ms:.1f}ms")

    response.headers["X-Request-ID"] = request_id
    return response

