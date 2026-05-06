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
        setError(null);
        try {
            const newTodo = await createTodo({ title });
            setTodos((prev) => [...prev, newTodo]);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to create todo.");
        }
    };

    const toggleTodo = async (id: number, done: boolean) => {
        setError(null);
        try {
            const updated = await updateTodo(id, { done });
            setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)));
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to update todo.");
        }
    };

    const removeTodo = async (id: number) => {
        try {
            await deleteTodo(id);
        } catch (err) {
            const is404 = err instanceof Error && err.message.includes("404");
            if (!is404) {
                setError("Failed to delete todo.");
                return;
            }
        }
        setTodos((prev) => prev.filter((t) => t.id !== id));
    };

    return { todos, loading, error, addTodo, toggleTodo, removeTodo };
}
