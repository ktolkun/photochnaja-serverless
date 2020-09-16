#!/bin/bash

source azure.conf

# Set DATABASE_USER variable
az functionapp config appsettings set \
  --name $m_function \
  --resource-group $m_group \
  --settings AzureWebJobsStorage=$m_azure_web_jobs_storage_conn_string

# Set DATABASE_USER variable
az functionapp config appsettings set \
  --name $m_function \
  --resource-group $m_group \
  --settings QUEUE_STORAGE_RESPONSE_CONNECTION_STRING=$m_queue_storage_conn_string

# Set DATABASE_USER variable
az functionapp config appsettings set \
  --name $m_function \
  --resource-group $m_group \
  --settings BLOB_STORAGE_IMAGE_CONNECTION_STRING=$m_blob_storage_conn_string