# Travel Monitor — v14

Aplicação Flask + MySQL para pesquisa e planejamento de viagens.

## Novidades desta versão

- **50 destinos em alta**: página dedicada com 50 destinos (25 Brasil + 25 internacionais), descrição e atrações de referência.
- **Pesquisa em modo demonstração**: resultados fictícios para testar a interface de voos, hotéis, ônibus e atrações. Eles ficam identificados como demonstração e não devem ser tratados como ofertas reais.
- **Pesquisa real** continua disponível quando as integrações reais estão configuradas.
- **Meu roteiro**: destino → quantidade de dias → dia → intervalo de horário → atividade, sem pedir o dia novamente para cada atividade.
- **Roteiro compartilhado**: proprietário pode compartilhar por link, adicionar pessoas por e-mail e remover membros. Proprietário e membros podem adicionar/remover atividades.
- **Viagem em grupo**: pacotes fictícios para planejamento, criação de viagem personalizada, convite por link, participantes e orçamento colaborativo.
- **Segurança**: senha com Argon2id, CSRF, rate limiting, sessão protegida e convite de roteiro assinado.

## Banco de dados

O `app.py` usa `db.create_all()` para criar tabelas novas automaticamente. O `database.sql` também contém as tabelas necessárias para instalação manual.

## Executar

```powershell
cd C:\caminho\do\projeto
& "C:\Users\estagiario.ti\AppData\Local\Programs\Python\Python314\python.exe" -m pip install -r requirements.txt
& "C:\Users\estagiario.ti\AppData\Local\Programs\Python\Python314\python.exe" app.py
```

Configure o `.env` com `SECRET_KEY` persistente e as credenciais das APIs reais quando quiser sair do modo demonstração.
