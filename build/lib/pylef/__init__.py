# -*- coding: utf-8 -*-
"""
PyLEF v0.1.0

Compilamos aqui as bibliotecas de aquisição de dados 
utilizados nos cursos do Laboratório de Ensino de 
Física (LEF) do Instituto de Física Gleb Wataghin na 
Unicamp.

Este projeto tem como objetivo facilitar a comunicação
com instrumentos utilizados nos cursos do IFGW. A 
comunicação é realizada através do VISA (Virtual 
Instrument Software Architecture), em particular da 
biblioteca PyVISA. 

Acesso à Documentação
---------------------

No momento, a documentação pode ser encontrada no 
código por meio das 'docstrings'. As "docstrings" 
podem ser acessadas por meio da função "help"

    >>> import pylef         # importa o pylef
    >>> print(help(pylef))   # imprime esta documentação na tela

onde os três sinais de 'maior que' (>>>) designam um 
código python. No Jupyter notebook, podemos também 
acessar a documentação colocando uma interrogação (?) 
antes da função

    >>> ?pylef         # imprime a documentação do pylef

Instrumentos
------------

Usaremos no curso dois instrumentos pricipais

    * Gerador de Funções: BK Precision BK4052
    * Osciloscópio Digital: Tektronix TBS1062

Ambos os instrumentos são definidos como objetos dentro 
do PyLEF,

    >>> gerador = pylef.BK452()   # definição do gerador de funções
    >>> scope = pylef.TBS1062()   # definição do osciloscópio

A documentação das funções de cada instrumento podem
ser encontradas também pelo comando help

    >>> print(help(scope))      # documentação do osciloscópio  
    >>> print(help(gerador))    # documentação do gerador

ou no Jupyter notebook

    >>> ?scope      # documentação do osciloscópio  
    >>> ?gerador    # documentação do gerador

"""

## import instrument modules
from .scope import TektronixTBS1062
from .generator import BK4052
from .methods import sweep_frequency
