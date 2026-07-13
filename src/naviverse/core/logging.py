import logging
import sys

from naviverse.core.settings import settings

def configure_logging():
    level = logging.INFO if settings.ENV != "development" else logging.DEBUG
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(level)
    if not root.handlers:
        root.addHandler(handler)

# call configure_logging() from application startup if desired
