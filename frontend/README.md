# Frontend – Todo Platform

Owner: Ahmad
Tech: React + Vite + TypeScript

## Setup

```bash
npm install
cp .env.example .env
npm run dev
```

## Dev server
http://localhost:5173

## Environment variables
| Variable       | Default                  | Description         |
|----------------|--------------------------|---------------------|
| VITE_API_URL   | http://localhost:8000    | Backend API base URL |

## Structure
```
src/
  app/           – App root component
  api/           – HTTP client and API functions
  types/         – TypeScript types
  features/
    todos/
      components/ – TodoForm, TodoList, TodoItem
      hooks/      – useTodos
      pages/      – TodosPage
tests/           – Test plan
```

## Fast startup (stale-while-revalidate)
The backend runs on a free host that sleeps when idle, so the first request
can take up to a minute. To keep the UI instant:

- The last list received from the server is cached in `localStorage` and
  rendered immediately on the next visit, then replaced by the fresh list.
- If the server takes longer than 2 s, a "Waking up the server" notice is shown
  instead of a silent loading state.
- If the server is unreachable, the cached list stays visible with a warning.

Only data confirmed by the server is written to the cache.
