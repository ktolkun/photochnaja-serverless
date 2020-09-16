#!/bin/bash

source azure.conf

# Create resource group
echo "-----Creating resource group:"
az group create \
	--name $m_group \
	--location $m_location
