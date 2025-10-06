# Laboratório Kali Linux & Metasploitable

🟡 **EM DESENVOLVIMENTO** - Última atualização: 6/OUT/2025

## Objetivo
Implementar e documentar um projeto prático de segurança ofensiva em ambiente controlado e isolado, utilizando Kali Linux e Metasploitable 2 para simular cenários de ataque de força bruta.    

_Imagem abaixo: Máquinas virtuais configuradas no VirtualBox, rede configurada, ataque no FTP com Medusa após varredura com Nmap._    
<img width="1763" height="970" alt="image" src="https://github.com/user-attachments/assets/9726481e-242d-4f3d-a74b-44684005507e" />    

**Análise Técnica da Exposição dos IPs e Login na Imagem:**  
- ✅ Configuração realizada com sucesso conforme metodologia do curso
- 👤 As credenciais msfadmin são padrão do Metasploitable 2 para fins educacionais e não representam uma vulnerabilidade real   
- 🔒 Endereços na faixa 192.168.56.0/24 - rede host-only do VirtualBox (sem internet)    
- 🌐 **Segmento de rede isolado** - tráfego restrito ao ambiente local  
- 📊 Segue o padrão de documentação técnica comum em laboratórios de pentest    
- 🔍 Demonstra corretamente conceitos de redes privadas sem exposição real    

Exibição segura para fins educacionais, mantendo boas práticas de documentação técnica.

Não é a versão final do projeto   

---

## Tutoriais 
- Fiz alguns tutoriais para ajudar quem está enfrendando dificuldades nas configurações dos aplicativos e ferramentas.  
- Espero que ajude!  

### 1. Guia de como baixar (download) e configurar a VirtualBox no Windows 11      
- ▶️ Clique na imagem abaixo para ver o vídeo:    
[![Assistir o vídeo](https://img.youtube.com/vi/VX0QesKhboI/0.jpg)](https://www.youtube.com/watch?v=VX0QesKhboI)   
*O vídeo mostra as configurações no Windows 11 para baixar e instalar o VirtualBox.*

### 2. Guia de como baixar (download) e configurar o Kali Linux na VirtualBox no Windows 11       
- ▶️ Clique na imagem abaixo para ver o vídeo:      
[![Assistir o vídeo](https://img.youtube.com/vi/HEjLa-scVCA/0.jpg)](https://www.youtube.com/watch?v=HEjLa-scVCA)  

### 3. 🎥 Guia passo-a-passo de como baixar (download) e configurar o Metasploitable 2   
- ▶️ Clique na imagem abaixo para ver o vídeo:   
[![Assistir o vídeo](https://img.youtube.com/vi/FprFn0oeEdE/0.jpg)](https://www.youtube.com/watch?v=FprFn0oeEdE)

*O vídeo mostra as configurações (e troubleshooting) de rede no VirtualBox.*

## 🔒 Sobre os IPs Mostrados no Vídeo

**IPv6 (fe80::) - É Seguro?**
- 🔐 **Endereço Local** - O IPv6 que aparece (fe80::) é do tipo "Link-Local"
- 🌐 **Não Tem Acesso à Internet** - Roteadores bloqueiam esse tipo de endereço
- 🏠 **Funciona Só no VirtualBox** - Como um número de telefone interno que só funciona dentro da sua casa virtual.
- ⚠️ **Não é Roteável** - Ninguém pode acessar esse IP de fora da sua máquina

**IPv4 (192.168.xx.x)**
- ✅ **Rede Privada** - Faixa de IP reservada para redes internas
- 🔒 **Host-Only** - Isolada pelo VirtualBox, sem conexão com internet
- 👤 **Credenciais msfadmin** - São padrão do Metasploitable para fins educacionais

---

## ⚠️ Aviso Importante  
**ESTE LABORATÓRIO É EXCLUSIVAMENTE PARA FINS EDUCACIONAIS**
> [!CAUTION]  
> - Todos os testes são realizados em ambiente controlado e isolado  
> - É estritamente proibido replicar estas técnicas sem autorização explícita
> - Não me responsabilizo pelo uso indevido deste conteúdo  

## Configuração do Ambiente
- Duas máquinas virtuais no VirtualBox (Kali Linux + Metasploitable 2)
- Rede interna configurada (host-only)
- Ferramenta Nmap para varredura na rede  
- Ferramenta Medusa para ataques de força bruta

## Serviços em Teste
- FTP - Testado
- DVWA (Damn Vulnerable Web Application) - Não testado  
- SMB - Não testado  

## Status Atual
Ambiente configurado e testes iniciais em andamento. Documentação sendo elaborada com:
- Comandos utilizados
- Evidências dos testes
- Dicas de configurações

---

*Projeto do bootcamp Santander Cibersegurança 2025 | DIO*


