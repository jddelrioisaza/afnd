import networkx as nx
import os
import gettext

from PySide6.QtCore import *
from PySide6.QtGui import QPixmap, QAction, QActionGroup
from PySide6.QtWidgets import *
from gtts import gTTS
from playsound import playsound

import matplotlib as matp
import matplotlib.pyplot as plt
import matplotlib.backends.backend_qt5agg

matp.use('Qt5Agg')

directorio_actual = os.getcwd()
localedir = os.path.join(directorio_actual, 'locale')

gettext.bindtextdomain('myapp', localedir)
gettext.textdomain('myapp')

class AutomataGUI(QMainWindow):

    def __init__(self, automata):

        plt.rcParams['toolbar'] = 'None'

        super().__init__()

        self.__automata = automata

        self.__grafo = nx.DiGraph()
        self.__grafo.add_nodes_from(self.__automata.getEstados())
        self.__grafo.add_weighted_edges_from(self.__generarAristas())

        # INICIALIZAR LAS OPCIONES DE LOS MENÚ
        self.idiomas_menu = None
        self.ingles_action = None
        self.frances_action = None
        self.espanol_action = None

        # PARA GENERAR LOS MENÚ DE LOS IDIOMAS
        self.idiomas_group = QActionGroup(self)
        self.idiomas_group.setExclusive(True)

        self.__crearInterfaz()

    def __crearInterfaz(self, idioma = 'es'):

        translations = gettext.translation('mensajes', localedir, languages=[idioma])
        translations.install()
        _ = translations.gettext

        # NOMBRE Y TAMAÑO DE LA VENTANA
        self.setWindowTitle(_("Autómata"))
        self.setGeometry(100, 100, 800, 600)

        # WIDGET PRNCIPAL
        widget = QWidget()
        self.setCentralWidget(widget)

        # ACTUALIZAR EL MENU DE IDIOMAS
        if self.idiomas_menu:
            self.__actualizarTextoIdiomasMenu()

        # BARRA DE MENU PARA CAMBIAR IDIOMA
        menu_bar = self.menuBar()

        if not self.idiomas_menu:

            self.idiomas_menu = menu_bar.addMenu(_("Idiomas"))

        if not self.ingles_action:

            self.ingles_action = QAction(_("Inglés"), self)
            self.idiomas_menu.addAction(self.ingles_action)
            self.ingles_action.setCheckable(True)
            self.idiomas_group.addAction(self.ingles_action)

        self.ingles_action.triggered.connect(lambda: self.__cambiarIdioma('en'))

        if not self.frances_action:

            self.frances_action = QAction(_("Francés"), self)
            self.idiomas_menu.addAction(self.frances_action)
            self.frances_action.setCheckable(True)
            self.idiomas_group.addAction(self.frances_action)

        self.frances_action.triggered.connect(lambda: self.__cambiarIdioma('fr'))

        if not self.espanol_action:

            self.espanol_action = QAction(_("Español"), self)
            self.idiomas_menu.addAction(self.espanol_action)
            self.espanol_action.setCheckable(True)
            self.idiomas_group.addAction(self.espanol_action)
            self.espanol_action.setChecked(True)

        self.espanol_action.triggered.connect(lambda: self.__cambiarIdioma('es'))

        # LAYOUT PRINCIPAL
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # QLABEL PARA MOSTRAR MENSAJE
        label_velocidad = QLabel(_("INTRODUZCA UNA CADENA:"))
        layout.addWidget(label_velocidad )

        # QLINEEDIT PARA INGRESAR LA CADENA
        self.__linee_cadena = QLineEdit()
        layout.addWidget(self.__linee_cadena)

        label_cadena = QLabel(_("VELOCIDAD:"))
        layout.addWidget(label_cadena)

        self.__deslizador = QSlider(Qt.Horizontal)
        self.__deslizador.setMinimum(1)
        self.__deslizador.setMaximum(5)
        self.__deslizador.setValue(1)
        layout.addWidget(self.__deslizador)

        # BOTÓN PARA PROCESAR
        btn_procesar = QPushButton(_("PROCESAR"))
        btn_procesar.clicked.connect(self.__procesar)
        layout.addWidget(btn_procesar)

        # CREAR UN WIDGET TIPO LIENZO PARA MOSTRAR LA IMAGEN
        self.__escena = QGraphicsScene()
        self.__lienzo = QGraphicsView(self.__escena)
        layout.addWidget(self.__lienzo)

        # QLABEL PARA MOSTRAR LA IMAGEN
        self.__label_imagen = QLabel()
        layout.addWidget(self.__label_imagen)

    def __procesarCadena(self, cadena):

        estado_actual = self.__automata.getEstadoInicial()

        self.__actualizarNodos(estado_actual)

        for simbolo in cadena:

            if (estado_actual, simbolo) in self.__automata.getTransiciones():

                self.__actualizarAristas(estado_actual, self.__automata.getTransiciones()[(estado_actual, simbolo)])
                estado_actual = self.__automata.getTransiciones()[(estado_actual, simbolo)]
                self.__actualizarNodos(estado_actual)

            else:

                return False

        return estado_actual in self.__automata.getEstadosFinales()

    def __procesar(self):

        if self.__procesarCadena(self.__linee_cadena.text()):

            self.__procesarVoz(self.traduccion("LA CADENA FUE ACEPTADA POR EL AUTÓMATA."))
            QMessageBox.information(self, self.traduccion("RESULTADO"), self.traduccion("LA CADENA FUE ACEPTADA POR EL AUTÓMATA."))

        else:

            self.__procesarVoz(self.traduccion("LA CADENA NO FUE ACEPTADA POR EL AUTÓMATA."))
            QMessageBox.warning(self, self.traduccion("RESULTADO"), self.traduccion("LA CADENA NO FUE ACEPTADA POR EL AUTÓMATA."))


    def __generarAristas(self):

        aristas = set()

        for clave in self.__automata.getTransiciones():

            aristas.add((clave[0], self.__automata.getTransiciones()[clave], clave[1]))

        return aristas

    def __actualizarNodos(self, estado):

        nx.draw(self.__grafo, self.__automata.getPos(), with_labels = True, node_color = ['blue' if node == estado else 'red' for node in self.__grafo.nodes()])
        self.__dibujarEtiquetas()

        plt.savefig('output.png', dpi = 300, format = 'png', bbox_inches = 'tight')
        self.__actualizarImagen()

        plt.pause(1 / self.__deslizador.value())

    def __actualizarAristas(self, estado_inicial, estado_final):

        nx.draw(self.__grafo, self.__automata.getPos(), with_labels = True, node_color = "red")
        nx.draw_networkx_edges(self.__grafo, self.__automata.getPos(), edgelist = {(estado_inicial, estado_final)}, edge_color = "blue")

        # OBTIENE EL PESO DE CADA ARISTA
        weight = nx.get_edge_attributes(self.__grafo, 'weight')
        # DIBUJA EL GRAFO CON LOS PESOS DE CADA ARISTA
        nx.draw_networkx_edge_labels(self.__grafo, self.__automata.getPos(), edge_labels = weight)

        nx.draw_networkx_edge_labels(self.__grafo, self.__automata.getPos(), edge_labels = {(estado_inicial, estado_final): weight[(estado_inicial, estado_final)]}, font_color = "blue")

        plt.savefig('output.png', dpi = 300, format = 'png', bbox_inches ='tight')
        self.__actualizarImagen()

        plt.pause(1 / self.__deslizador.value())

    def __dibujarEtiquetas(self):

        # OBTIENE EL PESO DE CADA ARISTA
        weight = nx.get_edge_attributes(self.__grafo, 'weight')
        # DIBUJA EL GRAFO CON LOS PESOS DE CADA ARISTA
        nx.draw_networkx_edge_labels(self.__grafo, self.__automata.getPos(), edge_labels = weight)

    def __actualizarImagen(self):

        pixmap = QPixmap("output.png")
        item = self.__escena.addPixmap(pixmap)
        item.setPos(0, 0)

        self.__lienzo.fitInView(item)

    def __procesarVoz(self, texto):

        objeto = gTTS(text = texto, lang = self.__obtenerIdioma(), slow = False)
        objeto.save("mensaje.mp3")

        playsound("mensaje.mp3", block = False)

        os.remove("mensaje.mp3")

    def __cambiarIdioma(self, idioma):

        if idioma == 'en':
            self.ingles_action.setChecked(True)
            locale = 'en'

        elif idioma == 'fr':
            self.frances_action.setChecked(True)
            locale = 'fr'

        else:
            self.espanol_action.setChecked(True)
            locale = 'es'

        gettext.install('mensajes', localedir, names=("ngettext",))
        gettext.translation('mensajes', localedir, languages=[locale]).install()

        self.__crearInterfaz(locale)

    def __obtenerIdioma(self):

        if self.ingles_action.isChecked():

            return 'en'

        elif self.frances_action.isChecked():

            return 'fr'

        elif self.espanol_action.isChecked():

            return 'es'

    def traduccion(self, mensaje):
        idioma = self.__obtenerIdioma()
        translations = gettext.translation('mensajes', localedir, languages=[idioma])
        translations.install()
        _ = translations.gettext

        return _(mensaje)

    def __actualizarTextoIdiomasMenu(self):
        self.ingles_action.setText(self.traduccion("Inglés"))
        self.espanol_action.setText(self.traduccion("Español"))
        self.frances_action.setText(self.traduccion("Francés"))
        self.idiomas_menu.setTitle(self.traduccion("Idiomas"))