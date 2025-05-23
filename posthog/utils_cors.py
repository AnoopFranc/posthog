from urllib.parse import urlparse
from django.http import HttpRequest, HttpResponse

CORS_ALLOWED_TRACING_HEADERS = (
    "traceparent",
    "request-id",
    "request-context",
    "x-amzn-trace-id",
    "x-cloud-trace-context",
    "Sentry-Trace",
    "Baggage",
    "x-highlight-request",
    "x-datadome-clientid",
    "x-posthog-token",
    "x-b3-sampled",
    "x-b3-spanid",
    "x-b3-traceid",
    "x-b3-parentspanid",
    "b3",
)


def cors_response(request: HttpRequest, response: HttpResponse) -> HttpResponse:
    if not request.META.get("HTTP_ORIGIN"):
        return response
    url = urlparse(request.META["HTTP_ORIGIN"])
    if url.netloc == "":
        response["Access-Control-Allow-Origin"] = "*"
    else:
        response["Access-Control-Allow-Origin"] = f"{url.scheme}://{url.netloc}"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"

    # Handle headers that sentry randomly sends for every request.
    # Would cause a CORS failure otherwise.
    # specified here to override the default added by the cors headers package in web.py
    allow_headers = request.META.get("HTTP_ACCESS_CONTROL_REQUEST_HEADERS", "").split(",")
    allow_headers = [header for header in allow_headers if header in CORS_ALLOWED_TRACING_HEADERS]

    response["Access-Control-Allow-Headers"] = "X-Requested-With,Content-Type" + (
        "," + ",".join(allow_headers) if len(allow_headers) > 0 else ""
    )
    response["Vary"] = "Origin"
    return response
