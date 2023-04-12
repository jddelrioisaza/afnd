from Automata import Automata
from AutomataGUI import AutomataGUI

from PySide6.QtWidgets import QApplication

import sys

def iniciar():

    automata = crearAutomata()

    # CREAR APLICACIÓN DE QT
    aplicacion = QApplication(sys.argv)

    # CREAR VENTANA PRINCIPAL
    ventana = AutomataGUI(automata)
    ventana.show()

    # EJECUTAR APLICACIÓN DE QT
    sys.exit(aplicacion.exec())


def crearAutomata():

    # PARÁMETROS REQUERIDOS PARA LA CREACIÓN DEL AUTOMATA
    # TODOS VIENEN YA PREDEFINIDOS
    estados = {'A', 'B', 'C', 'D', 'E', 'F'}
    transiciones = {
        ('A', 'a'): 'B',
        ('A', 'b'): 'C',
        ('B', 'a'): 'D',
        ('C', 'a'): 'E',
        ('C', 'b'): 'F',
        ('D', 'a'): 'E',
        ('D', 'b'): 'F',
        ('E', 'a'): 'F'
    }
    estado_inicial = 'A'
    estados_finales = {'F'}
    # POSICIÓN DE LOS NODOS (COLOCADOS ARBITRARIAMENTE)
    pos = {

        'A': (0, 0),
        'B': (1, 1),
        'C': (1, -1),
        'D': (2, 2),
        'E': (1, 0),
        'F': (2, -2)

        }

    automata = Automata(estados, transiciones, estado_inicial, estados_finales, pos)
    return automata

iniciar()
