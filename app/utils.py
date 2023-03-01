import base64
import logging
import os

from opencensus.ext.azure.log_exporter import AzureLogHandler
import uvicorn


def get_logger(APPLICATION_INSIGHTS_CONNECTION_STRING):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    FORMAT: str = "%(levelprefix)s %(asctime)s | %(message)s"

    formatter = uvicorn.logging.DefaultFormatter(FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.addHandler(AzureLogHandler(connection_string=APPLICATION_INSIGHTS_CONNECTION_STRING))
    return logger
