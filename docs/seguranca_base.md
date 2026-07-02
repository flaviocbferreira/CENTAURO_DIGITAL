# Seguranca base

Checklist inicial de seguranca do CENTAURO - DIGITAL PAINEL GERAL.

## Configuracoes obrigatorias

- [x] `SECRET_KEY` lida do `.env`.
- [x] `ALLOWED_HOSTS` lido do `.env`.
- [x] `.env` ignorado pelo Git.
- [x] `.env.example` criado sem dados reais.
- [x] `DEBUG=False` em `config/settings/prod.py`.
- [x] Cookies de sessao seguros em producao.
- [x] Cookies CSRF seguros em producao.
- [x] Redirecionamento HTTPS em producao.
- [x] HSTS configurado em producao.
- [x] Protecao contra iframe com `X_FRAME_OPTIONS="DENY"`.
- [x] Protecao contra content sniffing habilitada.

## Antes de publicar

- [ ] Trocar `SECRET_KEY` por um valor forte e unico.
- [ ] Definir `ALLOWED_HOSTS` com os dominios reais.
- [ ] Revisar `SECURE_HSTS_SECONDS` antes de ativar preload.
- [ ] Confirmar que o deploy usa HTTPS valido.
- [ ] Confirmar que nenhum dado sensivel foi versionado.
