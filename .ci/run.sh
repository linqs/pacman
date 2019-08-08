#!/bin/bash

trap exit SIGINT

python3 -m flake8 pacai
if [[ $? -eq 0 ]]; then
    echo "Style passed!"
else
    echo "Style failed. :("
fi
