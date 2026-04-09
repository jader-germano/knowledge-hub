# 🎫 Suporte Hostinger — Abertura de Portas SMTP

**Assunto:** Solicitação de abertura de portas SMTP (25, 465, 587) para VPS

**Mensagem:**

Olá, equipe de suporte da Hostinger.

Sou proprietário da VPS com IP **187.77.227.151** (Ubuntu 24.04).

Estou configurando um servidor de e-mail profissional (docker-mailserver) e identifiquei que as conexões externas para as portas **25, 465 e 587** estão sofrendo timeout, mesmo com os serviços rodando e ouvindo em 0.0.0.0.

Já realizei os seguintes testes:
1. Verifiquei que o firewall (UFW) está desativado na VPS.
2. O servidor de e-mail responde perfeitamente a conexões via localhost.
3. Testes via IP direto (sem proxy Cloudflare) também resultam em timeout externo.

**Evidência de erro no cliente de e-mail (macOS Mail):**
Ao tentar configurar a conta `jader@jpglabs.com.br`, o cliente retorna o erro: *"Não foi possível verificar o nome ou a senha da conta"*, confirmando que ele não consegue sequer atingir o servidor de autenticação devido ao bloqueio de rede.

(Veja a imagem anexada ao ticket: `CleanShot 2026-03-07 at 06.50.38@2x.png`)

Poderiam verificar se existe algum bloqueio de segurança a nível de rede da Hostinger nestas portas e realizar a liberação para que eu possa enviar e receber e-mails pelo meu domínio?

Agradeço o apoio.

Atenciosamente,
Jader Germano
JPGLabs
