# -*- coding: utf-8 -*-
"""
Created on Qua Jan 11 11:12:18 2017

@author: Felippe Barbosa

"""
import visa   # interface with NI-Visa
import numpy as np # numpy for array manipulation

class BK4052:
    # inicialization of the class 
    def __init__(self):
        self.id_bk = '0xF4ED'; # identificador do fabricante BK
        interface_name = self.find_interface()
        # instrument initialization
        self.instr = visa.ResourceManager().open_resource(interface_name)   ## resource name
        self.ch1 = Channel(self.instr, 'CH1')
        self.ch2 = Channel(self.instr, 'CH2')      
        self.functions = self.ch1.functions

    def find_interface(self):
        ''' Function to extract the interface name for the  BK function generator'''
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
    def write(self, msg):
        ''' write into the laser '''
        return self.instr.write(str(msg))
#
    def query(self, msg):
        ''' query into the laser '''
        return self.instr.query(str(msg)) 
#
    def read(self):
        ''' read from the laser '''
        return self.instr.read()    
#        
    def identify(self):
        ''' identify the resource'''
        return self.instr.query('*IDN?')
#################


class Channel:
    # inicialization of the class 
    def __init__(self, resource, channel):
        # instrument initialization
        self.instr = resource   ## resource name
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
        ''' turn on the specified channel. The channel must be either "CH1" or "CH2" '''
        if self.channel == "CH1" or self.channel == "CH2":
            state = self.instr.query('C1:Output?').split(',')[0].split(' ')[1]
            if state == 'ON': raise ValueError('The channel ' + channel + 'is already turned ON')
            else: self.instr.write('C' + self.channel[-1] + ':OUTput ON')
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')
        return None
####    
    def turn_off(self):
        ''' turn the specified channel OFF. The channel must be either "CH1" or "CH2" '''
        if self.channel == "CH1" or self.channel == "CH2":
            state = self.instr.query('C1:Output?').split(',')[0].split(' ')[1]
            if state == 'OFF': raise ValueError('The channel ' + channel + 'is already turned OFF')
            else: self.instr.write('C' + self.channel[-1] + ':OUTput OFF')
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')              
        return None

    def set_function(self, val):
        '''set the function at the channel '''
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
        '''set the function generator frequency '''
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
        '''set the function generator amplitude '''
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
        '''set the function generator offset '''
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
        '''set the function generator phase '''
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
        '''set the function generator signal symmetry '''
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
        '''set the function generator duty cycle '''
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
        '''return the wave information for "channel". If raw_output = True, the output from the function is returned without processing'''
        if self.channel == "CH1" or self.channel == "CH2":
            output = self.instr.query('C' + self.channel[-1] + ':BSWV?')
            if raw_output: return output
            else:
                temp = output.split(',')
                return {'type':temp[1], 'frequency':float(temp[3][:-2]), 'amplitude':float(temp[5][:-1]), 'offset':float(temp[7][:-1]), 'phase':float(temp[9][:-1])}
        else: 
            raise ValueError('The Channels must be either "CH1" or "CH2"')                 

    def sync_source(self):
        '''return the sync source'''
        return None
