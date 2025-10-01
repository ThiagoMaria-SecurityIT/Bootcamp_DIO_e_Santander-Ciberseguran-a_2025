# Laboratório Kali Linux & Metasploitable

🟡 **EM DESENVOLVIMENTO** - Última atualização: 30/09/2025  

## Objetivo
Implementar e documentar um projeto prático de segurança ofensiva em ambiente controlado e isolado, utilizando Kali Linux e Metasploitable 2 para simular cenários de ataque de força bruta.  

## ⚠️ Aviso Importante
**ESTE LABORATÓRIO É EXCLUSIVAMENTE PARA FINS EDUCACIONIS**
> [!CAUTION]  
> - Todos os testes são realizados em ambiente controlado e isolado  
> - É estritamente proibido replicar estas técnicas sem autorização explícita
> - Não me responsabilizo pelo uso indevido deste conteúdo  

## Configuração do Ambiente
- Duas máquinas virtuais no VirtualBox (Kali Linux + Metasploitable 2)
- Rede interna configurada (host-only)
- Ferramenta Medusa para ataques de força bruta

## Serviços em Teste
- FTP
- DVWA (Damn Vulnerable Web Application)
- SMB

## Status Atual
Ambiente configurado e testes iniciais em andamento. Documentação sendo elaborada com:
- Comandos utilizados
- Evidências dos testes
- Dicas de configurações

Imagem abaixo: Máquinas virtuais configuradas no VirtualBox, rede configurada, ataque no FTP com Medusa após varredura com Nmap.   
    
<img width="1763" height="970" alt="image" src="https://github.com/user-attachments/assets/9726481e-242d-4f3d-a74b-44684005507e" />    


**Análise Técnica da Exposição dos IPs na Imagem:**  
- ✅ Configuração realizada com sucesso conforme metodologia do curso    
- 🔒 Endereços na faixa 192.168.56.0/24 - rede host-only do VirtualBox (sem internet)    
- 🌐 **Segmento de rede isolado** - tráfego restrito ao ambiente local  
- 📊 Segue o padrão de documentação técnica comum em laboratórios de pentest    
- 🔍 Demonstra corretamente conceitos de redes privadas sem exposição real    

Exibição segura para fins educacionais, mantendo boas práticas de documentação técnica.

Não é a versão final do projeto  

---

*Projeto do bootcamp Santander Cibersegurança 2025 | DIO*
