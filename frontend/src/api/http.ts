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
        const body = await response.json().catch(() => ({}));
        throw new Error((body as { detail?: string }).detail ?? `HTTP error! status: ${response.status}`);
    }

    if (response.status === 204 || response.headers.get("content-length") === "0") {
        return undefined as T;
    }

    return response.json();
}
    