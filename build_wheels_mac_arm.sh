#!/bin/bash
#set -ex

for PYBIN in ~/.pyenv/versions/{3.8,3.9}*/bin; do
    "${PYBIN}/pip" install -r requirements.txt
    "${PYBIN}/pip" wheel . -w dist --no-deps
done
