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

### Loading Historical Data

- Download Historical Data from [San Diego Open Data Portal](https://data.sandiego.gov/datasets/police-calls-for-service/) and save to `via_docker_compose/logstash/data/`

### Starting Docker-Compose

- navigate to `via_docker_compose` directory
  - run `docker-compose`
    - use '-d' for _daemon mode_

### View Indices

using `httpie`:

- http -u elastic:changeme localhost:9200/\_cat/indices/pd\*

## Pandas/Python Version

- Create virtualenv
- install requirements using pip-tools (`pip-sync`) or `pip install -r requirements.txt`
- Navigate to `via_python`

### Download datasets

In `via_python/datasets.json` there are links for each of the years datasets. You can download them (from `via_python`) with.

`python download_datasets.py`

If you need to update a single document (like the current year) append the year to the end of it.

`python download_datasets.py 2021`

### Upload to Elasticsearch

Save your elasticsearch information to your environment.

`python ingest/add_to_elastic.py <FILENAMES you wish to load into elasticsearch>`

**FILENAME** is the csv file.
