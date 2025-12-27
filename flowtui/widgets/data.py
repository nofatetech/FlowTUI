MOCK_RESOURCES = {
    "user": {
        "id": "user",
        "route": "/users",
        "methods": ["GET", "POST"],
        "controller": "class UserFlow(BaseFlow):\n  ...",
        "model": "class User(Model):\n  id: int\n  name: str",
        "views": {
            "index.html": {
                "root": "div.container",
                "children": {
                    "h1": {"text": "Users"},
                    "table": {
                        "children": {
                            "thead": {"text": "Name, Email"},
                            "tbody": {"text": "(Loop over users)"},
                        }
                    },
                },
            },
            "show.html": {
                "root": "div.user-profile",
                "children": {"h1": {"text": "user.name"}},
            },
        },
    },
    "project": {
        "id": "project",
        "route": "/projects/{id}",
        "methods": ["GET", "PUT"],
        "controller": "class ProjectFlow(BaseFlow):\n  ...",
        "model": "class Project(Model):\n  id: int\n  title: str",
        "views": {
            "index.html": {
                "root": "div.container",
                "children": {"h1": {"text": "Projects"}},
            }
        },
    },
}
