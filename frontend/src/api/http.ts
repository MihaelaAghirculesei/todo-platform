const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function http<T>(
    path: string,
    options: RequestInit = {}
): Promise<T> {
    const response = await fetch(`${BASE_URL}${path}`, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    if (response.status === 204 || response.headers.get("content-length") === "0") {
        return undefined as T;
    }

    return response.json();
}
    