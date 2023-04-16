#!/bin/bash

docker run --name jervis_django --rm \
-e HOST=jervis_db -e PASSWORD=password -e USER=postgres -e DB=postgres -e DISCORD_HOST=jervis_discord \
-v jervis_backend_vol:jervis \
-p 8000:8000 -d jervis_django:1