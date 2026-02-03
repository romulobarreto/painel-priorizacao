# ⚡ Painel de Priorização de Perdas (Equatorial)

> Dashboard em **Streamlit** para visualizar e analisar UCs priorizadas pelo pipeline **alertas-regras-sinais**.

## 🎯 Por que esse painel existe?
Quando a priorização roda (alertas → regras → sinais), o time precisa **bater o olho** e responder rápido:
- Onde estão concentradas as UCs críticas? 🗺️
- Qual seccional/município tem mais oportunidades de recuperar energia? 📍
- Como está a distribuição por prioridade (P1/P2/P3)? 🚦

Esse painel entrega isso em 2 cliques: **upload do CSV do ETL** e pronto.

## ✅ O que ele faz (na prática)
- 📤 Upload de CSV (separador `;` e decimais com `,`).
- 🧰 Filtros globais (prioridade, motivo, seccional, alimentador, município, etc.).
- 🗺️ Mapa interativo (Folium + MarkerCluster) com **legenda** e limite de pontos para performance.
- 📋 Tabela detalhada com **exportação do recorte filtrado**.
- 📊 Aba **Análise Estatística** com gráficos de barras (Plotly) + **rótulos de dados** (estilo Excel/Power BI).

## 🧠 Como usar (workflow rápido)
1. Faça o upload do CSV gerado pelo pipeline.
2. Use os filtros para refinar o recorte.
3. Veja:
   - 📍 **Mapa** para localizar clusters/zonas
   - 📊 **Estatística** para entender distribuição e volume
   - 📋 **Tabela** para agir em cima das UCs

## 🧱 Estrutura do projeto
```text
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

## 🧩 Requisitos
- 🐍 Python **3.12+** (recomendado)
- Dependências em `pyproject.toml`

## ▶️ Rodando local (dev)
1) Clone o projeto
```bash
git clone https://github.com/romulobarreto/painel-priorizacao.git
```

2) Crie e ative o venv
```bash
poetry env use 3.12
source .venv/bin/activate  # macOS/Linux
# .venv\Scriptsctivate  # Windows
```

2) Instale as dependências
```bash
poetry install
```

3) Rode o app
```bash
task run
```

## 🧾 Formato esperado do CSV
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

## 🚀 Deploy na Streamlit Community Cloud
Repositório: https://github.com/romulobarreto/painel-priorizacao

### Passo a passo
1. Garanta que o app rode local (`streamlit run app.py`).
2. Verifique que `pyproject.toml` está na raiz do repo.
3. Acesse o Streamlit Cloud e conecte com seu GitHub.
4. Selecione o repositório `romulobarreto/painel-priorizacao`.
5. Configure:
   - **Main file path:** `app.py`
   - **Branch:** `main`
6. Clique em **Deploy**.

### Dicas de ouro (pra evitar dor de cabeça)
- ✅ Se der erro de dependência, confira `pyproject.toml`.
- ✅ Se der erro com caminho do logo, confira se o arquivo existe em `src/assets/` e o path está correto.
- ✅ CSV muito grande? Use filtros para reduzir o volume no mapa (o app limita pontos por performance).

## ⚙️ Performance
- O mapa limita a quantidade de pontos (ex.: 5000) para não travar o navegador.
- Use os filtros para reduzir o volume e navegar melhor.

## 🛣️ Roadmap (ideias)
- 🧊 Cache do carregamento (`st.cache_data`)
- 🔢 “Top N” configurável nos gráficos
- 🖼️ Exportar gráficos como imagem
- 🧭 Ranking de alimentadores / motivos por seccional

---

Feito com Streamlit + Plotly + Folium.

👨🏻‍💻 Autor Rômulo Barreto da Silva - Analista de Distribuição Pleno
