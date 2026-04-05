import { useState, FormEvent } from "react";

interface Props {
    onSubmit: (title: string) => Promise<void>;
}

export function TodoForm({ onSubmit }: Props) {
    const [title, setTitle] = useState("");

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        const trimmed = title.trim();
        if (!trimmed) return;
        await onSubmit(trimmed);
        setTitle("");
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="New todo..."
                maxLength={200}
            />
            <button type="submit">Add</button>
        </form>
    );
}
