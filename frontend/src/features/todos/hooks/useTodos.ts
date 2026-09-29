import { useState, useEffect, useCallback } from "react";
import { Todo } from "../../../types/todo";
import {
    getTodos,
    createTodo,
    updateTodo,
    deleteTodo,
} from "../../../api/todos.api";
import { HttpError } from "../../../api/http";

const CACHE_KEY = "todos-cache-v1";
// The free backend host sleeps when idle; a response slower than this
// means it is starting up, so the UI tells the user instead of hanging.
const WAKING_DELAY_MS = 2000;

function readCache(): Todo[] | null {
    try {
        const parsed: unknown = JSON.parse(localStorage.getItem(CACHE_KEY) ?? "null");
        return Array.isArray(parsed) ? (parsed as Todo[]) : null;
    } catch {
        return null;
    }
}

function writeCache(todos: Todo[]): void {
    try {
        localStorage.setItem(CACHE_KEY, JSON.stringify(todos));
    } catch {
        // Storage blocked or full: the cache is only an optimisation.
    }
}

interface UseTodosReturn {
    todos: Todo[];
    loading: boolean;
    waking: boolean;
    error: string | null;
    addTodo: (title: string) => Promise<void>;
    toggleTodo: (id: number, done: boolean) => Promise<void>;
    removeTodo: (id: number) => Promise<void>;
}

export function useTodos(): UseTodosReturn {
    // Stale-while-revalidate: render the last known list immediately,
    // then replace it with the server's list once it arrives.
    const [initialCache] = useState(readCache);
    const [todos, setTodos] = useState<Todo[]>(initialCache ?? []);
    const [synced, setSynced] = useState(false);
    const [syncing, setSyncing] = useState(true);
    const [waking, setWaking] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchTodos = useCallback(async () => {
        setSyncing(true);
        setError(null);
        const wakingTimer = setTimeout(() => setWaking(true), WAKING_DELAY_MS);
        try {
            const data = await getTodos();
            setTodos(data);
            setSynced(true);
        } catch {
            setError(
                initialCache
                    ? "Could not reach the server. Showing your last saved todos."
                    : "Failed to load todos."
            );
        } finally {
            clearTimeout(wakingTimer);
            setWaking(false);
            setSyncing(false);
        }
    }, [initialCache]);

    useEffect(() => {
        fetchTodos();
    }, [fetchTodos]);

    useEffect(() => {
        // Only persist data confirmed by the server, never the stale copy.
        if (synced) writeCache(todos);
    }, [todos, synced]);

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
            const is404 = err instanceof HttpError && err.status === 404;
            if (!is404) {
                setError("Failed to delete todo.");
                return;
            }
        }
        setTodos((prev) => prev.filter((t) => t.id !== id));
    };

    const loading = syncing && !initialCache;

    return { todos, loading, waking, error, addTodo, toggleTodo, removeTodo };
}
