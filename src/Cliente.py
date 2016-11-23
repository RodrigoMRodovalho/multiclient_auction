import socket
import sys
import linecache
from threading import Thread, BoundedSemaphore
from datetime import datetime
import time

OP_ADICIONA_USUARIO = 1


def lanca_produto(nome,descricao,lance_minimo,dia,mes,ano,hora,minuto,segundo,tempo_maximo):

    global resposta, s_resposta

    s_resposta.acquire()
    resposta = None
    s_resposta.release()

    envia_mensagem_servidor(
        'Lanca_produto,' + nome + ',' + descricao + ',' + lance_minimo + ',' + dia
        + ',' +mes + ',' + ano + ',' + hora + ',' + minuto + ',' + segundo + ',' +tempo_maximo)


def adiciona_usuario(nome,telefone,endereco,email,senha):

    global resposta,s_resposta

    s_resposta.acquire()
    resposta = None
    s_resposta.release()

    resp = 'Adiciona_usuario,'+nome+','+telefone+','+endereco+','+email+','+senha
    envia_mensagem_servidor(resp)

def faz_login(nome,senha):

    global resposta,s_resposta

    s_resposta.acquire()
    resposta = None
    s_resposta.release()

    envia_mensagem_servidor('Faz_login,'+nome+','+senha)


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

def escuta_servidor():

    global s_resposta,resposta

    while True:
        data = servidor_sock.recv(4096)
        log_mensagem_recebida(data)

        if 'Enviar_lance' not in data:
            s_resposta.acquire()
            resposta = data
            s_resposta.release()
        else:
            #todo
            stub = None




#Variaveis para guarda informacoes do servidor
host_ip=''
porta=''
# Declaracao do socket de conexao com servidor
servidor_sock = None
servidor_conectado = False
s_servidor_contectado = BoundedSemaphore()
s_usuario_logado = BoundedSemaphore()
usuario_logado = False
nome_usuario = ''
operacao_atual = None
s_operacao_atual = BoundedSemaphore()
resposta = None
s_resposta = BoundedSemaphore()

try:
    #host_ip = raw_input("Digite o IP do servidor...\n")
    #porta = raw_input("Digite a porta do servidor...\n")
    host_ip = '192.168.0.105'
    porta = 50053


    estabelece_conexao_servidor(host_ip, porta)

    s_servidor_contectado.acquire()
    if servidor_conectado:
        t = Thread(target=escuta_servidor)
        t.start()
    else:
        print 'Nao foi possivel conectar ao servidor \n'
    s_servidor_contectado.release()

    while True:
        s_usuario_logado.acquire()
        if usuario_logado:
            print 'Login :', nome_usuario, '\n'
        else:
            print 'Login : Deslogado\n'
        s_usuario_logado.release()

        print 'Leilao da UFF\n'
        print '1 - Cadastrar usuario'
        print '2 - Logar/Deslogar usuario'
        print '3 - Cadastrar produto'
        print '4 - Listar produtos'
        print '5 - Participar de um leilao'
        print '6 - Sair de um leilao'
        print '7 - Dar um lance'
        print '8 - Sair\n'

        opcao = raw_input("Digite sua opcao\n")

        if opcao == '1':
            nome = raw_input("Digite o nome\n")
            telefone = raw_input("Digite o telefone\n")
            endereco = raw_input("Digite o endereco\n")
            email = raw_input("Digite o email\n")
            senha = raw_input("Digite a senha\n")

            adiciona_usuario(nome,telefone,endereco,email,senha)

            while True:
                s_resposta.acquire()

                if resposta is not None:

                    if resposta == 'Ok':
                        print 'Cadastro efetuado com sucesso\n'
                    else:
                        print 'Nao foi possivel realizar o cadastro\n'

                    raw_input("Aperte enter para continuar\n")
                    resposta = None
                    s_resposta.release()
                    break
                s_resposta.release()
                time.sleep(0.3)

        elif opcao == '2':

            s_usuario_logado.acquire()

            if usuario_logado:
                envia_mensagem_servidor('Sair')
            else:
                nome = raw_input("Digite o nome\n")
                senha = raw_input("Digite a senha\n")

                faz_login(nome, senha)

                while True:
                    s_resposta.acquire()

                    if resposta is not None:

                        if resposta == 'Ok':
                            print 'Login efetuado com sucesso - Bem vindo Sr(a) ',nome,'\n'
                            usuario_logado = True
                            nome_usuario = nome

                        else:
                            print 'Nao foi possivel realizar o login\n'

                        raw_input("Aperte enter para continuar\n")
                        resposta = None
                        s_resposta.release()
                        break
                    s_resposta.release()
                    time.sleep(0.3)

            s_usuario_logado.release()

        elif opcao == '3':

            s_usuario_logado.acquire()

            if usuario_logado:
                nome = raw_input("Digite o nome\n")
                descricao = raw_input("Digite a descricao\n")
                lance_minimo = raw_input("Digite o lance minimo\n")
                dia = raw_input("Digite o dia de inicio do leilao\n")
                mes = raw_input("Digite o mes de inicio do leilao\n")
                ano = raw_input("Digite o ano de inicio do leilao\n")
                hora = raw_input("Digite a hora de inicio do leilao\n")
                minuto = raw_input("Digite o minuto de inicio do leilao\n")
                segundo = raw_input("Digite o segundo de inicio do leilao\n")
                tempo_maximo = raw_input("Digite o tempo maximo do leilao\n")

                lanca_produto(nome,descricao,lance_minimo,dia,mes,ano,hora,minuto,segundo,tempo_maximo)

                while True:
                    s_resposta.acquire()

                    if resposta is not None:

                        if resposta == 'Ok':
                            print 'Produto cadastrado com sucesso\n'
                        else:
                            print 'Nao foi possivel realizar o cadastro do produto ',nome,'\n'

                        raw_input("Aperte enter para continuar\n")
                        resposta = None
                        s_resposta.release()
                        break
                    s_resposta.release()
                    time.sleep(0.3)

            else:
                print 'Operacao somente permitida para usuarios logados'
                raw_input("Aperte enter para continuar\n")

            s_usuario_logado.release()

        print("\033c")


#Caso de um erro, mostra mensagem
except:
    PrintException()
#Por final, desconecta serviddor
finally:
    desconecta_servidor()
