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
└── 📄 utils.py
