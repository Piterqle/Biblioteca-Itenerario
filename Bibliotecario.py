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
        comando_selecionar = f"SELECT {selecionar} FROM {tabela} WHERE {coluna} = %s"
        cursor.execute(comando_selecionar, (valor,))
        resultado = cursor.fetchone()
        if resultado != None:
            id_selecionado = resultado[0]
        else:
            comando_adicionar = f"INSERT INTO {tabela} ({coluna}) VALUES (%s);"
            cursor.execute(comando_adicionar, (valor,))
            conexao.commit()
            comando_selecionar2 = f"SELECT {selecionar} FROM {tabela} WHERE {coluna} = %s"
            cursor.execute(comando_selecionar2, (valor,))
            resultado = cursor.fetchone()
            
            id_selecionado = resultado[0]
        return id_selecionado

def select(valor, selecionar, tabela, coluna):
    comando = f"SELECT {selecionar} FROM {tabela} WHERE {coluna} = %s"
    cursor.execute(comando, (valor, ))
    resultado = cursor.fetchone()
    if resultado:
        id_selecionado = resultado[0]
    else:
        id_selecionado = "Deu ERRO"
    return id_selecionado     

def delete(tree,tabela, coluna, indicie):
    item_selecionado = tree.selection()
    if item_selecionado:
        valor = tree.item(item_selecionado, "values")[indicie]
        comando = f"DELETE FROM {tabela} WHERE {coluna} = (%s)"
        cursor.execute(comando, (valor, ))
        
        conexao.commit()
        tree.delete(item_selecionado)
        messagebox.showinfo("Deletado", "Item deletado")






class Janela_Bibliotecario(tk.Tk):
    def __init__(self, *args):
        super().__init__()
        self.column = ["ID", "Livro", "Gênero", "Autor", "Idioma", "Localização","Status"]
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

        self.buttom_delete = tk.Button(frame_dash, text="Deletar", command=lambda:delete(self.tree_menu, "dim_biblioteca", "id_livro", 0),bg="White", width=20, font=("Arial", 10))
        self.buttom_delete.pack(anchor="center", pady=10)
        
        frame_pesquisa = tk.Frame(frame_dash, bg="Black")
        frame_pesquisa.pack(anchor="center", pady=20)

        tk.Label(frame_dash, text="Controle da Biblioteca", bg="Black", fg="white",font=("Arial", 15, "bold")).pack(padx=10)
        

        

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
        
        self.tree_menu = ttk.Treeview(tree_frame, columns= self.column, show="headings",)
        self.tree_menu.pack(expand=True, fill="both", side="left")

        self.combo_pesquisa = ttk.Combobox(frame_pesquisa, values=self.column, width=30)
        self.combo_pesquisa.grid(column=0, row=0, columnspan=3, pady=10)
        self.combo_pesquisa.set("Filtros:")

        #Entry de pesquisa
        self.txb_pesquisa = tk.Entry(frame_pesquisa, width=25, bd=4)
        self.txb_pesquisa.grid(column=0, row=1)
        self.txb_pesquisa.insert(0, "Pesquisar:")

        #Botão de Pesquisa no Estoque
        bt_pesquisa = tk.Button(frame_pesquisa, text="🔎", width=3, command=self.pesquisa)
        bt_pesquisa.grid(column=1, row=1)

        for col in self.column:
            self.tree_menu.heading(column=col, text=col)
            self.tree_menu.column(col, width=50)
        
        self.scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_menu.yview)
        self.scroll.pack(side="right")
        self.tree_menu.configure(yscrollcommand=self.scroll.set)
        
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
        
        frame_color = tk.Frame(root, width=1920, height=120, bg="Black")
        frame_color.pack(anchor="w")
        frame_color.propagate(False)

        tk.Label(frame_color, text="Menu de edição de Livro", font=("Arial", 26, "bold"), fg="White", bg="Black").pack(anchor="center", pady=35)

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
        self.lista_edi = ["Nome", "Gênero", "Autor", "Idioma", "Localização", "Status"]
        self.combo_topicoL = ttk.Combobox(frame_edL, width=50, values=self.lista_edi)
        self.combo_topicoL.pack(pady=10, anchor="w")

        tk.Label(frame_edL, text="Novo Valor:", font=("Arial", 12)).pack( anchor="w")
        self.entry_edit = tk.Entry(frame_edL, width=50)
        self.entry_edit.pack(pady=10, anchor="w")
        
        bt_salvar_edit = tk.Button(frame_edL, width=15, text="Salvar Edição",command=lambda:self.editar(root), bg="#2ecc71")
        bt_salvar_edit.pack(side="top", pady=10)

        bt_cancelar = tk.Button(frame_edL, width=15, text="Cancelar", bg="#e74c3c",command=lambda:self.off_windowns(root))
        bt_cancelar.pack(side="bottom")
        
    def adicionar_livro(self, root):
        titulo = self.entry_nomeL.get().capitalize()
        genero = self.entry_generoL.get().capitalize() 
        autor = self.entry_autorL.get().capitalize()
        idioma = self.entry_IdiomaL.get().capitalize()
        status = self.entry_StatusL.get()

        genero_fi = add_sql(genero,"id_generolivro", "fato_generolivro", "generolivro")
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
            genero = select(i[3], "generolivro", "fato_generolivro", "id_generolivro")
            autor = select(i[2], "autor", "fato_autor", "id_autor")
            idioma = select(i[4], "idioma", "fato_idioma", "id_idioma")
            status = select(i[6], "status", "fato_status", "id_status")
            if status == "Disponível":
                self.tree_menu.insert("", "end", values=(i[0], i[1], genero, autor, idioma, i[5], status), tags=("all", "dis",))
            else:
                self.tree_menu.insert("", "end", values=(i[0], i[1], genero, autor, idioma, i[5], status), tags=("all", "indis",))

    def editar (self, root):
        id_edit = self.combo_idL.get()
        topico = self.combo_topicoL.get()
        valor_edit = self.entry_edit.get()
        if topico == "Nome":
            topico = "Título"
            valor = valor_edit
        elif topico == "Gênero":
            
            coluna = "generolivro"
            selecionar = "id_generolivro"
            tabela = "fato_generolivro"
            valor = (valor_edit, selecionar, tabela, coluna)
        elif topico == "Autor":
            coluna = "autor"
            selecionar = 'id_autor'
            tabela = "fato_autor" 
            valor = add_sql(valor_edit, selecionar, tabela, coluna)
        elif topico == "Idioma":
            coluna = "idioma"
            selecionar = "id_idioma"
            tabela = "fato_idioma"
            valor = add_sql(valor_edit, selecionar, tabela, coluna)
        elif topico == "Localização":
            coluna = "carro"
            selecionar = "id_carro"
            tabela = "fato_localização"
            valor = add_sql(valor_edit, selecionar, tabela, coluna )
        
        try:
            comando = (f"UPDATE dim_biblioteca SET {topico} = '{valor}' WHERE id_livro = (%s)")
            cursor.execute(comando, (id_edit, ))
            conexao.commit()
            self.off_windowns(root)
        except:
            messagebox.showerror("ERRO", "Verifique se existe o tópico ou ID")
        
    def pesquisa(self):
        valor = f"{self.txb_pesquisa.get()}%"
        coluna = self.combo_pesquisa.get()
        valor = valor.replace("Pesquisar: " , "")
        if coluna == None:
            messagebox.showerror("ERRO", "Coloque um Filtro de Pesquisa")
        else:
            if coluna in self.column:
                if coluna == "ID":
                    coluna = "id_livro"
                    comando = f"SELECT * FROM dim_biblioteca WHERE {coluna} LIKE %s;"
                elif coluna == "Livro":
                    coluna = "Título"
                    comando = f"SELECT * FROM dim_biblioteca WHERE {coluna} LIKE %s;"
                elif coluna == "Gênero":
                    comando = "SELECT * FROM dim_biblioteca JOIN fato_generolivro ON Gênero = fato_generolivro.id_generolivro WHERE fato_generolivro.generolivro LIKE %s;"
                elif coluna == "Autor":
                    comando = "SELECT * FROM dim_biblioteca JOIN fato_autor ON Autor = fato_autor.id_autor WHERE fato_autor.autor LIKE %s"
                elif coluna == "Idioma":
                    comando = "SELECT * FROM dim_biblioteca JOIN fato_idioma ON Idioma = fato_autor.id_idioma WHERE fato_idioma.idioma LIKE %s"
                elif coluna == "Localização":
                    comando = "SELECT * FROM dim_biblioteca JOIN fato_localização ON Localização = fato_localização.id_carro WHERE fato_localização.carro LIKE %s"
                elif coluna == "Status":
                    comando = "SELECT * FROM dim_biblioteca JOIN fato_status ON Status = fato_status.id_status WHERE fato_status.status LIKE %s"
                
                for item in self.tree_menu.get_children():
                    self.tree_menu.delete(item)
                
                self.iniciar_tabela(cursor.execute(comando, (valor,)))
            else:
                messagebox.showerror("ERRO", "Coloque um Filtro que esteja nas opções")
        


if __name__ == "__main__": 
    app = Janela_Bibliotecario()
    app.mainloop()