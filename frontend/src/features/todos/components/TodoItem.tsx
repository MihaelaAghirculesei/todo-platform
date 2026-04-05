import { Todo } from "../../../types/todo";

interface Props {
    todo: Todo;
    onToggle: (id: number, done: boolean) => void;
    onDelete: (id: number) => void;
}

export function TodoItem({ todo, onToggle, onDelete }: Props) {
    return (
        <li>
            <input
                type="checkbox"
                checked={todo.done}
                onChange={(e) => onToggle(todo.id, e.target.checked)}
            />
            <span style={{ textDecoration: todo.done ? "line-through" : "none" }}>
                {todo.title}
            </span>
            <button onClick={() => onDelete(todo.id)}>Delete</button>
        </li>
    );
}
