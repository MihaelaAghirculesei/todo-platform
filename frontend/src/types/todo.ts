export interface Todo {
    id: number;
    title: string;
    done: boolean;
    createdAt: string;
}

export interface TodoCreateRequest{
    title: string;
}

export interface TodoUpdateRequest{
    title?: string;
    done?: boolean;
}