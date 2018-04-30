#!/bin/bash

path=$(cd -P -- "$(dirname -- "$(command -v -- "$0")")" && pwd -P)

cd ${path}

echo 'Building files...'

npm run build

echo 'Copying files...'

yes | cp -rf ./dist/static/ ./../server/

yes | cp -f ./dist/index.html ./../server/analitica/templates/

echo 'Done!'
