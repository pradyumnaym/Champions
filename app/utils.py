import base64
from datetime import datetime, timedelta
import logging
import os

from azure.storage.blob import AccountSasPermissions, BlobServiceClient, generate_blob_sas
from opencensus.ext.azure.log_exporter import AzureLogHandler
import uvicorn

from .config import STORAGE_ACCOUNT_KEY, STORAGE_ACCOUNT_NAME, STORAGE_CONTAINER

sas_token_days = 15
blob_service_client = BlobServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
    credential=STORAGE_ACCOUNT_KEY,
)


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


def get_sas_url(url):
    expiry = datetime.utcnow() + timedelta(days=sas_token_days)  # Set SAS token validity
    blob = url.split("/assets")[1]
    blob = blob[1:]
    blob_client = blob_service_client.get_blob_client(STORAGE_CONTAINER, blob)
    sas_token = generate_blob_sas(
        account_name=STORAGE_ACCOUNT_NAME,
        account_key=STORAGE_ACCOUNT_KEY,
        container_name=STORAGE_CONTAINER,
        blob_name=blob,
        permission=AccountSasPermissions(read=True),
        expiry=expiry,
    )
    new_url = blob_client.url + "?" + sas_token
    return new_url
