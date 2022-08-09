# kFLOW Knowledge Graph
A Knowledge Graph of Event and Relations


## GraphDB

Download latest version of GraphDB free by registering on the [product website](https://www.ontotext.com/products/graphdb/graphdb-free/). Place the obtained zip in the `graphdb` folder.
We will use version 9.8.0.

If you have the new Mac M1, run:

    export DOCKER_DEFAULT_PLATFORM=linux/amd64  


Then, run:

    make free VERSION=9.8.0 -f graphdb/Makefile

    docker-compose up -d

> For more details look at the [graphdb-docker](https://github.com/Ontotext-AD/graphdb-docker#building-a-docker-image-based-on-the-free-edition) repository.

Create the GraphDB repository

    pip install -r scripts/requirements.txt
    python3 scripts/create_repo.py


Upload dumps

    python3 scripts/load_dump.py hong
