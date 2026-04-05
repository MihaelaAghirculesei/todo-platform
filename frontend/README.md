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
