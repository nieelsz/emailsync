import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import imaplib
import email
import ssl

class EmailSyncApp(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        # Configuração responsiva
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Variáveis de controle para os campos de entrada
        self.server_source = tk.StringVar()
        self.port_source = tk.StringVar(value="993")
        self.security_source = tk.StringVar(value="SSL")
        self.email_source = tk.StringVar()
        self.password_source = tk.StringVar()

        self.server_destination = tk.StringVar()
        self.port_destination = tk.StringVar(value="993")
        self.security_destination = tk.StringVar(value="SSL")
        self.email_destination = tk.StringVar()
        self.password_destination = tk.StringVar()

        # Variável para o tema
        self.theme_choice = tk.StringVar(value="dark")

        # Criação dos widgets
        self.setup_widgets()

    def setup_widgets(self):
        # Frame principal para as configurações de sincronização
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Criação de uma Frame para os campos de entrada
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Configurações de Sincronização", padding=(10, 5))
        self.input_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Campos de entrada para Servidor de Origem
        ttk.Label(self.input_frame, text="Servidor IMAP de Origem:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_server_source = ttk.Entry(self.input_frame, textvariable=self.server_source)
        self.entry_server_source.grid(row=1, column=0, padx=5, pady=2, sticky="ew")

        ttk.Label(self.input_frame, text="Porta de Origem:").grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.entry_port_source = ttk.Entry(self.input_frame, textvariable=self.port_source)
        self.entry_port_source.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(self.input_frame, text="Segurança:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.combo_security_source = ttk.Combobox(self.input_frame, textvariable=self.security_source, values=["SSL", "TLS", "None"])
        self.combo_security_source.grid(row=1, column=2, padx=5, pady=2, sticky="ew")

        ttk.Label(self.input_frame, text="Email de Origem:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.entry_email_source = ttk.Entry(self.input_frame, textvariable=self.email_source)
        self.entry_email_source.grid(row=3, column=0, columnspan=3, padx=5, pady=2, sticky="ew")

        ttk.Label(self.input_frame, text="Senha de Origem:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.entry_password_source = ttk.Entry(self.input_frame, textvariable=self.password_source, show="*")
        self.entry_password_source.grid(row=5, column=0, columnspan=3, padx=5, pady=2, sticky="ew")

        # Campos de entrada para Servidor de Destino
        ttk.Label(self.input_frame, text="Servidor IMAP de Destino:").grid(row=6, column=0, padx=5, pady=2, sticky="w")
        self.entry_server_destination = ttk.Entry(self.input_frame, textvariable=self.server_destination)
        self.entry_server_destination.grid(row=7, column=0, padx=5, pady=2, sticky="ew")

        ttk.Label(self.input_frame, text="Porta de Destino:").grid(row=6, column=1, padx=5, pady=2, sticky="w")
        self.entry_port_destination = ttk.Entry(self.input_frame, textvariable=self.port_destination)
        self.entry_port_destination.grid(row=7, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(self.input_frame, text="Segurança:").grid(row=6, column=2, padx=5, pady=2, sticky="w")
        self.combo_security_destination = ttk.Combobox(self.input_frame, textvariable=self.security_destination, values=["SSL", "TLS", "None"])
        self.combo_security_destination.grid(row=7, column=2, padx=5, pady=2, sticky="ew")

        ttk.Label(self.input_frame, text="Email de Destino:").grid(row=8, column=0, padx=5, pady=2, sticky="w")
        self.entry_email_destination = ttk.Entry(self.input_frame, textvariable=self.email_destination)
        self.entry_email_destination.grid(row=9, column=0, columnspan=3, padx=5, pady=2, sticky="ew")

        ttk.Label(self.input_frame, text="Senha de Destino:").grid(row=10, column=0, padx=5, pady=2, sticky="w")
        self.entry_password_destination = ttk.Entry(self.input_frame, textvariable=self.password_destination, show="*")
        self.entry_password_destination.grid(row=11, column=0, columnspan=3, padx=5, pady=2, sticky="ew")

        # Combobox para escolher o tema
        ttk.Label(self.main_frame, text="Escolha o Tema:").grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.combo_theme = ttk.Combobox(self.main_frame, textvariable=self.theme_choice, values=["light", "dark"])
        self.combo_theme.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.combo_theme.bind("<<ComboboxSelected>>", self.change_theme)

        # Botão de Sincronização
        self.sync_button = ttk.Button(self.main_frame, text="Sincronizar", command=self.sync_emails, style="Accent.TButton")
        self.sync_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # Barra de progresso
        self.progress_frame = ttk.LabelFrame(self.main_frame, text="Progresso da Sincronização", padding=(10, 5))
        self.progress_frame.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Frame para as informações do criador, posicionado à direita
        self.creator_frame = ttk.Frame(self)
        self.creator_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.creator_frame.columnconfigure(0, weight=1)

        # Informações do Criador, com texto encapsulado
        creator_info = (
            "Nome do Criador: Daniel Roberto\n"
            "E-mail para Contato: danielroberto@suportemais.com\n"
            "GitHub: github.com/nieelsz\n"
            "Data de Criação: Agosto de 2024\n"
            "Versão do Software: 1.0.0\n\n"
            "\"Este aplicativo foi criado com o objetivo de facilitar a sincronização de e-mails "
            "entre diferentes servidores IMAP. Feedbacks são bem-vindos!\""
        )
        self.creator_label = ttk.Label(self.creator_frame, text=creator_info, justify="left", wraplength=200)
        self.creator_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def change_theme(self, event):
        selected_theme = self.theme_choice.get()
        self.master.tk.call("set_theme", selected_theme)

    def sync_emails(self):
        orig_host = self.server_source.get()
        orig_port = int(self.port_source.get())
        orig_security = self.security_source.get()
        orig_user = self.email_source.get()
        orig_pass = self.password_source.get()

        dest_host = self.server_destination.get()
        dest_port = int(self.port_destination.get())
        dest_security = self.security_destination.get()
        dest_user = self.email_destination.get()
        dest_pass = self.password_destination.get()

        try:
            # Conectar ao servidor de origem
            if orig_security == "SSL":
                orig_conn = imaplib.IMAP4_SSL(orig_host, orig_port)
            elif orig_security == "TLS":
                orig_conn = imaplib.IMAP4(orig_host, orig_port)
                orig_conn.starttls()
            else:
                orig_conn = imaplib.IMAP4(orig_host, orig_port)

            orig_conn.login(orig_user, orig_pass)
            orig_conn.select('inbox')

            # Conectar ao servidor de destino
            if dest_security == "SSL":
                dest_conn = imaplib.IMAP4_SSL(dest_host, dest_port)
            elif dest_security == "TLS":
                dest_conn = imaplib.IMAP4(dest_host, dest_port)
                dest_conn.starttls()
            else:
                dest_conn = imaplib.IMAP4(dest_host, dest_port)

            dest_conn.login(dest_user, dest_pass)
            dest_conn.select('inbox')

            # Buscar todos os e-mails na caixa de entrada
            status, messages = orig_conn.search(None, 'ALL')
            messages = messages[0].split()
            total_messages = len(messages)

            # Configurar a barra de progresso
            self.progress["maximum"] = total_messages

            for index, msg_id in enumerate(messages):
                status, msg_data = orig_conn.fetch(msg_id, '(RFC822)')
                raw_email = msg_data[0][1]

                # Fazer o upload do e-mail para o servidor de destino
                dest_conn.append('inbox', '', imaplib.Time2Internaldate(email.utils.parsedate_to_datetime(email.message_from_bytes(raw_email)['Date'])), raw_email)

                # Atualizar a barra de progresso
                self.progress["value"] = index + 1
                self.parent.update_idletasks()

            orig_conn.logout()
            dest_conn.logout()

            messagebox.showinfo("Sucesso", "Sincronização concluída!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sincronizador de Emails - Azure Theme")

    # Especifique o caminho absoluto para o arquivo azure.tcl
    theme_path = r'C:\py\Utilidades\importar_emails\Azure-ttk-theme-main\azure.tcl'
    root.tk.call("source", theme_path)

    # Define o tema padrão
    root.tk.call("set_theme", "dark")

    app = EmailSyncApp(root)
    app.pack(fill="both", expand=True)

    # Configuração da janela principal
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

    root.mainloop()
