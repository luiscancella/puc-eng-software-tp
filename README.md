# 📦 Sistema de Gestão de Estoque

## 1. Objetivo

Desenvolver um sistema de gestão de estoque que permita às empresas monitorar, controlar e otimizar a entrada e saída de produtos, garantindo maior eficiência no gerenciamento de recursos, redução de perdas e suporte à tomada de decisão.

## 2. Problema a ser resolvido

Muitas pequenas e médias empresas ainda fazem o controle de estoque de forma manual (planilhas ou registros físicos), o que resulta em:

- Falta de precisão na contagem de produtos
- Dificuldade em acompanhar entradas e saídas em tempo real
- Perdas financeiras por estoque parado ou rupturas de estoque
- Falta de relatórios claros para apoiar a tomada de decisão

O sistema proposto visa resolver esses problemas, automatizando o processo de controle de estoque.

## 3. Tipo de solução

Será desenvolvido um sistema web responsivo, acessível por computadores e dispositivos móveis, com foco em:

- Controle centralizado de estoque
- Interface intuitiva para facilitar o uso por diferentes perfis de usuários
- Relatórios e dashboards para acompanhamento de indicadores

## 4. Requisitos do sistema
### Requisitos Funcionais (RF)

- RF01 – Cadastrar produtos com nome, descrição, categoria, quantidade e valor unitário
- RF02 – Atualizar informações de produtos
- RF03 – Registrar entradas e saídas de produtos no estoque
- RF04 – Gerar relatórios de estoque (estoque atual, movimentações, produtos em baixa quantidade)
- RF05 – Emitir alertas para produtos abaixo do estoque mínimo
- RF06 – Permitir pesquisa e filtragem de produtos
- RF07 – Gerar histórico de movimentações de cada produto
- RF08 – Permitir exportação de relatórios em PDF/Excel
- RF09 – Permitir cadastro de usuários com diferentes níveis de permissão (administrador, operador)

### Requisitos Não Funcionais (RNF)

- RNF01 – O sistema deve ser acessível via navegador web moderno (Chrome, Firefox, Edge)
- RNF02 – Deve armazenar dados em um banco de dados relacional (ex: PostgreSQL ou MySQL)
- RNF03 – O tempo de resposta para consultas deve ser inferior a 2 segundos
- RNF04 – O sistema deve ter autenticação segura (com senha criptografada)
- RNF05 – A interface deve ser responsiva, adaptando-se a desktops, tablets e celulares
- RNF06 – O sistema deve ser desenvolvido seguindo boas práticas de versionamento com Git

## 5. Casos de Uso

O diagrama de caso de uso a seguir ilustra as principais interações dos atores com o sistema

![Diagrama de Caso de Uso](assets/casos_de_uso.png)

### Atores

- **Administrador**: Responsável pela gestão completa do sistema. Possui permissões para cadastrar, editar e excluir produtos, além de gerar relatórios e gerenciar usuários

- **Operador**: Usuário que realiza atividades operacionais no estoque. Tem acesso para registrar entradas e saídas de produtos e consultar relatórios básicos

### Casos de Uso

- Cadastrar Produto: Permite registrar novos produtos no sistema, incluindo informações como nome, descrição, quantidade inicial, categoria e valor unitário
- Atualizar Produto: Atualiza informações de produtos já cadastrados (ex.: alterar preço, ajustar quantidade, atualizar descrição)
- Excluir Produto: Remove produtos obsoletos ou incorretos do sistema
- Gerar Relatórios: Cria relatórios detalhados sobre movimentações, estoque atual, produtos em baixa e históricos
- Gerenciar Usuários: Permite criar, editar ou excluir contas de usuários do sistema, controlando níveis de acesso (administrador, operador)
- Consultar Estoque: Permite verificar a quantidade e os detalhes dos produtos cadastrados em tempo real
- Registrar Entrada de Produto: Registra a entrada de novos itens no estoque (ex.: reposição ou compra de fornecedor)
- Registrar Saída de Produto: Registra a saída de itens do estoque (ex.: venda, transferência ou baixa de produto)
- Visualizar Relatórios Básicos: Permite acessar relatórios simplificados, como produtos disponíveis, produtos em baixa quantidade e movimentações recentes.
