import json
import os

from config.settings import (
    JSON_MEMORIA_PATH,
    MSG_EXPORT_MEMORIA_ERROR,
    MSG_IMPORT_MEMORIA_ERROR,
    show_message,
)
from models import FAQ


def exportar_faqs_memoria(faqs_memoria):
    try:
        os.makedirs(os.path.dirname(JSON_MEMORIA_PATH), exist_ok=True)
        # Converte objetos FAQ para dicionários
        faqs_dict = [vars(faq) for faq in faqs_memoria]
        with open(JSON_MEMORIA_PATH, 'w', encoding='utf-8') as f:
            json.dump(faqs_dict, f, ensure_ascii=False, indent=4)
    except Exception as e:
        show_message(MSG_EXPORT_MEMORIA_ERROR.format(erro=e), 'error')


def importar_faqs_memoria():
    try:
        if os.path.exists(JSON_MEMORIA_PATH):
            with open(JSON_MEMORIA_PATH, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                faqs = json.loads(content)
                if isinstance(faqs, list):
                    # Converte dicionários em objetos FAQ
                    faqs_obj = [FAQ(**faq) for faq in faqs]
                    return faqs_obj
        return []
    except Exception as e:
        show_message(MSG_IMPORT_MEMORIA_ERROR.format(erro=e), 'error')
        return []
