import socket
import sys
import linecache
from threading import Thread, BoundedSemaphore
from datetime import datetime


PORT = 50053              # Arbitrary non-privileged port

class Leilao:

    def __init__(self,id,vendedor,nome,descricao,lance_minimo,dia,mes,ano,hora,minuto,segundo,tempo_maximo):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.lance_minimo = lance_minimo
        self.dia = dia
        self.mes = mes
        self.ano = ano
        self.hora = hora
        self.minuto = minuto
        self.segundo = segundo
        self.tempo_maximo = tempo_maximo
        self.vendedor = vendedor
        self.comprador = None
        self.lance_final = None
        self.dia_final = None
        self.mes_final = None
        self.ano_final = None
        self.hora_final = None
        self.minuto_final = None
        self.segundo_final = None


    def finaliza(self,comprador,lance_final,dia_final,mes_final,ano_final,hora_final,minuto_final,segundo_final):
        self.comprador = comprador
        self.lance_final = lance_final
        self.dia_final = dia_final
        self.mes_final = mes_final
        self.ano_final = ano_final
        self.hora_final = hora_final
        self.minuto_final = minuto_final
        self.segundo_final = segundo_final

class Usuario:

    def __init__(self,nome,telefone,endereco,email,senha,logado,conn):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.email = email
        self.senha = senha
        self.logado = logado
        self.conn = conn

    def atualiza_login(self,logado):
        self.logado = logado

def salva_leilao_arquivo(leilao):
    global s_arquivo_leiloes

    s_arquivo_leiloes.acquire()

    arquivo_leiloes = open('registro/leiloes.txt', 'r+')

    #todo colocar o dono, quem comrprou, e quando comprou
    arquivo_leiloes.write(
        leilao.controle_identificador_leilao + ',' +
        leilao.nome + ',' +
        leilao.descricao + ',' +
        leilao.lance_minimo + ',' +
        leilao.dia + ',' +
        leilao.mes + ',' +
        leilao.ano + ',' +
        leilao.hora + ',' +
        leilao.minuto + ',' +
        leilao.segundo + ',' +
        leilao.tempo_maximo + '\n')

    arquivo_leiloes.close()

    controle_identificador_leilao += 1
    s_arquivo_leiloes.release()

def cadastra_produto(usuario_dono,nome,descricao,lance_minimo,dia,mes,ano,hora,minuto,segundo,tempo_maximo):
    #todo verificar se usuario esta logado (client side)

    global controle_identificador_leilao,s_controle_identificador_leilao,leiloes,s_leiloes

    try:
        s_controle_identificador_leilao.acquire()
        s_leiloes.acquire()
        # Leilao, {usuario_no_leilao}
        leilao = Leilao(
            controle_identificador_leilao,
            usuario_dono,
            nome,
            descricao,
            lance_minimo,
            dia,mes,ano,hora,minuto,segundo,tempo_maximo)

        leiloes[controle_identificador_leilao] = [leilao,{}]

        s_leiloes.release()
        s_controle_identificador_leilao.release()

        return True

    except:
        PrintException()
        return False

def recebe_lance(identificador_leilao,valor):
    #todo para o usuario que deu o lance retornar ok ou not_ok, para os outros, retornar
    #todo Identificador do leilao, nome do usuario, valor, numero de usuarios no leilao no
    #todo momento, numero de lances que ja foram dados.
    #todo verificar se o lance dado e maior que o lance minimo
    #todo verificar se o lance dado e maior que os lances dados anteriormente

    global s_leiloes, leiloes

    s_leiloes.acquire()

    if valor > leiloes[identificador_leilao][0].lance_minimo:


    s_leiloes.release

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

    global s_leiloes,leiloes

    s_leiloes.acquire()

    descricao = ''

    if leiloes.count > 0:
        for leilao in leiloes:
            descricao += leilao.id + ',' + \
                         leilao.nome + ',' + leilao.descricao + ',' + \
                         leilao.lance_minimo + ',' + leilao.dia + ',' + \
                         leilao.mes + ',' + leilao.ano + ',' + leilao.hora + ',' + \
                         leilao.minuto + ',' + leilao.tempo_maximo + ',' + leilao.vendedor.nome + '\n'
    else:
        descricao = 'Nenhum leilao acontecendo'

    s_leiloes.release()

    return descricao

def entrar_leilao(identificador_leilao,conn):
    #todo verificar se usuario esta logado e cadastrado
    #todo inserir usuario no leilao
    global s_leiloes,leiloes,s_usuarios,usuarios

    s_leiloes.acquire()

    resultado = False
    if leiloes[identificador_leilao] is not None:

        s_usuarios.acquire()
        leiloes[identificador_leilao][1].append(usuarios[conn][0])
        s_usuarios.release()

        resultado = True

    s_leiloes.release()

    return resultado

def sair_leilao(identificador_leilao,conn):
    #todo verificar se usuario esta logado e cadastrado
    #todo remover usuario do leilao
    global s_leiloes, leiloes, s_usuarios, usuarios

    s_leiloes.acquire()

    resultado = False
    if leiloes[identificador_leilao] is not None:
        s_usuarios.acquire()
        leiloes[identificador_leilao][1].remove(usuarios[conn][0])
        s_usuarios.release()
        resultado = True

    s_leiloes.release()

    return resultado

def fim_leilao():
    #todo enviar para todos que participam do leilao
    #Identificador do leilao, valor de venda, usuario que comprou
    stub = None

def adiciona_usuario(nome,telefone,endereco,email,senha):

    # verifica no arquivo se ja existe algum usuario com o nome passado como parametro
    # insere informaoes de usuario no arquivo
    global s_arquivo_usuarios

    try:
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
    except:
        PrintException()
        return False

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

    resultado = False

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

        resultado = True

    s_arquivo_usuarios.release()

    return resultado

def faz_login(nome,senha,conn):

    global s_arquivo_usuarios,s_usuarios,usuarios

    #verificar se o usuario e senha estao no arquivo e se sao compativeis
    s_arquivo_usuarios.acquire()
    arquivo_usuarios = open('registro/usuarios.txt', 'r')

    usuario_cadastrado = False
    usuario_logado = None
    for linha in arquivo_usuarios:
        usuario = linha.split(',')
        if usuario[0] == nome and usuario[4].replace('\n', '') == senha:
            usuario_cadastrado = True
            usuario_logado = Usuario(conn,usuario[0],usuario[1],usuario[2],usuario[3],usuario[4],True)
            break

    arquivo_usuarios.close()
    s_arquivo_usuarios.release()

    if usuario_cadastrado:

        s_usuarios.acquire()

        usuarios[conn][0] = usuario_logado
        s_usuarios.release()

        return True
    else:
        return False

def processa_pedido(mensagem,conn):

    if 'Lanca_produto' in mensagem:
        mensagem = mensagem.split(',')
        resultado = cadastra_produto(
            usuarios[conn][0],
            mensagem[1],mensagem[2],mensagem[3],mensagem[4],mensagem[5],mensagem[6],
            mensagem[7],mensagem[8],mensagem[9],mensagem[10]
        )

        if resultado:
            envia_mensagem_cliente(conn, 'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

    if 'Lista_leiloes' == mensagem:
        envia_mensagem_cliente(conn,'Listagem,'+lista_leiloes())

    if 'Adiciona_usuario' in mensagem:
        mensagem = mensagem.split(',')
        #Pega os valores da mensagem e chama a funcao para adicionar o usuario
        # retorna True se conseguir adicionar
        resultado = adiciona_usuario(mensagem[1],mensagem[2],mensagem[3],mensagem[4],mensagem[5])

        if resultado:
            envia_mensagem_cliente(conn,'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

    if 'Apaga_usuario' in mensagem:
        mensagem = mensagem.split(',')

        resultado = apaga_usuario(mensagem[1],mensagem[2])

        if resultado:
            envia_mensagem_cliente(conn,'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

    if 'Faz_login' in mensagem:
        mensagem = mensagem.split(',')
        resultado = faz_login(mensagem[1],mensagem[2],conn)

        if resultado:
            envia_mensagem_cliente(conn,'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

    if 'Sair' == mensagem:
        s_usuarios.acquire()
        usuarios[conn][0] = None
        s_usuarios.release()

        envia_mensagem_cliente(conn,'Ok')

    if 'Entrar_leilao' in mensagem:
        mensagem = mensagem.split(',')

        resultado = entrar_leilao(mensagem[1],conn)

        if resultado:
            envia_mensagem_cliente(conn, 'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

    if 'Sair_leilao' in mensagem:
        mensagem = mensagem.split(',')

        sair_leilao(mensagem[1],conn)

        if resultado:
            envia_mensagem_cliente(conn, 'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

    if 'Enviar_lance' in mensagem:
        mensagem = mensagem.split(',')


def aceita(conn):

    global usuarios, s_usuarios

    s_usuarios.acquire()
    usuarios[conn] = [None,conn]
    s_usuarios.release()

    while True:
        msg = conn.recv(4096)
        print addr, ' >> ', msg
        #conn.send(msg)
        processa_pedido(msg,conn)
    conn.close()

def envia_mensagem_cliente(conn,mensagem):
    print >> sys.stderr, 'enviando ',mensagem,'  as ',datetime.now().time()
    conn.sendall(mensagem)

###Soluca da internet para ver todas as informacoes sobre o erro dentro do except:
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

HOST = '192.168.0.101'  # Symbolic name meaning all available interfaces
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4,tipo de socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))  # liga o socket com IP e porta

s_arquivo_usuarios = BoundedSemaphore()
s_arquivo_leiloes = BoundedSemaphore()

controle_identificador_leilao = 0
s_controle_identificador_leilao = BoundedSemaphore()

#{usario,conn}
usuarios = {}
s_usuarios = BoundedSemaphore()

#Leilao, {usuario_no_leilao}
leiloes = {}
s_leiloes = BoundedSemaphore()

print 'Rodando Servidor'



while 1:
    s.listen(1) #espera chegar pacotes na porta especificada
    conn, addr = s.accept()#Aceita uma conexao
    print 'Aceitou uma conexao de ', addr
    #todo criar thread para aceitar conexao
    t = Thread(target=aceita, args=(conn,))
    t.start()


