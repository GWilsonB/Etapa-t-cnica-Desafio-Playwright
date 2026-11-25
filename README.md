# Testes E2E do ServeRest com Playwright (Python)

Suíte de testes automatizados do [ServeRest](https://front.serverest.dev), uma loja virtual brasileira de código aberto feita para prática de testes. Cobre login, controle de acesso, cadastro de produtos e lista de compras, com a massa de dados preparada pela API.

## Como executar

Pré-requisitos: Python 3.14 e acesso à internet (os testes rodam contra o ambiente público).

```bash
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest
```

| Comando | O que faz |
|---|---|
| `pytest` | Roda tudo em paralelo (4 processos), sem abrir o navegador |
| `pytest --headed -n 0` | Roda com o navegador visível, um teste por vez |
| `pytest tests/test_login.py` | Roda um arquivo |
| `ruff check .` · `ruff format --check .` · `mypy` | Lint, formatação e tipos |

Depois da execução:

- `reports/report.html`: relatório em arquivo único. Em cada falha, traz screenshot e vídeo embutidos e o link para os traces.
- `test-results/`: os mesmos arquivos, por teste. O trace abre com `playwright show-trace <arquivo.zip>`.
- Testes que usam a API geram dois traces: o do navegador e o das chamadas de API.

Para apontar para outro ambiente, copie `.env.example` para `.env` e ajuste `BASE_URL` e `API_URL`.

## Cenários

| Arquivo | Cenário | Tipo |
|---|---|---|
| `test_login.py` | Admin entra pela interface e chega à home de admin | positivo |
| | Senha incorreta mostra erro e não grava token | negativo |
| `test_access_control.py` | Visitante sem sessão é redirecionado para o login | negativo |
| | Sessão expirada não consegue cadastrar produto | negativo |
| | Cliente comum não consegue cadastrar produto | negativo |
| `test_admin_products.py` | Admin cadastra produto; lista e API mostram os mesmos dados | positivo |
| | Nome de produto duplicado é recusado | negativo |
| `test_shopping_list.py` | Cliente adiciona produto e o total acompanha a quantidade | positivo |
| | Diminuir a última unidade remove o produto | bug conhecido (`xfail`) |

Nos cenários negativos de cadastro, a API confirma que nada foi gravado.

## Estrutura

```
support/     configuração, cliente da API, factories, seed (massa e limpeza), sessão
pages/       Page Objects
tests/       testes e fixtures (conftest.py)
.github/     pipeline
```

## Decisões

| Tema | Decisão | Motivo |
|---|---|---|
| Massa de dados | Cada teste cria seus usuários e produtos pela API e apaga tudo ao final | O ambiente é público, compartilhado e limpo diariamente |
| Sessão | Login pela API e sessão injetada no `localStorage`; a tela de login só é usada em `test_login.py` | Testes mais rápidos e independentes da tela de login |
| Sessão expirada | Simulada com um token inválido | A API responde o mesmo 401 para token ausente, inválido ou expirado; não é preciso esperar os 10 minutos |
| Locators | `data-testid` e papéis de acessibilidade; nenhum XPath ou CSS | Resistem a mudanças de layout |
| Paralelismo | 4 processos (`pytest-xdist`) | Dados isolados por teste; fica abaixo do limite de 300 requisições / 30 s da API |
| Evidências | Screenshot, vídeo e trace apenas em falha, anexados ao relatório | Diagnóstico completo sem custo nas execuções verdes |
| Ambientes | `BASE_URL` e `API_URL` por variável | Limitação: o front público chama sempre `https://serverest.dev`, então as duas URLs precisam ser da mesma stack |

## CI

GitHub Actions, em `.github/workflows/e2e.yml`:

- **Quando roda:** push e PR; dias úteis às 8h; manualmente, com as URLs do ambiente como parâmetro; e por `workflow_call`, para o pipeline da aplicação chamar a suíte após um deploy.
- **Gate:** lint e tipos primeiro, depois os testes. Qualquer falha reprova.
- **Estabilidade:** uma nova tentativa por teste. O que só passa na segunda aparece como *rerun* no relatório.
- **Evidências:** relatório e `test-results/` publicados como artefato, inclusive quando a execução falha.

Em um projeto real, a suíte rodaria depois do deploy em homologação e bloquearia a promoção para produção. Aqui o agendamento faz esse papel, porque a aplicação muda sem commits neste repositório.

## Achados na aplicação

| Achado | Onde | Tratamento na suíte |
|---|---|---|
| Botão "-" com quantidade 1 não remove o item | Lista de compras | Teste `xfail(strict=True)`: acusa quando o bug for corrigido |
| Busca feita antes de o catálogo carregar é sobrescrita pela lista completa | Loja | O Page Object espera o catálogo antes de buscar |
| Cliente comum abre as telas de admin; só a API barra a ação | Rotas `/admin/*` | Teste de cliente comum valida a recusa do backend |
| Sessão expirada não leva o usuário de volta ao login | Telas logadas | Teste de sessão expirada valida o erro exibido |
| `GET /usuarios` devolve as senhas em texto puro | API | Fora do escopo |

## Próximos passos

- Cadastro de usuário, edição e exclusão pela interface.
- Simular API fora do ar com `page.route` para validar o tratamento de erro do front.
- Separar smoke e regressão por marcadores e rodar em mais navegadores.
- Publicar o relatório no GitHub Pages.
