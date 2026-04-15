import streamlit as st
from prompt_builder import build_generate_prompt, build_shorten_prompt
from llm_client import gerar_legendas, encurtar_legenda
from copy_button import copy_button

st.set_page_config(page_title="LegendaAI", page_icon="✨")

st.title("✨ LegendaAI")
st.write("Crie legendas curtas e criativas para suas redes sociais!")

# Estado da sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

if "resultado" not in st.session_state:
    st.session_state.resultado = None

if "prompt" not in st.session_state:
    st.session_state.prompt = None

if "tom" not in st.session_state:
    st.session_state.tom = None

if "legendas_encurtadas" not in st.session_state:
    st.session_state.legendas_encurtadas = {}

tema = st.text_input(
  "Tema", 
  placeholder="Amor, Viagem, Amizade, etc."
)

tom = st.selectbox(
  "Tom",
  ["romântico", "poético", "leve", "profundo", "engraçado", "inspirador"]
)

quantidade = st.number_input(
  "Quantidade de legendas",
  min_value=1,
  max_value=5,
  value=3,
  step=1
)

tamanho = st.slider(
  "Máximo de palavras por legenda",
  min_value=5,
  max_value=30,
  value=10,
  step=1
)

if st.button("Gerar Legendas", use_container_width=True):
  if not tema.strip():
    st.warning("Informe um tema para gerar as legendas.")
  else:
    try:
      with st.spinner("Gerando legendas..."):
        prompt = build_generate_prompt(tema, tom, quantidade, tamanho)
        resultado = gerar_legendas(prompt)
        
        st.session_state.resultado = resultado
        st.session_state.prompt = prompt
        st.session_state.tom = tom
        st.session_state.legendas_encurtadas = {}

        st.session_state.historico.append({
            "tema": tema,
            "tom": tom,
            "quantidade": quantidade,
            "tamanho": tamanho,
            "legendas": resultado.get("legendas", []),
            "hashtags": resultado.get("hashtags", [])
        })

    except Exception as e:
      st.error(f"Erro ao gerar legendas: {e}") 

# Exibição dos resultados fora do botão principal
if st.session_state.resultado:
  resultado = st.session_state.resultado

  st.subheader("Legendas geradas:")

  legendas = resultado.get("legendas", [])
  if not legendas:
    st.warning("Nenhuma legenda foi gerada.")
  else:
    for i, item in enumerate(resultado["legendas"]):
      legenda_original = item.get("mensagem", "")

      with st.container(border=True):
        col1, col2 = st.columns([5, 2])
        with col1:
          st.markdown(f"- {legenda_original}")

        with col2:
          copy_button(legenda_original, "📋")

        #Legenda encurtada
        if st.button("Deixar mais curta", key=f"shorten_{i}"):
          try:
            with st.spinner("Encurtando legenda..."):
              prompt_shorten = build_shorten_prompt(legenda_original)
              nova_legenda = encurtar_legenda(prompt_shorten)

              st.session_state.legendas_encurtadas[i] = nova_legenda.get("mensagem", "")

          except Exception as e:
            st.error(f"Erro ao encurtar legenda: {e}")

        if i in st.session_state.legendas_encurtadas:
          legenda_curta = st.session_state.legendas_encurtadas[i]

          col1, col2 = st.columns([5, 2])
          with col1:
            st.markdown(f"**Versão mais curta:** {legenda_curta}")  

          with col2:
            copy_button(legenda_curta, "📋")

  # Exibição das hashtags
  hashtags = resultado.get("hashtags", [])
  if not hashtags:
    st.warning("Nenhuma hashtag foi gerada.")
  else:
    st.subheader("Hashtags sugeridas:")
    
    cols_per_row = 3

    for start in range(0, len(hashtags), cols_per_row):
        row_items = hashtags[start:start + cols_per_row]
        cols = st.columns(cols_per_row, gap="small")

        for col, hashtag in zip(cols, row_items):
            with col:
                with st.container(border=True):
                    st.markdown(f"**{hashtag}**")
                    copy_button(hashtag, "📋 Copiar")

st.write("")

# Exibição do histórico como card
if st.session_state.historico:
    with st.expander("Histórico"):

      if st.button("Limpar histórico", use_container_width=True):
          st.session_state.historico = []
          st.success("Histórico limpo com sucesso!")
          st.rerun()

      for item in reversed(st.session_state.historico):
          with st.container(border=True):
            col1, col2 = st.columns([2, 1])

            with col1:
              st.markdown(f"### {item['tema'].title()}")

            with col2:
              st.caption(f"#### Tom: {item['tom']}")
            
            st.caption(
              f"Quantidade: {item['quantidade']} • Máx. palavras: {item['tamanho']}"
            )

            if item["legendas"]:
                st.markdown("**Legendas:**")
                for legenda in item["legendas"]:
                    st.markdown(f"- {legenda['mensagem']}")

            if item["hashtags"]:
                st.markdown("**Hashtags:**")
                st.markdown(", ".join(item["hashtags"]))

            st.write("")

#with st.expander("Prompt utilizado"):
#  st.code(prompt, language="text")