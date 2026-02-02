import os

class CodeScannerService:
    """
    Scans the 'apps' directory to build a structured, recursive representation of the applications.
    """

    def _scan_directory_recursively(self, dir_path: str) -> dict:
        """
        Recursively scans a directory and returns a nested dictionary representing its structure.
        """
        tree = {}
        if not os.path.isdir(dir_path):
            return tree
            
        for name in os.listdir(dir_path):
            path = os.path.join(dir_path, name)
            if os.path.isdir(path):
                tree[name] = self._scan_directory_recursively(path)
            else:
                tree[name] = None  # Mark as file
        return tree

    def scan_project(self) -> dict:
        """
        Scans the project's 'apps' and 'backend' directories and builds a deep graph.

        Returns:
            A dictionary representing the application graph with full file trees.
        """
        project_graph = {
            "apps": {},
            "backend_tree": None,
        }

        # Scan the root backend directory
        if os.path.exists("backend") and os.path.isdir("backend"):
            project_graph["backend_tree"] = self._scan_directory_recursively("backend")

        # Scan the apps directory
        root_dir = "apps"
        if not os.path.exists(root_dir) or not os.path.isdir(root_dir):
            return project_graph

        for app_name in os.listdir(root_dir):
            app_path = os.path.join(root_dir, app_name)
            if not os.path.isdir(app_path):
                continue

            # Scan backend
            backend_path = os.path.join(app_path, "backend")
            backend_tree = None
            if os.path.exists(backend_path) and os.path.isdir(backend_path):
                backend_tree = self._scan_directory_recursively(backend_path)

            # Scan frontends
            frontends = []
            for item in os.listdir(app_path):
                item_path = os.path.join(app_path, item)
                if item.startswith("ext_frontend_") and os.path.isdir(item_path):
                    frontends.append({
                        "name": item,
                        "tree": self._scan_directory_recursively(item_path)
                    })

            project_graph["apps"][app_name] = {
                "backend_tree": backend_tree,
                "frontends": frontends
            }

        return project_graph
