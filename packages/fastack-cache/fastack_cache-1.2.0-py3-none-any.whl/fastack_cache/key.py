from hashlib import md5

from fastack import Fastack
from fastapi import Request


def get_cache_key(request: Request) -> str:
    path = request.url.path
    query_params = request.scope.get("query_string", b"").decode()
    part = path + query_params
    app: Fastack = request.app
    if app.get_setting("CACHE_INCLUDE_IP_ADDRESS", True):
        ip_address = request.client.host
        if ip_address:
            part += ip_address

    key = md5(part.encode()).hexdigest()
    return key
