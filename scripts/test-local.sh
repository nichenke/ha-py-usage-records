#!/bin/bash

CWD=$(cd "$(dirname "$0")" && pwd)

# use 1nce sample event stream data to curl to local docker container
data="[$(cat $CWD/../tests/testdata/sample.json)]"

# curl to local docker container and capture response
response=$(curl -s -X POST \
  http://localhost:8080/usage \
  -H 'Content-Type: application/json' \
  -d "$data")

# check if the curl command was successful
curl_exit_status=$?
if [ $curl_exit_status -eq 0 ]; then
  echo "Data sent successfully."
  
  # Check if jq is installed
  if command -v jq &> /dev/null; then
    # Use jq to parse and validate the response
    records_processed=$(echo $response | jq '.records_processed')
    
    if [ "$records_processed" = "1" ]; then
      echo "✅ Validation successful: records_processed = 1"
    else
      echo "❌ Validation failed: Expected records_processed = 1, got $records_processed"
      echo "Full response: $response"
    fi
  else
    echo "jq not found. Install jq to parse JSON responses."
    echo "Raw response: $response"
  fi
else
  echo "Failed to send data."
fi