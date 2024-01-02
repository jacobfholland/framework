from server.request import Request
from .server import url_map
import functools
import json
from typing import Callable, List

from werkzeug.routing import Rule
from werkzeug.wrappers import Response
from app.log.logger import create_logger

from app.utils.json import serialize

logger = create_logger(__name__)


def build_rule(cls, rule, url_prefix):
    if not url_prefix:
        rule = f"{cls._url_prefix}{rule}"
    else:
        rule = f"{url_prefix}{rule}"
    if rule.startswith("//"):
        rule = rule[1:]
    if rule.endswith("/") and not rule == "/":
        rule = rule[:-1]
    return rule


def route(cls: type, rule: str, methods: List[str] = ["GET"], url_prefix: str = None) -> Callable:
    rule = build_rule(cls, rule, url_prefix)

    def decorator(func):
        @functools.wraps(func)
        def wrapped(request, *args, **kwargs):
            return build_response(cls, request, func, *args, **kwargs)
        register_route(rule, wrapped, methods)
        return wrapped
    return decorator


def build_response(cls, request, func, *args, **kwargs):
    request = Request(request)
    result = func(cls, request, *args, **kwargs)
    if isinstance(result, Response):
        return result
    if isinstance(result, str) and result.strip().startswith("<"):
        return Response(
            result.strip(),
            content_type="text/html; charset=utf-8"
        )
    return Response(
        json.dumps(result, default=serialize),
        content_type="application/json; charset=utf-8"
    )


def register_route(rule, wrapped, methods):
    if not any([rule == r.rule for r in url_map.iter_rules()]):
        url_map.add(Rule(rule, endpoint=wrapped, methods=methods))
        logger.debug(f"Registered route {rule}")
