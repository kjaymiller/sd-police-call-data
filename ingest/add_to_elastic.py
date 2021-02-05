from elasticsearch import Elasticsearch
from download_assets import download
from pathlib import Path
from progress.bar import Bar
import asyncio
import click
import eland as ed
import pandas as pd
import json
import os

client = Elasticsearch(
    hosts=[os.environ["ELASTICSEARCH_HOST"]],  # for local instance
)


call_types = pd.read_csv(
    "assets/pd_cfs_calltypes_datasd.csv",
    keep_default_na=False,
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

            print(f"{df.count()=}")
            df["beat"] = df["beat"].apply(convert_floats_to_ints)
            df["priority"] = df["priority"].apply(strip_priority)
            df_w_call_type = pd.merge(df, call_types[['call_type','description']], on="call_type", how="left").fillna('').drop_duplicates('incident_num')

            ed.pandas_to_eland(
                df_w_call_type,
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
@click.argument("dataset_names", nargs=-1)
@click.option(
    "-f",
    "--filename",
    "filename",
    type=click.Path(exists=True),
    default="datasets.json",
)
@click.option("--data_group", default="datasets")
def download_and_update(dataset_names, filename, data_group):
    assets = download(dataset_names, filename, data_group)

    filepaths= []
    print(filepaths)

    with open(filename) as fp:
        json_data = json.load(fp)

    for dataset_name in dataset_names:
        print(dataset_name)
        filepath = Path("assets").joinpath(
                filepaths.append(Path(json_data[data_group][dataset_name]))
            )

    print(filepaths)
    ingest(filepaths)


if __name__ == "__main__":
    cli()
