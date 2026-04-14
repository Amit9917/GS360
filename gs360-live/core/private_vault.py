import os


class PrivateVault:
    """User-isolated upload storage helper."""

    def __init__(self, namespace):
        self.namespace = namespace

    def upload_path(self, filename: str) -> str:
        safe_name = filename.replace("..", "").replace("/", "_").replace("\\", "_")
        return self.namespace.ensure_user_path(os.path.join("uploads", safe_name))
