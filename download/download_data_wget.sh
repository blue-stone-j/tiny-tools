#!/bin/bash

FILE_ID="1i0SWkAqjVtyhPyeIDyAsQVO6KHhGkOtY"
COOKIE_FILE="/tmp/cookie"
DOWNLOAD_PATH="../data/"

# Fetch the download link and token
curl -sc $COOKIE_FILE "https://drive.google.com/uc?export=download&id=${FILE_ID}" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' $COOKIE_FILE)"
URL="https://drive.google.com/uc?export=download&confirm=${CODE}&id=${FILE_ID}"

# Use wget to download the file with the original name
# wget with the --content-disposition flag will handle the file name automatically if the server provides it.
wget --content-disposition --load-cookies $COOKIE_FILE -P "$DOWNLOAD_PATH" "$URL"
