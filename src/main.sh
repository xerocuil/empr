#!/bin/bash
APPDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export WEBKIT_DISABLE_DMABUF_RENDERER=1
cd "$APPDIR" || exit
pipenv run main
