import os

class CodeScannerService:
    """
    Scans the 'apps' directory to build a structured representation of the applications.
    """

    def scan_apps(self, root_dir: str = "apps") -> dict:
        """
        Scans the project's 'apps' directory and builds a graph of the applications.

        Returns:
            A dictionary representing the application graph.
        """
        apps_graph = {}
        if not os.path.exists(root_dir) or not os.path.isdir(root_dir):
            return apps_graph

        for app_name in os.listdir(root_dir):
            app_path = os.path.join(root_dir, app_name)
            if not os.path.isdir(app_path):
                continue

            backend_path = os.path.join(app_path, "backend")
            frontends = []

            for item in os.listdir(app_path):
                if item.startswith("ext_frontend_") and os.path.isdir(os.path.join(app_path, item)):
                    frontends.append({
                        "name": item,
                        "path": os.path.join(app_path, item)
                    })

            apps_graph[app_name] = {
                "path": app_path,
                "backend": backend_path if os.path.exists(backend_path) and os.path.isdir(backend_path) else None,
                "frontends": frontends
            }

        return apps_graph