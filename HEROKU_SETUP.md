# Guia de Deploy na Heroku - Labubu Brasil

## ✅ Status Atual
- Sistema PIX funcionando 100% no Replit
- API For4Payments testada e aprovada
- Chaves PIX validadas

## 🚨 Problema na Heroku
O erro está na configuração das variáveis de ambiente na Heroku.

## 📋 Como Configurar na Heroku

### 1. Configurar Variáveis de Ambiente na Heroku

No dashboard da sua app na Heroku:

1. Vá em **Settings**
2. Clique em **Reveal Config Vars**
3. Adicione estas variáveis:

```
SESSION_SECRET = qualquer-chave-secreta-123
FOR4PAYMENTS_SECRET_KEY = 0a562f72-7344-48ec-8632-c431ad3cea57
FOR4PAYMENTS_PUBLIC_KEY = sua-chave-publica-aqui
```

### 2. Verificar Deploy

Após configurar as variáveis, faça novo deploy:

```bash
git add .
git commit -m "Fix environment variables"
git push heroku main
```

### 3. Testar no Heroku

Após deploy, teste um pagamento PIX na sua app Heroku.

## 🔧 Debug na Heroku

Se ainda der erro, execute no terminal da Heroku:

```bash
heroku run python heroku_debug.py --app sua-app-name
```

Isso vai mostrar se as variáveis estão carregadas corretamente.

## ✅ Checklist de Deploy

- [ ] Procfile correto: `web: gunicorn --bind 0.0.0.0:$PORT main:app`
- [ ] .python-version: `3.11`
- [ ] pyproject.toml com dependências
- [ ] Variáveis de ambiente configuradas
- [ ] Sistema PIX testado localmente

## 📞 Suporte

Se ainda tiver problemas, verifique os logs da Heroku:

```bash
heroku logs --tail --app sua-app-name
```

O erro deve aparecer nos logs e poderemos corrigir.