import logging
from urllib.parse import urlparse

from environs import Env
from starlette.applications import Starlette

from .av_scanner.syndetect import SyndetectAVScanner
from .forwarder.httpx import HttpxForwarder
from .routes import configure_routes

env = Env(prefix="GRAV_")

LOG_LEVEL = env.str("LOG_LEVEL", "INFO")

SYNDETECT_API_URL = env.url("SYNDETECT_API_URL")
SYNDETECT_API_TOKEN = env.str("SYNDETECT_API_TOKEN")
SYNDETECT_API_RETRIES = env.int("SYNDETECT_API_RETRIES", 10)
SYNDETECT_API_MAX_POLL_TIME = env.int("SYNDETECT_API_MAX_POLL_TIME", 5)
SYNDETECT_API_POLL_TIME_FACTOR = env.float("SYNDETECT_API_POLL_TIME_FACTOR", 1.1)

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

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

av_scanner = SyndetectAVScanner(
    SYNDETECT_API_URL.geturl(),
    SYNDETECT_API_TOKEN,
    retries=SYNDETECT_API_RETRIES,
    max_poll_time=SYNDETECT_API_MAX_POLL_TIME,
    poll_time_factor=SYNDETECT_API_POLL_TIME_FACTOR,
)
doc_wk_forwarder = HttpxForwarder(FORWARD_DOC_WORKER_ORIGIN)
home_wk_forwarder = HttpxForwarder(FORWARD_HOME_WORKER_ORIGIN)

routes = configure_routes(av_scanner, doc_wk_forwarder, home_wk_forwarder)

app = Starlette(routes=routes)
