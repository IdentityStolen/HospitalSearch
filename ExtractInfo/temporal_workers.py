import asyncio
from concurrent.futures import ThreadPoolExecutor

from temporalio.client import Client
from temporalio.worker import Worker

from ExtractInfo.activity import transform_data_helper
from ExtractInfo.converter_utils import TASK_QUEUE
from ExtractInfo.workflow import ConversionWorkflow


async def main():
    import logging

    logging.basicConfig(level=logging.INFO)

    # Start client
    client = await Client.connect("host.docker.internal:7233", namespace="Conversion")

    # Run a worker for the workflow
    with ThreadPoolExecutor() as executor:
        worker = Worker(
            client=client,
            task_queue=TASK_QUEUE,
            workflows=[ConversionWorkflow],
            activities=[transform_data_helper],
            activity_executor=executor,
        )
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
