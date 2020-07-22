# Proxies

# Obtendo Tokens

### Chamada
```
curl -d "username=sca_username"\
     -d "password=sca_password"\
     -X POST "/proxies/token/"
```

### Resposta
```
{
    "access": <access-token>,
    "refresh": <refresh-token>
}
```

# Renovando Token de acesso

### Chamada

```
curl -d "refresh=<refresh-token>"\
      -X POST "proxies/refresh-token/"
```

### Resposta

```
{"access": <access-token>}
```

# Acesso ao Proxy de Placas do Solr

### Chamada
#### Argumentos:
 - **token**: token de acesso com ROLE necessária;
 - **dt_inicio**: Inicio do período de busca (ex.: 2020-01-01T12:00:00);
 - **dt_fim**: Fim do período de busca (ex.: 2020-01-01T12:00:00);
 - **placa**:
 - **start**: Início da paginação;
 - **rows**: Número de linhas da resposta.

```
curl -X GET\
 "/proxies/solr/placas?jwt=<access-token>&dt_inicio=<dt_inicio>&dt_fim=<dt_fim>&placa=<placa>&start=<start>&rows=<rows>"
```
