import logging
from urllib.parse import urlparse

from environs import Env
from starlette.applications import Starlette

from .av_scanner.syndetect import SyndetectAVScanner
from .forwarder.httpx import HttpxForwarder
from .routes import configure_routes

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

env = Env(prefix="GRAV_")

SYNDETECT_API_URL = env.url("SYNDETECT_API_URL")
SYNDETECT_API_TOKEN = env.str("SYNDETECT_API_TOKEN")
SYNDETECT_API_RETRIES = env.int("SYNDETECT_API_RETRIES", 10)

FORWARD_DOC_WORKER_ORIGIN = env.url(
    "FORWARD_DOC_WORKER_ORIGIN",
    urlparse("http://grist-lb"),
    require_tld=False,
)

FORWARD_HOME_WORKER_ORIGIN = env.url(
    "FORWARD_HOME_WORKER_ORIGIN",
    urlparse("http://grist-home-wk"),
    require_tld=False,
)


av_scanner = SyndetectAVScanner(
    SYNDETECT_API_URL.geturl(), SYNDETECT_API_TOKEN, SYNDETECT_API_RETRIES
)
doc_wk_forwarder = HttpxForwarder(FORWARD_DOC_WORKER_ORIGIN)
home_wk_forwarder = HttpxForwarder(FORWARD_HOME_WORKER_ORIGIN)

routes = configure_routes(av_scanner, doc_wk_forwarder, home_wk_forwarder)

app = Starlette(routes=routes)
