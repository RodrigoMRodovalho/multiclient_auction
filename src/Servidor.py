import socket
import sys
import linecache
from threading import Thread, BoundedSemaphore

PORT = 50053              # Arbitrary non-privileged port


def lanca_produto(nome,descricao,lance_minimo,dia,mes,ano,hora,minuto,segundo,tempo_maximo):
    #todo verificar se usuario esta logado
    #todo gerar identificador unico para leilao
    stub = None

def enviar_lance(identificador_leilao,valor):
    #todo para o usuario que deu o lance retornar ok ou not_ok, para os outros, retornar
    #todo Identificador do leilao, nome do usuario, valor, numero de usuarios no leilao no
    #todo momento, numero de lances que ja foram dados.
    stub = None

def contato_vendedor():
    #todo envia para o vendedor as informacoes do comprador
    #todo Identificador do leilao, valor de venda, nome, enderco, telefone, email
    stub = None

def contato_comprador():
    # todo envia para o comprador as informacoes do vendedor
    # todo Identificador do leilao, valor de venda, nome, enderco, telefone, email
    stub = None


def lista_leiloes():
    #Nao precisa ser cadastrado, nem estar logado
    #todo obter informacoes dos leiloes (nao mostra leiloes que ja terminaram)
    #todo um produto por linha:
        # (identificador do leilao)
        # nome do produto
        # descricao
        # lance minimo
        #  dia, mes, ano e hora, minuto de inicio do leilao
        # tempo maximo sem lances para o produto
        # dono do produto
    stub = None


def entrar_leilao(identificador_leilao):
    #todo verificar se usuario esta logado e cadastrado
    #todo inserir usuario no leilao
    stub = None

def sair_leilao(identificador_leilao):
    #todo verificar se usuario esta logado e cadastrado
    #todo remover usuario do leilao
    stub = None

def fim_leilao():
    #todo enviar para todos que participam do leilao
    #Identificador do leilao, valor de venda, usuario que comprou
    stub = None

def adiciona_usuario(nome,telefone,endereco,email,senha):

    # verifica no arquivo se ja existe algum usuario com o nome passado como parametro
    # insere informaoes de usuario no arquivo
    global s_arquivo_usuarios

    s_arquivo_usuarios.acquire()
    arquivo_usuarios = open('registro/usuarios.txt','r+')
    usuario_nao_cadastrado = True
    for linha in arquivo_usuarios:
        usuario = linha.split(',')
        if usuario[0] == nome:
            usuario_nao_cadastrado = False
            break

    if usuario_nao_cadastrado:
        arquivo_usuarios.write(nome + ',' + telefone + ',' + endereco + ',' + email + ',' + senha + '\n')

    arquivo_usuarios.close()
    s_arquivo_usuarios.release()

    return usuario_nao_cadastrado


def apaga_usuario(nome,senha):
    #todo verificar se usuario esta logado (lista de usuarios logados)

    #verifica no arquivo se o nome e senha sao compativeis, se sim, apaga informacoes do usuario
    global s_arquivo_usuarios

    s_arquivo_usuarios.acquire()
    arquivo_usuarios = open('registro/usuarios.txt', 'r')

    linha_para_remover = None
    for linha in arquivo_usuarios:
        usuario = linha.split(',')
        if usuario[0] == nome and usuario[4].replace('\n','') == senha:
            linha_para_remover = linha
            break

    arquivo_usuarios.close()

    if linha_para_remover is None:
        print 'Usuario e senha imcompativeis'
    else:
        arquivo_usuarios = open('registro/usuarios.txt', 'r+')

        linhas = arquivo_usuarios.readlines()
        arquivo_usuarios.seek(0)
        arquivo_usuarios.truncate()
        for linha in linhas:
            if linha != linha_para_remover:
                arquivo_usuarios.write(linha)

        arquivo_usuarios.close()

    s_arquivo_usuarios.release()

def faz_login(nome,senha):

    global s_arquivo_usuarios

    #verificar se o usuario e senha estao no arquivo e se sao compativeis
    s_arquivo_usuarios.acquire()
    arquivo_usuarios = open('registro/usuarios.txt', 'r')

    usuario_cadastrado = False
    for linha in arquivo_usuarios:
        usuario = linha.split(',')
        if usuario[0] == nome and usuario[4].replace('\n', '') == senha:
            usuario_cadastrado = True
            break

    arquivo_usuarios.close()
    s_arquivo_usuarios.release()

    if usuario_cadastrado:
        #todo inserir na lista de logados e retornar ok
        stub = None
    else:
        #todo retornar not_ok
        stub = None


def sair():
    #todo deslogar usuario
    stub = None

###Soluca da internet para ver todas as informacoes sobre o erro dentro do except:
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

HOST = '192.168.0.105'  # Symbolic name meaning all available interfaces
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4,tipo de socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))  # liga o socket com IP e porta

s_arquivo_usuarios = BoundedSemaphore()
s_arquivo_leiloes = BoundedSemaphore()

while 1:
    s.listen(1) #espera chegar pacotes na porta especificada
    conn, addr = s.accept()#Aceita uma conexão
    print 'Aceitou uma conexão de ', addr
    #todo criar thread para aceitar conexao
    #t = Thread(target=aceita, args=(conn,))
    #t.start()


