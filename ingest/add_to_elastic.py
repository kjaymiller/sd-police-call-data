from elasticsearch import Elasticsearch
from download_assets import download
from pathlib import Path
from progress.bar import Bar
import click
import eland as ed
import pandas as pd
import os

client = Elasticsearch(
    hosts=[os.environ["ELASTICSEARCH_HOST"]],  # for local instance
)


@click.group()
def cli():
    pass


def convert_floats_to_ints(val):
    try:
        return int(float(val))

    except (TypeError, ValueError):
        return val


def strip_priority(val):
    try:
        return convert_floats_to_ints(val[0])

    except (TypeError, ValueError, IndexError):
        return val


@cli.command()
@click.argument("filepaths", type=click.Path(exists=True), nargs=-1)
def ingest(filepaths):
    with Bar(
        f"Loading {len(filepaths)} files",
        max=len(filepaths),
    ) as bar:

        for filepath in filepaths:
            suffix = "%(percent).1f%%: %(elapsed_td)s - "
            bar.suffix = suffix + filepath
            bar.next()
            df = pd.read_csv(
                filepath,
                keep_default_na=False,
                parse_dates=["date_time"],
            )

            df["beat"] = df["beat"].apply(convert_floats_to_ints)
            df["priority"] = df["priority"].apply(strip_priority)

            ed.pandas_to_eland(
                df,
                es_client=client,
                es_dest_index=Path(filepath).stem,
                es_if_exists="replace",
                es_refresh=True,
                es_type_overrides={
                    "date_time": "date",
                    "address_dir_primary": "keyword",
                    "beat": "keyword",
                    "priority": "keyword",
                    "day_of_week": "keyword",
                },
            )


@cli.command()
@click.argument("dataset_name", nargs=-1)
@click.option(
    "-f",
    "--filename",
    "filename",
    type=click.Path(exists=True),
    default="datasets.json",
)
@click.option("-i", "--floats-to-ints", is_flag=True)
@click.option("--data_group", default="datasets")
def download_and_update(dataset_name, filename, data_group, floats_to_ints):
    download(dataset_name, filename, data_group, floats_to_ints)

    with open(filename) as fp:
        json_data = json.load(fp)
    filepath = Path("assets").joinpath(
        Path(json_data["datasets"][dataset_name[0]].name)
    )

    ingest_one(filepath, floats_to_ints)


if __name__ == "__main__":
    cli()
