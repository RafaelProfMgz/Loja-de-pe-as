import tkinter as tk
from tkinter import ttk, messagebox
from connector import ConnectarBanco
from LojaPecas import Lojapecas

class Login:
    def __init__(self):
        self.conect = ConnectarBanco()
        self.conect.connectar() 
        self.abrir()

    def abrir(self):
        self.janela_login = tk.Tk()  # Use Tk() como janela principal para a tela de login
        self.janela_login.title("Login de usuário")
        self.janela_login.configure(background='#3f3e3e')

        largura = 540
        altura = 240

        largura_tela = self.janela_login.winfo_screenwidth()
        altura_tela = self.janela_login.winfo_screenheight()

        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2

        self.janela_login.geometry(f"{largura}x{altura}+{x}+{y}")
        self.janela_login.minsize(largura, altura)
        self.janela_login.maxsize(largura, altura) 

        self.criar_entrada()
        self.criar_button()

    def criar_entrada(self):
        tk.Label(self.janela_login, text="Nome de Usuário:", font=("Helvetica", 10, "bold"), bg='#4b4b49').place(x=50, y=50)
        self.usuario_var = tk.StringVar()
        self.entrada_usuario = tk.Entry(self.janela_login, font=("Helvetica", 12, "bold"),
                                        bg='#92928f', highlightbackground='#ffc400', highlightthickness=1,
                                        textvariable=self.usuario_var)
        self.entrada_usuario.place(x=200, y=50)
        self.entrada_usuario.bind("<Return>", lambda event: self.verificar_login())

        tk.Label(self.janela_login, text="Senha:", font=("Helvetica", 10, "bold"), bg='#4b4b49').place(x=50, y=100)
        self.senha_var = tk.StringVar()
        self.entrada_senha = tk.Entry(self.janela_login, show="*", font=("Helvetica", 12, "bold"),
                                      bg='#92928f', highlightbackground='#ffc400', highlightthickness=1,
                                      textvariable=self.senha_var)
        self.entrada_senha.place(x=200, y=100)
        self.entrada_senha.bind("<Return>", lambda event: self.verificar_login())

    def criar_button(self):
        btn_login = ttk.Button(self.janela_login, text="Login", style="TButton", command=self.verificar_login)
        btn_login.place(x=240, y=150)

    def verificar_login(self):
        usuario = self.usuario_var.get()
        senha = self.senha_var.get()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        query = "SELECT * FROM usuarios WHERE NomeUsuario = %s AND Senha = %s"
        self.conect.cursor.execute(query, (usuario, senha))
        resultado = self.conect.cursor.fetchone()

        if resultado:
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.janela_login.destroy()  # Destrua a tela de login
            loja = Lojapecas()

        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha incorretos. Tente novamente.")

if __name__ == "__main__":
    login = Login()
    login.janela_login.mainloop()