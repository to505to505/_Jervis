#!/bin/bash

docker run --name jervis_discord --rm \
-e HOST=jervis_django -e APP_TOKEN=MTA5NTI4MjA5MzAyMzU2NzkxMg.GfSL-S.LB2-z5EuCwVC1T-veV2KzO26m3sqSKdUxbQ3e4 -e AUTH_TOKEN=MTA5NjExMjQxMzE0Njg5NDQzNw.G40cOT.w3XybsZRmg3sXG2DpEDxThpxDr44nmmiE0tuWI \
-p 80:80 -d jervis_discord:1
