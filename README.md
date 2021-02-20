# sd-police-call-data
Ingest, Map and Observe Police Call Data

## Ingest
### Download datasets

You can find the datasets for police call records for each year at the San Diego Open Data Portal.

I've also created an `assets.json` with links to the datasets.

`python ingest/download_datasets.py`

If you need to update a single document (like the current year) append the year to the end of it.

`python ingest/download_datasets.py 2021`

### Upload 

`python ingest/add_to_elastic.py <FILENAME>`

**FILENAME** is the csv file.
