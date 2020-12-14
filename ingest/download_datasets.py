from pathlib import Path
from typing import List
import httpx
import json
import asyncio
import click


async def download_file(filename):
    async with httpx.AsyncClient() as client:
        response = await client.get(filename)
        return response.content


async def write_file(filename, content):
    Path("assets").joinpath(filename.split("/")[-1]).write_bytes(content)


async def get_files(filename):
    content = await (download_file(filename))
    await write_file(filename, content)


def load_all(filename, data_group):
    """downloads the keys to download new datafiles. If None, download all datasets.
    Optionally download resources
    """
    with open(filename) as fp:
        json_data = json.load(fp)
    return [x for x in json_data[data_group].values()]


def load_many(files: List[str], filename, data_group):
    """downloads the keys to download new datafiles. If None, download all datasets.
    Optionally download resources
    """
    with open(filename) as fp:
        json_data = json.load(fp)
    return [json_data[data_group][data_name] for data_name in files]


async def load_queue(queue_files):
    queue = []
    queue.append(get_files(queue_files))
    await asyncio.wait(queue)


@click.group()
def cli():
    pass


@click.command()
@click.argument("dataset_name", nargs=-1, type=str)
@click.option(
    "-f",
    "--filename",
    "filename",
    type=click.Path(exist=True),
    default="assets/datasets.json",
)
@click.option("data_group", default="datasets")
def download(dataset_name, filename, data_group):
    if dataset_name:
        queue = load_many(
            files=dataset_name,
            filename=filename,
            data_group=data_group,
        )
    else:
        queue = load_all(
            filename=filename,
            data_group=data_group,
        )

    asyncio.run(load_queue(queue))


if __name__ == "__main__":
    cli()
