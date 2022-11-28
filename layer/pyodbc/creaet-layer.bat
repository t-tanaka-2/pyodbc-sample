@ECHO OFF
echo ----- Docker Image Build -----
docker build -t pyodbc-image .

echo ----- Container Delete And Create -----
docker rm -f pyodbc-container && docker create -ti --name pyodbc-container pyodbc-image bash

echo ----- Copy Lambda Layer Module -----
docker cp pyodbc-container:/opt/lambda-layer.zip ./lambda-layer.zip
dir /b lambda-layer.zip && echo Module Copy Success

echo ----- Docker Delete -----
docker rm -f pyodbc-container
