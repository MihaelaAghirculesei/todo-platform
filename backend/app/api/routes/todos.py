from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from ...schemas.todo import TodoCreate, TodoOut, TodoUpdate
from ...services.todo_service import TodoService
from ..dependencies import get_todo_service

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=list[TodoOut])
def list_todos(service: TodoService = Depends(get_todo_service)):
    return service.get_all()


@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, service: TodoService = Depends(get_todo_service)):
    return service.create(payload)


@router.patch("/{todo_id}", response_model=TodoOut)
def update_todo(
    todo_id: Annotated[int, Path(gt=0)],
    payload: TodoUpdate,
    service: Annotated[TodoService, Depends(get_todo_service)],
):
    return service.update(todo_id, payload)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int = Path(..., gt=0),
    service: TodoService = Depends(get_todo_service),
):
    service.delete(todo_id)
