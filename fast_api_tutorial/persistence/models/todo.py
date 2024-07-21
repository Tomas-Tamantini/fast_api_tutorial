from fast_api_tutorial.core import TodoCore, Todo


class TodoDbRequest(TodoCore):
    user_id: int


class TodoDbResponse(Todo):
    user_id: int
