def build_generate_prompt(tema, tom, quantidade, tamanho, plataforma):
  quantidade = min(quantidade, 5)
  tamanho = min(tamanho, 30)

  regras_plataforma = {
    "Instagram": """
      - Use linguagem emocional e envolvente
      - Pode usar emojis com moderação
      - Priorize apelo visual e engajamento
    """,
    "Facebook": """
      - Use linguagem natural e conversacional
      - Priorize clareza e proximidade com o leitor
      - Mantenha um estilo acessível e envolvente
    """,
    "LinkedIn": """
      - Use linguagem profissional e elegante
      - Priorize clareza, valor e reflexão
      - Evite emojis ou use apenas com muita moderação
    """,
    "TikTok": """
      - Use linguagem curta, moderna e cativante
      - Priorize impacto rápido
      - Pode usar emojis com moderação
    """
  }

  regra_plataforma = regras_plataforma.get(plataforma, "")

  system_prompt = f"""
        Você é um assistente especializado em criar legendas para redes sociais.
        Seu objetivo é gerar frases curtas e hashtags com base nas informações fornecidas pelo usuário.

        As frases devem respeitar:
          - Tema informado 
          - Plataforma informada, seguindo as regras específicas para cada plataforma
          - Tom solicitado (ex: romântico, poético, leve, profundo)
          - Quantidade de frases solicitada
          - Limite máximo de palavras por frase (tamanho)
        
        As hashtags devem ser relacionadas ao tema e tom e à plataforma, e devem ser criativas e relevantes.
        
        Regras:
          - Nunca ignore o tema informado
          - Nunca ignore o tom solicitado
          - Nunca ignore a plataforma informada e suas regras específicas
          - Cada frase deve ter no máximo {tamanho} palavras
          - Gere exatamente {quantidade} frases
          - Não repita frases
          - Não use explicações, apenas gere as frases
          - Evite clichês muito comuns
          - Seja criativo, mas mantenha coerência com o tema
          - Gere exatamente 5 hashtags, mesmo que o tema seja mais específico ou genérico
        
        Regras específicas para a plataforma:
        {regra_plataforma}
          
        Formato de resposta:
          - Não escreva nenhum texto antes ou depois do JSON
          - Não utilize markdown
          - Responda SOMENTE em JSON válido, sem nenhum texto adicional, exatamente no seguinte formato:
          {{
            "legendas": [
              {{ "mensagem": "frase 1" }}
            ],
            "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3", "#hashtag4", "#hashtag5"]
          }}"""
  
  user_context = f""" 
    Tema: {tema}
    Tom: {tom}
    Plataforma: {plataforma}
    Quantidade: {quantidade}
    Tamanho: {tamanho}
"""

  prompt_final = system_prompt + "\n\n" + user_context
  return prompt_final

def build_shorten_prompt(frase, tom):
  system_prompt = f"""
    Você é um assistente especializado em reescrever legendas curtas para redes sociais.

    Seu objetivo é encurtar a legenda fornecida, mantendo:
    - o sentido principal
    - o tom original
    - a naturalidade
    - a qualidade da escrita

    Regras:
      - Reduza o tamanho da legenda
      - Mantenha o tom original da frase: {tom}
      - A nova legenda deve ter obrigatoriamente menos palavras que a original
      - Mantenha o significado original da frase
      - Seja criativo, mas mantenha coerência com o tema
      - Não use explicações, apenas gere a frase encurtada

    Formato de resposta:
    {{
      "mensagem": "legenda encurtada"
    }}
  """

  user_context = f""" 
    Frase original: {frase}
"""

  prompt_final = system_prompt + "\n\n" + user_context
  return prompt_final