# pylef
Compilamos aqui as bibliotecas de aquisição de dados utilizados nos cursos do Laboratório de Ensino de Física (LEF) do Instituto de Física Gleb Wataghin, Unicamp

A idéia deste projeto é criar drivers para comunicação com instrumentos utilizados nos cursos do IFGW. 
Os drivers são implementados utilizandos classes do Python. A comunicação é realizada através do VISA (Virtual Instrument Software Architecture), em particular da biblioteca PyVISA. 

# Requerimentos

O pylef é construído em cima dos seguintes módulos:

1. pyvisa
2. numpy
4. pandas

para instalá-los vá até um prompt de comando como administrador e execute o seguinte comando

    pip install pyvisa numpy pandas

-------------------------
# Instalação

O pylef também pode ser instalado pelo pip. Abra um prompt como administrador e execute o seguinte comando

    pip install pylef

-------------------------
# Instrumentos Suportados

osciloscópio TekTronix TBS1062.
* [Página do instrumento no fabricante Tektronix] (http://www.tek.com/oscilloscope/tbs1000-digital-storage-oscilloscope-manual)

gerador de funções BK 4052.
* [Página do instrumento no fabricante BK precision]( http://www.bkprecision.com/products/signal-generators/4052-5-mhz-dual-channel-function-arbitrary-waveform-generator.html)

