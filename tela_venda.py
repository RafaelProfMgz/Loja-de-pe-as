import tkinter 
from tkinter import  messagebox
from tela_relatorio_produtos import RelatorioProdutos


class Atividades:
    def limpar_tela(self):
        #Limpa a tela quando chamado nas caixas de informação
        self.id_entrada.delete(0, tkinter.END)
        self.entrada_nomeProturo.delete(0, tkinter.END)
        self.entrada_Quantidade.delete(0, tkinter.END)
        self.entrada_valorProduto.delete(0, tkinter.END)
        self.entrada_valorProdutoVenda.delete(0, tkinter.END)

    def editar_produto(self):
        Id_produto = self.id_entrada.get()
        nome = self.entrada_nomeProturo.get()
        quantidade = self.entrada_Quantidade.get()
        valorCompra = self.entrada_valorProduto.get()
        valorVenda = self.entrada_valorProdutoVenda.get()
        
        try:
            if produto:
                # Verifica se o produto existe
                self.cursor.execute('SELECT * FROM estoque WHERE IdProduto=%s', (Id_produto,))
                produto = self.cursor.fetchone()
                if not produto:
                    messagebox.showerror("Erro", "Produto não encontrado.")
                    return

                # Se os campos nome, quantidade ou valor compra foram preenchidos, atualiza no banco
                if nome or quantidade or valorCompra or valorVenda:
                  
                    self.cursor.execute('UPDATE estoque SET nomeProduto=%s, quantidade=%s, valorCompra=%s,valorVenda WHERE IdProduto=%s',
                                        (nome or produto[1], quantidade or produto[2], valorCompra or produto[3],valorVenda or produto[4], Id_produto))
                    self.db_connection.commit()
                    messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

                    self.limpar_tela()
                else:
                    messagebox.showerror("Erro", "Pelo menos um campo (nome Produto, quantidade, valor Compra, valor Venda) deve ser preenchido!")

            else:
                messagebox.showerror("Erro", "O campo ID deve ser preenchido!")

        except ValueError:
            messagebox.showerror("Erro", "valorCompra. Por favor, verifique a formatação.")
    
    def excluir_produto(self):
        Id_produto = self.id_entrada.get()

        try:
            if Id_produto:
                self.cursor.execute('SELECT * FROM estoque WHERE IdProduto=%s', (Id_produto,))
                produto = self.cursor.fetchone()
                if not produto:
                    messagebox.showerror("Erro", "Produto não encontrado.")
                    return

                resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este Produto?")
                
                if resposta:
                    self.cursor.execute('DELETE FROM estoque WHERE IdProduto=%s', (Id_produto,))
                    self.db_connection.commit()
                    messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")

                    self.limpar_tela()

            else:
                messagebox.showerror("Erro", "O campo ID deve ser preenchido!")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao excluir o Produto: {e}")

    def cadastrar_produto(self):
        nome = self.entrada_nomeProturo.get()
        quantidade = self.entrada_Quantidade.get()
        valorCompra = self.entrada_valorProduto.get()
        valorVenda = self.entrada_valorProdutoVenda.get()

        try:
            if nome and quantidade and valorCompra and valorVenda:
                self.cursor.execute('SELECT * FROM estoque WHERE nomeProduto = %s AND quantidade = %s AND valorCompra = %s AND valorVenda = %s',
                                    (nome, quantidade, valorCompra, valorVenda))
                veiculo = self.cursor.fetchone()

                if veiculo:
                    resposta = messagebox.askyesno("Erro", "Este Produto já está cadastrado. Deseja continuar mesmo assim?")
                    if not resposta:
                        return

                self.cursor.execute('INSERT INTO estoque (nomeProduto, quantidade, valorCompra, valorVenda) VALUES (%s, %s, %s, %s)',
                                    (nome, quantidade, valorCompra, valorVenda))

                self.db_connection.commit()
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

                self.limpar_tela()

            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")

        except ValueError:
            messagebox.showerror("Erro", "valorCompra. Por favor, verifique a formatação..")

    def seleciona_lista(self):
        try:
            self.cursor.execute('SELECT * FROM tabalhopoo.estoque')
            return self.cursor.fetchall()
        except Exception as e:
            tkinter.messagebox.showerror("Erro", f"Ocorreu um erro ao selecionar os Produtos: {e}")

class TelaVenda(Atividades):
    def __init__(self, db_connection, cursor,janela_master):
        self.db_connection = db_connection
        self.cursor = cursor
        self.janela_master = janela_master

    def abrir(self):
        # Cria a janela de cadastro
        self.janela_venda = tkinter.Toplevel(self.janela_master)
        self.janela_venda.title("Venda")
        self.janela_venda.configure(background='#3f3e3e')
        self.janela_venda.geometry("1080x720")
        self.janela_venda.minsize(620, 500)
        self.janela_venda.grab_set()

        #Chamar função para criar o frame, botões e label.
        self.criar_frame()
        self.criar_button()
        self.criar_entrada()
        self.AppComBarraDeMenu()

    # Crie a barra de menu
    def AppComBarraDeMenu(self):

        #variavel definida para chamar o relatorio
        self.relatorioProdutos = RelatorioProdutos(self.db_connection, self.cursor, self.janela_venda)
        
        #Cria o menu e define a janela que ele vai ficar
        barra_menu = tkinter.Menu(self.janela_venda)
        self.janela_venda.config(menu=barra_menu)

        # Adicione um menu "Relatorio" à barra de menu
        menu_relatorio = tkinter.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Relatorios", menu=menu_relatorio)
        menu_relatorio.add_command(label="Relatorio Produto", command=self.acao_abrir_relatorio)
        menu_relatorio.add_separator()
        menu_relatorio.add_command(label="Sair", command=self.sair_cadastro_produtos)

    def acao_abrir_relatorio(self):
        self.relatorioProdutos.abrir()

    def sair_cadastro_produtos(self):
        self.janela_venda.destroy()
    #Fim da barra de menu
        
    def criar_button(self):
        # Botão limpar
        self.botao_limpar = tkinter.Button(self.frame_1, text="Limpar", font=("Helvetica", 12), command=self.limpar_tela ,bd=2, 
                                         bg='#c4a90d', highlightbackground='#ffc400',highlightthickness=4, width=20)
        self.botao_limpar.place(relx=0.20,rely=0.15,relheight=0.05,relwidth=0.1)
        
        # Botão novo
        self.botao_novo = tkinter.Button(self.frame_1, text="Novo", font=("Helvetica", 12), bd=2, command= self.cadastrar_produto,
                                         bg='#c4a90d', highlightbackground='#ffc400',highlightthickness=4, width=20)
        self.botao_novo.place(relx=0.32,rely=0.15,relheight=0.05,relwidth=0.1)
                
        # Botão Exluir
        botao_exluir = tkinter.Button(self.frame_1, text="Exluir", font=("Helvetica", 12),  bd=2, command=self.excluir_produto,
                                         bg='#c4a90d', highlightbackground='#ffc400',highlightthickness=4, width=20)
        botao_exluir.place(relx=0.88,rely=0.15,relheight=0.05,relwidth=0.1)

        # Botão Editar
        botao_editar = tkinter.Button(self.frame_1, text="Editar", font=("Helvetica", 12),bd=2, command= self.editar_produto,
                                         bg='#c4a90d', highlightbackground='#ffc400',highlightthickness=4, width=20)
        botao_editar.place(relx=0.76,rely=0.15,relheight=0.05,relwidth=0.1)

    def criar_frame(self):
        #Frame 1
        self.frame_1 = tkinter.Frame(self.janela_venda, bd=2, bg='#4b4b49', highlightbackground='#c4a90d',highlightthickness=2)
        self.frame_1.place(relx=0.02, rely=0.02, relheight=0.96, relwidth= 0.96)

    def criar_entrada(self):
            # Campo para a Codigo
            tkinter.Label(self.frame_1, text="Codigo", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.05,relheight=0.1,relwidth=0.1)
            
            self.id_entrada = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.id_entrada.place(relx=0.01,rely=0.15,relheight=0.05,relwidth=0.1)

            # Campo para a Nome Produto
            tkinter.Label(self.frame_1, text="Nome Produto", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.30,relheight=0.1,relwidth=0.2)
            
            self.entrada_nomeProturo = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_nomeProturo.place(relx=0.01,rely=0.40,relheight=0.05,relwidth=0.60)

            # Campo para a Quantidade
            tkinter.Label(self.frame_1, text="Quantidade", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.52,relheight=0.1,relwidth=0.2)
            
            self.entrada_Quantidade = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_Quantidade.place(relx=0.01,rely=0.62,relheight=0.05,relwidth=0.60)

            # Campo para a Valor Compra
            tkinter.Label(self.frame_1, text="Valor Compra", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.70, rely=0.30,relheight=0.1,relwidth=0.2)
            
            self.entrada_valorProduto = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_valorProduto.place(relx=0.70,rely=0.40,relheight=0.05,relwidth=0.20)
            
            # Campo para a Valor Venda
            tkinter.Label(self.frame_1, text="Valor Venda", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.70, rely=0.52,relheight=0.1,relwidth=0.2)
            
            self.entrada_valorProdutoVenda = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_valorProdutoVenda.place(relx=0.70,rely=0.62,relheight=0.05,relwidth=0.20)


        

