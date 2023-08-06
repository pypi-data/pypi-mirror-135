from fastapi import BackgroundTasks  # noqa: F401

from tktl.core.clients.future.arrow import ArrowClient  # noqa: F401
from tktl.core.clients.future.rest import RestClient  # noqa: F401

from .registration.decorator import Tktl  # noqa: F401
from .registration.endpoints import (  # noqa: F401
    ArrowEndpoint,
    EndpointResponse,
    ProfiledEndpoint,
    TypedEndpoint,
)
from .settings import Settings

settings = Settings()
