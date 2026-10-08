# task bocache

Executa o comando `bo cache update` do pacote `bo-cli`, que constrói um cache para armazenar o **ID** e o **caminho** dos objetos do **BusinessObjects**:

- Ao passar o caminho para o `bo export`, ele consegue buscar o ID no cache.

- Isso diminui o número de requisições a cada `bo export`.

```text
➜  dados-orcamentarios git:(main) task bocache
Construindo cache para <usuario>...
  83 objetos...
83 objetos salvos em ~/.bocli/cache.json
```

Exemplo curto do `cache.json`:

```json
{
  "updated_at": "2026-10-02T22:09:48.980751+00:00",
  "username": "<usuario>",
  "user_folder_id": 45016161,
  "children": {
    "45016161": [
      {"id":45048915,"name":"~WebIntelligence","type":"Folder"},
      {"id":45426145,"name":"dados_check_siafi","type":"Folder"},
      {"id":45122135,"name":"dados_classificadores","type":"Folder"},
      {"id":45119619,"name":"dados_siafi","type":"Folder"}
    ],
    "45426145": [
      {"id":45426146,"name":"current","type":"Folder"}
    ],
    "45426146": [
      {"id":45426235,"name":"alteracoes_orcamentarias","type":"Webi"},
      {"id":45426236,"name":"cota","type":"Webi"},
      {"id":45426237,"name":"credito","type":"Webi"},
      {"id":45426238,"name":"execucao","type":"Webi"},
      {"id":45426239,"name":"execucao_alem_credito","type":"Webi"},
      {"id":45426240,"name":"receita","type":"Webi"},
      {"id":45426241,"name":"restos_pagar","type":"Webi"},
      {"id":45426242,"name":"restos_pagar_folha","type":"Webi"}
    ]
  }
}
```
