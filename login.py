import tkinter as tk
import pymysql
import mysql.connector
from tkinter import messagebox
import datetime
from Bibliotecario import Janela_Bibliotecario as bibliotecario
from Bibliotecario import add_sql
from Cliente import ClienteApp


conexao = mysql.connector.connect(
            host= "localhost",
            user="root", 
            password="acesso123",
            database="biblioteca itinerante"
        )
cursor = conexao.cursor()

def focus_entry(entry, text):
    if entry.get() == text:
        entry.delete(0, tk.END)
        entry.config(fg="Black")


def Infocus_entry(entry, text):
    if entry.get() == "":
        entry.insert(0, text)
        entry.config(fg="gray")


class Login(tk.Tk):
    def __init__(self, *args):
        super().__init__(*args)
        self.txt_nome = "Digite seu Nome:"
        self.txt_senha = "Digite o seu CPF:"
       
        self.login_screen()

    def login_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("500x600")
        self.title("Login na Biblioteca")
        
        frame_login = tk.Frame(self, width=400, height=300)
        frame_login.pack(anchor="center")
        frame_login.propagate(False)
    
        tk.Label(frame_login, text="Login",font=("Arial", 40, "bold")).pack(pady=25)

        tk.Label(frame_login, text="Nome", font=("Arial", 17)).pack(anchor="w", pady=15)
        self.txb_nome = tk.Entry(frame_login, width=66, fg="Gray")
        self.txb_nome.pack(anchor="w")
        self.txb_nome.insert(0, self.txt_nome)
        self.txb_nome.bind("<FocusIn>", lambda event: focus_entry(self.txb_nome, self.txt_nome))
        self.txb_nome.bind("<FocusOut>", lambda event: Infocus_entry(self.txb_nome, self.txt_nome))

        tk.Label(frame_login, text="Senha", font=("Arial", 17)).pack(anchor="w", pady=15)
        self.txb_senha = tk.Entry(frame_login, width=66, fg="Gray")
        self.txb_senha.pack(anchor="w")
        self.txb_senha.insert(0, self.txt_senha )
        self.txb_senha.bind("<FocusIn>", lambda envet:focus_entry(self.txb_senha, self.txt_senha) )
        self.txb_senha.bind("<FocusOut>", lambda event: Infocus_entry(self.txb_senha, self.txt_senha))
        

        frame_buttom = tk.Frame(self)
        frame_buttom.pack(pady=60)
        login = tk.Button(frame_buttom, text="Entrar", font=("Arial", 10, "bold"), width=20, command=self.logar)
        login.pack(pady= 10)
        cancelar = tk.Button(frame_buttom, text="Cancelar", font=("Arial", 10, "bold"), width=20, command=lambda:self.sair(self))
        cancelar.pack()

        frame_label = tk.Frame(self)
        frame_label.pack(pady=10)
        tk.Label(frame_label, text="Voçê é novo aqui?", font=("Arial", 11)).grid(column=0, row=0)
        lb_cadastro = tk.Label(frame_label, text="Cadastra-se", font=("Arial", 11), fg="blue")
        lb_cadastro.grid(column=1, row=0)
        lb_cadastro.bind("<Button-1>", self.screen_cadastrar)

    def logar(self):
        nome_usuario = self.txb_nome.get()
        senha_usuario = self.txb_senha.get()

        for i in (self.txt_nome, self.txt_senha):
            if i in (nome_usuario,senha_usuario):
                messagebox.showerror("ERRO", "Preencha os espaços")
                break
        else:
            comando = "SELECT cargo FROM dim_leitor WHERE Nome = %s AND senha = %s"
            cursor.execute(comando, (nome_usuario, senha_usuario))
            resultado = cursor.fetchone()
            if resultado:
                if resultado[0] == 0:
                    ClienteApp.mainloop()
                elif resultado[0] == 1:
                    bibliotecario.mainloop()
            
            else:
                messagebox.showerror("ERRO", "Usário Inexistente")

    def screen_cadastrar(self, event=None):
        for widget in self.winfo_children():
            widget.destroy()
        
        frame_login = tk.Frame(self, width=400, height=700)
        frame_login.pack(anchor="center")
        frame_login.propagate(False)
    
        tk.Label(frame_login, text="Cadastro",font=("Arial", 40, "bold")).pack(pady=25)

        tk.Label(frame_login, text="Nome", font=("Arial", 14)).pack(anchor="w", pady=15)
        
        self.txb_nomecadastro = tk.Entry(frame_login, width=66, fg= "Gray")
        self.txb_nomecadastro.pack(anchor="w")
        self.txb_nomecadastro.insert(0, self.txt_nome)
        self.txb_nomecadastro.bind("<FocusIn>", lambda event: focus_entry(self.txb_nomecadastro, self.txt_nome))
        self.txb_nomecadastro.bind("<FocusOut>", lambda event: Infocus_entry(self.txb_nomecadastro, self.txt_nome))
    

        tk.Label(frame_login, text="Email", font=("Arial", 14)).pack(anchor="w", pady=15)
        self.txt_entryemail = "Digite o seu Email:"
        self.txb_email = tk.Entry(frame_login, width=66, fg="Gray")
        self.txb_email.pack(anchor="w")
        self.txb_email.insert(0, self.txt_entryemail)
        self.txb_email.bind("<FocusIn>", lambda event: focus_entry(self.txb_email, self.txt_entryemail))
        self.txb_email.bind("<FocusOut>", lambda event: Infocus_entry(self.txb_email, self.txt_entryemail))

        tk.Label(frame_login, text="Senha", font=("Arial", 14)).pack(anchor="w", pady=15)
        self.txb_senhacadastro = tk.Entry(frame_login, width=66, fg="Gray")
        self.txb_senhacadastro.pack(anchor="w")
        
        self.txb_senhacadastro.insert(0, self.txt_senha )
        self.txb_senhacadastro.bind("<FocusIn>", lambda envet:focus_entry(self.txb_senhacadastro, self.txt_senha) )
        self.txb_senhacadastro.bind("<FocusOut>", lambda event: Infocus_entry(self.txb_senhacadastro, self.txt_senha))

        tk.Label(frame_login, text="Confirmar Senha", font=("Arial", 14)).pack(anchor="w", pady=15)
        self.txt_entryconfi = "Digite seu CPF novamente:"
        self.txb_confirmcadastro = tk.Entry(frame_login, width=66, fg="Gray")
        self.txb_confirmcadastro.pack(anchor="w")
        self.txb_confirmcadastro.insert(0, self.txt_entryconfi)
        self.txb_confirmcadastro.bind("<FocusIn>", lambda event: focus_entry(self.txb_confirmcadastro, self.txt_entryconfi))
        self.txb_confirmcadastro.bind("<FocusOut>", lambda event: Infocus_entry(self.txb_confirmcadastro, self.txt_entryconfi))

        frame_buttom = tk.Frame(frame_login)
        frame_buttom.pack(pady=70)
        cadastrar = tk.Button(frame_buttom, text="Cadastrar", font=("Arial", 10, "bold"), width=15, command=self.cadastrar, bg="green")
        cadastrar.grid(column=0, row=0, padx=10)
        cancelar = tk.Button(frame_buttom, text="Cancelar", font=("Arial", 10, "bold"), width=15, command=self.login_screen, bg="red")
        cancelar.grid(column=1, row=0)

    def cadastrar(self):
        nome = self.txb_nomecadastro.get()
        email = self.txb_email.get()
        senha = self.txb_senhacadastro.get()
        senha_confirm= self.txb_confirmcadastro.get()
        for i in (self.txt_nome, self.txt_entryemail, self.txt_senha, self.txt_entryconfi):
            if  i in (nome, email, senha, senha_confirm):
                messagebox.showerror("Erro", "Preencha os Espaços")
                break
                
        else:
            if len(senha) == 11:
                if senha == senha_confirm:
                    comando= "INSERT INTO dim_leitor (Nome, email, senha) VALUES (%s, %s, %s)"
                    cursor.execute(comando, (nome, email, senha))
                    conexao.commit()
                    self.login_screen()
                else:
                    messagebox.showerror("ERRO", "Senhas não coincidem")
        
            else:
                resultado = 214 * 10 % 11
                print(resultado)
                messagebox.showerror("ERRO", "Verifique se Digitou a senha errada")
        
            

            
    
    def sair(self, root):
        root.destroy()

    
    
    
    def adds_sql(self, valores, tabela, colunas):
        pass
        
        

if __name__ == "__main__":
    app = Login()
    app.mainloop()