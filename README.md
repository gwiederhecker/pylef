# pylef
Compilamos aqui as bibliotecas de aquisição de dados utilizados nos cursos do Laboratório de Ensino de Física (LEF) do Instituto de Física Gleb Wataghin, Unicamp

A idéia deste projeto é criar drivers para comunicação com instrumentos utilizados nos cursos do IFGW. 
Os drivers são implementados utilizandos classes do Python. A comunicação é realizada através do VISA (Virtual Instrument Software Architecture), em particular da biblioteca PyVISA. 
Outras "imports" necessários para os drivers são:
1) numpy
2) os
3) time
4) pandas
-------------------------
bk.py: driver para comunicar com o gerador de sinal BK 4052.
Página do instrumento: http://www.bkprecision.com/products/signal-generators/4052-5-mhz-dual-channel-function-arbitrary-waveform-generator.html
-------------------------
tek.py: driver para comunicar com o osciloscópio TekTronix TBS1062.
Página do instrumento: http://www.tek.com/oscilloscope/tbs1000-digital-storage-oscilloscope-manual
-------------------------

