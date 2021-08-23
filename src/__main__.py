import uvicorn

from src.settings import settings

uvicorn.run(
    'src.app:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)
