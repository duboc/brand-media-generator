Prompt para Análise de Vídeo de Criador de Conteúdo e Identificação de Matches com Marcas (Output em JSON Schema)
Objetivo: Analisar o vídeo de um criador de conteúdo para identificar informações relevantes sobre seu público, estilo, temas abordados e engajamento, e determinar quais tipos de marcas seriam um bom "match" com esse criador, considerando os filtros inteligentes e hipersegmentados da plataforma descrita abaixo. O output deverá ser formatado em JSON seguindo o schema pré-definido.

Contexto: Uma plataforma ajuda marcas a encontrar criadores de conteúdo que se alinhem com seus valores e objetivos, facilitando o "match" perfeito. A plataforma oferece filtros inteligentes e hipersegmentados para busca rápida e precisa, permitindo analisar perfis completos em um só lugar. Graças às integrações oficiais com Instagram, TikTok e YouTube, a plataforma oferece uma visão unificada de tudo o que precisa, diretamente na plataforma.

Instruções:

Assista ao vídeo do criador de conteúdo atentamente.

Identifique e anote os seguintes elementos:

Temas Abordados: Quais são os principais temas que o criador aborda no vídeo? (Ex: moda, beleza, jogos, culinária, etc.)

Estilo de Conteúdo: Qual é o estilo do conteúdo do criador? (Ex: humorístico, informativo, educativo, inspirador, etc.)

Público-Alvo Estimado: Qual é a faixa etária, gênero, interesses e localização geográfica do público-alvo provável do criador?

Engajamento: Como o público interage com o conteúdo do criador? (Ex: comentários positivos, perguntas, compartilhamentos, etc.)

Valores e Tom: Quais valores o criador parece promover e qual é o tom geral do seu conteúdo? (Ex: sustentabilidade, inclusão, positividade, etc.; formal, informal, sarcástico, etc.)

Plataforma(s) Principal(is): Em qual(is) plataforma(s) o vídeo foi publicado (e o criador atua mais ativamente)? (Ex: Instagram, TikTok, YouTube)

Colaborações Anteriores (se houver): O criador já fez alguma colaboração com marcas anteriormente? Se sim, quais e em quais termos?

Com base nas informações coletadas, determine:

Nichos de Mercado: Em quais nichos de mercado o criador tem maior relevância?

Marcas "Match": Quais tipos de marcas (com exemplos) seriam um bom "match" com o criador, considerando os filtros inteligentes e hipersegmentados da plataforma? Justifique.

Tipos de Colaboração: Quais tipos de colaboração (ex: posts patrocinados, reviews de produtos, criação de conteúdo conjunto, etc.) seriam mais eficazes com esse criador?

Considerações sobre a Imagem da Marca: O que as marcas precisam considerar sobre a imagem do criador para garantir um "match" positivo?

Formate suas conclusões em um objeto JSON seguindo o schema abaixo.

Schema JSON:

{
  "type": "object",
  "properties": {
    "video_url": {
      "type": "string",
      "description": "URL do vídeo analisado."
    },
    "temas_abordados": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Lista dos principais temas abordados pelo criador no vídeo."
    },
    "estilo_conteudo": {
      "type": "string",
      "description": "Estilo do conteúdo do criador (ex: humorístico, informativo, etc.)."
    },
    "publico_alvo_estimado": {
      "type": "object",
      "properties": {
        "faixa_etaria": {
          "type": "string",
          "description": "Faixa etária estimada do público."
        },
        "genero": {
          "type": "string",
          "description": "Gênero predominante do público (ex: masculino, feminino, misto)."
        },
        "interesses": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Lista dos principais interesses do público."
        },
        "localizacao_geografica": {
          "type": "string",
          "description": "Localização geográfica predominante do público."
        }
      },
      "required": [
        "faixa_etaria",
        "genero",
        "interesses",
        "localizacao_geografica"
      ],
      "description": "Informações sobre o público-alvo estimado do criador."
    },
    "engajamento": {
      "type": "string",
      "description": "Descrição do engajamento do público com o conteúdo do criador."
    },
    "valores_e_tom": {
      "type": "object",
      "properties": {
        "valores": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Lista dos valores que o criador parece promover."
        },
        "tom": {
          "type": "string",
          "description": "Tom geral do conteúdo do criador (ex: formal, informal, etc.)."
        }
      },
      "required": [
        "valores",
        "tom"
      ],
      "description": "Valores e tom do conteúdo do criador."
    },
    "plataformas_principais": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Lista das plataformas principais onde o criador atua."
    },
    "colaboracoes_anteriores": {
      "type": "string",
      "description": "Descrição das colaborações anteriores do criador com marcas (ou 'Nenhuma' se não houver)."
    },
    "nichos_de_mercado": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Lista dos nichos de mercado com maior relevância para o criador."
    },
    "marcas_match": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "tipo_marca": {
            "type": "string",
            "description": "Tipo de marca (ex: moda feminina, produtos de beleza veganos, etc.)."
          },
          "exemplos": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "Lista de exemplos de marcas específicas."
          },
          "justificativa": {
            "type": "string",
            "description": "Justificativa para o 'match' com o criador."
          }
        },
        "required": [
          "tipo_marca",
          "exemplos",
          "justificativa"
        ]
      },
      "description": "Lista dos tipos de marcas que seriam um bom 'match' com o criador."
    },
    "tipos_de_colaboracao": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Lista dos tipos de colaboração mais eficazes com o criador."
    },
    "consideracoes_imagem_marca": {
      "type": "string",
      "description": "Considerações sobre a imagem do criador para garantir um 'match' positivo com a marca."
    }
  },
  "required": [
    "video_url",
    "temas_abordados",
    "estilo_conteudo",
    "publico_alvo_estimado",
    "engajamento",
    "valores_e_tom",
    "plataformas_principais",
    "colaboracoes_anteriores",
    "nichos_de_mercado",
    "marcas_match",
    "tipos_de_colaboracao",
    "consideracoes_imagem_marca"
  ]
}

Saída Esperada: Um objeto JSON formatado de acordo com o schema acima, contendo a análise do vídeo do criador de conteúdo e as sugestões de "matches" com marcas.