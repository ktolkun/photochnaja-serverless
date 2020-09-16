#!/bin/bash

source azure.conf

# Delete resource group
echo "Deleting resource group..."
az group delete \
  --resource-group $m_group \
  --yes