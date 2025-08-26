from typing import Optional, Dict, Any
from datetime import datetime

ALLOWED_AVALIACOES = {"BOA", "REGULAR", "RUIM"}

def _ensure_iso8601(dt: Optional[str]) -> str:
    """
    Se dt vier (ex. do front), tenta normalizar para ISO.
    Se dt for inválida ou None, usa agora().
    """
    if not dt:
        return datetime.now().isoformat(timespec="seconds")
    try:
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(dt, fmt).isoformat(timespec="seconds")
            except ValueError:
                pass
        return datetime.fromisoformat(dt).isoformat(timespec="seconds")
    except Exception:
        return datetime.now().isoformat(timespec="seconds")

class Feedback:
    """
    Classe para representar um feedback de paciente sobre a teleconsulta.
    
    Attributes:
        id: Identificador único do feedback
        avaliacao: Avaliação qualitativa (BOA, REGULAR, RUIM)
        dificuldade: Nível de dificuldade (1-5)
        nota: Nota numérica (1-5)
        comentario: Comentário opcional do paciente
        criado_em: Data e hora de criação do feedback
    """
    
    def __init__(self, id: int, avaliacao: str, dificuldade: int, nota: int,
                 comentario: Optional[str] = None, criado_em: Optional[str] = None):
        """
        Inicializa um novo feedback.
        
        Args:
            id: Identificador único do feedback
            avaliacao: Avaliação qualitativa (BOA, REGULAR, RUIM)
            dificuldade: Nível de dificuldade (1-5)
            nota: Nota numérica (1-5)
            comentario: Comentário opcional do paciente
            criado_em: Data e hora de criação (se None, usa data atual)
        """
        self.id = id
        self.avaliacao = avaliacao
        self.dificuldade = int(dificuldade)
        self.nota = int(nota)
        self.comentario = comentario
        self.criado_em = _ensure_iso8601(criado_em)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o feedback para dicionário.
        
        Returns:
            Dicionário com todos os dados do feedback
        """
        return {
            "id": self.id,
            "avaliacao": self.avaliacao,
            "dificuldade": self.dificuldade,
            "nota": self.nota,
            "comentario": self.comentario,
            "criado_em": self.criado_em,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Feedback":
        """
        Cria um feedback a partir de um dicionário.
        
        Args:
            d: Dicionário com os dados do feedback
            
        Returns:
            Instância de Feedback
            
        Raises:
            KeyError: Se campos obrigatórios estiverem faltando
        """
        return Feedback(
            id=d["id"],
            avaliacao=d["avaliacao"],
            dificuldade=d["dificuldade"],
            nota=d["nota"],
            comentario=d.get("comentario"),
            criado_em=d.get("criado_em"),
        )