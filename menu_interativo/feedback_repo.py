
from typing import List, Optional
from storage import JSONStorage
from feedback_model import Feedback, ALLOWED_AVALIACOES
from exceptions import ValidationError, NotFoundError

class FeedbackRepository:
    def __init__(self):
        self.storage = JSONStorage("feedbacks")

    def _next_id(self, items: List[dict]) -> int:
        return (max((it.get("id", 0) for it in items), default=0) + 1)

    def _validate(self, avaliacao: str, dificuldade: int, nota: int):
        # Validação DEFENSIVA (backend): simples e objetiva
        if avaliacao not in ALLOWED_AVALIACOES:
            raise ValidationError("Avaliação deve ser BOA, REGULAR ou RUIM.")
        try:
            dificuldade = int(dificuldade)
            nota = int(nota)
        except Exception:
            raise ValidationError("Dificuldade e Nota devem ser inteiros.")
        if not (1 <= dificuldade <= 5):
            raise ValidationError("Dificuldade deve estar entre 1 e 5.")
        if not (1 <= nota <= 5):
            raise ValidationError("Nota deve estar entre 1 e 10.")

    def create(self, avaliacao: str, dificuldade: int, nota: int,
               comentario: Optional[str] = None, criado_em: Optional[str] = None) -> Feedback:
        items = self.storage.load()
        self._validate(avaliacao, dificuldade, nota)
        fb = Feedback(
            id=self._next_id(items),
            avaliacao=avaliacao,
            dificuldade=dificuldade,
            nota=nota,
            comentario=comentario,
            criado_em=criado_em
        )
        items.append(fb.to_dict())
        self.storage.save(items)
        return fb

    def list_all(self) -> List[Feedback]:
        return [Feedback.from_dict(d) for d in self.storage.load()]

    def list_filtered(self, avaliacao: Optional[str] = None, min_dif: Optional[int] = None) -> List[Feedback]:
        data = self.list_all()
        if avaliacao:
            if avaliacao not in ALLOWED_AVALIACOES:
                raise ValidationError("Filtro de avaliação inválido.")
            data = [x for x in data if x.avaliacao == avaliacao]
        if isinstance(min_dif, int):
            data = [x for x in data if x.dificuldade >= min_dif]
        return data

    def delete(self, fid: int) -> None:
        items = self.storage.load()
        novo = [d for d in items if d.get("id") != fid]
        if len(novo) == len(items):
            raise NotFoundError("Feedback não encontrado.")
        self.storage.save(novo)

    def stats(self) -> dict:
        data = self.list_all()
        if not data:
            return {"media_nota": 0.0, "pct_dificuldade_alta": 0.0, "contagem": {"BOA":0,"REGULAR":0,"RUIM":0}}
        media = sum(x.nota for x in data) / len(data)
        alta = sum(1 for x in data if x.dificuldade >= 4) / len(data) * 100
        cont = {"BOA":0,"REGULAR":0,"RUIM":0}
        for x in data: cont[x.avaliacao] += 1
        return {"media_nota": round(media,2), "pct_dificuldade_alta": round(alta,1), "contagem": cont}
