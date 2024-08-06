#!/bin/bash

# Create HTML documentation for the current code.

readonly THIS_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd | xargs realpath)"

function main() {
    if [[ $# -gt 1 ]]; then
        echo "USAGE: $0 [out dir]"
        exit 1
    fi

    set -e
    trap exit SIGINT

    local outputDir="${THIS_DIR}/html"
    if [[ $# -gt 0 ]]; then
        outputDir=$1
    fi

    cd "${THIS_DIR}"

    mkdir -p "${outputDir}"

    pdoc3 --config show_inherited_members=True --html --force --output-dir "${outputDir}" pacai

    return 0
}

[[ "${BASH_SOURCE[0]}" == "${0}" ]] && main "$@"
