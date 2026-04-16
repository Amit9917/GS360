import json
import pathlib


class ContentPackManager:
    def __init__(self, root: pathlib.Path):
        self.root = root
        self.registry_path = self.root / "content-packs" / "registry.json"

    def list_packs(self) -> list[dict]:
        with self.registry_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("packs", [])

    def search(self, query: str) -> list[dict]:
        q = query.lower()
        result = []
        for item in self.list_packs():
            if q in item.get("id", "").lower() or q in item.get("path", "").lower():
                result.append(item)
        return result

    def set_enabled(self, pack_id: str, enabled: bool) -> bool:
        with self.registry_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        updated = False
        for item in data.get("packs", []):
            if item.get("id") == pack_id:
                item["enabled"] = enabled
                updated = True

        if updated:
            with self.registry_path.open("w", encoding="utf-8") as out:
                json.dump(data, out, indent=2)

        return updated
