import socket
import sys
from threading import Thread, BoundedSemaphore
from datetime import datetime
import wx
import wx.grid as gridlib
import time

#Classe que representa a janela para inserir os dados do servidor
class JanelaDadoServidor(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaDadoServidor, self).__init__(parent, -1, 'Dados do Servidor', style=style)

        #Configuracao de elementos de tela
        self.ip_texto = wx.StaticText(self, -1, "Digite o IP")
        self.ip_entrada = wx.TextCtrl(self, value="")
        self.ip_entrada.SetInitialSize((200, 20))
        self.porta_texto = wx.StaticText(self, -1, "Digite a porta")
        self.porta_entrada = wx.TextCtrl(self, value="")
        self.porta_entrada.SetInitialSize((200, 20))
        botoes = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ip_texto, 0, wx.ALL, 5)
        sizer.Add(self.ip_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.porta_texto, 0, wx.ALL, 5)
        sizer.Add(self.porta_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)

    #funcao para pegar os dados inseridos na janela
    def pegar_dados_servidor(self):
        return self.ip_entrada.GetValue() + "," + self.porta_entrada.GetValue()

#Classe que representa a janela para inserir os dados do login do usuario
class JanelaDadosLogin(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaDadosLogin, self).__init__(parent, -1, 'Dados de Login', style=style)
        # Configuracao de elementos de tela
        self.usuario_texto = wx.StaticText(self, -1, "Digite o usuario")
        self.usuario_entrada = wx.TextCtrl(self, value="")
        self.usuario_entrada.SetInitialSize((200, 20))
        self.senha_texto = wx.StaticText(self, -1, "Digite a senha")
        self.senha_entrada = wx.TextCtrl(self, value="", style=wx.TE_PASSWORD)
        self.senha_entrada.SetInitialSize((200, 20))
        self.botoes = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.usuario_texto, 0, wx.ALL, 5)
        sizer.Add(self.usuario_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.senha_texto, 0, wx.ALL, 5)
        sizer.Add(self.senha_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)

    # funcao para pegar os dados inseridos na janela
    def pegar_login(self):
        return self.usuario_entrada.GetValue() + "," + self.senha_entrada.GetValue()

#Classe que representa a janela para inserir os dados para entrar em um leilao
class JanelaEntrarLeilao(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaEntrarLeilao, self).__init__(parent, -1, 'Entrar em um leilao', style=style)
        # Configuracao de elementos de tela
        self.leilao_texto = wx.StaticText(self, -1, "Digite o identificador do leilao")
        self.identificador_leilao = wx.TextCtrl(self, value="")
        self.identificador_leilao.SetInitialSize((200, 20))
        self.botoes = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.leilao_texto, 0, wx.ALL, 5)
        sizer.Add(self.identificador_leilao, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)

    # funcao para pegar os dados inseridos na janela
    def pegar_identificador_leilao(self):
        return self.identificador_leilao.GetValue()

#Classe que representa a janela para inserir os dados para sair de um leilao
class JanelaSairLeilao(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaSairLeilao, self).__init__(parent, -1, 'Sair de um leilao', style=style)
        # Configuracao de elementos de tela'
        self.leilao_texto = wx.StaticText(self, -1, "Digite o identificador do leilao")
        self.identificador_leilao = wx.TextCtrl(self, value="")
        self.identificador_leilao.SetInitialSize((200, 20))
        self.botoes = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.leilao_texto, 0, wx.ALL, 5)
        sizer.Add(self.identificador_leilao, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)

    # funcao para pegar os dados inseridos na janela
    def pegar_identificador_leilao(self):
        return self.identificador_leilao.GetValue()

#Classe que representa a janela para inserir os dados de um lance do leilao
class JanelaDarLanceLeilao(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaDarLanceLeilao, self).__init__(parent, -1, 'Dar lance', style=style)
        # Configuracao de elementos de tela
        self.leilao_texto = wx.StaticText(self, -1, "Digite o identificador do leilao")
        self.identificador_leilao = wx.TextCtrl(self, value="")
        self.identificador_leilao.SetInitialSize((200, 20))
        self.lance = wx.StaticText(self, -1, "Digite a valor do lance")
        self.lance_entrada = wx.TextCtrl(self, value="")
        self.lance_entrada.SetInitialSize((200, 20))
        self.botoes = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.leilao_texto, 0, wx.ALL, 5)
        sizer.Add(self.identificador_leilao, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.lance, 0, wx.ALL, 5)
        sizer.Add(self.lance_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)

    # funcao para pegar os dados inseridos na janela
    def pegar_lance(self):
        return self.identificador_leilao.GetValue() + ',' + self.lance_entrada.GetValue()

#Classe que representa a janela de aviso
class JanelaAviso(wx.Dialog):
    def __init__(self, parent, texto):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaAviso, self).__init__(parent, -1, 'Aviso', style=style)
        # Configuracao de elementos de tela
        self.aviso_texto = wx.StaticText(self, -1, texto)
        self.botoes = self.CreateButtonSizer(wx.OK)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.aviso_texto, 0, wx.ALL, 5)
        sizer.Add(self.botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)

#Classe que representa a janela para inserir de cadastro de produto - criacao de leilao
class JanelaCadastraProduto(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaCadastraProduto, self).__init__(parent, -1, 'Cadastrar produto para leilao', style=style)
        # Configuracao de elementos de tela
        self.nome = wx.StaticText(self, -1, "Digite o nome")
        self.nome_entrada = wx.TextCtrl(self, value="")
        self.nome_entrada.SetInitialSize((200, 20))

        self.descricao = wx.StaticText(self, -1, "Digite a descricao")
        self.descricao_entrada = wx.TextCtrl(self, value="")
        self.descricao_entrada.SetInitialSize((200, 20))

        self.lance_minimo = wx.StaticText(self, -1, "Digite o lance minimo")
        self.lance_minimo_entrada = wx.TextCtrl(self, value="")
        self.lance_minimo_entrada.SetInitialSize((200, 20))

        self.dia = wx.StaticText(self, -1, "Digite o dia de inicio do leilao")
        self.dia_entrada = wx.TextCtrl(self, value="")
        self.dia_entrada.SetInitialSize((200, 20))

        self.mes = wx.StaticText(self, -1, "Digite o mes de inicio do leilao")
        self.mes_entrada = wx.TextCtrl(self, value="")
        self.mes_entrada.SetInitialSize((200, 20))

        self.ano = wx.StaticText(self, -1, "Digite o ano de inicio do leilao")
        self.ano_entrada = wx.TextCtrl(self, value="")
        self.ano_entrada.SetInitialSize((200, 20))

        self.hora = wx.StaticText(self, -1, "Digite o hora de inicio do leilao")
        self.hora_entrada = wx.TextCtrl(self, value="")
        self.hora_entrada.SetInitialSize((200, 20))

        self.minuto = wx.StaticText(self, -1, "Digite o minuto de inicio do leilao")
        self.minuto_entrada = wx.TextCtrl(self, value="")
        self.minuto_entrada.SetInitialSize((200, 20))

        self.segundo = wx.StaticText(self, -1, "Digite o segundo de inicio do leilao")
        self.segundo_entrada = wx.TextCtrl(self, value="")
        self.segundo_entrada.SetInitialSize((200, 20))

        self.tempo_maximo = wx.StaticText(self, -1, "Digite o tempo maximo entre lances")
        self.tempo_maximo_entrada = wx.TextCtrl(self, value="")
        self.tempo_maximo_entrada.SetInitialSize((200, 20))

        self.botoes = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nome, 0, wx.ALL, 5)
        sizer.Add(self.nome_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.descricao, 0, wx.ALL, 5)
        sizer.Add(self.descricao_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.lance_minimo, 0, wx.ALL, 5)
        sizer.Add(self.lance_minimo_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.dia, 0, wx.ALL, 5)
        sizer.Add(self.dia_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.mes, 0, wx.ALL, 5)
        sizer.Add(self.mes_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.ano, 0, wx.ALL, 5)
        sizer.Add(self.ano_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.hora, 0, wx.ALL, 5)
        sizer.Add(self.hora_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.minuto, 0, wx.ALL, 5)
        sizer.Add(self.minuto_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.segundo, 0, wx.ALL, 5)
        sizer.Add(self.segundo_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.tempo_maximo, 0, wx.ALL, 5)
        sizer.Add(self.tempo_maximo_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)

    # funcao para pegar os dados inseridos na janela
    def pegar_produto_leilao(self):
        return self.nome_entrada.GetValue() + ',' + \
               self.descricao_entrada.GetValue() + ',' + \
               self.lance_minimo_entrada.GetValue() + ',' + \
               self.dia_entrada.GetValue() + ',' + \
               self.mes_entrada.GetValue() + ',' + \
               self.ano_entrada.GetValue() + ',' + \
               self.hora_entrada.GetValue() + ',' + \
               self.minuto_entrada.GetValue() + ',' + \
               self.segundo_entrada.GetValue() + ',' + \
               self.tempo_maximo_entrada.GetValue()

#Classe que representa a janela para inserir os dados para cadastrar usuario
class JanelaCadastraUsuario(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaCadastraUsuario, self).__init__(parent, -1, 'Cadastrar usuario', style=style)
        # Configuracao de elementos de tela
        self.nome = wx.StaticText(self, -1, "Digite o nome")
        self.nome_entrada = wx.TextCtrl(self, value="")
        self.nome_entrada.SetInitialSize((200, 20))

        self.telefone = wx.StaticText(self, -1, "Digite a telefone")
        self.telefone_entrada = wx.TextCtrl(self, value="")
        self.telefone_entrada.SetInitialSize((200, 20))

        self.endereco = wx.StaticText(self, -1, "Digite o endereco")
        self.endereco_entrada = wx.TextCtrl(self, value="")
        self.endereco_entrada.SetInitialSize((200, 20))

        self.email = wx.StaticText(self, -1, "Digite o email")
        self.email_entrada = wx.TextCtrl(self, value="")
        self.email_entrada.SetInitialSize((200, 20))

        self.senha = wx.StaticText(self, -1, "Digite a senha")
        self.senha_entrada = wx.TextCtrl(self, value="", style=wx.TE_PASSWORD)
        self.senha_entrada.SetInitialSize((200, 20))

        self.botoes = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nome, 0, wx.ALL, 5)
        sizer.Add(self.nome_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.telefone, 0, wx.ALL, 5)
        sizer.Add(self.telefone_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.endereco, 0, wx.ALL, 5)
        sizer.Add(self.endereco_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.email, 0, wx.ALL, 5)
        sizer.Add(self.email_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.senha, 0, wx.ALL, 5)
        sizer.Add(self.senha_entrada, wx.EXPAND, wx.ALL, 5)
        sizer.Add(self.botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)

    # funcao para pegar os dados inseridos na janela
    def pegar_usuario(self):
        return self.nome_entrada.GetValue() + ',' + \
               self.telefone_entrada.GetValue() + ',' + \
               self.endereco_entrada.GetValue() + ',' + \
               self.email_entrada.GetValue() + ',' + \
               self.senha_entrada.GetValue()

#Classe que representa a janela para mostrar a lista de leiloes ativos
class JanelaListaLeiloes(wx.Dialog):
    def __init__(self, parent, listagem):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(JanelaListaLeiloes, self).__init__(parent, -1, 'Listagem de leiloes ativos', style=style)

        #Monta tabela na tela com as informacoes dos leiloes ativos
        listagem = listagem.replace('Listagem,', '').split('\n')
        tabela = gridlib.Grid(self)
        tabela.CreateGrid(len(listagem) - 1, 8)

        #configura o nome das colunas
        tabela.SetColLabelValue(0, "Identificador")
        tabela.SetColLabelValue(1, "Nome")
        tabela.SetColLabelValue(2, "Descricao")
        tabela.SetColLabelValue(3, "Lance Minimo")
        tabela.SetColLabelValue(4, "Data de inicio")
        tabela.SetColLabelValue(5, "Hora de inicio")
        tabela.SetColLabelValue(6, "Tempo maximo")
        tabela.SetColLabelValue(7, "Dono")

        #configura o nome das linhas
        tabela.SetRowLabelValue(0, "")
        tabela.SetRowLabelValue(1, "")
        tabela.SetRowLabelValue(2, "")
        tabela.SetRowLabelValue(3, "")
        tabela.SetRowLabelValue(4, "")
        tabela.SetRowLabelValue(5, "")
        tabela.SetRowLabelValue(6, "")
        tabela.SetRowLabelValue(7, "")

        posicao_coluna = 0

        #Para cada leilao ativo, insere uma linha com as informacoes
        for info in listagem:
            l = info.split(',')

            if l != ['']:
                tabela.SetCellValue(posicao_coluna, 0, l[0])
                tabela.SetReadOnly(posicao_coluna, 0, True)
                tabela.SetCellValue(posicao_coluna, 1, l[1])
                tabela.SetReadOnly(posicao_coluna, 1, True)
                tabela.SetCellValue(posicao_coluna, 2, l[2])
                tabela.SetReadOnly(posicao_coluna, 2, True)
                tabela.SetCellValue(posicao_coluna, 3, l[3])
                tabela.SetReadOnly(posicao_coluna, 3, True)
                tabela.SetCellValue(posicao_coluna, 4, l[4] + '/' + l[5] + '/' + l[6])
                tabela.SetReadOnly(posicao_coluna, 4, True)
                tabela.SetCellValue(posicao_coluna, 5, l[7] + ':' + l[8])
                tabela.SetReadOnly(posicao_coluna, 5, True)
                tabela.SetCellValue(posicao_coluna, 6, l[9])
                tabela.SetReadOnly(posicao_coluna, 6, True)
                tabela.SetCellValue(posicao_coluna, 7, l[10])
                tabela.SetReadOnly(posicao_coluna, 7, True)

                posicao_coluna += 1

        botoes = self.CreateButtonSizer(wx.OK)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tabela, 1, wx.EXPAND)
        sizer.Add(botoes, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(sizer)

#Classe que representa a tela principal
class TelaLeilao(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Leilao UFF", size=(1000, 280))

        # Configuracao de elementos de tela

        #Configuracoes de textos, botoes e os eventos de clique dos botoes
        self.bem_vindo = wx.StaticText(self, label="Bem vindo ao Leilao UFF", pos=(20, 10))
        self.usuario_texto = wx.StaticText(self, label="Usuario: ", pos=(20, 30))
        self.usuario_nome = wx.StaticText(self, label="Nao logado", pos=(80, 30))
        self.botao_cadastrar_usuario = wx.Button(self, label="Cadastrar Usuario", pos=(20, 60))
        self.Bind(wx.EVT_BUTTON, botao_cadastrar_usuario, self.botao_cadastrar_usuario)

        self.botao_logar_deslogar = wx.Button(self, label="Logar/Deslogar", pos=(20, 90))
        self.Bind(wx.EVT_BUTTON, botao_login_deslogar, self.botao_logar_deslogar)

        self.botao_cadastrar_produto = wx.Button(self, label="Cadastrar produto", pos=(20, 120))
        self.Bind(wx.EVT_BUTTON, botao_cadastrar_produto, self.botao_cadastrar_produto)

        self.botao_listar_leiloes = wx.Button(self, label="Listar leiloes", pos=(20, 150))
        self.Bind(wx.EVT_BUTTON, botao_listar_leiloes, self.botao_listar_leiloes)

        self.botao_entrar_leilao = wx.Button(self, label="Participar de um leilao", pos=(20, 180))
        self.Bind(wx.EVT_BUTTON, botao_entrar_leilao, self.botao_entrar_leilao)

        self.botao_sair_leilao = wx.Button(self, label="Sair de um leilao", pos=(20, 210))
        self.Bind(wx.EVT_BUTTON, botao_sair_leilao, self.botao_sair_leilao)

        self.botao_dar_lance = wx.Button(self, label="Dar um lance", pos=(20, 240))
        self.Bind(wx.EVT_BUTTON, botao_dar_lance, self.botao_dar_lance)

        #Configura tabela que mostra as informacoes dos leiloes que o usuario esta participando
        self.participando_leilao = wx.StaticText(self, label="Leiloes que voce esta participando", pos=(350, 20))
        self.tabela = gridlib.Grid(self, pos=(350, 40), size=(500, 50))
        self.tabela.CreateGrid(0, 5)

        self.tabela.SetColLabelValue(0, "Identificador")
        self.tabela.SetColLabelValue(1, "Nome do usuario")
        self.tabela.SetColLabelValue(2, "Valor atual")
        self.tabela.SetColLabelValue(3, "N# Usuarios")
        self.tabela.SetColLabelValue(4, "N# Lances dados")

        self.tabela.SetRowLabelValue(0, "")
        self.tabela.SetRowLabelValue(1, "")
        self.tabela.SetRowLabelValue(2, "")
        self.tabela.SetRowLabelValue(3, "")
        self.tabela.SetRowLabelValue(4, "")

        self.tabela.AutoSize()

    #funcao que insere leilao na tabela de leiloes que o usuario participa
    def insere_leilao_tabela(self, identificador):
        self.tabela.InsertRows()
        self.tabela.SetCellValue(0, 0, identificador)
        self.tabela.SetCellValue(0, 1, "-")
        self.tabela.SetCellValue(0, 2, "-")
        self.tabela.SetCellValue(0, 3, "-")
        self.tabela.SetCellValue(0, 4, "-")
        self.tabela.AutoSize()

    # funcao que atualiza as informacoes do leilao na tabela a partir de um lance que chegou
    def atualiza_leilao_tabela(self, lance):

        linha = 0
        lance = lance.replace("Lance,", '').split(",")
        #percorre as linhas da tabela e verifica que e a linha na tabela que esta o leilao que as informacoes vao ser atualizadas
        for i in xrange(self.tabela.GetNumberRows()):
            if self.tabela.GetCellValue(i, 0) == lance[0]:
                linha = i
                break
        #atualiza as informacoes de todas as colunas do leilao
        for j in xrange(5):
            self.tabela.SetCellValue(linha, j, lance[j])

    # funcao que remove leilao da tabela de leiloes
    def remove_leilao_tabela(self, identificador):

        # percorre as linhas da tabela e verifica que e a linha na tabela que esta o leilao que as informacoes vao ser atualizadas
        linha = 0
        for i in xrange(self.tabela.GetNumberRows()):
            if self.tabela.GetCellValue(i, 0) == identificador:
                linha = i
                break

        #Remove leilao da tabela
        self.tabela.DeleteRows(pos=int(linha))
        self.tabela.AutoSize()

    # funcao que atualiza a informacao de nome do usuario
    def atualiza_usuario(self, nome):
        self.usuario_nome.SetLabel(nome)

    # funcao que mostra janela de aviso para mostrar informacoes do contato do vendedor
    def mostra_vendedor(self, info):

        info = info.replace('Contato_vendedor,','').split(',')

        self.mostra_janela_aviso(
            'Boa noticia voce conseguiu vender o leilao ' +
            info[0] + ' por ' + info[1] + ' para ' + info[2] + ' End. ' + info[3] + ' Tel. ' + info[4] +
            ' Email. ' + info[5]
        )

    # funcao que mostra janela de aviso para mostrar informacoes do contato do comprador
    def mostra_comprador(self, info):
        info = info.replace('Contato_vendedor,', '').split(',')

        self.mostra_janela_aviso(
            'Boa noticia voce conseguiu comprar o leilao ' +
            info[0] + ' por ' + info[1] + ' do vendedor ' + info[2] + ' End. ' + info[3] + ' Tel. ' + info[4] +
            ' Email. ' + info[5]
        )

    # funcao que mostra janela de aviso para mostrar informacoes de final de leilao
    def mostra_fim_leilao(self, info):

        info = info.replace('Fim_leilao,','').split(',')

        #apos o fim do leilao, remove leilao da tabela
        self.remove_leilao_tabela(int(info[0]))
        self.mostra_janela_aviso('Leilao ' + info[0] + ' foi arrematado por ' + info[1] + ' pelo comprador ' + info[2])

    # funcao que cria uma janela de aviso
    def mostra_janela_aviso(self, aviso):
        j_aviso = JanelaAviso(None, aviso)
        j_aviso.Center()
        j_aviso.ShowModal()
        j_aviso.Destroy()

# funcao de evento de clique do botao para cadastrar usuario
def botao_cadastrar_usuario(evento):
    global s_resposta, resposta

    #criacao da janela de cadastro de usuario
    janela = JanelaCadastraUsuario(None)
    janela.Center()
    dados = None
    if janela.ShowModal() == wx.ID_OK:
        #apos clicar em OK da janela, pega as informacoes inseridas na janela
        dados = janela.pegar_usuario().split(',')
    janela.Destroy()

    if dados is not None:
        adiciona_usuario(dados[0], dados[1], dados[2], dados[3], dados[4])
        while True:
            s_resposta.acquire()

            if resposta is not None:

                if resposta == 'Ok':
                    tela.mostra_janela_aviso('Cadastro realizado com sucesso')
                else:
                    tela.mostra_janela_aviso('Nao foi possivel realizar o cadastro')

                resposta = None
                s_resposta.release()
                break
            s_resposta.release()
            time.sleep(0.3)

# funcao de evento de clique do botao para logar/deslogar
def botao_login_deslogar(evento):
    global s_resposta, resposta, s_usuario_logado, usuario_logado, nome_usuario

    s_usuario_logado.acquire()

    #verifica se o usuario esta logado - para ver se vai logar ou deslogar
    if usuario_logado:
        #envia mensagem para sair
        envia_mensagem_servidor('Sair')
        #espera retorno
        while True:
            s_resposta.acquire()

            if resposta is not None:

                if resposta == 'Ok':

                    usuario_logado = False
                    nome_usuario = 'Nao Logado'
                    #inicia nome de usuario como Nao logado
                    tela.atualiza_usuario(nome_usuario)
                    tela.mostra_janela_aviso('Saida realiza com sucesso')
                else:
                    tela.mostra_janela_aviso('Nao foi possivel realizar essa operacao')

                resposta = None
                s_resposta.release()
                break
            s_resposta.release()
            time.sleep(0.3)
    else:
        # criacao da janela de dados de login de usuario
        janela = JanelaDadosLogin(None)
        janela.Center()
        dados_login = None
        if janela.ShowModal() == wx.ID_OK:
            # apos clicar em OK da janela, pega as informacoes inseridas na janela
            dados_login = janela.pegar_login().split(',')
        janela.Destroy()

        if dados_login is not None:

            #chama funcao para fazer login
            faz_login(dados_login[0], dados_login[1])

            # espera retorno
            while True:
                s_resposta.acquire()

                if resposta is not None:

                    if resposta == 'Ok':

                        usuario_logado = True
                        nome_usuario = dados_login[0]
                        #atualiza nome do usuario logado na tela
                        tela.atualiza_usuario(nome_usuario)
                        tela.mostra_janela_aviso('Login efetuado com sucesso - Bem vindo Sr(a) ' + nome_usuario)
                    else:
                        tela.mostra_janela_aviso('Nao foi possivel realizar essa operacao')

                    resposta = None
                    s_resposta.release()
                    break
                s_resposta.release()
                time.sleep(0.3)

    s_usuario_logado.release()

# funcao de evento de clique do botao para cadastrar produto
def botao_cadastrar_produto(evento):
    global s_resposta, resposta, s_usuario_logado, usuario_logado

    s_usuario_logado.acquire()

    #verifica se o usuario esta logado
    if usuario_logado:
        # criacao da janela de cadastro de produto
        janela = JanelaCadastraProduto(None)
        janela.Center()
        dados = None
        if janela.ShowModal() == wx.ID_OK:
            # apos clicar em OK da janela, pega as informacoes inseridas na janela
            dados = janela.pegar_produto_leilao().split(',')
        janela.Destroy()

        if dados is not None:

            #chama funcao para lancar produto
            lanca_produto(dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], dados[6], dados[7], dados[8],
                          dados[9])

            # espera retorno
            while True:
                s_resposta.acquire()

                if resposta is not None:

                    if resposta == 'Ok':
                        tela.mostra_janela_aviso('Produto cadastrado com sucesso')
                    else:
                        tela.mostra_janela_aviso('Nao foi possivel realizar o cadastro do produto ' + dados[0])

                    resposta = None
                    s_resposta.release()
                    break
                s_resposta.release()
                time.sleep(0.3)

    else:
        tela.mostra_janela_aviso('Operacao somente permitida para usuarios logados')

    s_usuario_logado.release()

# funcao de evento de clique do botao para listar leiloes ativos
def botao_listar_leiloes(evento):
    global s_resposta, resposta

    #chama funcao para listar leiloes
    lista_leiloes()

    # espera retorno
    while True:
        s_resposta.acquire()

        if resposta is not None:

            #verifica se existe algum leilao ativo
            if 'Listagem,' == resposta:
                tela.mostra_janela_aviso('Nenhum leilao disponivel')
            else:
                #cria janela de leiloes para mostrar a lista de leiloes
                janela_lista_leiloes = JanelaListaLeiloes(None, resposta)
                janela_lista_leiloes.Center()
                if janela_lista_leiloes.ShowModal() == wx.ID_OK:
                    pass
                janela_lista_leiloes.Destroy()

            resposta = None
            s_resposta.release()
            break
        s_resposta.release()
        time.sleep(0.3)

# funcao de evento de clique do botao para entrar no leilao
def botao_entrar_leilao(evento):
    global s_resposta, resposta, s_usuario_logado, usuario_logado

    s_usuario_logado.acquire()

    #verifica se o usuario esta logado
    if usuario_logado:

        # criacao da janela para entrar em um leilao
        janela = JanelaEntrarLeilao(None)
        janela.Center()
        identificador = None
        if janela.ShowModal() == wx.ID_OK:
            # apos clicar em OK da janela, pega as informacoes inseridas na janela
            identificador = janela.pegar_identificador_leilao()
        janela.Destroy()

        if identificador is not None:

            #chama funcao para entrar no leilao
            entra_leilao(identificador)

            # espera retorno
            while True:
                s_resposta.acquire()

                if resposta is not None:

                    if resposta == 'Ok':
                        #insere leilao na tabela de leiloes participantes na tela
                        tela.insere_leilao_tabela(identificador)
                        tela.mostra_janela_aviso('Entrada no leilao ' + identificador + ' com sucesso')
                    else:
                        tela.mostra_janela_aviso('Nao foi possivel entrar no leilao ' + identificador)

                    resposta = None
                    s_resposta.release()
                    break
                s_resposta.release()
                time.sleep(0.3)

    else:
        tela.mostra_janela_aviso('Operacao somente permitida para usuarios logados')

    s_usuario_logado.release()

# funcao de evento de clique do botao para sair de um leilao
def botao_sair_leilao(evento):
    global s_resposta, resposta, s_usuario_logado, usuario_logado

    s_usuario_logado.acquire()

    #verifica se usuario esta logado
    if usuario_logado:

        # criacao da janela de saida de leilao
        janela = JanelaSairLeilao(None)
        janela.Center()
        identificador = None
        if janela.ShowModal() == wx.ID_OK:
            # apos clicar em OK da janela, pega as informacoes inseridas na janela
            identificador = janela.pegar_identificador_leilao()
        janela.Destroy()

        if identificador is not None:

            #chama funcao para sair do leilao
            sair_leilao(identificador)

            # espera retorno
            while True:
                s_resposta.acquire()

                if resposta is not None:

                    if resposta == 'Ok':
                        #remove leilao da tabela de leiloes
                        tela.remove_leilao_tabela(identificador)
                        tela.mostra_janela_aviso('Saida do leilao ' + identificador + ' com sucesso')
                    else:
                        tela.mostra_janela_aviso('Nao foi possivel sair do leilao ' + identificador)

                    resposta = None
                    s_resposta.release()
                    break
                s_resposta.release()
                time.sleep(0.3)

    else:
        tela.mostra_janela_aviso('Operacao somente permitida para usuarios logados')

    s_usuario_logado.release()

# funcao de evento de clique do botao para dar lance
def botao_dar_lance(evento):
    global s_resposta, resposta, s_usuario_logado, usuario_logado

    s_usuario_logado.acquire()

    #verifica se usuario esta logado
    if usuario_logado:

        # criacao da janela de dar lance
        janela = JanelaDarLanceLeilao(None)
        janela.Center()
        dados_lance = None
        if janela.ShowModal() == wx.ID_OK:
            # apos clicar em OK da janela, pega as informacoes inseridas na janela
            dados_lance = janela.pegar_lance().split(',')
        janela.Destroy()

        if dados_lance is not None:

            #chama funcao para enviar lance
            envia_lance(dados_lance[0], dados_lance[1])

            # espera retorno
            while True:
                s_resposta.acquire()

                if resposta is not None:

                    if resposta == 'Ok':
                        tela.mostra_janela_aviso('Lance realizado com sucesso')
                    else:
                        tela.mostra_janela_aviso('Nao foi possivel dar o lance')

                    resposta = None
                    s_resposta.release()
                    break
                s_resposta.release()
                time.sleep(0.3)

    else:
        tela.mostra_janela_aviso('Operacao somente permitida para usuarios logados')

    s_usuario_logado.release()

#funcao que envia pro servidor a mensagem para lancar produto
def lanca_produto(nome, descricao, lance_minimo, dia, mes, ano, hora, minuto, segundo, tempo_maximo):
    global resposta, s_resposta

    s_resposta.acquire()
    resposta = None
    s_resposta.release()

    envia_mensagem_servidor(
        'Lanca_produto,' + nome + ',' + descricao + ',' + lance_minimo + ',' + dia
        + ',' + mes + ',' + ano + ',' + hora + ',' + minuto + ',' + segundo + ',' + tempo_maximo)

#funcao que envia pro servidor a mensagem para adcionar usuario
def adiciona_usuario(nome, telefone, endereco, email, senha):
    global resposta, s_resposta

    s_resposta.acquire()
    resposta = None
    s_resposta.release()

    resp = 'Adiciona_usuario,' + nome + ',' + telefone + ',' + endereco + ',' + email + ',' + senha
    envia_mensagem_servidor(resp)

#funcao que envia pro servidor a mensagem para fazer login
def faz_login(nome, senha):
    global resposta, s_resposta

    s_resposta.acquire()
    resposta = None
    s_resposta.release()

    envia_mensagem_servidor('Faz_login,' + nome + ',' + senha)

#funcao que envia pro servidor a mensagem para enviar lance
def envia_lance(identificador_leilao, valor_lance):
    global resposta, s_resposta

    s_resposta.acquire()
    resposta = None
    envia_mensagem_servidor('Enviar_lance,' + identificador_leilao + ',' + valor_lance)
    s_resposta.release()

#funcao que envia pro servidor a mensagem para listar os leiloes
def lista_leiloes():
    global resposta, s_resposta

    s_resposta.acquire()
    resposta = None
    envia_mensagem_servidor('Lista_leiloes')
    s_resposta.release()

#funcao que envia pro servidor a mensagem para entrar em um leilao
def entra_leilao(identificador_leilao):
    global resposta, s_resposta
    s_resposta.acquire()
    resposta = None
    envia_mensagem_servidor('Entrar_leilao,' + identificador_leilao)
    s_resposta.release()

#funcao que envia pro servidor a mensagem para sair de um leilao
def sair_leilao(identificador_leilao):
    global resposta, s_resposta
    s_resposta.acquire()
    resposta = None
    envia_mensagem_servidor('Sair_leilao,' + identificador_leilao)
    s_resposta.release()

# Funcao que envia mensagem para o servidor
def envia_mensagem_servidor(mensagem):
    print >> sys.stderr, 'enviando ', mensagem, '  as ', datetime.now().time()
    servidor_sock.sendall(mensagem)

# Imprime as mensagens recebidas
def log_mensagem_recebida(mensagem):
    print >> sys.stderr, 'recebido ', mensagem, '  at ', datetime.now().time()

# Funcao que guarda nas variaveis o IP e Porta do servidor
def configura_servidor(host, port):
    global host_ip, porta
    host_ip = host
    porta = port


# Funcao que conecta socket do servidor
def conecta_servidor():
    global servidor_sock
    try:
        # Cria socket para conexao
        servidor_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Configura endereco - IP e Porta
        endereco_servidor = (host_ip, porta)
        print >> sys.stderr, 'Conectando em %s port %s' % endereco_servidor
        servidor_sock.connect(endereco_servidor)
        print >> sys.stderr, 'Conectado'
        return True
    except:
        return False

# Funcao que desconecta socket do servidor
def desconecta_servidor():
    servidor_sock.close()


# Funcao que realiza comunicacao com servidor
def estabelece_conexao_servidor(host_ip, porta):
    global s_servidor_contectado, servidor_conectado, mensagem_erro

    # Configura IP e Porta do Servidor
    configura_servidor(host_ip, porta)
    # Verifica se conecta com o servidor
    if (conecta_servidor()):
        # mensagem_erro = None
        # Libera a variavel que controla se conectou o servidor ou se deu erro
        s_servidor_contectado.acquire()
        servidor_conectado = True
        s_servidor_contectado.release()
    else:
        # mensagem_erro = 'Nao foi possivel conectar ao servidor'
        # Libera a variavel que controla se conectou o servidor ou se deu erro
        s_servidor_contectado.acquire()
        servidor_conectado = False
        s_servidor_contectado.release()

#Thread que escuta as mensagens vindas do servidor
def escuta_servidor():
    global s_resposta, resposta

    while True:
        data = servidor_sock.recv(4096)
        log_mensagem_recebida(data)

        #verifica o tipo da mensagem para processar
        if 'Contato_cliente' in data:
            #executa o metodo na thread da interface grafica
            wx.CallAfter(tela.mostra_comprador,str(data))
        elif 'Contato_vendedor' in data:
            # executa o metodo na thread da interface grafica
            wx.CallAfter(tela.mostra_vendedor,str(data))
        elif 'Lance' in data:
            tela.atualiza_leilao_tabela(str(data))
        elif 'Fim_leilao' in data:
            # executa o metodo na thread da interface grafica
            wx.CallAfter(tela.mostra_fim_leilao,str(data))
        else:
            s_resposta.acquire()
            resposta = str(data)
            s_resposta.release()


# Variaveis para guarda informacoes do servidor
host_ip = ''
porta = ''
# Declaracao do socket de conexao com servidor
servidor_sock = None
servidor_conectado = False
s_servidor_contectado = BoundedSemaphore()
usuario_logado = False
s_usuario_logado = BoundedSemaphore()
nome_usuario = ''
# operacao_atual = None
# s_operacao_atual = BoundedSemaphore()
resposta = None
s_resposta = BoundedSemaphore()

try:

    #cria interface grafica
    app = wx.App(False)

    #cria janela com dados do servidor
    janela = JanelaDadoServidor(None)
    janela.Center()
    if janela.ShowModal() == wx.ID_OK:
        dados_servidor = janela.pegar_dados_servidor().split(',')
        host_ip = dados_servidor[0]
        porta = int(dados_servidor[1])
        estabelece_conexao_servidor(host_ip, porta)
        #conecta servidor
        s_servidor_contectado.acquire()
        if servidor_conectado:
            #executa thread para escutar as mensagens
            t = Thread(target=escuta_servidor)
            t.setDaemon(True)
            t.start()
            #criacao da tela principal
            tela = TelaLeilao()
            tela.Show()
        else:
            #cria janela de aviso para mostrar que nao foi possivel conectar
            janela_aviso = JanelaAviso(None, 'Nao foi possivel conectar ao servidor')
            janela_aviso.Center()
            janela_aviso.ShowModal()
            janela_aviso.Destroy()
        s_servidor_contectado.release()
    janela.Destroy()
    app.MainLoop()

# Por final, desconecta serviddor
finally:
    desconecta_servidor()
