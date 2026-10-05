# Travel Monitor — versão didática

Esta é uma cópia didática do projeto funcional. O comportamento da aplicação foi preservado; a diferença é que os arquivos de código receberam comentários explicativos antes de cada linha não vazia.

## Como estudar

1. Comece por `app.py`: é o ponto central da aplicação Flask e contém as rotas.
2. Depois leia `models.py`: mostra como usuários, destinos, favoritos e demais dados são representados no banco.
3. Veja `extensions.py` e `config.py`: inicialização das extensões e configurações.
4. Entre em `services/`: concentra regras de negócio para destinos e viagens.
5. Em `templates/`, veja o HTML/Jinja que monta as páginas.
6. Em `static/js/`, veja a interação do navegador com a API e a interface.
7. Em `static/css/`, veja a aparência e responsividade.
8. `database.sql` mostra a estrutura SQL usada para persistência.

## Fluxo principal

**Login:** formulário → rota Flask → busca do usuário por e-mail ou telefone normalizado → criação da sessão → redirecionamento.

**Favorito:** clique no coração → JavaScript envia a ação → servidor verifica o usuário → grava/remove o favorito → página atualiza o coração.

**Perfil:** servidor identifica o usuário da sessão → consulta favoritos → template recebe os dados → navegador mostra os destinos salvos.

## Observação

Os comentários são intencionalmente detalhados para estudo. A versão normal/otimizada continua sendo a indicada para desenvolvimento, porque esta versão tem muitos comentários e fica mais difícil de ler como código de produção.
