# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:3.0-python3.7-appservice
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.7

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt /
RUN pip install -r /requirements.txt

ENV AzureWebJobsStorage="DefaultEndpointsProtocol=https;AccountName=photochnaja;AccountKey=FL/WUYVN+Eg9Oi+/LEDt2dQc2XGcg3/db2//Lv3eyfUegXcbbf0LxDZN3fqsJMrAoFLk3zEWY0yXk6UdzQm0iw==;EndpointSuffix=core.windows.net"

COPY . /home/site/wwwroot
