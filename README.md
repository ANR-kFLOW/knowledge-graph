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

    python3 scripts/load_dump.py eventcausality
    python3 scripts/load_dump.py ontoed
    python3 scripts/load_dump.py hong
    python3 scripts/load_dump.py timebank

## Apache Configuration and dereferencing

In `graphdb/config.yml` it is possible to configure the basic information about the database server, as well as the list of base paths to dereference
([more details](https://github.com/pasqLisena/list2dereference) about the used tool and syntax).

Running the following script (requires NodeJS installed)

    npx list2dereference graphdb/config.yml

2 files will be produced:
- kflow.eurecom.fr.conf is the configuration file for Apache and saved in `/etc/apache2/sites-available/`
- script_graphdb.sh should be run inside the Docker container using `docker exec -it kflow_graphdb bash`

> This procedure should be repeated when new base paths for dereferencing are needed
