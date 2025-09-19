from fastapi import APIRouter, HTTPException, Depends
from fastapi_utils.cbv import cbv
from application.task_producer.dto.task_producer_request import PendingBatchRequest, RunEnqueueRequest
from application.task_producer.dto.task_producer_response import (
    TaskProducerResponse, PendingResponse, ReleaseResponse,
    ConsumeResponse, EnqueueResponse, StatusResponse
)
from application.task_producer.port.out.task_producer_usecase_port import TaskProducerUseCasePort

router = APIRouter(prefix="/producer", tags=["task-producer"])


def get_task_producer_usecase() -> TaskProducerUseCasePort:
    from application.config.app_config import AppConfig
    app_config = AppConfig()
    return app_config.task_producer_usecase


@cbv(router)
class TaskProducerController:
    task_producer_usecase: TaskProducerUseCasePort = Depends(get_task_producer_usecase)

    def __init__(self):
        pass

    @router.post("/pending/{ticket}", response_model=TaskProducerResponse)
    def add_pending(self, ticket: str, req: PendingBatchRequest) -> TaskProducerResponse:
        try:
            stage_ids = [item.stage_id for item in req.items]
            payloads = [item.payload for item in req.items]
            result = self.task_producer_usecase.add_pending_tasks(ticket, stage_ids, payloads)

            response_data = PendingResponse(**result)
            return TaskProducerResponse(
                success=True,
                message="Tasks added to pending queue",
                data=response_data.dict()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/release/{ticket}", response_model=TaskProducerResponse)
    def release_one(self, ticket: str) -> TaskProducerResponse:
        try:
            result = self.task_producer_usecase.release_task_to_run(ticket)
            response_data = ReleaseResponse(**result)
            return TaskProducerResponse(
                success=result["success"],
                message="Task released to run queue" if result["success"] else "No tasks to release",
                data=response_data.dict()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/run/enqueue", response_model=TaskProducerResponse)
    def enqueue_run(self, req: RunEnqueueRequest) -> TaskProducerResponse:
        try:
            result = self.task_producer_usecase.enqueue_direct_run(req.ticket, req.stage_id, req.payload)
            response_data = EnqueueResponse(**result)
            return TaskProducerResponse(
                success=True,
                message="Task enqueued to run queue",
                data=response_data.dict()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/status/{ticket}", response_model=TaskProducerResponse)
    def get_status(self, ticket: str) -> TaskProducerResponse:
        try:
            result = self.task_producer_usecase.get_queue_status(ticket)
            response_data = StatusResponse(**result)
            return TaskProducerResponse(
                success=True,
                message="Queue status retrieved",
                data=response_data.dict()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))