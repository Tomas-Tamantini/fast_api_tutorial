from fast_api_tutorial.core import TodoCore


class TodoDbRequest(TodoCore):
    user_id: int
