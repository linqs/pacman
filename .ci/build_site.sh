#!/bin/bash

# Create a fill website including all documentation ready to be deployed.

readonly THIS_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd | xargs realpath)"
readonly ROOT_DIR="${THIS_DIR}/.."
readonly BASE_DIR="${THIS_DIR}/html"

readonly OUT_DIR="${ROOT_DIR}/._site"

readonly GEN_DOCS_SCRIPT="${ROOT_DIR}/gen_docs.sh"

function genDocs() {
    local latestDir="${OUT_DIR}/docs/latest"
    "${GEN_DOCS_SCRIPT}" "${latestDir}"
}

function main() {
    if [[ $# -ne 0 ]]; then
        echo "USAGE: $0"
        exit 1
    fi

    set -e
    trap exit SIGINT

    cd "${ROOT_DIR}"

    rm -rf "${OUT_DIR}"

    cp -r "${BASE_DIR}" "${OUT_DIR}"

    genDocs

    return 0
}

[[ "${BASH_SOURCE[0]}" == "${0}" ]] && main "$@"
