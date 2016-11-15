import socket
import sys
import linecache
from threading import Thread, BoundedSemaphore
from datetime import datetime

def lanca_produto(nome,descricao,lance_minimo,dia,mes,ano,hora,minuto,segundo,tempo_maximo):
    #todo verificar se usuario esta logado
    #todo gerar identificador unico para leilao
    stub = None

###Solucao da internet para ver todas as informacoes sobre o erro dentro do except:
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

#Funcao que envia mensagem para o servidor
def envia_mensagem_servidor(mensagem):
    print >> sys.stderr, 'enviando ',mensagem,'  as ',datetime.now().time()
    servidor_sock.sendall(mensagem)

#Imprime as mensagens recebidas
def log_mensagem_recebida(mensagem):
    print >> sys.stderr, 'recebido ', mensagem, '  at ', datetime.now().time()

#Funcao que guarda nas variaveis o IP e Porta do servidor
def configura_servidor(host,port):
    global host_ip,porta
    host_ip = host
    porta = port

#Funcao que conecta socket do servidor
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
        PrintException()
        return False

#Funcao que desconecta socket do servidor
def desconecta_servidor():
    servidor_sock.close()

# Funcao que realiza comunicacao com servidor
def estabelece_conexao_servidor(host_ip,porta):
    global s_servidor_contectado,servidor_conectado,mensagem_erro

    #Configura IP e Porta do Servidor
    configura_servidor(host_ip,porta)
    #Verifica se conecta com o servidor
    if (conecta_servidor()):
        mensagem_erro = None
    else:
        mensagem_erro = 'Nao foi possivel conectar ao servidor'

    #Libera a variavel que controla se conectou o servidor ou se deu erro
    s_servidor_contectado.acquire()
    servidor_conectado = True
    s_servidor_contectado.release()


#Variaveis para guarda informacoes do servidor
host_ip=''
porta=''
# Declaracao do socket de conexao com servidor
servidor_sock = None
servidor_conectado = False
s_servidor_contectado = BoundedSemaphore()
s_usuario_logado = BoundedSemaphore()
usuario_logado = False

try:
    #host_ip = raw_input("Digite o IP do servidor...\n")
    #porta = raw_input("Digite a porta do servidor...\n")
    host_ip = '192.168.0.101'
    porta = 50053


    estabelece_conexao_servidor(host_ip, porta)

    while True:
        msg = raw_input("Digite a mensagem")
        envia_mensagem_servidor(msg)

#Caso de um erro, mostra mensagem
except:
    PrintException()
#Por final, desconecta serviddor
finally:
    desconecta_servidor()
