# Email Sync App

**Versão:** 1.0.0  
**Criador:** Daniel Roberto  
**Data de Criação:** Agosto de 2024

## Descrição

O **Email Sync App** é um aplicativo em Python que permite sincronizar e-mails entre dois servidores IMAP. Ele é especialmente útil para transferir mensagens de uma conta de e-mail para outra, mantendo todas as mensagens intactas. O aplicativo oferece uma interface gráfica simples e fácil de usar, construída com `tkinter`, e suporta diferentes tipos de segurança, como SSL e TLS.

## Funcionalidades

- **Sincronização de E-mails:** Transfere e-mails de uma conta de origem para uma conta de destino.
- **Suporte a SSL/TLS:** Permite sincronizar e-mails usando conexões seguras.
- **Progresso Visual:** Mostra o progresso da sincronização em uma barra de progresso.
- **Escolha de Tema:** O usuário pode escolher entre temas claros e escuros.
- **Informações do Criador:** Exibe informações sobre o criador do aplicativo.

## Requisitos

- **Python 3.x**
- **Bibliotecas Padrão:** `tkinter`, `imaplib`, `email`, `ssl` (todas essas são bibliotecas padrão do Python e não precisam ser instaladas separadamente).

## Instalação

1. **Clone o Repositório:**
   ```bash
   git clone https://github.com/nieelsz/emailsync.git
   cd emailsync

## Problemas Conhecidos
Grandes Volumes de E-mails: A sincronização de caixas de e-mails muito grandes (e.g., 40 GB) pode demorar bastante e consumir muitos recursos. Recomenda-se executar a sincronização em partes.
