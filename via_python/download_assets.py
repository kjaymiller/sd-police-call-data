from pathlib import Path
from typing import List
import httpx
import json
import asyncio
import click


async def download_file(filename: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(filename)
        return response.content


async def write_file(filename, content):
    filepath = Path("assets", Path(filename).name)
    filepath.write_bytes(content)
    print(filepath, 'written')


async def get_files(filename):
    """downloads files and writes to filesystem"""
    
    content = await (download_file(filename))
    await write_file(filename, content)


def load_all(filename, data_group):
    """download all datasets in the data_group"""
    with open(filename) as fp:
        json_data = json.load(fp)
    return [x for x in json_data[data_group].values()]


def load_many(files: List[str], filename, data_group):
    """downloads datasets based on the provided keys"""
    with open(filename) as fp:
        json_data = json.load(fp)
    data_files = [json_data[data_group][data_name] for data_name in files]
    return data_files


async def load_queue(queue_files):
    """generate async queue for files to be downloaded"""
    queue = []
    for queue_file in queue_files:
        queue.append(get_files(queue_file))
    await asyncio.wait(queue)


@click.command()
@click.argument("dataset_name", nargs=-1, type=str)
@click.option(
    "-f",
    "--filename",
    "filename",
    type=click.Path(exists=True),
    default="datasets.json",
)
@click.option("--data-group", default="datasets")
def download(dataset_name, filename, data_group):
    """CLI Call to select and download a dataset"""
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
    download()
