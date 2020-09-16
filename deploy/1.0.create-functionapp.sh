#!/bin/bash

source azure.conf

az functionapp create \
  --name $m_function \
  --resource-group $m_group \
  --os-type $m_os_type \
  --consumption-plan-location $m_location \
  --runtime $m_runtime \
  --runtime-version $m_runtime_version \
  --functions-version $m_version \
  --storage-account $m_storage
