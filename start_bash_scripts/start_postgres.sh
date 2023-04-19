#!/bin/bash

docker run --name jervis_db --rm \
-e POSTGRES_PASSWORD=password -e POSTGRES_USER=postgres -e POSTGRES_DB=postgres \
-v jervis_postgres_vol:/var/lib/postgresql/data \
-p 5432:5432 -d postgres
