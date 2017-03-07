# -*- coding: utf-8 -*-

""" Compilamos aqui as bibliotecas de aquisição de dados utilizados nos cursos do Laboratório de Ensino de Física (LEF) do Instituto de Física Gleb Wataghin, Unicamp

A idéia deste projeto é criar drivers para comunicação com instrumentos utilizados nos cursos do IFGW. Os drivers são implementados utilizandos classes do Python. A comunicação é realizada através do VISA (Virtual Instrument Software Architecture), em particular da biblioteca PyVISA. """
   
## import instrument modules
from .scope import TektronixTBS1062
from .generator import BK4052
