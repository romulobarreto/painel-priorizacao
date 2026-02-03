# Painel de Priorização de Perdas (Equatorial)

Dashboard em **Streamlit** para visualizar e analisar UCs priorizadas pelo pipeline **alertas-regras-sinais**.

## O que ele faz
- Upload de CSV (separador `;` e decimais com `,`).
- Filtros globais (prioridade, motivo, seccional, alimentador, município, etc.).
- Mapa interativo (Folium + MarkerCluster) com legenda e limite de pontos para performance.
- Tabela detalhada com exportação do recorte filtrado.
- Aba **Análise Estatística** com gráficos de barras (Plotly) e rótulos (estilo Excel/Power BI).

## Estrutura do projeto
```
.
├── app.py
├── requirements.txt
└── src
    ├── assets
    │   └── Logo_Grupo_Equatorial_Energia.png
    ├── data
    │   └── loader.py
    ├── styles
    │   └── custom.py
    └── ui
        ├── analytics.py
        ├── filters.py
        ├── map.py
        ├── metrics.py
        └── table.py
```

## Requisitos
- Python 3.11+ (recomendado)
- Dependências em `requirements.txt`

## Como rodar localmente
1) Crie e ative um ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scriptsctivate  # Windows
```

2) Instale as dependências
```bash
pip install -r requirements.txt
```

3) Rode o app
```bash
streamlit run app.py
```

## Formato esperado do CSV
O loader foi feito para CSV com:
- Separador: `;`
- Decimal: `,` (ex.: latitude/longitude)

Colunas mínimas esperadas:
- `UC`
- `PRIORIDADE` (P1/P2/P3)
- `LATITUDE`
- `LONGITUDE`

Colunas usadas pelos filtros/gráficos (se existirem no arquivo):
- `STATUS_COMERCIAL`, `MOTIVO_PRIORIDADE`, `SECCIONAL`, `SE_AL_NORM`, `MUNICIPIO`, `CONDOMINIO`, `PERIMETRO`, `CLASSE_CONSUMO`

## Observações de performance
- O mapa limita a quantidade de pontos (ex.: 5000) para não travar o navegador.
- Use os filtros para reduzir o volume e navegar melhor.

## Deploy (resumo)
Você pode publicar de três jeitos comuns:

### Opção A) Streamlit Community Cloud (mais simples)
1. Suba o projeto no GitHub.
2. Garanta que `requirements.txt` esteja na raiz e que o entrypoint seja `app.py`.
3. No Streamlit Cloud, selecione o repositório e informe `app.py` como arquivo principal.

### Opção B) Docker (bom pra servidor interno)
Crie um `Dockerfile` e rode em qualquer servidor.

### Opção C) Plataforma interna/empresa
Subir em VM/servidor com systemd + nginx (ou só rodar o Streamlit em porta interna).

## Próximos passos (ideias)
- Cache de carregamento (`st.cache_data`)
- “Top N” configurável nos gráficos
- Exportar gráficos como imagem
- Expandir a aba de *Análise Estatística* (rankings, cruzamentos, etc.)
