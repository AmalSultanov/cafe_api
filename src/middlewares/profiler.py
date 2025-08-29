from fastapi import Request
from fastapi.responses import HTMLResponse
from pyinstrument import Profiler


def setup_profiler(app):
    @app.middleware("http")
    async def profile_request(request: Request, call_next):
        if "profile" in request.query_params:
            profiler = Profiler()
            profiler.start()
            await call_next(request)
            profiler.stop()

            return HTMLResponse(
                content=profiler.output_html(), status_code=200
            )
        return await call_next(request)
