import tkinter as tk
from tkinter import messagebox, ttk
import pymysql
import datetime
import mysql.connector


conexao = mysql.connector.connect(
            host= "localhost",
            user="root", 
            password="acesso123",
            database="biblioteca itinerante"
        )
cursor = conexao.cursor()

def add_sql(valor, selecionar,tabela, coluna):
        comando_selecionar = "SELECT "+ selecionar +  " FROM " + tabela + " where " + coluna + "= %s"
        cursor.execute(comando_selecionar, (valor,))
        resultado = cursor.fetchone()
        if resultado != None:
            for i in resultado:
                id_selecionado = i
                break
            return id_selecionado
        else:
            comando_adicionar = "INSERT INTO `biblioteca itinerante`."+ f"`{tabela}`" + f"({coluna})" +" VALUES (%s);"
            cursor.execute(comando_adicionar, (valor,))
            conexao.commit()
            cursor.execute(comando_selecionar, (valor,))
            resultado = cursor.fetchone()
            
            for i in resultado:
                id_selecionado = i 
                break
            return id_selecionado
            

class Janela_Bibliotecario(tk.Tk):
    def __init__(self, *args):
        super().__init__()
        self.main_screen()


    def main_screen(self):
        self.geometry("950x600")
        self.title("Área do Gerente")

        #Frames aléatorios 
        frame_dash = tk.Frame(self, width=250 , height=1080, bg="Black") #Frame Dashboard
        frame_dash.pack(anchor="w",side="left")
        frame_dash.propagate(False)
        
        frame_pesquisa = tk.Frame(frame_dash, bg="Black")
        frame_pesquisa.pack(anchor="e", pady=20)

        tk.Label(frame_dash, text="Controle da Biblioteca", bg="Black", fg="white",font=("Arial", 15, "bold")).pack(padx=10)

        
        
        #Botão de Pesquisa no Estoque
        bt_pesquisa = tk.Button(frame_pesquisa, text="🔎", width=3)
        bt_pesquisa.grid(column=1, row=0)

        #Entry de pesquisa
        self.txb_pesquisa = tk.Entry(frame_pesquisa, width=25, bd=4)
        self.txb_pesquisa.grid(column=0, row=0)

        #Frame dos Buttons
        frame_buttons = tk.Frame(frame_dash, bg="Black")
        frame_buttons.pack(anchor="center")
       
        #Botão para abrir o Painel de Adicionar Produtos
        bt_AddProtudo = tk.Button(frame_buttons, text="➕ Adicionar Livro",command=self.screen_livro,anchor="w", bg="white", width=20, font=("Arial", 10))
        bt_AddProtudo.pack(pady=5)
       
        #Botão Para abrir o Painel de Vendas
        bt_Vendas = tk.Button(frame_buttons, text="💸     Vendas",anchor="w", bg="White", width=20, font=("Arial", 10))
        bt_Vendas.pack()
        
        #Botão para abrir o Painel de edição de Items
        bt_Edit= tk.Button(frame_buttons, text="🖊️Editar Item", anchor="w", bg="White", width=20 , font=("Arial", 10))
        bt_Edit.pack(pady=5)

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True)
        estilo = ttk.Style()
        estilo.configure("Treeview", font=("Arial", 10))
        column = ["ID", "Nome", "Livro", "Data", "Status"]
        self.tree_menu = ttk.Treeview(tree_frame, columns= column, show="headings",)
        self.tree_menu.pack(expand=True, fill="both", side="left")

        for col in column:
            self.tree_menu.heading(column=col, text=col)
            self.tree_menu.column(col, width=50)

    def screen_livro(self):
        #Layout do Painel de Registro
        root = tk.Tk()
        root.geometry("350x400")
        root.title("Cadastro do Produto")

        frame_addP = tk.Frame(root, width=200, height=100 )
        frame_addP.pack( anchor="center", pady=10)
        
        tk.Label(frame_addP, text="Título do Livro:", font=("Arial", 11)).pack( anchor="w")
        self.entry_nomeL = tk.Entry(frame_addP, width=50, )
        self.entry_nomeL.pack(pady=10, anchor="w")

        tk.Label(frame_addP, text="Gênero", font=("Arial", 11) ).pack(anchor="w")
        self.entry_generoL = tk.Entry(frame_addP, width=50, )
        self.entry_generoL.pack(pady=10, anchor="w")
        
        tk.Label(frame_addP, text="Autor", font=("Arial", 11) ).pack(anchor="w")
        self.entry_autorL = tk.Entry(frame_addP, width=50, )
        self.entry_autorL.pack(pady=10, anchor="w")

        tk.Label(frame_addP, text="Idioma", font=("Arial", 11)).pack(anchor="w")
        self.entry_IdiomaL = tk.Entry(frame_addP, width=50, )
        self.entry_IdiomaL.pack(pady=10, anchor="w")

        bt_salvar = tk.Button(frame_addP, width=15, text="Salvar Produto",command=lambda:self.adicionar_livro(root), bg="#2ecc71")
        bt_salvar.pack(side="top", pady=10)

        bt_cancelar = tk.Button(frame_addP, width=15, text="Cancelar", bg="#e74c3c",command=lambda:self.off_windowns(root))
        bt_cancelar.pack(side="bottom")
    
    def adicionar_livro(self, root):
        titulo = self.entry_nomeL.get()
        genero = self.entry_generoL.get()
        autor = self.entry_autorL.get()
        idioma = self.entry_IdiomaL.get()

        genero_fi = add_sql(genero,"id_categoria", "fato_categoria", "categoria")
        autor_fi = add_sql(autor, "id_autor", "fato_autor", "autor")
        idioma_fi = add_sql(idioma, "id_idioma", "fato_idioma", "idioma")

    
        cursor.execute("INSERT INTO dim_biblioteca (título, autor, categoria, idioma) Values (%s, %s, %s, %s)", (titulo, autor_fi, genero_fi, idioma_fi))
        conexao.commit()
        self.off_windowns(root)
    
    def off_windowns(self, root):
        root.destroy()

    


if __name__ == "__main__": 
    app = Janela_Bibliotecario()
    app.mainloop()