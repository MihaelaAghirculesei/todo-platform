import { useTodos } from "../hooks/useTodos";
import { TodoForm } from "../components/TodoForm";
import { TodoList } from "../components/TodoList";

export function TodosPage() {
    const { todos, loading, waking, error, addTodo, toggleTodo, removeTodo } =
        useTodos();

    return (
        <main>
            <h1>Todos</h1>
            <TodoForm onSubmit={addTodo} />
            {waking ? (
                <p role="status" style={{ color: "#666" }}>
                    Waking up the server (free hosting) – this can take up to a minute…
                </p>
            ) : (
                loading && <p>Loading...</p>
            )}
            {error && <p style={{ color: "red" }}>{error}</p>}
            {!loading && (
                <TodoList
                    todos={todos}
                    onToggle={toggleTodo}
                    onDelete={removeTodo}
                />
            )}
        </main>
    );
}
