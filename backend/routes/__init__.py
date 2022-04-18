from sanic import Blueprint, Sanic

from . import static
from .apis import auth_api, core_api, download_api, upload_api


def load_views(app: Sanic) -> None:
    app.blueprint([static.blueprint])
    app.blueprint(
        Blueprint.group(
            auth_api.blueprint,
            core_api.blueprint,
            download_api.blueprint,
            upload_api.blueprint,
            url_prefix="/api",
        )
    )
