# Simulação de Ataque Password Spraying em SMB - Metasploitable 2

## 📋 Visão Geral do Desafio

Este projeto demonstra técnicas de enumeração de usuários e password spraying no protocolo SMB, utilizando o ambiente controlado do Metasploitable 2. O objetivo é compreender vulnerabilidades comuns em implementações SMB e praticar medidas defensivas.

## 🔍 Conceitos Fundamentais

### Enumeração de Usuários
Técnica que identifica usuários válidos em um sistema através de análise de respostas do servidor. No contexto SMB, servidores mal configurados podem revelar informações sobre contas locais, políticas de senha e grupos de usuários.

### Password Spraying
Estratégia de ataque que testa poucas senhas comuns contra múltiplos usuários, evitando bloqueios por tentativas excessivas. Contrasta com ataques de força bruta tradicional que testam muitas senhas contra poucos usuários.

## Configuração do Ambiente de Testes

### 🔧 Ambiente Isolado e Seguro

Este laboratório foi configurado com **rede Host-Only no VirtualBox** para garantir um ambiente completamente isolado e seguro para os testes. 

### Características da Configuração:
- **🌐 Sem acesso à internet**: As máquinas virtuais não possuem conectividade com redes externas
- **🔒 Rede interna privada**: Comunicação restrita apenas entre o host e as VMs
- **🛡️ Ambiente controlado**: Ideal para testes ofensivos sem riscos de impacto em sistemas reais

### Por que essa configuração?
- Permite focar exclusivamente nas técnicas de segurança
- Elimina preocupações com tráfego indesejado para redes externas
- Cria um sandbox perfeito para aprendizado e experimentação
- Mantém todo o tráfego de rede visível e controlável

### VMs Utilizadas:
- **Kali Linux** - Ferramentas de teste de penetração
- **Metasploitable 2** - Alvo vulnerável deliberadamente

Esta abordagem garante que todos os exercícios permaneçam dentro do ambiente educacional, seguindo as melhores práticas de ethical hacking.

---

## 🛠️ Execução do Teste

### 1. Enumeração com Enum4linux
```bash
enum4linux -a 192.168.56.110 | tee enum4_output.txt
```
- **enum4linux**: Ferramenta de enumeração para protocolos SMB/RPC
- **192.168.56.102**: IP do Metasploitable 2 (no seu lab pode ser diferente)
- **-a**: Ativa todas as técnicas de enumeração disponíveis
- **tee**: Armazena a saída em arquivo enquanto exibe no terminal
- **Propósito**: Coletar informações sobre usuários, shares, grupos e configurações SMB

## Observações Adicionais:

O **enum4linux** é um wrapper que combina várias ferramentas como **smbclient**, **rpcclient**, **nmblookup** e **net** para realizar uma enumeração abrangente de serviços SMB.

A saída do comando pode revelar:
- Usuários locais e de domínio
- Shares de rede disponíveis
- Políticas de senha
- Informações do sistema
- Grupos e permissões

Está muito bom! Só ajustei o IP para manter consistência com a documentação anterior.

### 2. Análise dos Resultados
```bash
less enum4_output.txt
```
Examina o arquivo gerado para identificar usuários válidos e informações do sistema.

### 3. Criação de Wordlist de Usuários
```bash
echo -e "user\nmsfadmin\nservice" > smb_users.txt
```
Gera lista contendo nomes de usuários comuns para teste.

### 4. Preparação de Senhas para Spraying
```bash
echo -e "password\n123456\nWelcome1213\nmsfadmin" > senhas_spray.txt
```
Cria lista reduzida de senhas comuns para o ataque de password spraying.

### 5. Ataque com Medusa
```bash
medusa -h 192.168.56.110 -U smb_users.txt -P senhas.txt -M smbnt -t 2 -T 50
```
- **-h**: IP do alvo
- **-U**: Arquivo contendo usuários
- **-P**: Arquivo contendo senhas
- **-M smbnt**: Especifica módulo SMB
- **-t 2**: Threads simultâneas
- **-T 50**: Timeout entre tentativas

### 6. Validação de Acesso
```bash
smbclient -L //192.168.56.110 -U msfadmin
```
Agora é só testar o username e o password encontrado com o comando da Medusa.  
A conexão SMB é bem-sucedida com as credenciais comprometidas (do Metasploitable 2).  

## 🛡️ Medidas de Mitigação

### Contramedidas Recomendadas
- Implementar políticas de bloqueio de conta após tentativas falhas
- Utilizar autenticação multifator
- Configurar logs e monitoramento para detecção de tentativas
- Aplicar senhas complexas e únicas por conta
- Restringir acesso SMB à rede interna quando possível
- Atualizar e corrigir sistemas regularmente

## 💡 Aprendizados Adquiridos

- Compreensão prática de vulnerabilidades em serviços SMB
- Técnicas de enumeração em ambientes Windows/Linux
- Estratégias de password spraying e diferenciação de força bruta
- Configuração e uso de ferramentas de teste de penetração
- Importância de logging e monitoramento contínuo

## ⚠️ Considerações Éticas

Este teste foi realizado em ambiente controlado e isolado, utilizando máquinas virtuais dedicadas para fins educacionais. Todas as técnicas devem ser aplicadas apenas em sistemas onde você possui autorização explícita.

---
**Este projeto foi desenvolvido como parte do Santander Open Academy em parceria com a DIO (Digital Innovation One), representando uma valiosa oportunidade de aprimoramento técnico na área de segurança ofensiva e testes de penetração.**

*[Projeto educacional do desafio do Bootcamp Santander Cibersegurança 2025 em parceria com a DIO](https://web.dio.me/home)*

*Documentação técnica para fins educacionais - Contribuição para comunidade de segurança da informação*
