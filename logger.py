import os
import sys
import logging
from loguru import logger

# LOG_PATH = "/web/tomcat/logs/aigc.label.com/stdout.log"
LOG_PATH = "./stdout.log"

LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False
logging.root.setLevel(LOG_LEVEL)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage())


intercept_handler = InterceptHandler()
seen = set()
for name in [
    *logging.root.manager.loggerDict.keys(),
    "gunicorn",
    "gunicorn.access",
    "gunicorn.error",
    "uvicorn",
    "uvicorn.access",
    "uvicorn.error",
]:
    if name not in seen:
        seen.add(name.split(".")[0])
        logging.getLogger(name).handlers = [intercept_handler]
logger.configure(handlers=[
    {"sink": sys.stdout, "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"},
    {"sink": LOG_PATH, "serialize": JSON_LOGS}
])
