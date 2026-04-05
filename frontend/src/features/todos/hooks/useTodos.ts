import { useState, useEffect, useCallback } from "react";
import { Todo } from "../../../types/todo";
import {
    getTodos,
    createTodo,
    updateTodo,
    deleteTodo,
} from "../../../api/todos.api";

interface UseTodosReturn {
    todos: Todo[];
    loading: boolean;
    error: string | null;
    addTodo: (title: string) => Promise<void>;
    toggleTodo: (id: number, done: boolean) => Promise<void>;
    removeTodo: (id: number) => Promise<void>;
}

export function useTodos(): UseTodosReturn {
    const [todos, setTodos] = useState<Todo[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchTodos = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await getTodos();
            setTodos(data);
        } catch {
            setError("Failed to load todos.");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchTodos();
    }, [fetchTodos]);

    const addTodo = async (title: string) => {
        try {
            const newTodo = await createTodo({ title });
            setTodos((prev) => [...prev, newTodo]);
        } catch {
            setError("Failed to create todo.");
        }
    };

    const toggleTodo = async (id: number, done: boolean) => {
        try {
            const updated = await updateTodo(id, { done });
            setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)));
        } catch {
            setError("Failed to update todo.");
        }
    };

    const removeTodo = async (id: number) => {
        try {
            await deleteTodo(id);
            setTodos((prev) => prev.filter((t) => t.id !== id));
        } catch {
            setError("Failed to delete todo.");
        }
    };

    return { todos, loading, error, addTodo, toggleTodo, removeTodo };
}
