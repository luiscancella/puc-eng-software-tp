# Arquitetura do Sistema de Gestão de Estoque

## Sumário

- Objetivo deste documento
- Visão geral da solução
- Escolha de tecnologias
- Modelo arquitetural (C4)
  - Contexto do Sistema (C1)
  - Contêineres (C2)
  - Componentes principais (C3)
- Justificativa do modelo escolhido
- Implantação e ambiente de desenvolvimento
- Observações e próximos passos

## Objetivo deste documento

Descrever a arquitetura da solução proposta para o “Sistema de Gestão de Estoque”, apontando decisões tecnológicas, modelo arquitetural (C4) e justificativas para as escolhas. Este documento serve como referência para implementação, revisões de código e alinhamento da equipe.

## Visão geral da solução

O sistema é uma aplicação web responsiva que permite:

- cadastrar produtos;
- registrar entradas e saídas;
- gerar relatórios e alertas para estoque mínimo;
- gerenciar usuários com níveis de permissão (Administrador, Operador).

Requisitos não-funcionais importantes: banco relacional (Postgres), tempo de resposta < 2s, autenticação segura, responsividade e boa experiência em dispositivos móveis.

## Escolha de tecnologias (resumo)

As escolhas abaixo visam equilíbrio entre produtividade, escalabilidade e facilidade de deploy:

### Front-end

- **React** (CRA / Vite): ecossistema maduro, componetização e interoperabilidade.
- **TypeScript**: tipagem estática, menos bugs e autocompletar.
- **Tailwind CSS**: produtividade na estilização e layout responsivo com baixo CSS custom.
- **React Query** (ou SWR): cache/estado para chamadas HTTP, ótimo para dados de listagem/consulta.
- **Axios / fetch**: cliente HTTP.

### Back-end

- **Micronaut (Java)** *ou* **Spring Boot (Java)**:
  - Preferência: **Micronaut** se a equipe já tem experiência (menor tempo de startup, boa para microsserviços). **Spring Boot** é alternativa sólida se preferir ecossistema mais comum.
- **JWT** para autenticação stateless.
- **Spring Security** / Micronaut Security para autorização.
- **JPA / Hibernate** (se Java) para mapeamento objeto-relacional.

### Banco de Dados

- **PostgreSQL**: integridade transacional, queries analíticas, compatível com exportações e relatórios.

### DevOps / Infra

- **Docker + Docker Compose** para desenvolvimento local.
- **GitHub Actions** para CI (build, testes, lint, build image).
- **Heroku / Render / DigitalOcean App Platform** ou **container registry + Kubernetes** para produção (depende do escopo).
- **Flyway / Liquibase** para versionamento do schema.

### Observabilidade

- Logs estruturados (JSON) + rotacionamento.
- Métricas básicas via Prometheus (opcional) e dashboards simples (Grafana) em projetos maiores.

## Modelo arquitetural (C4)

### C1 — Contexto do Sistema

O Sistema de Gestão de Estoque (SGE) oferece funcionalidade de controle de produtos e movimentações aos usuários (Administrador e Operador). Interage com fornecedores externos (importação/CSV), e com sistemas de pagamento / ERP no futuro (integrações).

**Atores:**

- **Administrador** — gerencia produtos e usuários, gera relatórios.
- **Operador** — registra entradas/saídas, consulta estoques.
- **Sistema Web (navegador/ dispositivo móvel)** — UI cliente.
- **Banco de Dados (Postgres)** — persistência.

(PlantUML C1 abaixo no anexo.)

### C2 — Contêineres

Visão em contêineres (cada item pode rodar em container Docker):

1. **Web App (Front-end)**  
   - Tecnologia: React + TypeScript + Tailwind  
   - Responsabilidade: UI, validação de formulário, chamadas às APIs, consumo de WebSocket para alertas (opcional).

2. **API (Back-end)**  
   - Tecnologia: Micronaut (ou Spring Boot) + Java + JPA  
   - Responsabilidade: regras de negócio, autenticação/autorização, endpoints REST, geração de relatórios, exportação (PDF/Excel).  
   - Autenticação: JWT.  
   - Observação: expor também endpoints para integração futura (ex.: importação CSV).

3. **Banco de Dados (PostgreSQL)**  
   - Responsabilidade: persistência ACID, índices para consultas frequentes.

4. **Worker / Scheduler (opcional)**  
   - Tecnologia: mesmo runtime que API ou Node/Python  
   - Responsabilidade: tarefas agendadas, envio de alertas por e-mail, geração periódica de relatórios.

5. **Reverse Proxy / CDN (opcional)**  
   - NGINX para servir front e fazer TLS termination em produção.

6. **CI/CD (GitHub Actions)**  
   - Build, testes, lint, publicar container image.

### C3 — Componentes (do back-end)

Dentro do container **API**, componentes principais:

- **Auth Service** — login, refresh tokens, roles/claims.
- **Product Service** — CRUD produtos, buscas, filtros, baixo estoque.
- **Stock Movement Service** — registrar entradas/saídas, validar regras (ex.: não permitir saída se insuficiente).
- **Report Service** — gerar relatórios e endpoints de exportação (CSV/PDF/Excel).
- **User Management** — cadastrar/editar/excluir usuários.
- **Notification Component** — envio de alertas (via WebSocket e e-mail).
- **Repository Layer** — JPA repositories (ProductRepository, MovementRepository, UserRepository).
- **API Layer (Controller)** — endpoints REST, DTOs e validações.
- **Integration Layer** — import CSV e endpoints externos.

---

## Justificativa do modelo escolhido

- **C4** é leve, bem aceito e facilita a comunicação entre stakeholders e devs. Permite passar da visão de negócio (C1) até componentes técnicos (C3) sem se aprofundar no código.
- Arquitetura em contêiner desacoplada facilita testes e deploy contínuo, e permite escalar apenas o que é necessário (ex.: replicar API, manter um único banco).
- **Micronaut/Spring Boot + Postgres**: escolha madura para aplicações CRUD com requisitos transacionais. Integridade e desempenho para consultas de inventário.
- **React + TypeScript + Tailwind**: entrega UX responsiva com alta produtividade e manutenção simples.