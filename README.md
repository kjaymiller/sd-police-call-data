# sd-police-call-data

Ingest, Map and Observe Police Call Data

## Why Two Methods?

I understand that some folks will be more comfortable using pandas/eland over docker/logstash.

There are advantages to both.

**Docker/Logstash** - Great for all in one builds. All the Elasticsearch bits are included. Also the most recent dataset is auto-updated every 6 hours.

**Pandas/Eland** - Great if you're doing a one-time build and just need data to look at.

## Docker-Compose Instructions

- Install [docker-compose](https://docs.docker.com/compose/ "Overview of Docker Compose - Docker Documentation") is installed.
  **On macOS (using Homebrew)** - `brew install docker-compose`
- Set ES_VERSION to Elasticsearch/Kibana/Logstash Version
  `echo ES_VERSION=7.15.0 >> .env`
- navigate to `via_docker_compose` directory
  - run `docker-compose`
    - use '-d' for _daemon mode_

## Pandas/Python Version

- Create VirtualEnv
-

## Ingest

### Download datasets

You can find the datasets for police call records for each year at the [San Diego Open Data Portal](https://data.sandiego.gov/datasets/police-calls-for-service/).

I've also created an `assets.json` with links to the datasets.

`python ingest/download_datasets.py`

If you need to update a single document (like the current year) append the year to the end of it.

`python ingest/download_datasets.py 2021`

### Upload

`python ingest/add_to_elastic.py <FILENAME>`

**FILENAME** is the csv file.
