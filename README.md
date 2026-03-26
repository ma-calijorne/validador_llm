# LLM Validation MVP

Sistema local para apoio à **validação humana (Human-in-the-Loop)** de respostas de LLMs no domínio de **Enterprise-Grade Data Intelligence**.

---

# Objetivo

Este projeto fornece um ambiente para:

- consultar uma base documental técnica com RAG,
- comparar respostas de um LLM com referências confiáveis,
- apoiar decisões de avaliação humana,
- registrar avaliações estruturadas.

> Importante: o sistema **não substitui o avaliador humano**. Ele atua como **assistente técnico com grounding documental**.

---

# Arquitetura do sistema

```text
PDFs → Ingestão → Chunking → Embeddings → ChromaDB → RAG → LLM local → Interface → Avaliação
````

---

# Estrutura do projeto

```text
llm_validation_mvp/
├── app/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── models.py
│   │   └── utils.py
│   ├── embeddings/
│   │   ├── __init__.py
│   │   ├── embedder.py
│   │   └── index_builder.py
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── repository.py
│   │   ├── rubric.py
│   │   └── schema.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── build_corpus.py
│   │   ├── chunker.py
│   │   ├── clean_text.py
│   │   └── parse_pdf.py
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   ├── prompt_builder.py
│   │   └── retriever.py
│   └── ui/
│       ├── __init__.py
│       └── streamlit_app.py
├── data/
│   ├── raw/
│   │   └── pdf/
│   ├── processed/
│   └── vectordb/
├── database/
│   └── evaluations.db
├── prompts/
├── scripts/
│   ├── __init__.py
│   ├── build_corpus.py
│   ├── build_index.py
│   └── run_ui.py
├── .env
├── README.md
└── requirements.txt
```

---

# Pré-requisitos

## 1. Python

Recomendado: **Python 3.11+**

## 2. Ambiente virtual

Crie e ative o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Dependências

Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

## 4. Ollama

Este projeto usa um modelo local via **Ollama**.

Exemplo:

```bash
ollama pull qwen2.5:7b
ollama list
```

---

# requirements.txt

Use este conteúdo no arquivo `requirements.txt`:

```txt
chromadb==1.0.15
streamlit==1.48.0
sentence-transformers==3.0.1
pymupdf==1.24.9
pydantic==2.8.2
python-dotenv==1.0.1
pandas==2.2.2
ollama==0.3.1
tqdm==4.66.5
```

---

# Arquivo .env

Crie um arquivo `.env` na raiz do projeto com o conteúdo abaixo:

```env
APP_NAME=llm_validation_mvp
DATA_DIR=./data
RAW_PDF_DIR=./data/raw/pdf
PROCESSED_DIR=./data/processed
VECTORDB_DIR=./data/vectordb
SQLITE_PATH=./database/evaluations.db

EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
OLLAMA_MODEL=qwen2.5:7b

CHROMA_COLLECTION=enterprise_data_intelligence_docs
TOP_K=5
CHUNK_SIZE=1200
CHUNK_OVERLAP=200
```

---

# Como usar o sistema

## Passo 1. Adicionar documentos

Coloque os arquivos PDF da base técnica em:

```text
data/raw/pdf/
```

## Boas práticas para os documentos

Prefira documentos:

* técnicos,
* confiáveis,
* com texto extraível,
* relacionados diretamente ao domínio.

Exemplos adequados:

* Data Governance
* Data Mesh
* Data Architecture
* Data Quality
* Metadata / Lineage
* Data Observability
* BI / Analytics
* IA aplicada a dados corporativos

Evite:

* PDFs escaneados sem OCR,
* conteúdo promocional fraco,
* documentos duplicados,
* materiais muito curtos ou pouco técnicos.

---

## Passo 2. Gerar o corpus

Na raiz do projeto, execute:

```bash
python -m scripts.build_corpus
```

### O que esse comando faz

* lê os PDFs em `data/raw/pdf/`,
* extrai o texto,
* limpa o conteúdo,
* divide em chunks,
* salva:

```text
data/processed/documents.jsonl
data/processed/chunks.jsonl
```

### Resultado esperado

```text
Documents processed: X
Chunks generated: Y
```

---

## Passo 3. Construir o índice vetorial

Execute:

```bash
python -m scripts.build_index
```

### O que esse comando faz

* lê os chunks processados,
* gera embeddings,
* grava o índice no ChromaDB em:

```text
data/vectordb/
```

### Resultado esperado

```text
Indexed chunks: Y
```

---

## Passo 4. Executar a interface

Suba a interface Streamlit com:

```bash
python -m scripts.run_ui
```

Se quiser rodar diretamente:

```bash
PYTHONPATH=. streamlit run app/ui/streamlit_app.py
```

### Acesso

Abra no navegador:

```text
http://localhost:8501
```

---

# Fluxo de uso do app

## 1. Informar o nome do avaliador

Na barra lateral, preencha o nome do avaliador.

Exemplo:

```text
Marco Soares
```

## 2. Ajustar o Top-K

`Top-K` controla quantos chunks serão recuperados da base.

Sugestão prática:

* perguntas objetivas: `Top-K = 5`
* perguntas mais amplas: `Top-K = 7 ou 8`

## 3. Inserir o prompt avaliado

No campo **Prompt avaliado**, informe a pergunta usada no teste.

Exemplo:

```text
Explain the role of data lineage in enterprise-grade data intelligence.
```

## 4. Inserir a resposta do LLM avaliado

No campo **Resposta do LLM avaliado**, cole a resposta gerada pelo modelo da empresa.

## 5. Consultar a base RAG

Clique em **Consultar base RAG**.

O sistema irá:

* recuperar os chunks mais relevantes,
* montar um contexto,
* consultar o modelo local,
* exibir a resposta assistida,
* exibir os trechos recuperados.

## 6. Analisar a resposta RAG e os chunks

Compare:

* a resposta do LLM avaliado,
* a resposta do assistente RAG,
* os documentos recuperados.

Leia também os chunks originais. Não use apenas o resumo do modelo local.

## 7. Preencher a rubrica

Atribua notas de 1 a 5 para cada critério.

## 8. Registrar observações

Explique:

* o que estava correto,
* o que faltou,
* o que parece alucinação,
* se a base recuperada foi suficiente.

## 9. Salvar a avaliação

Clique em **Salvar avaliação**.

Os registros serão gravados em:

```text
database/evaluations.db
```

---

# Rubrica de avaliação

Cada critério deve receber nota de **1 a 5**.

## Critérios

### 1. Corretude técnica

Avalia a precisão conceitual da resposta.

### 2. Cobertura

Avalia se a resposta cobre os principais aspectos da pergunta.

### 3. Aderência ao contexto enterprise

Avalia se a resposta está em nível corporativo e arquitetural adequado.

### 4. Grounding documental

Avalia se a resposta encontra suporte nas fontes recuperadas.

### 5. Clareza

Avalia organização, compreensão e fluidez.

### 6. Precisão terminológica

Avalia o uso correto da terminologia técnica.

### 7. Honestidade epistêmica

Avalia se a resposta reconhece limites, ambiguidades e incertezas.

### 8. Risco de alucinação

Sugestão de interpretação:

| Nota | Interpretação     |
| ---- | ----------------- |
| 5    | risco muito baixo |
| 4    | risco baixo       |
| 3    | risco moderado    |
| 2    | risco alto        |
| 1    | risco muito alto  |

---

# Exemplo de observação do avaliador

```text
A resposta está correta ao definir data lineage como rastreabilidade da movimentação e transformação dos dados, mas faltou conectá-lo à governança, auditoria e observabilidade. O suporte documental recuperado confirma o conceito central, porém a resposta ficou aquém do nível enterprise esperado.
```

---

# Quando reconstruir a base

Você deve rodar novamente:

```bash
python -m scripts.build_corpus
python -m scripts.build_index
```

quando:

* adicionar novos documentos,
* remover documentos,
* alterar chunking,
* trocar o modelo de embeddings,
* perceber baixa qualidade de recuperação.

---

# Problemas comuns

## O app abre, mas o RAG não responde

Verifique:

* se o Ollama está rodando,
* se o modelo existe,
* se o nome configurado em `OLLAMA_MODEL` está correto.

---

## Os resultados recuperados são ruins

Possíveis causas:

* documentos fracos,
* base pequena,
* chunking inadequado,
* embeddings pouco adequados ao idioma,
* pergunta genérica demais.

---

# Boas práticas

* Não confie apenas no texto do RAG.
* Leia os chunks recuperados.
* Não penalize respostas corretas apenas por redação diferente.
* Avalie sempre o nível enterprise.
* Use o campo de observações para justificar a nota.
* Mantenha consistência entre as avaliações.

---

# Exemplo de uso

## Prompt

```text
Compare Data Mesh and centralized data warehouse approaches in enterprise-grade data intelligence.
```

## O que observar na resposta

* distingue descentralização e centralização,
* menciona data as a product,
* aborda governança federada,
* evita simplificações absolutas,
* contextualiza a visão enterprise.

---

---

# Sequência recomendada de execução

## 1. Ativar ambiente virtual

```bash
source .venv/bin/activate
```

## 2. Instalar dependências

```bash
pip install -r requirements.txt
```

## 3. Garantir que o modelo local exista

```bash
ollama pull qwen2.5:7b
```

## 4. Adicionar PDFs

Salvar em:

```text
data/raw/pdf/
```

## 5. Gerar corpus

```bash
python -m scripts.build_corpus
```

## 6. Criar índice vetorial

```bash
python -m scripts.build_index
```

## 7. Rodar interface

```bash
python -m scripts.run_ui
```

---

# Licença

Uso educacional e experimental.