import { useTodos } from "../hooks/useTodos";
import { TodoForm } from "../components/TodoForm";
import { TodoList } from "../components/TodoList";

export function TodosPage() {
    const { todos, loading, error, addTodo, toggleTodo, removeTodo } =
        useTodos();

    return (
        <main>
            <h1>Todos</h1>
            <TodoForm onSubmit={addTodo} />
            {loading && <p>Loading...</p>}
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
