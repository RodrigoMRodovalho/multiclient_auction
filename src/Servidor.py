import socket
import sys
import linecache
from threading import Thread, BoundedSemaphore
from datetime import datetime, timedelta

import time

PORT = 50053  # Arbitrary non-privileged port

#Classe que corresponde aos leiloes
class Leilao:

    #funcao de inicializacao das informacoes do leilao
    def __init__(self, id, vendedor, nome, descricao, lance_minimo, dia, mes, ano, hora, minuto, segundo, tempo_maximo):
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
        self.dia_final = None
        self.mes_final = None
        self.ano_final = None
        self.hora_final = None
        self.minuto_final = None
        self.segundo_final = None
        self.lance_atual = -1
        self.numero_lances = 0
        self.data_inicial = datetime.strptime(ano + mes + dia + hora + minuto + segundo, '%Y%m%d%H%M%S')
        self.tempo_termina_leilao = None
        self.data_venda = None

    #funcao de atualizacao das informacoes do leilao
    def atualiza_lance_atual(self, lance_atual,comprador):
        self.lance_atual = lance_atual
        self.numero_lances += 1
        ts = datetime.now() + timedelta(seconds=int(self.tempo_maximo))
        self.tempo_termina_leilao = datetime.strptime(ts.strftime('%Y%m%d%H%M%S'), '%Y%m%d%H%M%S')
        self.comprador = comprador
        self.data_venda = datetime.now()

#Classe que corresponde aos usuarios
class Usuario:

    #funcao de inicializacao das informacoes de usuario
    def __init__(self, nome, telefone, endereco, email, senha, logado, conn):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.email = email
        self.senha = senha
        self.logado = logado
        self.conn = conn


#Funcao para salvar o historico de leiloes
def salva_leilao_arquivo(leilao):
    global s_arquivo_leiloes

    s_arquivo_leiloes.acquire()

    #abertura do arquivo
    arquivo_leiloes = open('leiloes.txt', 'r+')

    #escrita no arquivo
    arquivo_leiloes.write(
        str(leilao.id) + ',' +
        str(leilao.nome) + ',' +
        str(leilao.descricao) + ',' +
        str(leilao.lance_atual) + ',' +
        str(leilao.data_venda) + '\n')

    arquivo_leiloes.close()
    s_arquivo_leiloes.release()

#funcao que cadastra produtos (leilao)
def cadastra_produto(usuario_dono, nome, descricao, lance_minimo, dia, mes, ano, hora, minuto, segundo, tempo_maximo):
    global controle_identificador_leilao, s_controle_identificador_leilao, leiloes, s_leiloes,s_numero_leiloes_ativos,numero_leiloes_ativos

    try:
        s_controle_identificador_leilao.acquire()
        s_leiloes.acquire()
        # Leilao, {usuario_no_leilao}

        #cria um novo leilao com as informacoes do produto
        leilao = Leilao(
            controle_identificador_leilao,
            usuario_dono,
            nome,
            descricao,
            lance_minimo,
            dia, mes, ano, hora, minuto, segundo, tempo_maximo)

        #coloca o novo leilao na lista de leiloes
        leiloes[controle_identificador_leilao] = [leilao, []]
        controle_identificador_leilao += 1
        s_leiloes.release()
        s_controle_identificador_leilao.release()

        #incrementa o identificador para ser usado na criacao do proximo leilao
        s_numero_leiloes_ativos.acquire()
        numero_leiloes_ativos += 1
        s_numero_leiloes_ativos.release()

        return True

    except:
        PrintException()
        return False

#funcao que processa a recepcao dos lances
def recebe_lance(identificador_leilao, valor, conn):
    # para o usuario que deu o lance retornar ok ou not_ok, para os outros, retornar
    # Identificador do leilao, nome do usuario, valor, numero de usuarios no leilao no
    # momento, numero de lances que ja foram dados.

    global s_leiloes, leiloes, usuarios, s_usuarios

    s_leiloes.acquire()
    resultado = False
    #verifica se o leilao existe na lista de leiloes
    if leiloes[identificador_leilao] is not None:
        s_usuarios.acquire()
        #verifica se o usuario que deu o lance esta participando do leilao solicitado
        if usuarios[conn][0] in leiloes[int(identificador_leilao)][1]:
            #verifica se o lance dado e maior que o lance minimo
            if valor > int(leiloes[identificador_leilao][0].lance_minimo):
                #verifica se o lance dado e maior que o valor do lance atual
                if valor > int(leiloes[identificador_leilao][0].lance_atual):
                    #atualiza o valor do lance atual e o usuario que deu o lance atual do leilao na lista de leiloes
                    leiloes[identificador_leilao][0].atualiza_lance_atual(valor,usuarios[conn][0])

                    #cria as informacoes do lance
                    lance = str(identificador_leilao) + ',' + \
                            usuarios[conn][0].nome + ',' + \
                            str(valor) + ',' + \
                            str(len(leiloes[identificador_leilao][1])) + ',' + \
                            str(leiloes[identificador_leilao][0].numero_lances)

                    #envia para todos os usuarios participantes do leilao as informacoes do lance dado
                    for usuario_leilao in leiloes[identificador_leilao][1]:
                        envia_mensagem_cliente(usuario_leilao.conn, 'Lance,' + lance)

                    resultado = True

        s_usuarios.release()
    s_leiloes.release()

    return resultado

#funcao que retorna a descricao dos leiloes ativos
def lista_leiloes():
    # Nao precisa ser cadastrado, nem estar logado
    # (identificador do leilao)
    # nome do produto
    # descricao
    # lance minimo
    #  dia, mes, ano e hora, minuto de inicio do leilao
    # tempo maximo sem lances para o produto
    # dono do produto

    global s_leiloes, leiloes

    s_leiloes.acquire()

    descricao = ''

    #verifica se existe algum leilao ativo
    if len(leiloes) > 0:
        #cria a descricao contendo as informacoes de todos os leiloes
        for leilao in leiloes:
            descricao += str(leiloes[leilao][0].id) + ',' + \
                         str(leiloes[leilao][0].nome) + ',' + \
                         str(leiloes[leilao][0].descricao) + ',' + \
                         str(leiloes[leilao][0].lance_minimo) + ',' + \
                         str(leiloes[leilao][0].dia) + ',' + \
                         str(leiloes[leilao][0].mes) + ',' + \
                         str(leiloes[leilao][0].ano) + ',' + \
                         str(leiloes[leilao][0].hora) + ',' + \
                         str(leiloes[leilao][0].minuto) + ',' + \
                         str(leiloes[leilao][0].tempo_maximo) + ',' + \
                         str(leiloes[leilao][0].vendedor.nome) + '\n'

    s_leiloes.release()

    return descricao

#Funcao que insere usuario na lista de participantes de um leilao
def entrar_leilao(identificador_leilao, conn):
    global s_leiloes, leiloes, s_usuarios, usuarios

    s_leiloes.acquire()

    resultado = False
    try:
        #verifica se o leilao existe
        if leiloes[int(identificador_leilao)] is not None:

            diferenca = datetime.now() - leiloes[int(identificador_leilao)][0].data_inicial

            # verifica se a entrada no leilao e de 30 min do inicio
            if diferenca.total_seconds() > 1800:
                resultado = False
            else:
                s_usuarios.acquire()

                #verifica se o usuario ja nao esta no leilao
                if usuarios[conn][0] not in leiloes[int(identificador_leilao)][1]:
                    leiloes[int(identificador_leilao)][1].append(usuarios[conn][0])
                    resultado = True

                s_usuarios.release()
    except:
        print 'Tentativa de entrar em um leilao inexistente'

    s_leiloes.release()

    return resultado

#funcao que remove usuario da lista de partipantes de um leilao
def sair_leilao(identificador_leilao, conn):
    global s_leiloes, leiloes, s_usuarios, usuarios

    s_leiloes.acquire()

    resultado = False
    #verifica se o leilao existe
    if leiloes[int(identificador_leilao)] is not None:
        s_usuarios.acquire()
        #verifica se o usuario esta participando do leilao
        if usuarios[conn][0] in leiloes[int(identificador_leilao)][1]:
            #remove usuario do leilao
            leiloes[int(identificador_leilao)][1].remove(usuarios[conn][0])
            resultado = True

        s_usuarios.release()

    s_leiloes.release()

    return resultado

#funcao que adiciona usuario no sistema
def adiciona_usuario(nome, telefone, endereco, email, senha):
    # verifica no arquivo se ja existe algum usuario com o nome passado como parametro
    # insere informaoes de usuario no arquivo
    global s_arquivo_usuarios

    try:
        s_arquivo_usuarios.acquire()
        #abertura de arquivo em modo leitura e escrita
        arquivo_usuarios = open('usuarios.txt', 'r+')
        usuario_nao_cadastrado = True
        #verifica se o usuario ja esta cadastrado
        for linha in arquivo_usuarios:
            usuario = linha.split(',')
            if usuario[0] == nome:
                usuario_nao_cadastrado = False
                break

        #caso o usuario nao esteja cadastrado entao escreve no arquivo
        if usuario_nao_cadastrado:
            arquivo_usuarios.write(nome + ',' + telefone + ',' + endereco + ',' + email + ',' + senha + '\n')

        arquivo_usuarios.close()
        s_arquivo_usuarios.release()

        return usuario_nao_cadastrado
    except:
        PrintException()
        return False

#Funcao que apaga usuario do sistema
def apaga_usuario(nome, senha):

    # verifica no arquivo se o nome e senha sao compativeis, se sim, apaga informacoes do usuario
    global s_arquivo_usuarios

    s_arquivo_usuarios.acquire()
    #abre o arquivo de usuarios no modo leitura
    arquivo_usuarios = open('usuarios.txt', 'r')

    linha_para_remover = None
    for linha in arquivo_usuarios:
        usuario = linha.split(',')
        if usuario[0] == nome and usuario[4].replace('\n', '') == senha:
            linha_para_remover = linha
            break

    arquivo_usuarios.close()

    resultado = False

    if linha_para_remover is None:
        print 'Usuario e senha imcompativeis'
    else:
        arquivo_usuarios = open('usuarios.txt', 'r+')

        #faz a leitura das linhas do arquivo
        linhas = arquivo_usuarios.readlines()
        #bota o cursor do arquivo na primeira posicao
        arquivo_usuarios.seek(0)
        arquivo_usuarios.truncate()
        for linha in linhas:
            if linha != linha_para_remover:
                arquivo_usuarios.write(linha)

        arquivo_usuarios.close()

        resultado = True

    s_arquivo_usuarios.release()

    return resultado

#Funcao que faz login de usuario
def faz_login(nome, senha, conn):
    global s_arquivo_usuarios, s_usuarios, usuarios

    # verificar se o usuario e senha estao no arquivo e se sao compativeis
    s_arquivo_usuarios.acquire()
    arquivo_usuarios = open('usuarios.txt', 'r')

    usuario_cadastrado = False
    usuario_logado = None
    #percorre o arquivo e verifica se o usuario existe
    for linha in arquivo_usuarios:
        usuario = linha.split(',')
        if usuario[0] == nome and usuario[4].replace('\n', '') == senha:
            usuario_cadastrado = True
            #faz login de um usuario com as informacoes lidas do arquivo
            usuario_logado = Usuario(usuario[0], usuario[1], usuario[2], usuario[3], usuario[4], True, conn)
            break

    arquivo_usuarios.close()
    s_arquivo_usuarios.release()

    #verifica se o usuario e cadastrado e coloca ele na lista de usuarios
    if usuario_cadastrado:
        s_usuarios.acquire()
        usuarios[conn][0] = usuario_logado
        s_usuarios.release()

        return True
    else:
        return False

#Funcao que recebe mensagens dos clientes e processa
def processa_pedido(mensagem, conn):
    if 'Lanca_produto' in mensagem:
        mensagem = mensagem.split(',')
        resultado = cadastra_produto(
            usuarios[conn][0],
            mensagem[1], mensagem[2], mensagem[3], mensagem[4], mensagem[5], mensagem[6],
            mensagem[7], mensagem[8], mensagem[9], mensagem[10]
        )

        if resultado:
            envia_mensagem_cliente(conn, 'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

    if 'Lista_leiloes' == mensagem:
        envia_mensagem_cliente(conn, 'Listagem,' + lista_leiloes())

    if 'Adiciona_usuario' in mensagem:
        mensagem = mensagem.split(',')
        # Pega os valores da mensagem e chama a funcao para adicionar o usuario
        # retorna True se conseguir adicionar
        resultado = adiciona_usuario(mensagem[1], mensagem[2], mensagem[3], mensagem[4], mensagem[5])

        if resultado:
            envia_mensagem_cliente(conn, 'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

    if 'Apaga_usuario' in mensagem:
        mensagem = mensagem.split(',')

        resultado = apaga_usuario(mensagem[1], mensagem[2])

        if resultado:
            envia_mensagem_cliente(conn, 'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

    if 'Faz_login' in mensagem:
        mensagem = mensagem.split(',')
        resultado = faz_login(mensagem[1], mensagem[2], conn)

        if resultado:
            envia_mensagem_cliente(conn, 'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

    if 'Sair' == mensagem:
        #remove usuario da lista de usuarios
        s_usuarios.acquire()
        del usuarios[conn]
        s_usuarios.release()

        envia_mensagem_cliente(conn, 'Ok')

    if 'Entrar_leilao' in mensagem:
        mensagem = mensagem.split(',')

        resultado = entrar_leilao(mensagem[1], conn)

        if resultado:
            envia_mensagem_cliente(conn, 'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

    if 'Sair_leilao' in mensagem:
        mensagem = mensagem.split(',')

        resultado = sair_leilao(mensagem[1], conn)

        if resultado:
            envia_mensagem_cliente(conn, 'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

    if 'Enviar_lance' in mensagem:
        mensagem = mensagem.split(',')

        resultado = recebe_lance(int(mensagem[1]), int(mensagem[2]), conn)

        if resultado:
            envia_mensagem_cliente(conn, 'Ok')
        else:
            envia_mensagem_cliente(conn, 'not_ok')

#Thread que aceita as conexoes dos clientes
def aceita(conn,addr):
    global usuarios, s_usuarios

    #coloca a referencia da conexao socket na lista de usuarios
    s_usuarios.acquire()
    usuarios[conn] = [None, conn]
    s_usuarios.release()

    #recebe a mensagem vinda do cliente e repassa para funcao para processar as informacoes
    while True:
        msg = conn.recv(4096)

        if len(msg) == 0:
            break

        print addr, ' >> ', msg
        processa_pedido(msg, conn)

    #retira usuario da lista apos encerramento da conexao
    print 'conexao encerrada ', addr
    s_usuarios.acquire()
    del usuarios[conn]
    s_usuarios.release()
    conn.close()

#Thread para monitorar o tempo dos leiloes
def conta_tempo():
    global s_numero_leiloes_ativos, numero_leiloes_ativos, s_leiloes, leiloes,s_usuarios,usuarios,s_numero_leiloes_ativos,numero_leiloes_ativos

    while True:

        s_numero_leiloes_ativos.acquire()

        #verifica se existem leiloes ativos
        if numero_leiloes_ativos > 0:

            s_leiloes.acquire()

            #Para cada leilao ativo, verifica se passou o tempo entre lances do leilao
            for leilao in leiloes:

                tempo_leilao = leiloes[leilao][0].tempo_termina_leilao

                if tempo_leilao is not None:

                    diferenca = datetime.now() - tempo_leilao

                    # verifica se passou o tempo entre lances do leilao
                    if diferenca.total_seconds() > int(leiloes[leilao][0].tempo_maximo):

                        s_usuarios.acquire()

                        #Envia Fim de leilao para todos os usuarios que partipam do leilao que terminou
                        for usuario_leilao in leiloes[leilao][1]:

                            #envia final do leiao
                            envia_mensagem_cliente(usuario_leilao.conn,
                                                   'Fim_leilao,'+str(leilao) +','+
                                                   str(leiloes[leilao][0].lance_atual) +
                                                   "," + str(leiloes[leilao][0].comprador.nome))

                        #envia contato do vendedor
                        envia_mensagem_cliente(leiloes[leilao][0].comprador.conn,'Contato_vendedor,' + str(leilao) + ',' +
                                                 str(leiloes[leilao][0].lance_atual) + ',' +
                                                 str(leiloes[leilao][0].vendedor.nome) + ', ' +
                                                 str(leiloes[leilao][0].vendedor.endereco) + ', ' +
                                                 str(leiloes[leilao][0].vendedor.telefone) + ', ' +
                                                 str(leiloes[leilao][0].vendedor.email))

                        # envia contato do comprador
                        envia_mensagem_cliente(leiloes[leilao][0].vendedor.conn, 'Contato_cliente,' + str(leilao) + ',' +
                                               str(leiloes[leilao][0].lance_atual) + ',' +
                                               str(leiloes[leilao][0].comprador.nome) + ', ' +
                                               str(leiloes[leilao][0].comprador.endereco) + ', ' +
                                               str(leiloes[leilao][0].comprador.telefone) + ', ' +
                                               str(leiloes[leilao][0].comprador.email))

                        s_usuarios.release()

                        #chama funcao para salvar leilao no historico
                        salva_leilao_arquivo(leiloes[leilao][0])
                        #remove leilao da lista de leiloes
                        del leiloes[leilao]

                        #decrementa o numero de leiloes ativos
                        s_numero_leiloes_ativos.acquire()
                        numero_leiloes_ativos -= 1
                        s_numero_leiloes_ativos.release()

            s_leiloes.release()
            s_numero_leiloes_ativos.release()
        else:
            s_numero_leiloes_ativos.release()
            #espera 1 segundo
            time.sleep(1)

#Funcao para enviar mensagem para usuario
def envia_mensagem_cliente(conn, mensagem):
    print >> sys.stderr, 'enviando ', mensagem, '  as ', datetime.now().time()
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

#Configuracoes de socket do servidor
HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4,tipo de socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))  # liga o socket com IP e porta

#semaforos para acesso a arquivos de usuarios e leiloes
s_arquivo_usuarios = BoundedSemaphore()
s_arquivo_leiloes = BoundedSemaphore()

#variavel para controlar identificador do leilao, usado para criacao dos leiloes
controle_identificador_leilao = 0
s_controle_identificador_leilao = BoundedSemaphore()

# Lista de usuarios, contendo {Usario,conn}
usuarios = {}
s_usuarios = BoundedSemaphore()

# Lista de leiloes, contendo {Leilao, usuarios_no_leilao}
leiloes = {}
s_leiloes = BoundedSemaphore()

s_numero_leiloes_ativos = BoundedSemaphore()
numero_leiloes_ativos = 0

print 'Rodando Servidor'

t = Thread(target=conta_tempo, args=())
t.start()

while 1:
    s.listen(1)  # espera chegar pacotes na porta especificada
    conn, addr = s.accept()  # Aceita uma conexao
    print 'Aceitou uma conexao de ', addr
    t = Thread(target=aceita, args=(conn,addr,))
    t.start()
