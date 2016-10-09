class Usuario:

    def __init__(self,nome,telefone,endereco,email,senha):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.email = email
        self.senha = senha
        self.logado = False

    def atualiza_login(self,logado):
        self.logado = logado
