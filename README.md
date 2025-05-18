# orquestracao_dados

Repositório de treinamento para orquestração e manipulação de dados com PySpark.

---

## 📚 Objetivo

Este projeto tem como principal objetivo oferecer um ambiente didático e prático para aprendizado e desenvolvimento de pipelines de dados utilizando PySpark, com foco em:

- Construção e orquestração de pipelines de ETL/ELT locais, trabalhando com arquivos CSV de dados brutos.
- Tratamento e transformação progressiva dos dados, aplicando boas práticas de engenharia de dados.
- Exploração de conceitos de camadas de dados, incluindo Stage, SOR, SOT e Mesh.
- Testes unitários para garantir qualidade e confiabilidade das transformações.
- Integração contínua via GitHub Actions para validação automática do código e pipeline.
- Otimização de performance Spark para processamento eficiente em ambiente local.

---

## 🏗️ Arquitetura e Camadas do Pipeline

O pipeline segue uma arquitetura em camadas, onde cada etapa é responsável por uma transformação específica:

| Camada   | Descrição                                                  | Saída                                   |
|----------|------------------------------------------------------------|-----------------------------------------|
| **STAGE -> SOR**  | Leitura e parsing inicial dos dados brutos (CSV). | DataFrame com tipos e formato corretos.|
| **SOR -> SOT**  | Tratamento avançado, enriquecimento e validação dos dados. | Dados prontos para análise e uso.       |
| **SOT -> MESH** | Geração do JSON/PARQUET final tratado, formato consumível para APIs ou downstream. | Arquivos JSON prontos para consumo.    |

---

## ⚙️ Tecnologias e Ferramentas

- **Python 3.10+**  
- **PySpark** para processamento distribuído e manipulação de grandes volumes de dados  
- **Faker** para geração de dados sintéticos e testes  
- **pytest** para testes unitários  
- **Poetry** para gerenciamento de dependências e ambiente  
- **GitHub Actions** para integração contínua (CI/CD) com validação automática  

---

## 📁 Estrutura do Repositório

📄 .gitignore
📄 LICENSE
📄 README.md
📂 data
│ └── 📄 dados_brutos.csv
📂 outputs
📂 .github
│ 📂 workflows
    │ └── 📄 ci.yml
📂 tests
│ ├── 📄 init.py
│ ├── 📄 test_end_to_end.py
│ ├── 📄 test_mesh.py
│ ├── 📄 test_sor.py
│ ├── 📄 test_sot.py
│ └── 📄 test_stage.py
📂 src
└── pipeline
├── 📄 init.py
├── 📄 sor_sot.py
├── 📄 sot_mesh.py
├── 📄 stage_sor.py
📂 utils
└── 📄 utils.py
└── 📄 json_logger.py
---

## JSON Logger Python


### Logger estruturado em JSON para aplicações Python, com agrupamento visual, contexto, rastreamento de exceções e gravação opcional em arquivo.


### Exemplo de Uso
```python
from json_logger import log_json

# Log de sucesso (INFO)
log_json("Processo finalizado com sucesso.")

# Log de aviso (WARNING)
log_json("Arquivo de configuração não encontrado, usando valores padrão.", level="WARNING")

# Log de erro (ERROR)
try:
    1 / 0
except Exception as e:
    log_json("Erro ao executar operação crítica.", level="ERROR", exc=e)
```


### Exemplo de Saída

```json
==================== ORQUESTRACAO ==================== 
Log de Sucesso (INFO)
{ 
    "timestamp": "2025-05-18T15:03:02.700714-03:00", 
    "level": "INFO", 
    "log_groups": "orquestracao", 
    "message": "Processo finalizado com sucesso.",
    "execution_id": "d4b824e1-c2bb-4c4f-99d0-6ce72651beea",
    "function": "__main__", 
    "file": "main.py:10" 
}

Log de Aviso (WARNING)
{ 
    "timestamp": "2025-05-18T15:03:03.123456-03:00",
    "level": "WARNING", 
    "log_groups": "orquestracao", 
    "message": "Arquivo de configuração não encontrado, usando valores padrão.", 
    "execution_id": "d4b824e1-c2bb-4c4f-99d0-6ce72651beea", 
    "function": "__main__", 
    "file": "main.py:13" 
}

Log de Erro (ERROR)

{
    "timestamp": "2025-05-18T15:15:51.738759-03:00",
    "level": "ERROR",
    "log_groups": "orquestracao",
    "message": "Erro ao executar operação crítica.",
    "execution_id": "d4b824e1-c2bb-4c4f-99d0-6ce72651beea",
    "function": "main",
    "file": "main.py",
    "context": {
        "input": "1/0"
    },
    "error_location": "main.py:17",
    "stacktrace": "ZeroDivisionError: division by zero"
}
```

### Recursos
- Agrupamento visual por grupo de log (group)
- Contexto adicional via parâmetro context
- Rastreamento detalhado de exceções (exc)
- Gravação opcional em arquivo (log_to_file)
- Identificação de função, arquivo e linha do log