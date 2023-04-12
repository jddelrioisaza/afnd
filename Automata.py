class Automata():

    def __init__(self, estados, transiciones, estado_inicial, estados_finales, pos):

        self.__estados = estados
        self.__transiciones = transiciones
        self.__estado_inicial = estado_inicial
        self.__estados_finales = estados_finales
        self.__pos = pos

    def getEstados(self):

        return self.__estados

    def getTransiciones(self):

        return self.__transiciones

    def getEstadoInicial(self):

        return self.__estado_inicial

    def getEstadosFinales(self):

        return self.__estados_finales

    def getPos(self):

        return self.__pos
