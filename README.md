# ✈️ Travel Monitor

> Plataforma web para planejamento e organização de viagens, desenvolvida em Python.

O **Travel Monitor** foi criado para centralizar informações importantes de uma viagem em um único lugar. A aplicação permite explorar destinos, montar roteiros, organizar informações da viagem, salvar destinos favoritos e acessar tudo através de um perfil de usuário.

O projeto também conta com autenticação por **e-mail ou número de telefone**, tornando o acesso mais flexível.

---

## 📌 Sobre o projeto

O Travel Monitor nasceu com a proposta de facilitar o planejamento de viagens de forma simples e organizada.

A aplicação reúne recursos para:

- 🌍 Explorar destinos turísticos
- ❤️ Salvar destinos favoritos
- 🗺️ Criar e organizar roteiros
- 👤 Gerenciar o perfil do usuário
- 🔐 Fazer login com e-mail ou telefone
- 📋 Visualizar informações relacionadas à viagem
- 💰 Organizar informações de orçamento
- 🌦️ Consultar informações de clima
- 👥 Trabalhar com recursos de compartilhamento e grupos

---

## ✨ Principais funcionalidades

### 🔐 Autenticação

O sistema permite autenticação utilizando:

- E-mail
- Número de telefone

O telefone pode ser informado com ou sem formatação, facilitando o acesso do usuário.

### ❤️ Favoritos

Os destinos podem ser adicionados aos favoritos diretamente na área de destinos.

O comportamento é visual:

```text
♡  Destino não favoritado

♥  Destino favoritado
```

Os favoritos ficam associados ao perfil do usuário e podem ser consultados posteriormente.

### 🌎 Destinos

O projeto possui uma coleção de **50 destinos** para exploração.

Cada destino pode ser utilizado como parte do planejamento da viagem e também pode ser salvo como favorito.

### 🗺️ Meu roteiro

A área de roteiro permite organizar os elementos da viagem em um único lugar.

A interface foi organizada para manter uma apresentação consistente de títulos, categorias e informações.

### 👤 Perfil

O perfil concentra informações relacionadas ao usuário e seus destinos favoritos.

### 💰 Orçamento

A aplicação possui uma área dedicada à organização das informações financeiras da viagem.

### 🌦️ Clima

O projeto possui uma área específica para informações climáticas relacionadas à viagem.

### 👥 Compartilhamento e grupos

Também existem recursos voltados para compartilhamento de informações e organização em grupos.

---

## 🛠️ Tecnologias

O projeto utiliza principalmente:

| Tecnologia | Utilização |
|---|---|
| 🐍 Python | Backend da aplicação |
| 🌐 HTML | Estrutura das páginas |
| 🎨 CSS | Interface e estilos |
| ⚡ JavaScript | Interações da interface |
| 🗄️ SQL | Estrutura do banco de dados |
| 🧩 Jinja | Renderização dos templates |

---

## 📁 Estrutura do projeto

```text
Travel-Monitor/
│
├── app.py
├── config.py
├── extensions.py
├── models.py
├── database.sql
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── services/
│   ├── destinations.py
│   └── travel.py
│
├── templates/
│   ├── _sidebar.html
│   ├── base.html
│   ├── cadastro.html
│   ├── clima.html
│   ├── compartilhado.html
│   ├── dashboard.html
│   ├── destinos.html
│   ├── grupo.html
│   ├── login.html
│   ├── orcamento.html
│   ├── perfil.html
│   └── roteiro.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        ├── auth.js
        ├── budget.js
        ├── compartilhado.js
        ├── dashboard.js
        ├── destinos.js
        ├── grupo.js
        ├── profile.js
        ├── roteiro.js
        ├── search.js
        └── weather.js
```

---

## 🚀 Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/travel-monitor.git
cd travel-monitor
```

Substitua `SEU-USUARIO` pelo seu usuário do GitHub.

### 2. Crie um ambiente virtual

No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` baseado no exemplo:

```bash
cp .env.example .env
```

No Windows, também é possível simplesmente copiar `.env.example` e renomeá-lo para `.env`.

Preencha as variáveis necessárias de acordo com a configuração do seu ambiente.

> **Importante:** nunca publique o arquivo `.env` no GitHub.

### 5. Configure o banco de dados

Utilize o arquivo:

```text
database.sql
```

para criar a estrutura necessária do banco.

Depois, confira as configurações de conexão no arquivo `.env`.

### 6. Execute a aplicação

```bash
python app.py
```

Depois, abra no navegador o endereço exibido pela aplicação.

---

## 🔒 Segurança

Este projeto possui um `.gitignore` preparado para evitar o envio acidental de arquivos sensíveis ou temporários.

Não publique no GitHub:

- `.env`
- senhas
- chaves de API
- credenciais de banco
- tokens
- arquivos `.pyc`
- diretórios `__pycache__`
- arquivos de ambiente virtual

Antes de colocar o projeto em produção, revise também as configurações de segurança do ambiente.

---

## 🧹 Organização do código

A estrutura foi organizada para evitar código desnecessariamente repetido.

Por exemplo, elementos compartilhados da interface ficam em templates reutilizáveis, como:

```text
templates/_sidebar.html
```

A lógica relacionada a funcionalidades específicas também foi separada em módulos dentro de:

```text
services/
```

Isso facilita manutenção, leitura e evolução do projeto.

---

## ❤️ Sistema de favoritos

O sistema de favoritos foi desenvolvido para manter o estado associado ao usuário.

Fluxo básico:

```text
Usuário
   │
   ▼
Escolhe um destino
   │
   ▼
Clica no coração
   │
   ├── ♡ → ♥  Adiciona aos favoritos
   │
   └── ♥ → ♡  Remove dos favoritos
   │
   ▼
Favorito permanece associado ao perfil
```

Dessa forma, o usuário pode sair da página e consultar posteriormente os destinos que escolheu.

---

## 🗺️ Fluxo geral da aplicação

```text
                    ┌───────────────┐
                    │    Usuário    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    Login      │
                    │ E-mail/Fone   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   Dashboard   │
                    └───────┬───────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
     ┌──────────┐      ┌──────────┐      ┌──────────┐
     │ Destinos │      │  Roteiro │      │  Perfil  │
     └────┬─────┘      └──────────┘      └────┬─────┘
          │                                    │
          ▼                                    ▼
     ┌──────────┐                        ┌───────────┐
     │ Favoritos│◄───────────────────────│ Favoritos │
     └──────────┘                        └───────────┘
```

---

## 📱 Interface

O projeto utiliza HTML, CSS e JavaScript para criar uma interface web interativa.

A aplicação foi estruturada com componentes reutilizáveis para reduzir repetição entre páginas e facilitar futuras alterações no visual.

---

## 🧪 Validação

Antes da publicação, recomenda-se verificar:

- [ ] Cadastro de usuário
- [ ] Login por e-mail
- [ ] Login por telefone
- [ ] Logout
- [ ] Acesso ao perfil
- [ ] Visualização dos 50 destinos
- [ ] Adição de favorito
- [ ] Remoção de favorito
- [ ] Persistência dos favoritos
- [ ] Criação/visualização do roteiro
- [ ] Área de orçamento
- [ ] Área de clima
- [ ] Recursos de compartilhamento
- [ ] Recursos de grupos

---

## 🔮 Próximos passos

Algumas evoluções que podem ser adicionadas futuramente:

- [ ] Recuperação de senha
- [ ] Confirmação de telefone/e-mail
- [ ] Melhorias de responsividade
- [ ] Testes automatizados
- [ ] Paginação ou filtros avançados de destinos
- [ ] Upload de fotos de viagem
- [ ] Integração com mapas
- [ ] Sistema de avaliações de destinos
- [ ] Deploy em ambiente de produção
- [ ] CI/CD com GitHub Actions

---

## 📚 Objetivo do projeto

Além de ser uma aplicação funcional, o Travel Monitor também serve como projeto de estudo e portfólio para desenvolvimento web com Python.

O projeto aborda conceitos como:

- Desenvolvimento backend
- Templates HTML
- Banco de dados
- Autenticação
- CRUD
- Persistência de dados
- JavaScript no frontend
- Organização de projetos
- Separação de responsabilidades
- Desenvolvimento de interfaces web

---

## 👨‍💻 Autor

**Enzo Coutinho**

GitHub:

https://github.com/EnzoCoutinh0

---

