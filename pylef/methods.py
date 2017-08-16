#-*- coding: utf-8 -*-

""" Class for the Methods """

#################################
import visa   # interface with NI-Visa
<<<<<<< HEAD
import numpy as np  # module for array manipulation
import matplotlib.pyplot as plt
import os   # module for general OS manipulation
import time # module for time related funtions
import pandas as pd # module for general data analysis
import pylef
################################

#bibliotecas para atualizacoa de grafico
from IPython.core.display import clear_output
from IPython.display import display, Javascript

'''
--------------------------
Funções para graficar ao vivo e adquirir dados
NÃO ALTERE NADA NESTA CÉLULA
--------------------------
'''
#***********************************************
#***********************************************
def plot_bode(freq,phase,T,T_dB,spacing='log'):
    '''
    Função para graficar transmistância e fase
    ===============
    Uso simples:
    >>> figure = plot_bode(freq,phase,T,T_dB,spacing)
    entrada:
    --------
    freq: vetor de frequências (lista ou numpy.array)
    phase: vetor de fases (lista ou numpy.array)
    T: vetor de transmitância linear (lista ou numpy.array)
    T_dB: vetor de transmitância em decibéis (lista ou numpy.array)
    spacing (opcional): 'linear' (espaçamento linear) ou 'log' (espaçamento logarítmico); por padrao o espaçamento é linear
    --------
    saída:
    figure:objeto gráfico do Matplotlib
    '''
    #Identificando se é linear ou log
    npt = len(T_dB)
    fig, ax = plt.subplots(2, sharex=True)
    if spacing=='log':
        y=T_dB
        y_label='Transmissão (dB)'
    elif spacing=='linear':
        y=T
        y_label='Transmissão'
    #-----------------------------------
    #TRANSMISSION PLOT
    #-----------------------------------
    ax[0] = plt.subplot(211)  # define um eixo
    ax[0].plot(freq[0:npt], y[0:npt], 'ro')   # plota a transmissão
    ax[0].set_xscale(spacing)   # seta a escala de x para logaritmica
    # Por que não usamos escala log no eixo y também?
    #ax[0].set_xlabel('frequência (Hz)')   # seta escala do eixo x
    ax[0].set_ylabel(y_label)   # seta escala do eixo y
    plt.xlim((freq.min(),freq.max()))
    #-----------------------------------
    #PHASE PLOT
    #-----------------------------------
    ax[1] = plt.subplot(212)  # define um eixo
    ax[1].plot(freq[0:npt], phase[0:npt], 'bo')   # plota a transmissão
    ax[1].set_xscale(spacing)   # seta a escala de x para logaritmica
    # Por que não usamos escala log no eixo y também?
    ax[1].set_xlabel('frequência (Hz)')   # seta escala do eixo x
    ax[1].set_ylabel('Fase (graus)')   # seta escala do eixo y
    plt.xlim((freq.min(),freq.max()))
    plt.ylim((-180,180))
    #------------------------------------
    clear_output(True)
    display(fig)
    plt.close()
    return fig
#***********************************************
#***********************************************
def sweep_frequency(freq0, freq1, Nfreq, path = '', fname='', spacing = 'linear', average = 4):
    '''
    Função para realizar um sweep e fazer gráfico
    ===============
    Uso simples:
    >>> figure, freq, vpp1, vpp2, phase = sweep_frequency(freq0,freq1,Nfreq,spacing = 'linear')
    figure: figura
    freq0: frequência inicial (Hz)
    freq1: frequencia final (Hz)
    Nfreq: número de pontos no vetor de frequências
    spacing (opcional): 'linear' (espaçamento linear) ou 'log' (espaçamento logarítmico)
    average: número de médias a serem realizadas
    '''
    # display(Javascript("""
    # require(
    # ["base/js/dialog"],
    # function(dialog) {
    #     dialog.modal({
    #         title: 'Hello world',
    #         body: 'Hi, lorem ipsum and such',
    #         buttons: {
    #             'kthxbye': {}
    #             }
    #         });
    #     }
    # );"""))

    func_gen = pylef.BK4052()  # definição do gerador de funções
    scope = pylef.TektronixTBS1062()  # definição do osciloscópio
    #------------------
    #constroi vetor de frequencias
    #------------------
    if spacing == 'linear':
        freq = np.linspace(freq0, freq1, Nfreq, endpoint = True)  # varredura logaritmica
    elif spacing == 'log':
        freq = np.logspace(np.log10(freq0), np.log10(freq1), Nfreq, endpoint = True)  # varredura logaritmica
    else:
        raise ValueError('O espaçamento entre os pontos deve ser linear ou log')
    #### Aquisição de dados!! ####
    scope.set_average_number(average)  # ajusta o número de médias
    scope.set_average()    # turn average ON
    #-----------------
    Vpp1, Vpp2 = [], []    # listas para guardar as variáveis
    #phase1, phase2 = [], []    # listas para guardar as variáveis
    phase = []   # listas para guardar as variáveis
    ### aquisição de dados no gerador com varredura de frequência
    scope.write('MEASUREment:MEAS1:TYPE NONE')
    scope.write('MEASUREment:MEAS2:TYPE NONE')
    scope.write('MEASUREment:MEAS3:TYPE NONE')
    scope.write('MEASUREment:MEAS4:TYPE NONE')
    scope.write('MEASUREment:MEAS5:TYPE NONE')
    for m, freqP in enumerate(list(freq)):  # loop de aquisição
        #print('Medida ' + str(m + 1))
        print('Frequencia atual={:2g} Hz'.format(freq[m]))
        start=time.time()
        ### ajuste dos instrumentos
        func_gen.ch1.set_frequency(freqP)   # muda a frequência
        periodP = 1./freqP   # período da onda
        scope.set_horizontal_scale(periodP/4.)  # escala horizontal = 1/4 período (2.5 oscilações em tela)
        scope.ch1.set_smart_scale()    #  rescala o canal 1
        scope.ch2.set_smart_scale()    #  rescala o canal 2
        ### aquisição de dados
        Vpp1.append(scope.ch1.measure.Vpp()) # acumula a medida do Vpp no canal 1
        phase.append(-scope.ch1.measure.phase()) # acumula a medida da fase no canal 1
        Vpp2.append(scope.ch2.measure.Vpp())  # acumula a medida do Vpp no canal 2
        #---------plotting stuff-------
        T = (np.array(Vpp2)/np.array(Vpp1))**2   # cálculo da transmissão
        T_dB = 10*np.log10(T)  # transmissão em dB
        # plota o diagrama de bode para a transmissão e exporta em png
        fig = plot_bode(freq,phase,T,T_dB,spacing)
        #-------
    print('Fim! Tempo total de medida={:2g} s'.format(time.time()-start))
    Vpp1 = np.array(Vpp1)  # convete a lista em array
    Vpp2 = np.array(Vpp2)  # convete a lista em array
    phase = np.array(phase)  # convete a lista em array
    ''' encerra a comunicação osciloscópio e o gerador de funções '''
    scope.close()
    func_gen.close()
    ''' organizando dados'''
    # calculando a transmitância
    T = Vpp2 / Vpp1  # cálculo da transmissão
    T_dB = 20 * np.log10(T)  # transmissão em dB
    # gerando tabelas
    dados = pd.DataFrame()  # inicializa um dataframe do pandas
    dados['Vpp1 (V)'], dados['Vpp2 (V)'] = Vpp1, Vpp2
    dados['fase (Ch2-Ch1) (graus)'] = phase
    dados['frequencia (Hz)'], dados['T'], dados['T_dB'] = freq, T, T_dB
    ## parametros de varredura
    path0 = '/Users/usuario/F429/'  # pasta onde salvar todos os arquivos
    datapasta = time.strftime('dia_%D_hora_%H', time.localtime(time.time())).replace('/','-')
    path = path0+datapasta
    if fname=='':
        fname = 'sweep'
    ##--------------------------------------------------------
    # Cria a pasta no computador, veja a variável PATH
    try:
        os.makedirs(path)  # make new directory unless it already exists
    except OSError:
        if not os.path.isdir(path):
            raise
    # qual pasta estou?
    print('Pasta dos arquivos:', os.path.abspath(path))
    time_suf = time.strftime('_%H_%M_%S', time.localtime(time.time()))
    nome_fig = os.path.join(path,fname + '_bode' + time_suf + '.png')
    nome_csv = os.path.join(path,fname + '_dados' + time_suf + '.dat')
    # Salvando
    fig.savefig(nome_fig, bbox_inches='tight')  # salva figura na pasta de trabalho
    dados.to_csv(nome_csv, sep='\t', index=False)  # \t significa que o separador é uma tabulação, index=False remove os indices da coluna
    return fig, dados


