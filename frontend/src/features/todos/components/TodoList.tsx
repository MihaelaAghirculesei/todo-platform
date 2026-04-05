import { Todo } from "../../../types/todo";
import { TodoItem } from "./TodoItem";

interface Props {
    todos: Todo[];
    onToggle: (id: number, done: boolean) => void;
    onDelete: (id: number) => void;
}

export function TodoList({ todos, onToggle, onDelete }: Props) {
    if (todos.length === 0) {
        return <p>No todos yet.</p>;
    }

    return (
        <ul>
            {todos.map((todo) => (
                <TodoItem
                    key={todo.id}
                    todo={todo}
                    onToggle={onToggle}
                    onDelete={onDelete}
                />
            ))}
        </ul>
    );
}
