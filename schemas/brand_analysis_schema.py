from google.genai import types

BRAND_ANALYSIS_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "video_url": {
            "type": "STRING",
            "description": "URL do vídeo analisado."
        },
        "temas_abordados": {
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            },
            "description": "Lista dos principais temas abordados pelo criador no vídeo."
        },
        "estilo_conteudo": {
            "type": "STRING",
            "description": "Estilo do conteúdo do criador (ex: humorístico, informativo, etc.)."
        },
        "publico_alvo_estimado": {
            "type": "OBJECT",
            "properties": {
                "faixa_etaria": {
                    "type": "STRING",
                    "description": "Faixa etária estimada do público."
                },
                "genero": {
                    "type": "STRING",
                    "description": "Gênero predominante do público (ex: masculino, feminino, misto)."
                },
                "interesses": {
                    "type": "ARRAY",
                    "items": {
                        "type": "STRING"
                    },
                    "description": "Lista dos principais interesses do público."
                },
                "localizacao_geografica": {
                    "type": "STRING",
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
            "type": "STRING",
            "description": "Descrição do engajamento do público com o conteúdo do criador."
        },
        "valores_e_tom": {
            "type": "OBJECT",
            "properties": {
                "valores": {
                    "type": "ARRAY",
                    "items": {
                        "type": "STRING"
                    },
                    "description": "Lista dos valores que o criador parece promover."
                },
                "tom": {
                    "type": "STRING",
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
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            },
            "description": "Lista das plataformas principais onde o criador atua."
        },
        "colaboracoes_anteriores": {
            "type": "STRING",
            "description": "Descrição das colaborações anteriores do criador com marcas (ou 'Nenhuma' se não houver)."
        },
        "nichos_de_mercado": {
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            },
            "description": "Lista dos nichos de mercado com maior relevância para o criador."
        },
        "marcas_match": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "tipo_marca": {
                        "type": "STRING",
                        "description": "Tipo de marca (ex: moda feminina, produtos de beleza veganos, etc.)."
                    },
                    "exemplos": {
                        "type": "ARRAY",
                        "items": {
                            "type": "STRING"
                        },
                        "description": "Lista de exemplos de marcas específicas."
                    },
                    "justificativa": {
                        "type": "STRING",
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
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            },
            "description": "Lista dos tipos de colaboração mais eficazes com o criador."
        },
        "consideracoes_imagem_marca": {
            "type": "STRING",
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