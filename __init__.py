# -*- coding: utf-8 -*-
#####################################
##
## 
##
##
##
##
##
##
##
##
##
##
##
#####################################

###### methos needed #######
import visa   # interface with NI-Visa
import numpy as np # numpy for array manipulation
import os   # module for general OS manipulation
import time # module for time related funtions
import pandas as pd # module for general data analysis

class BK4052:
    def __init__(self):
        """
            Gerador de funções
        """
        self.id_bk = '0xF4ED'; # identificador do fabricante BK
        interface_name = self.find_interface()
        # instrument initialization
        self.instr = visa.ResourceManager().open_resource(interface_name)   ## resource name
        self.ch1 = ChannelFuncGen(self.instr, 'CH1')
        self.ch2 = ChannelFuncGen(self.instr, 'CH2')      
        self.functions = self.ch1.functions

    def find_interface(self):
        """ Function to extract the interface name for the  BK function generator"""
        resources = visa.ResourceManager().list_resources()
        instr_n = len(resources)
        if instr_n == 0:
            raise ValueError('Nenhum instrumento foi identificado: \n Verique se estao' \
                             'ligados e se o cabo USB foi conectado. Se o problema persistir \n'\
                             'desconecte os cabos USB, aguarde 20 segundos e conecte novamente.')
        bk_str = ''
        for resource in resources:
            fab_id = resource.split('::')[1]
            if fab_id == self.id_bk:
                instr = visa.ResourceManager().open_resource(resource)
                bk_str = instr.query('*IDN?')
                resource_out = resource
                print("Gerador de Funções conectado! Id = " + bk_str)
        if tek_str == '':
            raise ValueError('O osciloscopio BK scope nao foi identificado:\n'\
                         'Verique se o equipamento está ligado e se o cabo USB \n'\
                         'foi conectado. Se o problema persistir, \n'\
                         'desconecte o cabo USB, aguarde 20 segundos \n'\
                         'e conecte novamente.')
        return resource_out
        
####### Communications wraps    ########
    def identify(self):
        """ identify the resource"""
        return self.instr.query('*IDN?')
#
    def write(self, msg):
        """ write into the laser """
        return self.instr.write(str(msg))
#
    def query(self, msg):
        """ query into the laser """
        return self.instr.query(str(msg)) 
#
    def read(self):
        """ read from the laser """
        return self.instr.read()    
#        
    def close(self):
        """ close the instrument """
        return self.instr.close()
#
class TektronixTBS1062:
    def __init__(self):
        """
            Classe para o osciloscópio
        """
        self.id_tek = '0x0699'; # identificador do fabricante TEK
        interface_name = self.find_interface()
        self.instr = visa.ResourceManager().open_resource(interface_name)   ## resource name
        self.ch1 = ChannelScope(self.instr, 'CH1')  # channel 1
        self.ch2 = ChannelScope(self.instr, 'CH2')   # channel 2
        self.math = Channel(self.instr, 'MATH')   # channel 2
        self.average_list = [4, 16, 64, 128]
        self.channel_list = self.ch1.channel_list
        self.trigger_list = ['CH1', 'CH2', 'EXT', 'EXT5', 'EXT10', 'AC LINE']
        self.instr.timeout = 10000 # set timeout to 10 seconds
        self.instr.chunk_size = 40960  # set the buffer size to 40 kB
        self.instr.write('Data:ENCDg SRI')  # set the instrument to read binary
        self.instr.write('Data:Width 1')
        self.instr.values_format.is_binary = True
        self.instr.values_format.datatype = 'b'
        self.instr.values_format.is_big_endian = True
        self.instr.values_format.container = np.array    

    def find_interface(self):
        """ 
            Function to extract the interface name for the Tektronics scope
        """
        resources = visa.ResourceManager().list_resources()
        instr_n = len(resources)
        if instr_n == 0:
            raise ValueError('Nenhum instrumento foi identificado: \n Verique se estao' \
                             'ligados e se o cabo USB foi conectado. Se o problema persistir \n'\
                             'desconecte os cabos USB, aguarde 20 segundos e conecte novamente.')
        tek_str = ''
        for resource in resources:
            fab_id = resource.split('::')[1]
            if fab_id == self.id_tek:
                instr = visa.ResourceManager().open_resource(resource)
                tek_str = instr.query('*IDN?')
                resource_out = resource
                print("Osciloscópio conectado! Id = " + tek_str)
        if tek_str == '':
            raise ValueError('O osciloscopio TEK 1062 nao foi identificado:\n'\
                         'Verique se o equipamento está ligado e se o cabo USB \n'\
                         'foi conectado. Se o problema persistir, \n'\
                         'desconecte o cabo USB, aguarde 20 segundos \n'\
                         'e conecte novamente.')
        return resource_out
#
####### Communications wraps    ########    
    def identify(self):
        """ identify the resource"""
        return self.instr.query('*IDN?')
#
    def write(self, msg):
        """ write into the instrument """
        return self.instr.write(str(msg))
#
    def query(self, msg):
        """ query from the instrument """
        return self.instr.query(str(msg)) 
#
    def read(self):
        """ read from the instrument """
        return self.instr.read()
#
    def close(self):
        """ close the instrument """
        return self.instr.close()

##### test commands ###########
    def aquisition_params(self):
        """ return the aquisition parameters  """
        return self.instr.query('ACQuire?').split(';')
#    
    def average_number(self):
        """ return the number of waveforms used in the average """
        return int(self.instr.query('ACQuire:NUMAVg?').split(':')[-1].split(' ')[-1])

    def set_average_number(self, msg):
        """ set the number of waveforms used in the average """
        if int(msg) in self.average_list:                
            self.instr.write('ACQuire:NUMAVg %3d' % int(msg))   
            return None
        else: 
            raise ValueError("The number of waveforms must be one of " + ', '.join(['%3d' % l for l in self.average_list]))
#          
##### waveform reading commands #####
    def start_acquisition(self):
        """ start the aquisition of the waveform """
        return self.instr.write('ACQuire:STATE RUN')
#
    def stop_acquisition(self):
        """ stop the aquisition of the waveform """
        return self.instr.write('ACQuire:STATE STOP')
#
    def set_trigger_source(self, source):
        """ set trigger source"""
        if source in self.trigger_list:
            self.instr.write('TRIGGER:MAIN:EDGE:SOURCe ' + source)
        else:
            raise ValueError('The trigger should be one of those: ' + ', '.join([l for l in self.trigger_list]))
#
    def trigger_source(self):
        return self.instr.query('TRIGGER:MAIN:EDGE:SOURCe?')[:-1]
#
    def set_trigger_level(self, val):
        """ set trigger level"""
        self.instr.write('TRIGGER:MAIN:LEVEL ' + str(val))
#
    def trigger_level(self):
        return float(self.instr.query('TRIGGER:MAIN:LEVEL?'))
    
############## Saving functions ##### (They shouldn' t be here!!)
    def save_channels(self, name, header = ['time (s)', 'Channel 1 (V)', 'Channel 2 (V)'], PATH = 'C:\\Users\\Gaeta Integra\\Documents\\Python Scripts\\Felippe\\'):
        """ save the the channels 1 and 2 and save the with the "header" in the "PATH" ad with the file name "name") """
##### reading and setting directory name
        x, y1 = self.ch1.read_channel()   # read channel 1
        x0, y2 = self.ch2.read_channel()   # read channel 2
        dir_name =  PATH + time.strftime('%Y_%m_%d\\', time.localtime(time.time())) # set directory name
        # check the directory exist and create it automaticaly
        try: 
            os.makedirs(dir_name)     # make new directory unless it already exists
        except OSError:
            if not os.path.isdir(dir_name):
                raise
###### name of the file        
        Npts = x.shape[0]
        indexh = range(Npts)
        df = pd.DataFrame(columns = header, index = indexh)    # initialization of the filtered dataframe        
        df[header[0]] = x
        df[header[1]] = y1
        df[header[2]] = y2
#
        time_stamp_suf = time.strftime('_%H_%M_%S', time.localtime(time.time()))
        full_name = dir_name + name + time_stamp_suf        
        df.to_csv(full_name + '.csv')
        print('... file => ' + name + time_stamp_suf + ' saved!!')
        return x, y1, y2

########################################
class ChannelScope:
    def __init__(self, instrument, channel):
        """ 
           Channel class for the oscilloscopes
        
        """
        self.instr = instrument  ## resource name
        self.channel_list = ['CH1', 'CH2']
        self.measure = Measure(self.instr, channel)
#
    def get_active_channel(self):
        """ return the active channel for the waveform aquisition """
        return self.instr.query('DATa:SOUrce?').split(' ')[-1][:-1]
#
    def set_active_channel(self, channel):
        """ set the active channel for waveform aquisition """
        if msg in self.channel_list:
            self.instr.write('DATa:SOUrce ' + str(channel))
        else:
            raise ValueError("The channels should be one of " + ', '.join([l for l in self.channel_list]))            
#
    def read_preface(self):
        """ return a list with the praface parameters  """
        return self.instr.query('WFMPRe?').split(':')[-1].split(',')  # read the preface and convert into a list
#
    def waveform_conversion_old(self):
        """ return the waveform convertion values in the form
        "[[x_zero, x_factor, x_offset], [y_zero, y_factor, y_offset]]" """
        temp = self.read_preface()[5].split(';')   # read the 6 position of the preface and convert into a list
        temp = [x.split(' ') for x in temp]   
        for test in temp:
            if test[0] == 'XZERO': x_zero = float(test[1])
            if test[0] == 'XINCR': x_factor = float(test[1])
            if test[0] == 'PT_OFF': x_offset = float(test[1])
            if test[0] == 'YZERO': y_zero = float(test[1])
            if test[0] == 'YMULT': y_factor = float(test[1])
            if test[0] == 'YOFF': y_offset = float(test[1])        
        return [[x_zero, x_factor, x_offset], [y_zero, y_factor, y_offset]]
#
    def waveform_conversion(self):
        """ return the waveform convertion values in the form
        "[[x_zero, x_factor, x_offset], [y_zero, y_factor, y_offset]]" """
        temp = self.read_preface()[5].split(';')   # read the 6 position of the preface and convert into a list
        x_factor, x_offset, x_zero = float(temp[2]), float(temp[3]), float(temp[4]) 
        y_factor, y_offset, y_zero = float(temp[6]), float(temp[7]), float(temp[8]) 
        return [[x_zero, x_factor, x_offset], [y_zero, y_factor, y_offset]]   
#
    def acquire_y_raw_ascii(self):
        """acquire the raw curve of whatever channel is set in "set_channel" """
        return np.array(self.instr.query('CURVe?').split(' ')[-1].split(','), float)
#
    def acquire_y_raw(self):
        """acquire the raw curve of whatever channel is set in "set_channel" """
        return np.array(self.instr.query_values('CURVe?'))
#
    def read_active_channel(self):
        """ returns a tuple with both the x and y axis already converted. It creates the x axis and reads the y axis from the active channel set with the function "set_channel". The y acquisition is done using the function "acquire_y_raw" the converting factor by using the "waveform_conversion" function """
        y_raw = self.acquire_y_raw()    # acquire y raw curve
        [[x_zero, x_factor, x_offset], [y_zero, y_factor, y_offset]] = self.waveform_conversion()
        x_raw = np.arange(len(y_raw))        
        x = x_zero + x_factor*(x_raw - x_offset)
        y = y_zero + y_factor*(y_raw - y_offset)
        return (x, y)
#
    def read_channel(self, channel):
        """ read the channel and return the x and y axis """ 
        self.set_active_channel(channel)
        return self.read_active_channel()    
    
# subclass with the measurements     
class Measure:
    def __init__(self, resource, source):
        # instrument initialization
        """ Make the all measure"""
        self.instr = resource   ## resource name
        self.source = source   # source variable
#        
    def do_measure(self, prop):
        """measure the property on channel """
        self.instr.write('MEASUREMENT:IMMED:TYPE ' + prop)
        self.instr.write('MEASUREMENT:IMMED:Source ' + self.source)
        if prop.lower() == 'phase':
            self.instr.write('MEASUREMENT:IMMED:Source2 CH1')                        
            self.instr.write('MEASUREMENT:IMMED:Source ' + self.source)            
        return float(self.instr.query('MEASUREMENT:IMMED:Value?'))
#
    def phase(self):
        """measure the phase """
        return float(self.do_measure('PHASE'))
    def Vpp(self):
        """measure the peak-to-peak voltage """
        return float(self.do_measure('PK2PK'))
    def frequency(self):
        """measure the frequency in Hz """
        return float(self.do_measure('FREQ'))
    def period(self):
        """measure the period in s """
        return float(self.do_measure('PERIOS'))
    def mean(self):
        """measure the average value """
        return float(self.do_measure('MEAN'))
    def cycle_rms(self):
        """measure the RMS voltage in one period in V """
        return float(self.do_measure('CRMS'))
    def rms(self):
        """measure the RMS voltage in the screen in V """
        return float(self.do_measure('RMS'))
##############################
class ChannelFuncGen:
    def __init__(self, instrument, channel):
        """
            Class for the channels of the function generator
        """
        self.instr = instrument   ## resource name
        self.channel = channel
        self.functions = ['SINE', 'SQUARE', 'RAMP', 'PULSE', 'NOISE', 'ARB', 'DC']  # list of allowed functions
        # instrument limits
        self.frequency_max = 5.e6  # maximum freqeuncy in Hertz
        self.frequency_min = 1.e-6   # minimum freqeuncy in Hertz
        self.amplitude_max = 20         # maximum amplitude in V
        self.amplitude_min = 0.0004           # minimum amplitude in V
        self.offset_max = 10    # maximum offset in V  
        self.offset_min = -10   # minimum offset in V
        self.phase_max = 360   # maximum phase in degrees
        self.phase_min = 0     # minimum phase in degrees
        self.symmetry_max = 100   # maximum symmetry in percentage
        self.symmetry_min = 0     # minimum symmetry in percentage
        self.duty_max = 90   # maximum duty cycle in percentage
        self.duty_min = 10     # minimum duty cycle in percentage

# Basic Commands
    def turn_on(self):
        # Implementar a checagem se o canal já está ligado ou desligado
        # Talvez juntar os comandos turn_on and turn_off no mesmo comando        
        """ turn on the specified channel. The channel must be either "CH1" or "CH2" """
        if self.channel == "CH1" or self.channel == "CH2":
            state = self.instr.query('C1:Output?').split(',')[0].split(' ')[1]
            if state == 'ON': raise ValueError('The channel ' + channel + 'is already turned ON')
            else: self.instr.write('C' + self.channel[-1] + ':OUTput ON')
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')
        return None
####    
    def turn_off(self):
        """ turn the specified channel OFF. The channel must be either "CH1" or "CH2" """
        if self.channel == "CH1" or self.channel == "CH2":
            state = self.instr.query('C1:Output?').split(',')[0].split(' ')[1]
            if state == 'OFF': raise ValueError('The channel ' + channel + 'is already turned OFF')
            else: self.instr.write('C' + self.channel[-1] + ':OUTput OFF')
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')              
        return None

    def set_function(self, val):
        """set the function at the channel """
        if self.channel == "CH1" or self.channel == "CH2":
            cmd = 'C' + self.channel[-1] + ':BSWV'
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')
            # type checking
        if val in self.functions:
            cmd = cmd + ' WVTP,' + val
            self.instr.write(cmd)
        else:
            raise ValueError("The functions must be one of those:", self.functions)
        return None    

    def set_frequency(self, val):
        """set the function generator frequency """
        if self.channel == "CH1" or self.channel == "CH2":
            cmd = 'C' + self.channel[-1] + ':BSWV'
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')
        if val <= self.frequency_max and val >= self.frequency_min:
            cmd = cmd + ' FRQ,' + str(float(val)) + 'Hz'
            self.instr.write(cmd)
        else: 
            raise ValueError("The frequency must be between %4.2f uHz and %4.2f MHz" % (1e6*self.frequency_min, 1e-6*self.frequency_max))                 
        return None    

    def set_amplitude(self, val):
        """set the function generator amplitude """
        if self.channel == "CH1" or self.channel == "CH2":
            cmd = 'C' + self.channel[-1] + ':BSWV'
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')
        if val <= self.amplitude_max and val >= self.amplitude_min:
            cmd = cmd + ' AMP,' + str(float(val)) + 'V'
            self.instr.write(cmd)
        else: 
            raise ValueError("The amplitude must be between %4.2f V and %4.2f V" % (self.amplitude_min, self.amplitude_max))                 
        return None
    
    def set_offset(self, val):
        """set the function generator offset """
        if self.channel == "CH1" or self.channel == "CH2":
            cmd = 'C' + self.channel[-1] + ':BSWV'
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')
        if val <= self.offset_max and val >= self.offset_min:
            cmd = cmd + ' OFST,' + str(float(val)) + 'V'
            self.instr.write(cmd)
        else: 
            raise ValueError("The offset must be between %4.2f V and %4.2f V" % (self.offset_min, self.offset_max))                 
        return None    
    
    def set_phase(self, val):
        """set the function generator phase """
        if self.channel == "CH1" or self.channel == "CH2":
            cmd = 'C' + self.channel[-1] + ':BSWV'
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')
        if val <= self.phase_max and val >= self.phase_min:
            cmd = cmd + ' PHSE,' + str(float(val))
            self.instr.write(cmd)
        else: 
            raise ValueError("The phase must be between %4.2f and %4.2f degrees" % (self.phase_min, self.phase_max))                 
        return None

    def set_symmetry(self, val):
        """set the function generator signal symmetry """
        if self.channel == "CH1" or self.channel == "CH2":
            cmd = 'C' + self.channel[-1] + ':BSWV'
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')
        if val <= self.symmetry_max and val >= self.symmetry_min:
            cmd = cmd + ' SYM,' + str(float(val))
            self.instr.write(cmd)
        else: 
            raise ValueError("The symmetry must be between %4.0f and %4.0f percent" % (self.symmetry_min, self.symmetry_max))                 
        return None  
    
    def set_duty(self, val):
        """set the function generator duty cycle """
        if self.channel == "CH1" or self.channel == "CH2":
            cmd = 'C' + self.channel[-1] + ':BSWV'
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')
        if val <= self.duty_max and val >= self.duty_min:
            cmd = cmd + ' DUTY,' + str(float(val))
            self.instr.write(cmd)
        else: 
            raise ValueError("The duty cycle must be between %4.0f and %4.0f percent" % (self.duty_min, self.duty_max))                 
        return None  
   
### Measurements commands
    def full_wave(self, raw_output = False):
        """return the wave information for "channel". If raw_output = True, the output from the function is returned without processing"""
        if self.channel == "CH1" or self.channel == "CH2":
            output = self.instr.query('C' + self.channel[-1] + ':BSWV?')
            if raw_output: return output
            else:
                temp = output.split(',')
                return {'type':temp[1], 'frequency':float(temp[3][:-2]), 'amplitude':float(temp[5][:-1]), 'offset':float(temp[7][:-1]), 'phase':float(temp[9][:-1])}
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')                 

    def sync_source(self):
        """return the sync source"""
        return None
