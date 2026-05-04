import { http } from "./http";
import {
    Todo,
    TodoCreateRequest,
    TodoUpdateRequest,
} from "../types/todo";

type TodoRaw = Omit<Todo, "createdAt"> & { created_at: string };

function mapTodo(raw: TodoRaw): Todo {
    return {
        id: raw.id,
        title: raw.title,
        done: raw.done,
        createdAt: raw.created_at,
    };
}

export function getTodos(): Promise<Todo[]> {
    return http<TodoRaw[]>("/todos").then((raws) => raws.map(mapTodo));
}

export function createTodo(payload: TodoCreateRequest): Promise<Todo> {
    return http<TodoRaw>("/todos", {
        method: "POST",
        body: JSON.stringify(payload),
    }).then(mapTodo);
}

export function updateTodo(
    id: number,
    payload: TodoUpdateRequest
): Promise<Todo> {
    return http<TodoRaw>(`/todos/${id}`, {
        method: "PATCH",
        body: JSON.stringify(payload),
    }).then(mapTodo);
}

export function deleteTodo(id: number): Promise<void> {
    return http<void>(`/todos/${id}`, {
        method: "DELETE",
    });
}
