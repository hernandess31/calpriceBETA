import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import hashlib
import os

class CalPriceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CalPrice - Sistema de Gerenciamento")
        self.root.geometry("800x600")
        
        # Dados do aplicativo
        self.pedidos = []
        self.receitas_salvas = []
        
        # Carregar dados
        self.carregar_dados()
        
        # Estilo
        self.setup_style()
        
        # Tela de login/cadastro
        self.setup_login_screen()
    
    def setup_style(self):
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Error.TLabel', foreground='red')
    
    def setup_login_screen(self):
        # Limpar a tela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=50, padx=50, fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Bem-vindo ao CalPrice", style='Header.TLabel').pack(pady=20)
        
        # Frame de login
        login_frame = ttk.Frame(main_frame)
        login_frame.pack(pady=20)
        
        # Usuário
        ttk.Label(login_frame, text="Usuário:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.usuario_entry = ttk.Entry(login_frame, width=25)
        self.usuario_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Senha
        ttk.Label(login_frame, text="Senha:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.senha_entry = ttk.Entry(login_frame, width=25, show="*")
        self.senha_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Login", command=self.fazer_login).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar_usuario).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Sair", command=self.root.quit).grid(row=0, column=2, padx=10)
        
        # Mensagem de erro
        self.login_msg = ttk.Label(main_frame, text="", style='Error.TLabel')
        self.login_msg.pack(pady=10)
    
    def hash_senha(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def carregar_usuarios(self):
        try:
            with open("usuarios.txt", "r", encoding="utf-8") as f:
                return [linha.strip().split(":") for linha in f if ":" in linha]
        except FileNotFoundError:
            return []
    
    def fazer_login(self):
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get().strip()
        
        if not usuario or not senha:
            self.login_msg.config(text="Preencha todos os campos!")
            return
        
        usuarios = self.carregar_usuarios()
        
        for user, senha_hash in usuarios:
            if user == usuario and self.hash_senha(senha) == senha_hash:
                self.login_msg.config(text="")
                self.show_main_menu()
                return
        
        self.login_msg.config(text="Usuário ou senha incorretos!")
    
    def cadastrar_usuario(self):
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get().strip()
        
        if not usuario or not senha:
            self.login_msg.config(text="Preencha todos os campos!")
            return
        
        usuarios = self.carregar_usuarios()
        
        # Verificar se usuário já existe
        for user, _ in usuarios:
            if user == usuario:
                self.login_msg.config(text="Usuário já existe!")
                return
        
        # Cadastrar novo usuário
        with open("usuarios.txt", "a", encoding="utf-8") as f:
            f.write(f"{usuario}:{self.hash_senha(senha)}\n")
        
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.login_msg.config(text="")
    
    def carregar_dados(self):
        try:
            with open("receitas.txt", "r", encoding="utf-8") as f:
                self.receitas_salvas = [linha.strip() for linha in f.readlines()]
        except FileNotFoundError:
            pass
        
        try:
            with open("pedidos.txt", "r", encoding="utf-8") as f:
                self.pedidos = [linha.strip() for linha in f.readlines()]
        except FileNotFoundError:
            pass
    
    def show_main_menu(self):
        # Limpar a tela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cabeçalho
        ttk.Label(main_frame, text="CalPrice - Menu Principal", style='Header.TLabel').pack(pady=20)
        
        # Botões do menu
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Calculadora de Preço", 
                  command=self.show_calculadora, width=25).pack(pady=10)
        ttk.Button(btn_frame, text="Receitas", 
                  command=self.show_receitas, width=25).pack(pady=10)
        ttk.Button(btn_frame, text="Controle de Pedidos", 
                  command=self.show_pedidos, width=25).pack(pady=10)
        ttk.Button(btn_frame, text="Sair", 
                  command=self.root.quit, width=25).pack(pady=10)
    
    def show_calculadora(self):
        # Limpar a tela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cabeçalho
        ttk.Label(main_frame, text="Calculadora de Preço", style='Header.TLabel').pack(pady=20)
        
        # Formulário
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        # Preço pago
        ttk.Label(form_frame, text="Preço pago (R$):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.preco_entry = ttk.Entry(form_frame)
        self.preco_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Quantidade embalagem
        ttk.Label(form_frame, text="Quantidade da embalagem (g/ml):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.pacote_entry = ttk.Entry(form_frame)
        self.pacote_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Quantidade receita
        ttk.Label(form_frame, text="Quantidade na receita (g/ml):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.usado_entry = ttk.Entry(form_frame)
        self.usado_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Botão calcular
        ttk.Button(form_frame, text="Calcular", command=self.calcular_preco).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Resultado
        self.resultado_label = ttk.Label(form_frame, text="", font=('Arial', 12, 'bold'))
        self.resultado_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Botão voltar
        ttk.Button(main_frame, text="Voltar ao Menu", command=self.show_main_menu).pack(pady=20)
    
    def calcular_preco(self):
        try:
            preco = float(self.preco_entry.get())
            pacote = float(self.pacote_entry.get())
            usado = float(self.usado_entry.get())
            
            if pacote == 0:
                messagebox.showerror("Erro", "A quantidade da embalagem não pode ser zero!")
                return
                
            conta = preco / pacote * usado
            self.resultado_label.config(text=f"Valor a ser cobrado: R$ {conta:.2f}")
        except ValueError:
            messagebox.showerror("Erro", "Digite valores numéricos válidos!")
    
    def show_receitas(self):
        # Limpar a tela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cabeçalho
        ttk.Label(main_frame, text="Gerenciador de Receitas", style='Header.TLabel').pack(pady=20)
        
        # Frame de botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Adicionar Receita", command=self.show_adicionar_receita).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Voltar ao Menu", command=self.show_main_menu).pack(side=tk.LEFT, padx=5)
        
        # Lista de receitas
        ttk.Label(main_frame, text="Receitas Salvas:").pack(pady=10)
        
        scroll_frame = ttk.Frame(main_frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.receitas_listbox = tk.Listbox(scroll_frame, yscrollcommand=scrollbar.set, width=80, height=15)
        self.receitas_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.receitas_listbox.yview)
        
        # Preencher lista
        for receita in self.receitas_salvas:
            self.receitas_listbox.insert(tk.END, receita)
    
    def show_adicionar_receita(self):
        # Janela de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Adicionar Receita")
        dialog.geometry("600x400")
        
        # Frame principal
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(main_frame, text="Nova Receita", style='Header.TLabel').pack(pady=10)
        
        # Área de texto
        ttk.Label(main_frame, text="Digite sua receita:").pack(pady=5)
        self.receita_text = scrolledtext.ScrolledText(main_frame, width=60, height=15)
        self.receita_text.pack(pady=10)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=lambda: self.salvar_receita(dialog)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def salvar_receita(self, dialog):
        receita = self.receita_text.get("1.0", tk.END).strip()
        
        if not receita:
            messagebox.showerror("Erro", "A receita não pode estar vazia!")
            return
        
        # Confirmar
        if messagebox.askyesno("Confirmar", "Deseja salvar esta receita?"):
            self.receitas_salvas.append(receita)
            
            # Salvar no arquivo
            with open("receitas.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(receita + "\n")
            
            messagebox.showinfo("Sucesso", "Receita salva com sucesso!")
            dialog.destroy()
            self.show_receitas()  # Atualizar a lista
    
    def show_pedidos(self):
        # Limpar a tela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cabeçalho
        ttk.Label(main_frame, text="Controle de Pedidos", style='Header.TLabel').pack(pady=20)
        
        # Frame de botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Adicionar Pedido", command=self.show_adicionar_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Voltar ao Menu", command=self.show_main_menu).pack(side=tk.LEFT, padx=5)
        
        # Lista de pedidos
        ttk.Label(main_frame, text="Pedidos Realizados:").pack(pady=10)
        
        scroll_frame = ttk.Frame(main_frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.pedidos_listbox = tk.Listbox(scroll_frame, yscrollcommand=scrollbar.set, width=80, height=15)
        self.pedidos_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.pedidos_listbox.yview)
        
        # Preencher lista
        for pedido in self.pedidos:
            self.pedidos_listbox.insert(tk.END, pedido)
    
    def show_adicionar_pedido(self):
        # Janela de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Adicionar Pedido")
        dialog.geometry("400x200")
        
        # Frame principal
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(main_frame, text="Novo Pedido", style='Header.TLabel').pack(pady=10)
        
        # Campo de entrada
        ttk.Label(main_frame, text="Nome do Pedido:").pack(pady=5)
        self.pedido_entry = ttk.Entry(main_frame, width=40)
        self.pedido_entry.pack(pady=10)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=lambda: self.salvar_pedido(dialog)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def salvar_pedido(self, dialog):
        pedido = self.pedido_entry.get().strip()
        
        if not pedido:
            messagebox.showerror("Erro", "O pedido não pode estar vazio!")
            return
        
        # Confirmar
        if messagebox.askyesno("Confirmar", "Deseja salvar este pedido?"):
            self.pedidos.append(pedido)
            
            # Salvar no arquivo
            with open("pedidos.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(pedido + "\n")
            
            messagebox.showinfo("Sucesso", "Pedido salvo com sucesso!")
            dialog.destroy()
            self.show_pedidos()  # Atualizar a lista

if __name__ == "__main__":
    root = tk.Tk()
    app = CalPriceApp(root)
    root.mainloop()