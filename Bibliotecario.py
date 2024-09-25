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
        for widget in self.winfo_children():
            widget.destroy()

        #Frames aléatorios 
        frame_dash = tk.Frame(self, width=227 , height=1080, bg="Black") #Frame Dashboard
        frame_dash.pack(anchor="w",side="left")
        frame_dash.propagate(False)
        
        frame_pesquisa = tk.Frame(frame_dash, bg="Black")
        frame_pesquisa.pack(anchor="center", pady=20)

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
        bt_Vendas = tk.Button(frame_buttons, text="📨 Empréstimo", anchor="w", bg="White", width=20, font=("Arial", 10))
        bt_Vendas.pack()
        
        #Botão para abrir o Painel de edição de Items
        bt_Edit= tk.Button(frame_buttons, text="🖊️ Editar Item", anchor="w",command=self.screen_edição, bg="White", width=20 , font=("Arial", 10))
        bt_Edit.pack(pady=5)

        cursor.execute("Select id_livro From dim_biblioteca")
        resultado = cursor.fetchall()
        if resultado:
            for i in resultado:
                quantidade = i[0]
        else:
            quantidade = 0 
        self.Label = tk.Label(frame_dash, text=f"Quantidade de livros: {quantidade}", fg="White", font=("Arial", 12, "bold"), bg="Black")
        self.Label.pack(side="bottom", pady=15)

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True)
        estilo = ttk.Style()
        estilo.configure("Treeview", font=("Arial", 10))
        self.column = ["ID", "Livro", "Gênero", "Autor", "Idioma", "Localização","Status"]
        self.tree_menu = ttk.Treeview(tree_frame, columns= self.column, show="headings",)
        self.tree_menu.pack(expand=True, fill="both", side="left")

        for col in self.column:
            self.tree_menu.heading(column=col, text=col)
            self.tree_menu.column(col, width=50)
        
        self.tree_menu.tag_configure("dis", background="#00FF00")
        self.tree_menu.tag_configure("indis", background="#FF2400")
        self.tree_menu.tag_configure("all", font=("Arial", 10))
        self.iniciar_tabela(cursor.execute("Select * from dim_biblioteca"))
    
    def screen_livro(self):
        #Layout do Painel de Registro
        root = tk.Tk()
        root.geometry("350x420")
        root.title("Cadastro do Produto")

        frame_addP = tk.Frame(root, width=200, height=100 )
        frame_addP.pack( anchor="center", pady=10)
        
        tk.Label(frame_addP, text="Título do Livro:", font=("Arial", 12)).pack( anchor="w")
        self.entry_nomeL = tk.Entry(frame_addP, width=50, )
        self.entry_nomeL.pack(pady=10, anchor="w")

        tk.Label(frame_addP, text="Gênero", font=("Arial", 12) ).pack(anchor="w")
        self.entry_generoL = tk.Entry(frame_addP, width=50, )
        self.entry_generoL.pack(pady=10, anchor="w")
        
        tk.Label(frame_addP, text="Autor", font=("Arial", 12) ).pack(anchor="w")
        self.entry_autorL = tk.Entry(frame_addP, width=50, )
        self.entry_autorL.pack(pady=10, anchor="w")

        tk.Label(frame_addP, text="Idioma", font=("Arial", 12)).pack(anchor="w")
        self.entry_IdiomaL = tk.Entry(frame_addP, width=50, )
        self.entry_IdiomaL.pack(pady=10, anchor="w")

        self.list_status = ["Disponível", "Indiponível"]
        tk.Label(frame_addP, text="Status", font=("Arial", 12)).pack(anchor="w")
        self.entry_StatusL = ttk.Combobox(frame_addP, values=self.list_status, width=47)
        self.entry_StatusL.pack(pady=10, anchor="w")

        bt_salvar = tk.Button(frame_addP, width=15, text="Cadastrar Lviro",command=lambda:self.adicionar_livro(root), bg="#2ecc71")
        bt_salvar.pack(side="top", pady=10)

        bt_cancelar = tk.Button(frame_addP, width=15, text="Cancelar", bg="#e74c3c",command=lambda:self.off_windowns(root))
        bt_cancelar.pack(side="bottom")
    
    def screen_edição(self):
        self.destroy
        root = tk.Tk()
        root.geometry("500x600")

        frame_edL = tk.Frame(root, width=200, height=100 )
        frame_edL.pack( anchor="center", pady=10)

        tk.Label(frame_edL, text="ID do Livro:", font=("Arial", 12)).pack( anchor="w")
        lista_id = []
        cursor.execute("Select id_livro From dim_biblioteca")
        for i in cursor.fetchall():
            lista_id.append(i[0])
        self.combo_idL = ttk.Combobox(frame_edL, width=50, values=lista_id)
        self.combo_idL.pack(pady=10, anchor="w")

        tk.Label(frame_edL, text="Editar Atributo:", font=("Arial", 12)).pack( anchor="w")
        lista_edi = ["Nome", "Gênero", "Autor", "Idioma", "Localização", "Status"]
        self.combo_topicoL = ttk.Combobox(frame_edL, width=50, values=lista_edi)
        self.combo_topicoL.pack(pady=10, anchor="w")


        
    
    def adicionar_livro(self, root):
        titulo = self.entry_nomeL.get()
        genero = self.entry_generoL.get()
        autor = self.entry_autorL.get()
        idioma = self.entry_IdiomaL.get()
        status = self.entry_StatusL.get()

        genero_fi = add_sql(genero,"id_categoria", "fato_categoria", "categoria")
        autor_fi = add_sql(autor, "id_autor", "fato_autor", "autor")
        idioma_fi = add_sql(idioma, "id_idioma", "fato_idioma", "idioma")

        if status in self.list_status:
            status = add_sql(status, "id_status", "fato_status", "status")
            cursor.execute("INSERT INTO dim_biblioteca (Título, Autor, Gênero, Idioma, Status) Values (%s, %s, %s, %s, %s)", (titulo, autor_fi, genero_fi, idioma_fi, status))
            conexao.commit()
            self.off_windowns(root)
        else:
            messagebox.showerror("ERRO", "Coloque o Status certo")
    
    def off_windowns(self, root):
        root.destroy()
        self.main_screen()
    
    def iniciar_tabela(self, comando):
        comando
        for i in cursor.fetchall():
            genero = add_sql(i[2], "categoria", "fato_categoria", "id_categoria")
            autor = add_sql(i[3], "autor", "fato_autor", "id_autor")
            idioma = add_sql(i[4], "idioma", "fato_idioma", "id_idioma")
            status = add_sql(i[6], "status", "fato_status", "id_status")
            if status == "Disponível":
                self.tree_menu.insert("", "end", values=(i[0], i[1], genero, autor, idioma, i[5], status), tags=("all", "dis",))
            else:
                self.tree_menu.insert("", "end", values=(i[0], i[1], genero, autor, idioma, i[5], status), tags=("all", "indis",))

    def editar (self):
        id_edit = self.combo_idL.get()
        topico = self.combo_idL.get()
        valor_edit = self.entry_edit.get()
        if topico == "Nome":
            valor = valor_edit
        elif topico == "Gênero":
            coluna = "genero"
            selecionar = "id_genero"
            tabela = "fato_genero"
            valor = add_sql(valor_edit, selecionar, tabela, coluna)
        
        try:
            cursor.execute("Update dim_biblioteca Set "f"{topico} = {valor} Where id_livro" + " = %s", (id_edit))
        except:
            messagebox.showerror("ERRO", "Verifique se existe o tópico")


if __name__ == "__main__": 
    app = Janela_Bibliotecario()
    app.mainloop()