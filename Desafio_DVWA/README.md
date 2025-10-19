![medusavshydradvwa](https://github.com/ThiagoMaria-SecurityIT/Bootcamp_DIO_e_Santander-Ciberseguran-a_2025/blob/main/Desafio_DVWA/images/medusahydradvwa.png)

🟢 FINALIZADO - Atividades concluídas e revisadas (Entregue antes do prazo)  

> [!Important]
> - Sucesso no Brute Force com Hydra após perceber que a Medusa não consegue lidar com CSRF.  
> - O nível do DVWA estava no `Impossible`
> - Foi modificado um dos scripts do DVWA (login.php), comentando uma linha expecíficia que valida os tokens de segurança CSRF


# Desafio: Simulando um Ataque de Brute Force com Medusa e Análise de Proteções CSRF

**Desafio Santander Cibersegurança 2025 em parceria com a DIO**
>[!TIP]
> - O script Python para automação de tentativas em formulário web (DVWA nível low) está aqui: [Redirect Brute Forcer](https://github.com/ThiagoMaria-SecurityIT/Bootcamp_DIO_e_Santander-Ciberseguran-a_2025/blob/main/Desafio_DVWA/redirect_brute_forcer.py)
> - O Desafio de ataque em FTP do Metasploitable 2 está aqui: [Desafio Brute Force Ataque FTP Metasploitable](https://github.com/ThiagoMaria-SecurityIT/Bootcamp_DIO_e_Santander-Ciberseguran-a_2025/tree/main/Desafio%20de%20For%C3%A7a%20Bruta%20em%20FTP%20do%20Metasploitable%202)

## Índice
1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)[.](#tutorial-rápido-e-secreto-nível-impossible-ou-qualquer-outro)
2. [Configuração do Ambiente](#2-configuração-do-ambiente)
3. [Análise Inicial com cURL](#3-análise-inicial-com-curl)
4. [Entendendo o CSRF na Prática](#4-entendendo-o-csrf-na-prática)
5. [Testes com Medusa](#5-testes-com-medusa)
6. [Análise do Código-Fonte](#6-análise-do-código-fonte)
7. [Resultados](#7-resultados-antes-e-depois-de-entender-como-desativar-a-validação-do-csrf)
8. [Análise Detalhada](#8-análise-detalhada-dos-resultados)
9. [Conclusões Técnicas](#9-conclusões-técnicas)
10. [Lições Aprendidas como Profissional de Segurança](#10-lições-aprendidas-como-profissional-de-segurança)
11. [Recomendações de Mitigação](#11-recomendações-de-mitigação)
12. [Próximos Passos e Expansão](#12-próximos-passos-e-expansão)
13. [Conclusão Final](#13-conclusão-final)
14. [About Me](#14-about-me--contact)

## 1. Visão Geral do Projeto

### Objetivo Principal
Este projeto teve como objetivo principal entender na prática como mecanismos de segurança modernos, especificamente proteções CSRF (Cross-Site Request Forgery), impactam a eficácia de ferramentas automatizadas de brute force. Como profissional de segurança em constante evolução, busquei ir além do uso superficial de ferramentas e compreender os porquês por trás dos sucessos e falhas.

### Metodologia Adotada
Adotei uma abordagem científica para o projeto:
- **Análise**: Estudo detalhado do alvo antes de qualquer ataque
- **Experimentação**: Testes controlados com diferentes ferramentas
- **Documentação**: Registro detalhado de cada etapa e resultado
- **Análise**: Interpretação dos resultados e extração de aprendizado

### Ferramentas Utilizadas
- **Kali Linux**: Sistema operacional para testes de segurança
- **DVWA (Damn Vulnerable Web Application)**: Alvo controlado para testes
- **Medusa**: Ferramenta de brute force
- **Hydra**: Alternativa para comparação
- **cURL**: Ferramenta essencial para análise manual
- **GitHub**: Plataforma para documentação e portfólio

## 2. Configuração do Ambiente

### Download, Configuração e Instação do Kali e Metasploitable 2 na VirtualBox  

  Para essa parte fiz um outro repositório para ajudar os outros estudantes a entenderem:  
  
  - Quais sites encontrar as ferramentas (VirtualBox, Kali Linux e Metasploitable) utilizdas nesse projeto  
  - Como fazer o download e configurar o Kali Linux e a Metasploitable na VirtualBox  
  - Dicas para resolver problemas simples de configuração  

Esse é o link do repositório com os vídeos [Laboratório Kali Linux & Metasploitable](https://github.com/ThiagoMaria-SecurityIT/Bootcamp_DIO_e_Santander-Ciberseguran-a_2025/tree/main/security-training-lab)

### Instalação do DVWA  

Existem outros jeito de utilizar o DVWA que não seja fazendo o download do Metasploitable 2.  
A partir daqui, todos os testes do DVWA foram feitos com a versão instalada pelo terminal do Kali Linux e não a versão que vem com o Metasploitable.  
Lembrando que:

- Estou com o Kali Linux instalado na VirtualBox somente para esse desafio (não utilizei essa máquina virtual antes).
- A internet foi utilizada somente para o download do DVWA pelo terminal.
- A rede da máquina virtual com Kali foi mudada para "host only" antes de iniciar o DVWA.
- A máquina virtual com Kali não estava compartilhando arquivos com o host (meu computador de lab de segurança).
- A máquina virtual com Kali foi deletada após o esse desafio.

 >[!Tip]
 >- Você pode utilizar o DVWA online em sites como o TryHackMe, HackTheBox e VulnHub

- Você pode utilizar a versão que preferir, pois é a mesma ferramenta    


 > [!CAUTION]  
 > Não instale o DVWA na sua máquina do dia-a-dia, independe da distro Linux que você utiliza  
 > **Existem riscos significativos** em instalar o DVWA diretamente no Linux que você utiliza no dia-a-dia como:
 >  - Configurações de segurança podem ser comprometidas
 >  - Arquivos de configuração podem ser alterados/acidentais
 >  - Exposição acidental à internet se serviços não forem configurados corretamente
 >  - Vulnerabilidades reais no DVWA podem afetar seu sistema principal
 >  - Risco de backdoors se não isolado adequadamente
 >  - Conflito de versões (PHP, Apache, MySQL)
 >  - Portas em uso (80, 443, 3306 podem já estar ocupadas)



- Algumas configurações para outros cenários podem ser diferentes dessas:
  
```bash
# Atualização do sistema
sudo apt update

# Instalação do DVWA
sudo apt install dvwa

# Inicialização do serviço
dvwa-start
```

**Observação** (Desligue a internet): O comando `dvwa-start` faz automaticamente:
- Inicia os serviços necessários (Apache, MySQL)
- Configura o banco de dados
- Abre o navegador padrão no endereço `http://127.0.0.1:42001/login.php`

### Configuração Inicial do DVWA

Após a instalação, foi necessário:
1. **Login inicial** com credenciais padrão: `admin`/`password`
2. **Configuração do banco de dados** através do script de setup
3. **Ajuste do nível de segurança** para "Low" para testes iniciais

### Estrutura do Ambiente

```
VirtualBox (Virtualização dos Ambientes)
    ↓
Kali Linux (Atacante)
    ↓
DVWA (127.0.0.1:42001) (Alvo)
    ↓
Formulário de Login (/login.php)
    ↓
Mecanismo CSRF (Proteção)
```

## 3. Análise Inicial com cURL

### Primeira Investigação

Comecei com uma análise básica do formulário de login do DVWA:

```bash
# Comando básico para visualizar o HTML do formulário
curl http://127.0.0.1:42001/login.php -s

# Filtrando apenas elementos relevantes
curl http://127.0.0.1:42001/login.php -s | grep -E "username|password|token|submit"
```

**Resultado Esperado:**
```html
<input type="text" class="loginInput" size="20" name="username">
<input type="password" class="loginInput" size="20" name="password">
<input type="submit" value="Login" name="Login">
<input type='hidden' name='user_token' value='8afba5f0f1431a381e5698f891e1eac3' />
```

### Análise Detalhada dos Elementos

**Campos Identificados:**
1. **username**: Campo de texto para nome de usuário
2. **password**: Campo de senha
3. **Login**: Botão de submissão (com name attribute)
4. **user_token**: Campo hidden com token CSRF

### Testes Manuais de Login

**Teste com Credenciais Corretas:**
```bash
curl -X POST http://127.0.0.1:42001/login.php \
  -d "username=admin&password=password&Login=Login" \
  -c cookies.txt -L -v
```

**Teste com Credenciais Incorretas:**
```bash
curl -X POST http://127.0.0.1:42001/login.php \
  -d "username=admin&password=wrongpassword&Login=Login" \
  -s | grep "Login failed"
```

### Análise de Headers e Cookies

```bash
# Verificando headers de resposta
curl -I http://127.0.0.1:42001/login.php

# Analisando cookies de sessão
curl http://127.0.0.1:42001/login.php -c cookies.txt -v
```

**Descoberta Importante**: Cada requisição gerava um novo token CSRF, mesmo dentro da mesma sessão.

## 4. Entendendo o CSRF na Prática

### O Que é CSRF?

CSRF (Cross-Site Request Forgery) é um mecanismo de segurança que:
- **Gera tokens únicos** para cada formulário
- **Vincula tokens à sessão** do usuário
- **Valida a origem** das requisições
- **Previne ataques automatizados** que não mantêm estado

### Como Funciona no DVWA

**Fluxo Normal:**
1. Usuário acessa `/login.php`
2. Servidor gera token único `ABC123` e armazena na sessão
3. Token é enviado no formulário como campo hidden
4. Ao submeter, servidor compara token do form com token da sessão
5. Se coincidirem: login processado
6. Se divergirem: login bloqueado

**Fluxo com Ataque Automatizado:**
1. Ferramenta acessa `/login.php` e recebe token `ABC123`
2. Ferramenta tenta login, mas o token já expirou
3. Servidor gera novo token `DEF456` para próxima requisição
4. Ferramenta continua usando token antigo `ABC123`
5. Todas as tentativas falham por token inválido

### Testes com Diferentes Abordagens

**Teste 1 - Token Estático:**
```bash
# Tentativa com token fixo 
curl -X POST http://127.0.0.1:42001/login.php \
  -d "username=admin&password=password&Login=Login&user_token=123456" \
  -s -w "Status: %{http_code}\n"
```

**Teste 2 - Sem Token:**
```bash
# Tentativa sem token 
curl -X POST http://127.0.0.1:42001/login.php \
  -d "username=admin&password=password&Login=Login" \
  -s -w "Status: %{http_code}\n"
```

**Teste 3 - Token Dinâmico:**
```bash
# Extraindo token dinamicamente
TOKEN=$(curl http://127.0.0.1:42001/login.php -s | grep -o "user_token' value='[^']*" | cut -d"'" -f3)
curl -X POST http://127.0.0.1:42001/login.php \
  -d "username=admin&password=password&Login=Login&user_token=$TOKEN" \
  -c cookies.txt -L -v
```

### Análise de Comportamento

**Padrões Identificados:**
- **Status 302 + Location: login.php** → Falha de autenticação
- **Status 302 + Location: index.php** → Login bem-sucedido
- **Status 200 com "Login failed"** → Credenciais incorretas
- **Status 200 sem redirecionamento** → Token CSRF inválido

---

## 5. Testes com Medusa

### Preparação para os Testes

#### Criação das Wordlists

Antes de iniciar os testes com Medusa, preparei wordlists específicas e realistas:

**usernames.txt:**
```bash
administrator
root2
admin
root
admin2
test
user
username
```

**passwords.txt:**
```bash
admin
123456
letmein
password
default
test
pass123
```

**Justificativa das Wordlists:**
- **Usernames**: Incluí variações comuns de "admin" e usuários padrão
- **Passwords**: Senhas comuns e default do DVWA ("password")
- **Tamanho controlado**: Para testes rápidos e eficientes

#### Comando Base do Medusa

```bash
medusa -h 127.0.0.1 -U usernames.txt -P passwords.txt -M web-form \
  -m FORM:"/login.php" \
  -m DENY-SIGNAL:"Login failed" \
  -m FORM-DATA:"post?username=&password=&Login=Login" \
  -n 42001 \
  -v 4
```

### Primeira Tentativa - Falha Imediata

**Comando Executado:**
```bash
medusa -h 127.0.0.1 -U usernames.txt -P passwords.txt -M web-form \
  -m FORM:"/login.php" \
  -m DENY-SIGNAL:"Login failed" \
  -m FORM-DATA:"post?username=&password=&Login=Login" \
  -v 4
```

**Resultado:**
```
Medusa v2.3 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks <jmk@foofus.net>

NOTICE: web-form.mod: failed to connect, port 443 was not open on 127.0.0.1
```

**Análise do Erro:**
- Medusa tentou usar HTTPS (porta 443) por padrão
- DVWA estava rodando em HTTP na porta 42001
- Necessidade de ajuste na sintaxe

### Segunda Tentativa - Correção de Porta

**Comando Corrigido:**
```bash
medusa -h 127.0.0.1 -U usernames.txt -P passwords.txt -M web-form \
  -m FORM:"/login.php" \
  -m DENY-SIGNAL:"Login failed" \
  -m FORM-DATA:"post?username=&password=&Login=Login" \
  -n 42001 \
  -v 4
```

**Resultado:**
```
ACCOUNT CHECK: [web-form] Host: 127.0.0.1 User: administrator Password: admin
ERROR: The answer was NOT successfully received, understood, and accepted while trying administrator admin: error code  302
```

**Análise Detalhada:**
- Medusa conseguiu conectar na porta correta
- Recebeu resposta 302 (Redirect) do servidor
- Não conseguiu processar o redirecionamento
- Falha na detecção do sinal "Login failed"

### Terceira Tentativa - Ajuste na Detecção

**Comando com Debug Ativado:**
```bash
medusa -h 127.0.0.1 -U usernames.txt -P passwords.txt -M web-form \
  -m FORM:"/login.php" \
  -m DENY-SIGNAL:"302 Found" \
  -m FORM-DATA:"post?username=&password=&Login=Login" \
  -n 42001 \
  -v 6
```

**Resultado com Verbose:**
```
DEBUG MODULE: [web-form.mod] Sending Web Form Authentication (POST).
DEBUG: Data sent: POST //login.php HTTP/1.0
Host: 127.0.0.1:42001
User-Agent: I'm not Mozilla, I'm Ming Mong
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 49

username=administrator&password=admin&Login=Login

DEBUG MODULE: [web-form.mod] Retrieving server response.
DEBUG: Data received (485): HTTP/1.1 302 Found
Server: nginx/1.28.0
Location: login.php
Set-Cookie: PHPSESSID=53117d204cb5a239b5c6bc199c5e589f
```

**Problema Identificado:**  
- Servidor respondia com 302 Found e Location: login.php  
- Medusa não seguia redirecionamentos  
- Nunca via a página com "Login failed" (essencial para automação do brute force com Medusa)  
- Impossível detectar sucesso/falha corretamente  

### Análise das Limitações do Medusa

**Problemas Encontrados:**
1. **Não mantém sessão**: Cada requisição era independente
2. **Não segue redirecionamentos**: Perdia a resposta real do servidor
3. **Não extrai tokens dinâmicos**: Usava o mesmo token em todas as tentativas
4. **User-Agent fixo**: Fácil de identificar e bloquear

**Comando de Teste com cURL para Comparação:**
```bash
# Simulando o que o Medusa enviava
curl -X POST http://127.0.0.1:42001/login.php \
  -H "User-Agent: I'm not Mozilla, I'm Ming Mong" \
  -d "username=administrator&password=admin&Login=Login" \
  -s -I
```

## 6. Análise do Código-Fonte

### Localização do Arquivo de Login

```bash
# Encontrando o arquivo login.php
sudo find / -name "login.php" 2>/dev/null | grep dvwa

# Resultado: /usr/share/dvwa/login.php
```

### Análise da Implementação CSRF

**Trecho Relevante do Código:**
```php
<?php
// ... código anterior ...

if( isset( $_POST[ 'Login' ] ) ) {
    // Anti-CSRF
    if (array_key_exists ("session_token", $_SESSION)) {
        $session_token = $_SESSION[ 'session_token' ];
    } else {
        $session_token = "";
    }

    checkToken( $_REQUEST[ 'user_token' ], $session_token, 'login.php' );

    // ... processamento do login ...
}

// ... código posterior ...

// Anti-CSRF
generateSessionToken();

// ... renderização do formulário ...
echo tokenField();
?>
```

### Estrutura de Proteção Identificada

**1. Geração do Token:**
```php
generateSessionToken(); // Gera novo token a cada carregamento
```

**2. Inclusão no Formulário:**
```php
echo tokenField(); // Output: <input type='hidden' name='user_token' value='TOKEN_AQUI' />
```

**3. Validação no Submit:**
```php
checkToken($_REQUEST['user_token'], $session_token, 'login.php');
// Retorna erro se tokens não coincidirem
```

### Modificação para Testes Controlados

**Antes da Modificação:**
```php
checkToken( $_REQUEST[ 'user_token' ], $session_token, 'login.php' );
```

**Após Modificação:**
```php
// checkToken( $_REQUEST[ 'user_token' ], $session_token, 'login.php' );
```

**Comando para Modificação:**
```bash
sudo nano /usr/share/dvwa/login.php
# Localizar linha com checkToken e comentar
```

### Análise do Mecanismo de Token

**Como os Tokens Funcionam:**
- **Geração**: `generateSessionToken()` cria token único
- **Armazenamento**: Salvo em `$_SESSION['session_token']`
- **Validação**: `checkToken()` compara token do form com token da sessão
- **Rotatividade**: Novo token a cada requisição

**Impacto nos Testes:**
- Cada tentativa do Medusa usava token diferente
- Sem manutenção de sessão, tokens nunca coincidiam
- Todas as validações falhavam, mesmo com credenciais corretas

## 7. Resultados (`antes e depois` de entender como desativar a validação do CSRF)

#### Esses resultados foram conquistados após todas as análises das ferramentas e dos sistemas requeridos (e ensinados pela DIO) no desafio. As análises estão um pouco mais pra cima dessa parte.

- **1. A ferramenta Medusa** mostrava `[SUCCESS]` em **todos** os logins e senhas tentadas nos ataques, o que não era real.
  - Os resultados estavam estranhos - todos usernames e senhas que eu criava apareciam como "SUCCESS", indicando que eram logins válidos para acessar o sistema web DVWA. 
  - De imediato desconfiei, e a partir desses resultados estranhos comecei uma análise detalhada (era nítido que a ferramenta não estava funcionando direito).
  - Comecei a coletar, guardar e organizar as evidências relacionadas aos resultados estranhos da ferramenta Medusa.

- **2. A ferramenta Hydra** (que também funciona igual a Medusa, fazendo ataques de brute force), também mostrava que todas as palavras (wordlists) testadas eram válidas como logins verdadeiros.
  - Testar dois ou três logins comprovavam que não eram válidos e que as ferramentas não estavam mostrando resultados reais.
  - Ou seja, eram resultados **falsos-positivos**.

**Imagem abaixo**: ferramenta Hydra mostrando que todos os usernames e senhas são verdadeiros para acessar o sistema web DVWA.   

![falsopositivodahydra](https://github.com/ThiagoMaria-SecurityIT/Bootcamp_DIO_e_Santander-Ciberseguran-a_2025/blob/main/Desafio_DVWA/images/hydra1.png) 

### Análise do Comportamento do Hydra

**Problemas Identificados:**
- Hydra também não mantinha estado de sessão
- Cada tentativa recebia token CSRF diferente
- Validação sempre falhava por token inválido
- Mesmo com credenciais corretas, o acesso era bloqueado

### Teste Após Desativar Validação CSRF

**Após comentar a linha do `checkToken()` no código login.php do DVWA, executei o comando da Hydra novamente:**  
  - Primeiro testei com tokens diferentes, resultado: Funcionou
  - Depois testei sem token, resultado: Funcionou também
  - Resumo da Hydra: após desativar o `checkToken()` a Hydra conseguiu fazer o ataque BruteForce
  - Resumo da Medusa: não conseguiu fazer o ataque de BruteForce mesmo com o `checkToken()` desativado

```bash
hydra -L username.txt -P passwords.txt 127.0.0.1 http-post-form \
  "/login.php:username=^USER^&password=^PASS^&Login=Login:F=Login failed" \
  -vV -s 42001
```
  
- Mesmo desativando a validação de Token (checkToken), o DVWA ainda continuava a gerar tokens.     
- A ferramenta Hydra conseguiu funcionar corretamente mesmo a geração de tokens, porém a Medusa não conseguiu.    
- Depois desativei algumas outras partes do código para não gerar os Tokens mas mesmo assim a Medusa não conseguiu realizar com sucesso o ataque de Brute Force no formulário web da DVWA.    
- Não vou colocar todos os testes porque não funcionaram, pois todos os níveis de dificuldade do DVWA tem a geração de token, tanto o low, até o Impossible.    
- Para a Medusa funcionar, teria que remover a geração de Tokens em cada um dos níveis, não só no login.php.    
- Como a Hydra funcionou e a já era esperado que a Medusa não funcionária, pois não tem como gerenciar Brute Force com Tokens na Medusa, partir para a conclusão do desafio.    
- A ferramenta Medusa funcionou normalmente atacando o Metasploitable, como ftp, que exige só uma linha de comando para concluir o ataque com sucesso.    


**Imagem 1:** colocando "//" na linha do `checkToken` para desativar a validação do CSRF no DVWA (script: login.php)   

![](https://github.com/ThiagoMaria-SecurityIT/Bootcamp_DIO_e_Santander-Ciberseguran-a_2025/blob/main/Desafio_DVWA/images/loginphpcomment.png)   

- **Teste 1**: Mesmo desativando o checkToken, os tokens ainda eram gerados, então tentei o BruteForce com o mesmo token da sessão.   
**Image 2:** Resultado após comentar // na linha do checkToken, com Token no comando de ataque diferente do token da sessão = Funcionou
  
![](https://github.com/ThiagoMaria-SecurityIT/Bootcamp_DIO_e_Santander-Ciberseguran-a_2025/blob/main/Desafio_DVWA/images/hydrasuccess.png) 

- **Teste 2**: Minha lógica continuou no que deu certo: "Se o ataque funcionou com tokens deiferentes pois os tokens não são validados (desativamos comentando com "//"), então não precisa dos números e letras dos tokens no comando do ataque."
    - Então removi o token do comando de ataque da Hydra, comprovando que minha lógica estava certa: Não precisa de token no ataque `SE` não existe a validação dos mesmos.
    - A lógica continuou nos tokens, "se a Hydra funcionou, vou testar se a Medusa também funciona agora que os tokens não são validados".
         - Mas não, a Medusa não conseguiu fazer o ataque com sucesso, pois mesmo que não exista a validação dos tokens, eles `AINDA` estavam sendo gerados.
         - Conclusão:
           -   A ferramenta Medusa não consegue lidar com tokens em ataques de brute force sozinha.
           -   Já a Hydra consegue lidar com tokens gerados, sozinha, mas não consegue lidar com a validação dos tokens (precisa de outras ferramentas).  
    
      
  
**Image 3:** Sucesso após rodar a Hydra sem expecificar um token no comando de ataque do Terminal (pois o checkToken estava desativado no login.php)  
![](https://github.com/ThiagoMaria-SecurityIT/Bootcamp_DIO_e_Santander-Ciberseguran-a_2025/blob/main/Desafio_DVWA/images/hydrasucessoweb.png)



### Comparação Entre Ferramentas

| Aspecto | Medusa | Hydra |
|---------|---------|--------|
| **Manutenção de Sessão** | ❌ Não mantém | ❌ Não mantém |
| **Tokens CSRF** | ❌ Não manipula | ❌ Não manipula |
| **Redirecionamentos** | ❌ Não segue | ✅ Segue |
| **Detecção de Sucesso** | ❌ Limitada | ✅ Flexível |
| **Velocidade** | ⚡ Muito rápida | 🐢 Mais lenta |

### Testes com Múltiplos Usuários

**Comandos Hydra com Lista de Usuários:**
```bash
hydra -L usernames.txt -P passwords.txt 127.0.0.1 http-post-form \
  "/login.php:username=^USER^&password=^PASS^&Login=Login:F=Login failed" \
  -vV -s 42001
```

```bash
#Comando em uma linha
hydra -L usernames.txt -P passwords.txt 127.0.0.1 http-post-form "/login.php:username=^USER^&password=^PASS^&Login=Login:F=Login failed" -vV -s 42001
```

**Resultado:**
- **Sucesso**: `admin:password`
- **Falha**: Todos os outros usuários
- **Tempo**: Aproximadamente 30 segundos para 56 combinações

---

## 8. Análise Detalhada dos Resultados

### Comparação Técnica Aprofundada

#### Comportamento com CSRF Ativo

**Medusa com CSRF Ativo:**
```bash
# Comando executado
medusa -h 127.0.0.1 -U usernames.txt -P passwords.txt -M web-form \
  -m FORM:"/login.php" -m DENY-SIGNAL:"Login failed" \
  -m FORM-DATA:"post?username=&password=&Login=Login" -n 42001 -v 4

# Comportamento observado
- Conexão estabelecida com sucesso
- Resposta HTTP 302 recebida
- Não consegue detectar "Login failed" (não segue redirect)
- Falha em todas as tentativas
- Taxa de sucesso: 0%
```

**Hydra com CSRF Ativo:**
```bash
# Comando executado
hydra -L usernames.txt -P passwords.txt 127.0.0.1 http-post-form "/login.php:username=^USER^&password=^PASS^&Login=Login&user_token=ccdd7f329362a78cc6bed4122bf0b5e5:F=Login failed" -vV -s 42001

# Comportamento observado
- Segue redirecionamentos
- Detecta página de login após redirect
- Consegue ver "Login failed" 
- Mas validação CSRF bloqueia acesso
- Taxa de sucesso: 0%
```

#### Comportamento com CSRF Desativado

**Medusa com CSRF Desativado:**
```bash
# Mesmo comportamento - ainda falha
- Continua sem seguir redirects
- Não mantém sessão entre tentativas
- Taxa de sucesso: 0%
```

**Hydra com CSRF Desativado:**
```bash
# Comando executado
hydra -L usernames.txt -P passwords.txt 127.0.0.1 http-post-form "/login.php:username=^USER^&password=^PASS^&Login=Login:F=Login failed" -vV -s 42001

# Comportamento radicalmente diferente
- Segue redirecionamentos normalmente
- Detecta corretamente sucesso/falha
- Encontra credenciais admin:password
- Taxa de sucesso: 100% para credenciais conhecidas
```

### Análise de Performance

**Tempos de Execução:**
- **Medusa**: ~5 segundos (falha rápida)
- **Hydra (CSRF ativo)**: ~20 segundos (tentativas completas mas sem sucesso)
- **Hydra (CSRF desativado)**: ~30 segundos (sucesso na 4ª tentativa)

**Eficiência de Detecção:**
- **Medusa**: Não detecta nenhum cenário corretamente
- **Hydra**: Detecta todos os cenários quando CSRF está desativado

## 9. Conclusões Técnicas

### Eficácia do CSRF como Mecanismo de Defesa

**Proteção Comprovada:**
- ✅ Bloqueia ferramentas automatizadas simples
- ✅ Requer manipulação manual para bypass
- ✅ Implementação relativamente simples
- ✅ Impacto mínimo em usuários legítimos

**Estatísticas de Eficácia:**
- **Medusa**: 100% de bloqueio
- **Hydra**: 100% de bloqueio (com validação ativa)
- **Scripts simples**: 100% de bloqueio
- **Ataques manuais**: Requer conhecimento técnico avançado

### Limitações das Ferramentas de Brute Force

**Problemas Comuns Identificados:**

1. **Falta de Manutenção de Estado:**
```python
# Exemplo do problema
# Ferramentas fazem:
request1 = GET /login.php → token_ABC
request2 = POST /login.php (com token_ABC) → token já expirou

# Deveriam fazer:
session = requests.Session()
request1 = session.get(/login.php) → token_ABC  
request2 = session.post(/login.php, token_ABC) → token ainda válido
```

2. **Processamento Insuficiente de JavaScript:**
- Muitas aplicações modernas usam JS para manipular tokens
- Ferramentas CLI não executam JavaScript
- Tokens dinâmicos via JS são completamente invisíveis

3. **Gestão Primitiva de Cookies:**
```bash
# Gestão básica (ferramentas atuais)
curl -b cookies.txt -c cookies.txt

# Gestão ideal necessária
- Manter sessões separadas por usuário
- Renovar cookies de sessão automaticamente
- Lidar com múltiplos domínios/paths
```

## 10. Lições Aprendidas como Profissional de Segurança

**Habilidades Desenvolvidas:**

1. **Análise Forense de Aplicações Web:**
```bash
# Técnicas que funcionaram bem
curl -s URL | grep -E "token|csrf|hidden"  # Identificação rápida
curl -I URL # Análise de headers
curl -v URL # Debug detalhado
```

2. **Metodologia de Testes Estruturada:**
```
Minha Abordagem:
1. Reconhecimento → Análise do formulário
2. Diagnóstico → Identificação de proteções  
3. Experimentação → Testes com diferentes ferramentas
4. Documentação → Registro de resultados
5. Análise → Interpretação e aprendizado
```

3. **Pensamento Adaptativo:**
- Quando Medusa falhou, não desisti
- Usei cURL para entender o problema
- Testei alternativas (Hydra)
- Adaptei a abordagem baseado nos resultados

**Competências Técnicas Comprovadas:**

- **Análise de Código-Fonte**: Capacidade de ler e entender implementações de segurança
- **Diagnóstico de Problemas**: Habilidade para identificar causas raiz de falhas
- **Conhecimento Multi-Ferramenta**: Versatilidade com diferentes tecnologias
- **Documentação Técnica**: Clareza na comunicação de descobertas complexas

## 11. Recomendações de Mitigação

### Para Desenvolvedores

**Implementação de CSRF (Exemplo Python/Flask):**
```python
from flask import Flask, session, request, render_template_string
import secrets
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def generate_csrf_token():
    """Gera e armazena token CSRF na sessão"""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_urlsafe(32)
    return session['csrf_token']

def validate_csrf_token():
    """Valida token CSRF para requisições POST"""
    if request.method == "POST":
        token = session.get('csrf_token')
        form_token = request.form.get('csrf_token')
        if not token or token != form_token:
            return False
    return True

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not validate_csrf_token():
            return "Erro de segurança CSRF", 400
            
        # Processar login normalmente
        username = request.form['username']
        password = request.form['password']
        # ... validação de credenciais
        
    # Renderizar formulário com token
    return render_template_string('''
        <form method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
            <input type="text" name="username" placeholder="Usuário">
            <input type="password" name="password" placeholder="Senha">
            <button type="submit">Login</button>
        </form>
    ''', csrf_token=generate_csrf_token())
```

**Camadas Adicionais de Segurança Recomendadas:**

1. **Rate Limiting:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # 5 tentativas por minuto por IP
def login_post():
    # ... lógica de login
```

2. **Proteção Contra Credenciais Comuns:**
```python
COMMON_PASSWORDS = {'password', '123456', 'admin', 'letmein'}

def is_common_password(password):
    return password.lower() in COMMON_PASSWORDS
```

### Para Administradores de Sistemas

**Configurações de Servidor Web (Exemplo Nginx):**
```nginx
# Rate limiting no nível do servidor
http {
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    
    server {
        location /login.php {
            limit_req zone=login burst=10 nodelay;
            # ... outras configurações
        }
    }
}
```

**Monitoramento e Detecção:**
```bash
# Exemplo de monitoramento com fail2ban
# /etc/fail2ban/jail.d/web-login.conf
[web-login]
enabled = true
port = http,https
filter = web-login
logpath = /var/log/nginx/access.log
maxretry = 5
bantime = 3600
```

### Para Equipes de Segurança

**Testes Recomendados:**
```bash
# Script de teste CSRF básico
#!/bin/bash
echo "=== Teste de Proteção CSRF ==="

# Teste 1: Requisição sem token
echo "Teste 1 - Sem token CSRF:"
curl -X POST $URL -d "username=test&password=test" -s -w "Status: %{http_code}\n"

# Teste 2: Requisição com token inválido  
echo "Teste 2 - Token CSRF inválido:"
curl -X POST $URL -d "username=test&password=test&csrf_token=invalid" -s -w "Status: %{http_code}\n"

# Teste 3: Verificar se token está presente
echo "Teste 3 - Verificar presença de token:"
curl -s $URL | grep -q "csrf_token" && echo "✅ CSRF detectado" || echo "❌ CSRF não detectado"
```

## Validação do Aprendizado

### Competências Demonstradas

**Habilidades Técnicas:**
- ✅ Análise de aplicações web
- ✅ Uso de ferramentas de brute force
- ✅ Diagnóstico de mecanismos de segurança
- ✅ Manipulação de sessões HTTP
- ✅ Análise de código-fonte

**Habilidades Metodológicas:**
- ✅ Abordagem científica para testes
- ✅ Documentação técnica detalhada
- ✅ Análise crítica de resultados
- ✅ Adaptação estratégica
- ✅ Comunicação de descobertas

**Habilidades de Segurança:**
- ✅ Compreensão de vetores de ataque
- ✅ Conhecimento de controles defensivos
- ✅ Avaliação de eficácia de segurança
- ✅ Desenvolvimento de recomendações
- ✅ Consciência ética

### Aplicação Prática do Conhecimento

**Como Este Conhecimento se Aplica no Mundo Real:**

1. **Testes de Penetração:**
- Agora entendo por que alguns ataques automatizados falham
- Posso explicar aos clientes a eficácia de suas proteções
- Sei quando investir tempo em ataques manuais vs automatizados

2. **Desenvolvimento Seguro:**
- Posso implementar proteções CSRF eficazes
- Compreendo a importância da segurança em camadas
- Sei balancear segurança e usabilidade

3. **Arquitetura de Segurança:**
- Posso recomendar controles baseado em eficácia comprovada
- Entendo as limitações de diferentes abordagens
- Posso priorizar implementações baseado em risco

## 12. Próximos Passos e Expansão

### Melhorias para Este Projeto

**Script de Automação:**
```python
#!/usr/bin/env python3
"""
Script avançado para teste de brute force com manipulação de CSRF
"""
import requests
from bs4 import BeautifulSoup
import sys

class AdvancedBruteForcer:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        
    def extract_csrf_token(self, html_content):
        """Extrai token CSRF do HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        token_input = soup.find('input', {'name': 'user_token'})
        return token_input['value'] if token_input else None
    
    def attempt_login(self, username, password):
        """Tenta login mantendo sessão e tokens"""
        # Primeiro, obtém a página de login
        response = self.session.get(self.target_url)
        csrf_token = self.extract_csrf_token(response.text)
        
        if not csrf_token:
            print("❌ Token CSRF não encontrado")
            return False
            
        # Prepara dados do formulário
        login_data = {
            'username': username,
            'password': password,
            'Login': 'Login',
            'user_token': csrf_token
        }
        
        # Envia requisição de login
        response = self.session.post(self.target_url, data=login_data)
        
        # Verifica se login foi bem-sucedido
        return "Login failed" not in response.text

# Implementação futura...
```

### Expansões Possíveis

1. **Testes com Outras Ferramentas:**
   - Burp Suite Intruder
   - OWASP ZAP
   - Patator
   - Ncrack

2. **Cenários Adicionais:**
   - Proteções com CAPTCHA
   - Autenticação multi-fator
   - Block por IP
   - Análise de comportamento

3. **Integração com CI/CD:**
   - Testes automatizados de segurança
   - Scan de vulnerabilidades
   - Relatórios automáticos

## 13. Conclusão Final

Este projeto demonstrou de forma prática e mensurável que:

### Proteções CSRF são eficazes mas podem ser contornadas   
- **Eficácia comprovada** contra ferramentas automatizadas tradicionais (Medusa e Hydra)  
- **Implementação simples** com grande impacto em proteção
- **Mínimo impacto** na experiência do usuário legítimo (não consome muitos recursos do navegador ou do computador)  

### As Ferramentas Tem Limitações Significativas
- **Medusa**: Inadequado para aplicações com CSRF
- **Hydra**: Limitado sem manipulação manual
- **Automação**: Requer scripts customizados para eficácia
- **CSRF não é 100% de garantia de proteção:** No Kali tem outras ferramentas que contornam o CSRF, esse projeto simples é somente para Brute Force com Medusa e Hydra e não envolve outras ferramentas do Kali.  

### O Conhecimento Técnico é Fundamental
- **Ferramentas são meios, não fins**
- **Análise manual complementa automação**
- **Documentação acelera o aprendizado**

### Valor para Minha Carreira
Como profissional de segurança, este projeto:
- **Validou conhecimentos** teóricos na prática
- **Expandiu meu toolkit** técnico
- **Reforçou a importância** da metodologia
- **Demonstrou competência** em documentação técnica

**Próximo Nível:** O desafio me motivou a explorar desenvolvimento de ferramentas customizadas e testes mais avançados, solidificando meu caminho como especialista em segurança ofensiva.

---

**Autor:** Thiago Maria   
**Data:** Outubro de 2025   
**Desafio:** Santander Cibersegurança 2025 em parceria com a DIO     

---

### Tutorial rápido e secreto (nível `Impossible` ou qualquer outro):

1. Instale o DVWA  
```bash
# Atualização do sistema
sudo apt update

# Instalação do DVWA
sudo apt install dvwa

# Inicialização do serviço
dvwa-start
```
2. Entre no login.php do DVWA  

```
sudo nano /usr/share/dvwa/login.php
```
3. Comente com `//` para desativar o checkToken  
```
// checkToken( $_REQUEST[ 'user_token' ], $session_token, 'login.php' );
```
4. Rode a Hydra
```
hydra -L usernames.txt -P passwords.txt 127.0.0.1 http-post-form "/login.php:username=^USER^&password=^PASS^&Login=Login:F=Login failed" -vV -s 42001
```

*"A segurança não é um produto, mas um processo contínuo de aprendizado e adaptação."*

---

## 14. About Me & Contact

**Thiago Maria - From Brazil to the World 🌎**  
*Senior Information Security Professional | Security Risk & Compliance Specialist | AI Security Researcher | Software Developer | Post-Quantum Cryptography Enthusiast*

My passion for programming and my professional background in security analysis led me to create this GitHub account to share my knowledge of security information, cybersecurity, Python, and AI development practices. My work primarily focuses on prioritizing security in organizations while ensuring usability and productivity.

Let's Connect:  

👇🏽 Click on the badges below:  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/thiago-cequeira-99202239/)  
[![Hugging Face](https://img.shields.io/badge/🤗Hugging_Face-AI_projects-yellow)](https://huggingface.co/ThiSecur)  
   


