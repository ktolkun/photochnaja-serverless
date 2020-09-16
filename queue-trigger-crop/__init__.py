import json
import logging
import os
from io import BytesIO

import azure.functions as func
from PIL import Image
from azure.storage.blob import BlobServiceClient, PublicAccess
from azure.storage.queue import QueueServiceClient

QUEUE_STORAGE_RESPONSE_CONNECTION_STRING = os.getenv(
    'QUEUE_STORAGE_RESPONSE_CONNECTION_STRING')
if not QUEUE_STORAGE_RESPONSE_CONNECTION_STRING:
    QUEUE_STORAGE_RESPONSE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=photochnajatku;AccountKey=4jh1tuQr22ChB2cJL0jELFtvLfhYBcGV9Z8sDkGa9za7gcpLxX9p37VcqtHCWGbA4Dxz4hmiaiavazSw57FqPw=='

BLOB_STORAGE_IMAGE_CONNECTION_STRING = os.getenv(
    'BLOB_STORAGE_IMAGE_CONNECTION_STRING')
if not BLOB_STORAGE_IMAGE_CONNECTION_STRING:
    BLOB_STORAGE_IMAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=photochnajatku;AccountKey=4jh1tuQr22ChB2cJL0jELFtvLfhYBcGV9Z8sDkGa9za7gcpLxX9p37VcqtHCWGbA4Dxz4hmiaiavazSw57FqPw=='


def main(msg: func.QueueMessage) -> None:
    message_body = json.loads(msg.get_body())
    container_name = message_body['container_name']
    blob_name = message_body['blob_name']
    queue_name = message_body['queue_name']
    crop_config = message_body['crop_config']
    logging.info("\n\nGET MESSAGE")
    logging.info(
        'container_name: %s;\nblob_name: %s;\nqueue_name: %s;\ncrop_config: %s;',
        container_name, blob_name, queue_name, crop_config)
    crop(container_name, blob_name, crop_config)
    send_message_result(queue_name, {'blob_name': blob_name})

    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))


def crop(container_name, blob_name, crop_config):
    logging.info("\n\nSTART CROP")

    blob_service_client = BlobServiceClient.from_connection_string(
        BLOB_STORAGE_IMAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(container_name)
    if not any(container.name == container_name for container in
               blob_service_client.list_containers()):
        container_client.create_container(public_access=PublicAccess.Blob)

    blob_client = container_client.get_blob_client(blob_name)

    logging.info(
        'before stream: %s, %s, %s',
        container_name, blob_name, crop_config)

    stream = BytesIO(blob_client
                     .download_blob()
                     .readall())

    image = Image.open(stream)
    x = crop_config['x']
    y = crop_config['y']
    width = crop_config['width']
    height = crop_config['height']
    cropped_image = image.crop((x, y, x + width, y + height))

    content_settings = blob_client.get_blob_properties().content_settings
    blob_client.delete_blob()

    image_bytes = BytesIO()
    content_type = content_settings.content_type
    format = content_type[content_type.rindex('/') + 1:].upper()
    cropped_image.save(image_bytes, format=format)

    blob_client.upload_blob(image_bytes.getvalue(),
                            content_settings=content_settings)
    logging.info("END CROP")

def send_message_result(queue_name, message):
    queue_service_client = QueueServiceClient.from_connection_string(
        QUEUE_STORAGE_RESPONSE_CONNECTION_STRING)

    queue_client = queue_service_client.get_queue_client(queue_name)
    if not any(queue.name == queue_name for queue in
               queue_service_client.list_queues()):
        queue_client.create_queue()

    queue_client.send_message(json.dumps(message),
                                             visibility_timeout=0)
