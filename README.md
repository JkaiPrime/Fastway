# 🚀 FastWay - Sistema de Automação TEF  

**Solução integrada para gestão de transações TEF através do Sitef (Elgin/Comnect)**  

---

## ✒️ Autores  
- **[@Jkai](https://github.com/JkaiPrime)**  

---

## 🎯 Funcionalidades Principais  
- Autenticação automática no portal Software Express  
- Armazenamento seguro de credenciais (usuário, senha, OTP)  
- Consulta de histórico de vendas por usuário  
- Interface de linha de comando (CLI) intuitiva  
- Compatibilidade com ambientes Windows  

---

## 📚 Documentação Técnica  
Para detalhes de implementação e manual avançado, consulte:  
[Documentação Completa](https://github.com/JkaiPrime/Fastway)  

---

## 🖥️ Exemplos de Uso  
1. **Primeiro acesso**:  
   - Execute o aplicativo como administrador  
   - Selecione a opção de cadastro de credenciais  
   - Insira os dados conforme solicitado  

2. **Operações diárias**:  
   - Inicie o sistema e escolha a ação desejada no menu  
   - Para acesso rápido ao portal, selecione a opção correspondente ao servidor  

---

## 🌍 Empresas Utilizadoras  
[Tefway](https://tefway.com.br/)  
*Solução implementada em rede nacional de vendas de Tef*  

---

## ⚙️ Arquitetura Técnica  
Tecnologia | Função | Versão  
-----------|--------|--------  
Python | Lógica de negócios | 3.11+  
SQLite | Armazenamento local | 3.39+  
Selenium | Automação Web | 4.10+  
PyOTP | Geração de tokens | 2.8+  
PyInstaller | Distribuição Windows | 5.13+  

---
Estrutura:
```
Fastway
├─ LICENSE
├─ README.md
├─ app.py
├─ assets
│  └─ favicon.ico
├─ requirements.txt
└─ src
   ├─ Services
   │  └─ service_db.py
   ├─ database.py
   └─ fiserv_and_linx
      ├─ express.py
      └─ relatorio_express.py

```
---
## 📜 Licenciamento  
Distribuído sob licença **MIT** - Consulte os termos completos em:  
[Licença MIT](https://github.com/JkaiPrime/Fastway/blob/main/LICENSE)  

---

## 📬 Contato & Suporte  
**Equipe de Desenvolvimento**  
✉️ suporte@tefway.com.br

**Responsável Técnico**  
👤 [@Jkai](https://github.com/JkaiPrime)  
