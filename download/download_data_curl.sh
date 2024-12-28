#!/bin/bash

FILE_ID="1i0SWkAqjVtyhPyeIDyAsQVO6KHhGkOtY"
FILE_NAME="../data/1d_fast_fourier_transform.csv"

curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=${FILE_ID}" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=${FILE_ID}" -o ${FILE_NAME}
