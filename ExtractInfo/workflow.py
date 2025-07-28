from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from typing import Dict

with workflow.unsafe.imports_passed_through():
    from ExtractInfo.activity import transform_data_helper


@workflow.defn
class ConversionWorkflow:
    @workflow.run
    async def run(self, hospital: Dict) -> Dict:
        return await workflow.execute_activity(
            transform_data_helper,
            hospital,
            schedule_to_close_timeout=timedelta(5),
            retry_policy=RetryPolicy(
                maximum_interval=timedelta(seconds=2), maximum_attempts=2
            ),
        )
