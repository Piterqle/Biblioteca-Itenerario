import tkinter as tk
import pymysql
import mysql.connector
from tkinter import messagebox
import datetime
from Bibliotecario import Janela_Bibliotecario as bibliotecario
from Bibliotecario import add_sql


conexao = mysql.connector.connect(
            host= "localhost",
            user="root", 
            password="acesso123",
            database="biblioteca itinerante"
        )
cursor = conexao.cursor()


class Login(tk.Tk):
    def __init__(self, *args):
        super().__init__(*args)
        
       
        self.login_screen()

    def login_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("500x700")
        self.title("Login na Biblioteca")
        
        frame_login = tk.Frame(self, width=400, height=300)
        frame_login.pack(anchor="center")
        frame_login.propagate(False)
    
        tk.Label(frame_login, text="Login",font=("Arial", 40, "bold")).pack(pady=30)

        tk.Label(frame_login, text="Nome", font=("Arial", 17)).pack(anchor="w", pady=15)
        self.txb_nome = tk.Entry(frame_login, width=66)
        self.txb_nome.pack(anchor="w")

        tk.Label(frame_login, text="Senha", font=("Arial", 17)).pack(anchor="w", pady=15)
        self.txb_senha = tk.Entry(frame_login, width=66)
        self.txb_senha.pack(anchor="w")

        frame_buttom = tk.Frame(self)
        frame_buttom.pack(pady=100)
        login = tk.Button(frame_buttom, text="Entrar", font=("Arial", 10, "bold"), width=20, command=self.logar)
        login.pack(pady= 10)
        cancelar = tk.Button(frame_buttom, text="Cancelar", font=("Arial", 10, "bold"), width=20, command=lambda:self.sair(self))
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
        
        frame_login = tk.Frame(self, width=400, height=700)
        frame_login.pack(anchor="center")
        frame_login.propagate(False)
    
        tk.Label(frame_login, text="Cadastro",font=("Arial", 40, "bold")).pack(pady=30)

        tk.Label(frame_login, text="Nome", font=("Arial", 14)).pack(anchor="w", pady=15)
        self.txb_nomecadastro = tk.Entry(frame_login, width=66)
        self.txb_nomecadastro.pack(anchor="w")
        
        tk.Label(frame_login, text="Sobrenome", font=("Arial", 14)).pack(anchor="w", pady=15)
        self.txb_snomecadastro = tk.Entry(frame_login, width=66)
        self.txb_snomecadastro.pack(anchor="w")

        tk.Label(frame_login, text="Email", font=("Arial", 14)).pack(anchor="w", pady=15)
        self.txb_email = tk.Entry(frame_login, width=66)
        self.txb_email.pack(anchor="w")

        tk.Label(frame_login, text="Senha", font=("Arial", 14)).pack(anchor="w", pady=15)
        self.txb_senhacadastro = tk.Entry(frame_login, width=66)
        self.txb_senhacadastro.pack(anchor="w")

        tk.Label(frame_login, text="Confirmar Senha", font=("Arial", 14)).pack(anchor="w", pady=15)
        self.txb_confirmcadastro = tk.Entry(frame_login, width=66)
        self.txb_confirmcadastro.pack(anchor="w")

        tk.Label(frame_login, text="Gênero", font=("Arial", 14)).pack(anchor="w", pady=15)
        frame_rb = tk.Frame(frame_login)
        frame_rb.pack(anchor="w")
        
        self.rb_val = tk.IntVar(value=0)
        rb_Masculino = tk.Radiobutton(frame_rb, variable=self.rb_val, value=1,text="Masculino", font=("Arial", 10))
        rb_Masculino.grid(column=0, row=0)
        rb_Feminino = tk.Radiobutton(frame_rb, variable=self.rb_val, value=2,text="Feminino", font=("Arial", 10))
        rb_Feminino.grid(column=1, row=0)

        frame_buttom = tk.Frame(frame_login)
        frame_buttom.pack(pady=15)
        cadastrar = tk.Button(frame_buttom, text="Cadastrar", font=("Arial", 10, "bold"), width=15, command=self.cadastrar)
        cadastrar.grid(column=0, row=0, padx=10)
        cancelar = tk.Button(frame_buttom, text="Cancelar", font=("Arial", 10, "bold"), width=15, command=self.login_screen)
        cancelar.grid(column=1, row=0)

    def cadastrar(self):
        nome = self.txb_nomecadastro.get()
        sbn = self.txb_snomecadastro.get()
        genero = self.verificar_genero()
        email = self.txb_email.get()
        senha = self.txb_senhacadastro.get()
        senha_confirm= self.txb_confirmcadastro.get()

        if genero != None:
            add_sql(genero, "fato_genero", "genero")
            messagebox.showinfo("Login Cadastrado", f"Gênero = {genero}")
            cursor.execute("INSERT INTO `teste` (teste) VALUES `fato_genero`.id_genero where genero = 'Masculino'")
            conexao.commit()
            self.login_screen()
            

        else:
            messagebox.showerror("Erro", "Preencha os Espaços")

            
    
    def sair(self, root):
        root.destroy()
    
    def verificar_genero(self):
        valor = self.rb_val.get()
        if valor == 1:
            return "Masculino"
        elif valor == 2:
            return "Feminino"
        else:
            return None
    
    
    
    def adds_sql(self, valores, tabela, colunas):
        pass
        
        

if __name__ == "__main__":
    app = Login()
    app.mainloop()