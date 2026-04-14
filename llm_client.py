import json
from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]

if not OPENAI_API_KEY:
  raise RuntimeError("OPEN_API_KEY não encontrada no ambiente.")

client = OpenAI(api_key=OPENAI_API_KEY)

def gerar_legendas(prompt: str, model: str = "gpt-5.4-mini") -> dict:
  try:
    response = client.responses.create(
      model=model,
      input=prompt,
      text={
        "format": {
          "type": "json_schema",
          "name": "Legendas_response",
          "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
              "legendas": {
                "type": "array",
                "additionalProperties": False,
                "items": {
                  "type": "object",
                  "additionalProperties": False,
                  "properties": {
                    "mensagem": {
                      "type": "string"
                    }
                  },
                  "required":["mensagem"]
                }
              },
              "hashtags": {
                "type": "array",
                "additionalProperties": False,
                "items": {
                  "type": "string"
                }
              }
            },
            "required": ["legendas", "hashtags"]
          }
        }
      }
    )

    if not response.output_text:
      raise ValueError("A resposta da API veio sem output_text.")
    
    return json.loads(response.output_text)
  
  except json.JSONDecodeError as e:
    raise ValueError(f"Resposta inválida em JSON: {e}") from e

  except Exception as e:
    raise RuntimeError(f"Erro ao gerar legendas: {e}") from e
  
def encurtar_legenda(prompt: str, model: str = "gpt-5.4-mini") -> dict:
  try:
    response = client.responses.create(
      model=model,
      input=prompt,
      text={
        "format": {
          "type": "json_schema",
          "name": "Shorten_response",
          "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
              "mensagem": {
                "type": "string"
              }
            },
            "required": ["mensagem"]
          }
        }
      }
    )

    if not response.output_text:
      raise ValueError("A resposta da API veio sem output_text.")
    
    return json.loads(response.output_text)
  
  except Exception as e:
    raise RuntimeError(f"Erro ao encurtar legenda: {e}") from e