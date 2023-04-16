#!/bin/bash

docker run --name jervis_tg --rm \
-e HOST=jervis_django -e APP_TOKEN=6076696755:AAHWtI_46iKQG3NxYAfV65Zi4sXFWME3TmQ \
-d jervis_tg:1