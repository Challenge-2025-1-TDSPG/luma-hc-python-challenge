import json, os
from typing import List, Dict

DATA_DIR = "data"
EXPORT_DIR = "export"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

class JSONStorage:
    def __init__(self, name: str):
        self.name = name
        self.path = os.path.join(DATA_DIR, f"{name}.json")

    def load(self) -> List[Dict]:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"[ERRO] Carregar {self.name}: {e}")
            return []

    def save(self, items: List[Dict]) -> None:
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ERRO] Salvar {self.name}: {e}")
        finally:
            pass  # demonstra o finally