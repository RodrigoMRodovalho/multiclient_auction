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
