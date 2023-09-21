#!/bin/bash

readonly THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

trap exit SIGINT

exitStatus=0

# Run tests.
echo "Running tests ..."

"${THIS_DIR}/../run_tests.py"
if [[ $? -eq 0 ]]; then
    echo "Tests passed!"
else
    echo "Tests failed. :("
    exitStatus=1
fi

exit ${exitStatus}
