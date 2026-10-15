import json
import requests
from django.conf import settings

SYSTEM_PROMPT = """Você é um especialista em Educação Física, Biomecânica, Periodização de Treino e Arquiteto de Software de IA para Aplicações Fitness.

Sua função é gerar e atualizar planos de treino personalizados com base nas respostas de um formulário de anamnese preenchido pelo usuário.

DIRETRIZES DE PRESCRIÇÃO E PERIODIZAÇÃO:

A. Divisão do Treino (Split)
- Monte a divisão ideal (Fullbody, AB, ABC, Push/Pull/Legs, Upper/Lower) alinhada exatamente à quantidade de dias especificada.
- O tempo total estimado por sessão deve caber rigorosamente no limite informado.

B. Linha de Base e Segurança
- Utilize os valores de cargas e séries/repetições informados como ponto de partida para indicar progressões seguras sem sobrecarga excessiva.
- Adapte a seleção de exercícios de acordo com as restrições informadas em observações, substituindo movimentos contraindicados.

C. Reavaliação periódica (quando houver ficha anterior)
- Sobrecarga progressiva: se houve evolução nas cargas, reajuste intensidade e densidade.
- Variação de estímulos: mantenha os compostos base (agachamento, supino, terra, remadas), varie os isoladores (ângulos, pegadas, equipamentos).
- Mudança de objetivo: se o objetivo mudou, recalcule faixas de repetição e tempos de descanso.

FORMATO DE SAÍDA — responda SOMENTE com um JSON válido, sem texto antes ou depois, sem blocos markdown, seguindo EXATAMENTE este formato:

{
  "resumo": "texto resumindo a divisão de dias, agrupamentos musculares e tempo estimado por sessão",
  "dias": {
    "NomeDoDia": [
      {"exercicio": "nome", "series": 4, "repeticoes": "8-12", "carga_sugerida": "20kg", "descanso": "60s"}
    ]
  },
  "orientacoes": "texto com recomendações de cadência, aquecimento e progressão segura de cargas para os próximos 30 dias"
}

As chaves de "dias" devem ser exatamente os nomes dos dias recebidos no campo "days" do usuário."""


def _montar_payload(ficha):
    return {
        "submissionDate": ficha.data_submissao.isoformat(),
        "status": ficha.status,
        "goal": ficha.objetivo,
        "timeMinutes": ficha.tempo_minutos,
        "days": ficha.dias,
        "exercises": ficha.exercicios_atuais,
        "loads": ficha.cargas_atuais,
        "setsReps": ficha.series_repeticoes_atual,
        "observations": ficha.observacoes,
    }


def _extrair_json(texto):
    """Pega o JSON mesmo que a IA tenha colocado texto ou ``` em volta."""
    inicio = texto.find('{')
    fim = texto.rfind('}')
    if inicio == -1 or fim == -1:
        raise json.JSONDecodeError('Nenhum JSON encontrado na resposta', texto, 0)
    return json.loads(texto[inicio:fim + 1])


def gerar_plano_treino(ficha, ficha_anterior=None):
    """
    Chama a API do Google Gemini pra gerar o plano de treino.
    Se ficha_anterior for passada, inclui no contexto pra aplicar a lógica
    de reavaliação (sobrecarga progressiva, variação de estímulos, etc.)
    """
    payload_atual = _montar_payload(ficha)

    mensagem = json.dumps(payload_atual, ensure_ascii=False)
    if ficha_anterior:
        payload_anterior = _montar_payload(ficha_anterior)
        mensagem = (
            f"Ficha anterior (para fins de reavaliação): {json.dumps(payload_anterior, ensure_ascii=False)}\n\n"
            f"Ficha atual: {mensagem}"
        )

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent",
        headers={"x-goog-api-key": settings.GEMINI_API_KEY},
        json={
            "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [{"role": "user", "parts": [{"text": mensagem}]}],
            "generationConfig": {"responseMimeType": "application/json", "maxOutputTokens": 8000},
        },
        timeout=120,
    )
    response.raise_for_status()

    partes = response.json()["candidates"][0]["content"]["parts"]
    return _extrair_json("".join(parte.get("text", "") for parte in partes if not parte.get("thought")))