#-*- coding: utf-8 -*-

import visa # interface with NI-Visa
################################
def read_only_properties(*attrs):
    """
        decorator to make some class variables read-only
        made by oz123 from   
        https://github.com/oz123/oz123.github.com/blob/master/media/uploads/readonly_properties.py
    """
    def class_rebuilder(cls):
        "The class decorator example"

        class NewClass(cls):
            "This is the overwritten class"
            def __setattr__(self, name, value):

                if name not in attrs:
                    pass
                elif name not in self.__dict__:
                    pass
                else:
                    raise AttributeError("Can't touch {}".format(name))

                super().__setattr__(name, value)

        return NewClass

    return class_rebuilder

##########################
@read_only_properties('id_bk', 'instr', 'ch1', 'ch2', )
class BK4052:
    def __init__(self):
        """
        BK4052
        =========
   
        This is a virtual object that represents the arbitrary function 
        generator BK4052 and mimics it's behaviour. The user should 
        interact with this object in the same fashion he or she interacts 
        with the function generator. As it is the case for the real function 
        generator, we have independent access to the both channels, which 
        are represented by "ch1" and "ch2".
         
        The instrument has a "identify" function that returns the instrument
        information and 3 pyvisa wrapped functions: "read", "write", "query" 
        and "close" (go to pyvisa documentation for more detail). There is also
        a function "find_interface" that automatic find in which USB port
        the function generator is connected.
                     
        Usage:
  
        >>> import pylef        # import the pylef package
        >>> instrument = pylef.BK4052()  # define the instrument
        >>> instrument.idenfify()   # idenfity the instrument

        The channels are independently defined and accessed. For each one of 
        them we can set up the function properties, such as 'frequency' and 
        'peak-to-peak voltage' and many channel attibutes, such as 'inversion',
        'load impedance' and 'TTL sync output'. We can also, turn the channels
        ON and OFF.
 
        >>> channel1 = instrument.ch1()   # define channel 1
        >>> channel1.turn_on()       # turn channel 1 ON
        >>> channel1.sync_on()       # turn the TTL sync output for channel 1 

        The most important is the 'function type', which can be one of those:
        'SINE', 'SQUARE', 'RAMP', 'PULSE', 'NOISE', 'ARB', 'DC' and each one of 
        them are defined by a particular set of properties. Those properties are
        one of: 'frequency', 'Vpp', 'offset', 'phase', 'symmetry', 'duty', 'mean',
        'stdev', 'delay'. Some of those properties are share by more the one 
        function type and some are privative to only one type. For example, 'SINE', 
        'SQUARE', 'RAMP', 'ARB' and 'PULSE' have the 'frequency' and 'Vpp' properties
        while 'noise' type is the only one who has the 'mean' and 'stded' properties. 

        Usage:
  
        >>> channel1.set_function('ramp')  # create a triangular wave
        >>> channel1.set_frequency(100)    # set the frequency to 100 Hz 
        >>> channel1.set_Vpp(2)            # set the peak-to-peak voltage to 2 V
        >>> channel1.set_frequency()

        >>> channel2.turn_on()              # turn channel 2 ON
        >>> channel2.set_function('noise')  # create a noise
        >>> channel2.set_mean(0)            # set the average 0 V
        >>> channel2.set_stdev(0.5)         # set the standard deviation to 0.5 V 
          
        The function "wave_info" returns a python dictionay with the particular wave
        information

        Usage:

        >>> info1 = channel1.wave_info()   # current wave information of channel 1
        >>> print(info1['frequency'])      # will return 100
        >>> print(info1['type'])      # will return ramp
        >>> info2 = channel2.wave_info()   # current wave information of channel 2
        >>> print(info2['stdev'])          # will return 0.5            
        """

        self.id_bk = '0xF4ED'; # identificador do fabricante BK
        interface_name = self.find_interface()
        # instrument initialization
        self.instr = visa.ResourceManager().open_resource(interface_name)   ## resource name
        self.ch1 = ChannelFuncGen(self.instr, 'CH1')
        self.ch2 = ChannelFuncGen(self.instr, 'CH2')
        self.instr.timeout = 10000 # set timeout to 10 seconds
        self.instr.chunk_size = 40960  # set the buffer size to 40 kB  

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
                print("Gerador de Funções conectado! Id = " + bk_str[:-1])
        if bk_str == '':
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
    def wait(self):
        """ wait for the task to end """
        return self.instr.query('*OPC?')
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

#######
@read_only_properties('instrument', 'channel', 'functions', 'other_chan', 'dict_info', 'tag_volts', 'frequency_max', 'frequency_min', 'Vpp_max', 'Vpp_min', 'offset_max', 'offset_min', 'phase_max', 'phase_min', 'symmetry_max', 'symmetry_min', 'duty_max', 'duty_min', 'stdev_max', 'stdev_min', 'mean_max', 'mean_min', 'delay_max', 'delay_min')
class ChannelFuncGen:
    def __init__(self, instrument, channel):
        """
            Class for the channels of the function generator
        """
        self.instr = instrument   ## resource name
        self.channel = channel
        self.functions = ['SINE', 'SQUARE', 'RAMP', 'PULSE', 'NOISE', 'ARB', 'DC']  # list of allowed functions
        self.other_chan = {'CH1':'2', 'CH2':'1'}
        self.dict_info = {'WVTP':'type', 'FRQ':'frequency', 'AMP':'Vpp', 'OFST':'offset', 'PHSE':'phase', 
             'DUTY':'duty_cycle', 'SYM':'symmetry', 'DLY':'delay', 'STDEV':'stdev', 'MEAN':'mean'}
        self.tag_volts = ['Vpp', 'mean', 'stdev', 'offset']
        # instrument limits
        self.frequency_max = 5.0e6  # maximum freqeuncy in Hertz
        self.frequency_min = 1.0e-6   # minimum freqeuncy in Hertz
        self.Vpp_max = 20         # maximum peak-to-peak Voltage in V
        self.Vpp_min = 0.0004           # minimum peak-to-peak Voltage in V
        self.offset_max = 10    # maximum offset in V  
        self.offset_min = -10   # minimum offset in V
        self.phase_max = 360   # maximum phase in degrees
        self.phase_min = 0     # minimum phase in degrees
        self.symmetry_max = 100   # maximum symmetry in percentage
        self.symmetry_min = 0     # minimum symmetry in percentage
        self.duty_max = 99.9   # maximum duty cycle in percentage
        self.duty_min = 0.1     # minimum duty cycle in percentage
        self.stdev_max = 2.222   # maximum standard deviation in volts
        self.stdev_min = 0.4e-3     # minimum standard deviation in volts
        self.mean_max = 2.222   # maximum mean in volts
        self.mean_min = 0.4e-3     # minimum mean in Voltse
        self.delay_max = 1000   # maximum delay in seconds
        self.delay_min = 0     # minimum duty delay in seconds

# Basic Commands
    def state(self):
        """ return the specified channel state """
        return self.instr.query('C' + self.channel[-1] + ':OUTput?').split(' ')[1].split(',')[0]
#    
    def turn_on(self):
        """ turn the specified channel ON """
        self.instr.write('C' + self.channel[-1] + ':OUTput ON')
        return None
#
    def turn_off(self):
        """ turn the specified channel OFF """
        self.instr.write('C' + self.channel[-1] + ':OUTput OFF')
        return None
####
    def sync(self):
        """ return the specified channel sync response """
        return self.instr.query('C' + self.channel[-1] + ':SYNC?')
#
    def sync_on(self):
        """ turn the specified channel sync ON """
        self.instr.write('C' + self.channel[-1] + ':SYNC ON')
        return None
#    
    def sync_off(self):
        """ turn the specified channel sync OFF """
        self.instr.write('C' + self.channel[-1] + ':SYNC OFF')
        return None
#####
    def load(self):
        """ return the specified channel load """
        return self.instr.query('C' + self.channel[-1] + ':OUTput?')[:-1].split(',')[-1]
#    
    def set_load_hz(self):
        """ set the channel load to HZ """
        return self.instr.write('C' + self.channel[-1] + ':OUTput LOAD,HZ')
#
    def set_load_50(self):
        """ set the channel load to 50 Ohms """
        return self.instr.write('C' + self.channel[-1] + ':OUTput LOAD,50')
####
    def invert_on(self):
        """ turn the specified channel inversion ON"""
        self.instr.write('C' + self.channel[-1] + ':INVerT ON')
        return None
#    
    def invert_off(self):
        """ turn the specified channel inversion OFF """
        self.instr.write('C' + self.channel[-1] + ':INVerT OFF')
        return None   
####    
    def set_function(self, val):
        """set the function at the channel """
        val = val.upper()  # convert to upper case
        if val in self.functions:
            cmd = 'C' + self.channel[-1] + ':BSWV WVTP,' + val
            self.instr.write(cmd)
        else:
            raise ValueError('The functions must be one of those: ' + ', '.join([l.lower() for l in self.functions]))
        return None
#
    def set_frequency(self, val):
        """set the function generator frequency """
        if val <= self.frequency_max and val >= self.frequency_min:
            cmd = 'C' + self.channel[-1] + ':BSWV FRQ,' + str(float(val)) + 'Hz'
            self.instr.write(cmd)
        else: 
            raise ValueError("The frequency must be between %4.2f uHz and %4.2f MHz" % (1e6*self.frequency_min, 1e-6*self.frequency_max))                 
        return None    

    def set_Vpp(self, val):
        """set the function generator voltage peak-to-peak """
        if val <= self.Vpp_max and val >= self.Vpp_min:
            cmd = 'C' + self.channel[-1] + ':BSWV AMP,' + str(float(val)) + 'V'
            self.instr.write(cmd)
        else: 
            raise ValueError("The Vpp must be between %4.2f V and %4.2f V" % (self.Vpp_min, self.Vpp_max))                 
        return None
    
    def set_offset(self, val):
        """set the function generator offset """
        if val <= self.offset_max and val >= self.offset_min:
            cmd = 'C' + self.channel[-1] + ':BSWV OFST,' + str(float(val)) + 'V'
            self.instr.write(cmd)
        else: 
            raise ValueError("The offset must be between %4.2f V and %4.2f V" % (self.offset_min, self.offset_max))                 
        return None    
    
    def set_phase(self, val):
        """set the function generator phase """
        if val <= self.phase_max and val >= self.phase_min:
            cmd = 'C' + self.channel[-1] + ':BSWV PHSE,' + str(float(val))
            self.instr.write(cmd)
        else: 
            raise ValueError("The phase must be between %4.2f and %4.2f degrees" % (self.phase_min, self.phase_max))                 
        return None

    def set_symmetry(self, val):
        """set the function generator signal symmetry """
        if val <= self.symmetry_max and val >= self.symmetry_min:
            cmd = 'C' + self.channel[-1] + ':BSWV SYM,' + str(float(val))
            self.instr.write(cmd)
        else: 
            raise ValueError("The symmetry must be between %4.0f and %4.0f percent" % (self.symmetry_min, self.symmetry_max))                 
        return None  
    
    def set_duty(self, val):
        """set the function generator duty cycle """
        if val <= self.duty_max and val >= self.duty_min:
            cmd = 'C' + self.channel[-1] + ':BSWV DUTY,' + str(float(val))
            self.instr.write(cmd)
        else: 
            raise ValueError("The duty cycle must be between %4.0f and %4.0f percent" % (self.duty_min, self.duty_max))                 
        return None
#
    def set_mean(self, val):
        """set the function generator mean in Volts"""
        if val <= self.mean_max and val >= self.mean_min:
            cmd = 'C' + self.channel[-1] + ':BSWV MEAN,' + str(float(val)) + 'V'
            self.instr.write(cmd)
        else: 
            raise ValueError("The noise mean must be between %4.2f V and %4.2f V" % (self.mean_min, self.mean_max))                 
        return None
#
    def set_stdev(self, val):
        """set the noise function generator standard deviation in Volts"""
        if val <= self.stdev_max and val >= self.stdev_min:
            cmd = 'C' + self.channel[-1] + ':BSWV STDEV,' + str(float(val)) + 'V'
            self.instr.write(cmd)
        else: 
            raise ValueError("The standard deviation must be between %4.0f V and %4.0f V" % (self.stdev_min, self.stdev_max))                 
        return None
#    
    def set_delay(self, val):
        """set the function generator pulse delay in seconds """
        if val <= self.delay_max and val >= self.delay_min:
            cmd = 'C' + self.channel[-1] + ':BSWV DLY,' + str(float(val)) + 'S'
            self.instr.write(cmd)
        else: 
            raise ValueError("The delay must be between %4.0f s and %4.0f s" % (self.delay_min, self.delay_max))                 
        return None
#
    def wave_info(self, raw_output = False):
        """return the wave information for "channel". If raw_output = True, the output from the function is returned without processing"""
        output = self.instr.query('C' + self.channel[-1] + ':BSWV?')
        if not raw_output:
            info = output.split(' ')[-1][:-1].split(',') 
            info_tags, info_vals = info[0:][::2], info[1:][::2]
            N = len(info_tags)
            output = {}
            for n in list(range(N)):
                tag = self.dict_info[info_tags[n]]
                if tag in self.tag_volts:
                    val = float(info_vals[n][:-1])
                elif tag == 'frequency':
                    val = float(info_vals[n][:-2])
                elif tag == 'type': val = info_vals[n].lower()
                else: val = float(info_vals[n])
                output[tag] = val
        return output
#          
    def copy_to(self):
        """
            copy the parameters to this channel from the other channel 
        """
        self.instr.write('PAraCoPy C' + self.other_chan[self.channel] + ',C' + self.channel[-1])
        return None
#          
    def copy_from(self):
        """
            copy the parameters from this channel to the other channel 
        """
        self.instr.write('PAraCoPy C' + self.channel[-1] + ',C' + self.other_chan[self.channel])
        return None


