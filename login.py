import tkinter as tk
import pymysql
import mysql.connector
from tkinter import messagebox
import datetime

 

class Login(tk.Tk):
    def __init__(self, *args):
        super().__init__(*args)
        self.conexao = mysql.connector.connect(
            host= "localhost",
            user="root", 
            password="acesso123",
            database="biblioteca itinerante"
        )
        self.cursor = self.conexao.cursor()
        self.login_screen()

    def login_screen(self):
        self.geometry("500x600")
        self.title("Login na Biblioteca")

        frame_login = tk.Frame(self, width=400, height=300)
        frame_login.pack(anchor="center")
        frame_login.propagate(False)
    
        tk.Label(frame_login, text="Login",font=("Arial", 40, "bold")).pack(pady=30)

        tk.Label(frame_login, text="Nome", font=("Arial", 17)).pack(anchor="w", pady=15)
        self.txb_nome = tk.Entry(frame_login, width=60)
        self.txb_nome.pack(anchor="w")

        tk.Label(frame_login, text="Senha", font=("Arial", 17)).pack(anchor="w", pady=15)
        self.txb_senha = tk.Entry(frame_login, width=60)
        self.txb_senha.pack(anchor="w")

        frame_buttom = tk.Frame(self)
        frame_buttom.pack(pady=30)
        login = tk.Button(frame_buttom, text="Entrar", font=("Arial", 10, "bold"), width=15, command=self.logar)
        login.pack(pady= 10)
        cancelar = tk.Button(frame_buttom, text="Cancelar", font=("Arial", 10, "bold"), width=15, command=lambda:self.sair(self))
        cancelar.pack()

        frame_label = tk.Frame(self)
        frame_label.pack(pady=20)
        tk.Label(frame_label, text="Voçê é novo aqui?", font=("Arial", 11)).grid(column=0, row=0)
        lb_cadastro = tk.Label(frame_label, text="Cadastra-se", font=("Arial", 11), fg="blue")
        lb_cadastro.grid(column=1, row=0)
        lb_cadastro.bind("<Button-1>", self.screen_cadastrar)

    def logar(self):
        nome_usuario = self.txb_nome.get()
        senha_usuario = self.txb_senha.get()

    def screen_cadastrar(self, event=None):
        for widget in self.winfo_children():
            widget.destroy()
        
        frame_login = tk.Frame(self, width=400, height=450)
        frame_login.pack(anchor="center")
        frame_login.propagate(False)
    
        tk.Label(frame_login, text="Cadastro",font=("Arial", 40, "bold")).pack(pady=30)

        tk.Label(frame_login, text="Nome", font=("Arial", 14)).pack(anchor="w", pady=15)
        self.txb_nomecadastro = tk.Entry(frame_login, width=60)
        self.txb_nomecadastro.pack(anchor="w")

        tk.Label(frame_login, text="Email", font=("Arial", 14)).pack(anchor="w", pady=15)
        self.txb_email = tk.Entry(frame_login, width=60)
        self.txb_email.pack(anchor="w")

        tk.Label(frame_login, text="Senha", font=("Arial", 14)).pack(anchor="w", pady=15)
        self.txb_senhacadastro = tk.Entry(frame_login, width=60)
        self.txb_senhacadastro.pack(anchor="w")

        tk.Label(frame_login, text="Confirmar Senha", font=("Arial", 14)).pack(anchor="w", pady=15)
        self.txb_confirmcadastro = tk.Entry(frame_login, width=60)
        self.txb_confirmcadastro.pack(anchor="w")

        frame_buttom = tk.Frame(self)
        frame_buttom.pack(pady=30)
        cadastrar = tk.Button(frame_buttom, text="Entrar", font=("Arial", 10, "bold"), width=15, command=self.cadastrar)
        cadastrar.pack(pady= 10)
        cancelar = tk.Button(frame_buttom, text="Cancelar", font=("Arial", 10, "bold"), width=15, command=lambda:self.sair(self))
        cancelar.pack()

    def cadastrar(self):
        nome = self.txb_nomecadastro.get()
        email = self.txb_email.get()
        senha = self.txb_senhacadastro.get()
        senha_confirm= self.txb_confirmcadastro.get()

        comando = "INSERT INTO dim_usuario (usuário, email) VALUES (%s, %s)"
        val = (nome, email)

        self.cursor.execute(comando, val)
        self.conexao.commit()
    
    def sair(self, root):
        root.destroy()
        

if __name__ == "__main__":
    app = Login()
    app.mainloop()