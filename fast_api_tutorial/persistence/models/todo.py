from fast_api_tutorial.schemas import TodoCore


class TodoDbRequest(TodoCore):
    user_id: int
