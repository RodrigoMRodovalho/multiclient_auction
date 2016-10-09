import socket
import sys
import linecache
from threading import Thread, BoundedSemaphore

PORT = 50053              # Arbitrary non-privileged port


def lanca_produto(nome,descricao,lance_minimo,dia,mes,ano,hora,minuto,segundo,tempo_maximo):
    #todo verificar se usuario esta logado
    #todo gerar identificador unico para leilao

def enviar_lance(identificador_leilao,valor):
    #todo para o usuario que deu o lance retornar ok ou not_ok, para os outros, retornar
    #todo Identificador do leilão, nome do usuário, valor, número de usuários no leilão no
    #todo momento, número de lances que já foram dados.

def contato_vendedor():
    #todo envia para o vendedor as informações do comprador
    #todo Identificador do leilão, valor de venda, nome, endereço, telefone, e - mail

def contato_comprador():
    # todo envia para o comprador as informações do vendedor
    # todo Identificador do leilão, valor de venda, nome, endereço, telefone, e - mail


def lista_leiloes():
    #Nao precisa ser cadastrado, nem estar logado
    #todo obter informacoes dos leiloes (nao mostra leiloes que ja terminaram)
    #todo um produto por linha:
        # (identificador do leilão)
        # nome do produto
        # descrição
        # lance mínimo
        #  dia, mês, ano e hora, minuto de início do leilão
        # tempo máximo sem lances para o produto
        # dono do produto


def entrar_leilao(identificador_leilao):
    #todo verificar se usuario esta logado e cadastrado
    #todo inserir usuario no leilao

def sair_leilao(identificador_leilao):
    #todo verificar se usuario esta logado e cadastrado
    #todo remover usuario do leilao

def fim_leilao():
    #todo enviar para todos que participam do leilao
    #Identificador do leilão, valor de venda, usuário que comprou

def adiciona_usuario(nome,telefone,endereco,email,senha):
    #todo verificar no arquivo se já existe algum usuário com o nome passado como parâmetro
    #todo inserir informaoes de usuario no arquivo

def apaga_usuario(nome,senha):
    #todo verificar se usuario esta logado (lista de usuarios logados)
    #todo verificar no arquivo se o nome e senha são compativeis, se sim, apagar informacoes do usuario

def faz_login(nome,senha):
    #todo verificar se o usuario e senha estão no arquivo e se são compatíveis

def sair():
    #todo deslogar usuario

###Solução da internet para ver todas as informações sobre o erro dentro do except:
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

while 1:
    s.listen(1) #espera chegar pacotes na porta especificada
    conn, addr = s.accept()#Aceita uma conexão
    print 'Aceitou uma conexão de ', addr
    #todo criar thread para aceitar conexao
    #t = Thread(target=aceita, args=(conn,))
    #t.start()


