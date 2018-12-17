# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 16:36:20 2018

@author: Ben
"""

import numpy as np
import statistics
import struct
import visa
import nidaqmx

class gpib_instrument:

    def __init__(self, addr):
        addr_str = 'GPIB0::'+str(addr)+'::INSTR'
        self.instr = visa.ResourceManager().open_resource(addr_str)
    
    def write(self, message, return_output = 0):
        # message = str
        # return_output = 1 to return the instrument's response
        if return_output:
            return self.instr.write(message)
        else:
            self.instr.write(message)
        
    def query(self, message):
        # message = str
        return self.instr.query(message)
    
    def write_raw(self, message, return_output = 0):
        # message = bytes
        if return_output:
            return self.instr.write_raw(message)
        else:
            self.instr.write_raw(message)

    def read_raw(self):
        # message = str
        return self.instr.read_raw()

    def set_timeout(self,timeout):
        # sets timeout (in milliseconds)
        # timeout = float
        self.instr.timeout = timeout



"""
*******************************************************************************
*******************************************************************************
"""

class keysight_n5183b(gpib_instrument):
    
    def __init__(self, addr):
        # inherit all the methods of gpib_instrument class
        super().__init__(addr)

    def set_frequency(self, freq):
        #freq = float
        message = ':freq '+str(freq)
        self.write(message)
        
    def set_power(self, power, units = 'dbm'):
        # power = float
        # units = str
        #   options: 'dbm', 'mv', 'dBuV', 'dBuVemf', 'uV', 'mVemf', 'uVemf'
        message = ':pow '+str(power)+units
        self.write(message)
        
    def set_phase(self, phase, units = 'rad'):
        # phase = float
        # units = str: 'rad' or 'deg'
        message = ':phas '+str(phase)+units
        self.write(message)
        
    def toggle_output(self, state):
        # turns RF output on or off
        # state = 0,1 (off,on)
        message = ':outp '+str(state)
        self.write(message)
        
    def toggle_modulation(self, state):
        # turns modulation on or off
        # state = 0,1 (off,on)
        message = ':outp:mod '+str(state)
        self.write(message)
        
    def toggle_pulse_mode(self, state):
        # turns pulse mode on or off
        # state = 0,1 (off,on)
        message = ':pulm:stat '+str(state)
        self.write(message)

    def toggle_alc(self, state):
        # turns on and off automatic leveling control
        #   - useful for ultra-narrow-width (UNW) pulse generation
        # state = 0,1 (off,on)
        message = ':pow:alc '+str(state)
        self.write(message)
        
    def set_pulse_source(self, source):
        # sets the source for the pulse modulation tone
        # source = str
        #   options:
        #       'ext'   -external pulse modulates output
        #       'trig'  -internal source, triggered
        #       'frun'  -internal source, free run
        #       'ado'   -internal source, see manual
        #       'doub'  -internal source, see manual
        #       'gate'  -internal source, see manual
        #       'ptr'   -internal source, see manual
        if source == 'ext':
            message = 'pulm:sour '+source
        else:
            message = 'pulm:sour:int '+source
                
        self.write(message)

    def set_pulse_delay(self, delay, units='s'):
        # sets pulse delay
        # delay = float
        # units = str: 's','us','ns'
        message = ':pulm:int:del '+str(delay)+units
        self.write(message)
        
    def set_pulse_width(self, width, units='s'):
        # sets pulse delay
        # width = float
        # units = str: 's','us','ns'
        message = ':pulm:int:pwid '+str(width)+units
        self.write(message)

"""
*******************************************************************************
*******************************************************************************
"""    
    
class agilent_e8257c(gpib_instrument):
    # SIGNAL GENERATOR
    
    def __init__(self, addr):
        # inherit all the methods of gpib_instrument class
        super().__init__(addr)

    def toggle_output(self, state):
        # turns output off or on
        # state = 0,1 (off,on)
        message = ':outp '+str(state)
        self.write(message)
        
    def toggle_modulation(self, state):
        # turns modulation off or on
        # state = 0,1 (off,on)
        message = ':outp:mod '+str(state)
        self.write(message)
    
    def set_frequency(self, freq, units = 'Hz'):
        # set the frequency
        # freq = float , scientific notation OK
        # units = str: 'Hz', 'kHz', 'MHz', 'GHz' all OK
        message = ':freq '+str(freq)+units
        self.write(message)
        
    def set_phase(self, phase, units = 'rad'):
        # phase = float
        # units = str: 'rad' or 'deg'
        message = ':phas '+str(phase)+units
        self.write(message)
        
    def toggle_alc(self, state):
        # turns automatic leveling control off,on
        # state = 0,1 (off,on)
        message = ':pow:alc '+str(state)
        self.write(message)
        
    def set_power(self, power, units = 'dbm'):
        # power = float
        # units = str
        #   options: 'dbm', 'mv', 'dBuV', 'dBuVemf', 'uV', 'mVemf', 'uVemf'
        message = ':pow '+str(power)+units
        self.write(message)
        
    def toggle_pulse_mode(self, state):
        # turns pulse mode on or off
        # state = 0,1 (off,on)
        message = ':pulm:stat '+str(state)
        self.write(message)

    def set_pulse_source(self, source):
        # sets the source for the pulse modulation tone
        # source = str
        #   options:
        #       'ext'   -external pulse modulates output
        #       'squ'   -internal source, square
        #       'trig'  -internal source, triggered
        #       'frun'  -internal source, free run
        #       'doub'  -internal source, see manual
        #       'gate'  -internal source, see manual
        if source == 'ext':
            message = 'pulm:sour '+source
        else:
            message = 'pulm:sour:int '+source
                
        self.write(message)

    def set_pulse_delay(self, delay, units='s'):
        # sets pulse delay
        # delay = float
        # units = str: 's','us','ns'
        message = ':pulm:int:del '+str(delay)+units
        self.write(message)
        
    def set_pulse_width(self, width, units='s'):
        # sets pulse delay
        # width = float
        # units = str: 's','us','ns'
        message = ':pulm:int:pwid '+str(width)+units
        self.write(message)


"""
*******************************************************************************
*******************************************************************************
"""    

class hp_83711b(gpib_instrument):
    # SIGNAL GENERATOR
    
    def __init__(self, addr):
        # inherit all the methods of gpib_instrument class
        super().__init__(addr)

    def set_frequency(self, freq, units = 'Hz'):
        # set the frequency
        # freq = float , scientific notation OK
        # units = str: 'Hz', 'kHz', 'MHz', 'GHz' all OK
        message = 'freq '+str(freq)+units
        self.write(message)

    def set_power(self, power, units = 'dBm'):
        # set the power
        # power = float
        # units = str: 'dBm', 'mV', 'V', etc.
        message = 'pow '+str(power)+units
        self.write(message)

    def toggle_output(self, state):
        # turns output off or on
        # state = 0,1 (off,on)
        message = 'outp '+str(state)
        self.write(message)


"""
*******************************************************************************
*******************************************************************************
"""    

class hp_8648c(gpib_instrument):
    # SIGNAL GENERATOR
    
    def __init__(self, addr):
        super().__init__(addr)

    def set_frequency(self, freq, units='Hz'):
        message = ':freq ' + str(freq) + units
        self.write(message)

    def toggle_output(self, state):
        message = 'outp ' + str(state)
        self.write(message)

    def set_power(self, power, units='dBm'):
        message = 'pow ' + str(power) + units
        self.write(message)

"""
*******************************************************************************
*******************************************************************************
"""    

class hp_34401a(gpib_instrument):
    # MULTIMETER
    
    def __init__(self, addr):
        super().__init__(addr)

    def get_voltage(self):
        message = 'meas:volt:dc?'
        return float(self.query(message))

"""
*******************************************************************************
*******************************************************************************
"""    

class agilent_e3634a(gpib_instrument):
    # DC POWER SUPPLY
    
    def __init__(self, addr):
        super().__init__(addr)

    def toggle_output(self, state):
        message = 'outp ' + str(state)
        self.write(message)

    def apply(self, voltage, current, v_units='V', i_units='A'):
        message = 'appl ' + str(voltage) + v_units + ', ' + str(current) + i_units
        self.write(message)

    def set_voltage(self, voltage, units='V'):
        message = 'volt ' + str(voltage) + units
        self.write(message)

    def set_current(self, current, units='A'):
        message = 'curr ' + str(current) + units
        self.write(message)

    def measure_voltage(self):
        message = 'meas:volt?'
        return self.query(message)

    def measure_current(self):
        message = 'meas:curr?'
        return self.query(message)

"""
*******************************************************************************
*******************************************************************************
"""    

class agilent_e4404b(gpib_instrument):
    # SPECTRUM ANALYZER
    # ONLY TESTED FOR 4408B, SHOULD BE THE SAME
    
    def __init__(self, addr):
        # inherit all the methods of gpib_instrument class
        super().__init__(addr)
        
    def abort(self):
        message = ':abor'
        self.write(message)

    def force_trigger(self):
        message = '*trg'
        self.write(message)

    def toggle_coupling(self, state):
        if state:
            cpl_str = 'all'
        else:
            cpl_str = 'none'
        message = ':coup ' + cpl_str
        self.write(message)

    def toggle_continuous_sweep(self, state):
        message = ':init:cont ' + str(state)
        self.write(message)

    def restart(self):
        message = ':init:rest'
        self.write(message)

    def set_input_coupling(self, coupling_str):
        message = ':inp:coup ' + coupling_str
        self.write(message)

    def toggle_averaging(self, state):
        message = ':aver ' + str(state)
        self.write(message)

    def set_averaging(self, counts):
        message = ':aver:count ' + str(counts)
        self.write(message)

    def set_averaging_type(self, type_str):
        message = ':aver:type ' + type_str
        self.write(message)

    def set_resolution_bandwidth(self, bandwidth, units='Hz'):
        message = ':band ' + str(bandwidth) + units
        self.write(message)

    def get_resolution_bandwidth(self):
        message = ':band?'
        return float(self.query(message))

    def toggle_automatic_resolution_bandwidth(self, state):
        message = ':band:auto ' + str(state)
        self.write(message)

    def set_video_bandwidth(self, bandwidth, units='Hz'):
        message = ':band:vid ' + str(bandwidth) + units
        self.write(message)

    def get_video_bandwidth(self):
        message = ':band:vid?'
        return float(self.query(message))

    def toggle_automatic_video_bandwidth(self, state):
        message = ':band:vid:auto ' + str(state)
        self.write(message)

    def set_detection_type(self, type_str):
        message = ':det ' + type_str
        self.write(message)

    def set_frequency_center(self, frequency, units='Hz'):
        message = ':freq:cent ' + str(frequency) + units
        self.write(message)

    def set_frequency_span(self, frequency, units='Hz'):
        message = ':freq:span ' + str(frequency) + units
        self.write(message)

    def set_frequency_start(self, frequency, units='Hz'):
        message = ':freq:star ' + str(frequency) + units
        self.write(message)

    def set_frequency_stop(self, frequency, units='Hz'):
        message = ':freq:stop ' + str(frequency) + units
        self.write(message)

    def set_freqs(self, freq1, freq2, interval='range', channel=None):
        if interval == 'range':
            self.set_frequency_start(freq1)
            self.set_frequency_stop(freq2)
        else:
            if interval == 'span':
                self.set_frequency_center(freq1)
                self.set_frequency_span(freq2)
            else:
                print('ERROR: Invalid Interval Type!')

    def set_sweep_points(self, num_points):
        message = ':swe:poin ' + str(num_points)
        self.write(message)

    def get_trace_data(self, convert=True):
        message = ':trac? trace1'
        trace = self.query(message)
        if convert:
            trace = trace.split(',')
            trace = [float(ii) for ii in trace]
        return trace

"""
*******************************************************************************
*******************************************************************************
"""    

class agilent_e4408b(gpib_instrument):
    # SPECTRUM ANALYZER
    
    def __init__(self, addr):
        # inherit all the methods of gpib_instrument class
        super().__init__(addr)

    def abort(self):
        message = ':abor'
        self.write(message)

    def force_trigger(self):
        message = '*trg'
        self.write(message)

    def toggle_coupling(self, state):
        if state:
            cpl_str = 'all'
        else:
            cpl_str = 'none'
        message = ':coup ' + cpl_str
        self.write(message)

    def toggle_continuous_sweep(self, state):
        message = ':init:cont ' + str(state)
        self.write(message)

    def restart(self):
        message = ':init:rest'
        self.write(message)

    def set_input_coupling(self, coupling_str):
        message = ':inp:coup ' + coupling_str
        self.write(message)

    def toggle_averaging(self, state):
        message = ':aver ' + str(state)
        self.write(message)

    def set_averaging(self, counts):
        message = ':aver:count ' + str(counts)
        self.write(message)

    def set_averaging_type(self, type_str):
        message = ':aver:type ' + type_str
        self.write(message)

    def set_resolution_bandwidth(self, bandwidth, units='Hz'):
        message = ':band ' + str(bandwidth) + units
        self.write(message)

    def get_resolution_bandwidth(self):
        message = ':band?'
        return float(self.query(message))

    def toggle_automatic_resolution_bandwidth(self, state):
        message = ':band:auto ' + str(state)
        self.write(message)

    def set_video_bandwidth(self, bandwidth, units='Hz'):
        message = ':band:vid ' + str(bandwidth) + units
        self.write(message)

    def get_video_bandwidth(self):
        message = ':band:vid?'
        return float(self.query(message))

    def toggle_automatic_video_bandwidth(self, state):
        message = ':band:vid:auto ' + str(state)
        self.write(message)

    def set_detection_type(self, type_str):
        message = ':det ' + type_str
        self.write(message)

    def set_frequency_center(self, frequency, units='Hz'):
        message = ':freq:cent ' + str(frequency) + units
        self.write(message)

    def set_frequency_span(self, frequency, units='Hz'):
        message = ':freq:span ' + str(frequency) + units
        self.write(message)

    def set_frequency_start(self, frequency, units='Hz'):
        message = ':freq:star ' + str(frequency) + units
        self.write(message)

    def set_frequency_stop(self, frequency, units='Hz'):
        message = ':freq:stop ' + str(frequency) + units
        self.write(message)

    def set_freqs(self, freq1, freq2, interval='range', channel=None):
        if interval == 'range':
            self.set_frequency_start(freq1)
            self.set_frequency_stop(freq2)
        else:
            if interval == 'span':
                self.set_frequency_center(freq1)
                self.set_frequency_span(freq2)
            else:
                print('ERROR: Invalid Interval Type!')

    def set_sweep_points(self, num_points):
        message = ':swe:poin ' + str(num_points)
        self.write(message)

    def get_trace_data(self, convert=True):
        message = ':trac? trace1'
        trace = self.query(message)
        if convert:
            trace = trace.split(',')
            trace = [float(ii) for ii in trace]
        return trace

"""
*******************************************************************************
*******************************************************************************
"""    

class agilent_e5071c(gpib_instrument):
    # NETWORK ANALYZER
    
    def __init__(self, addr):
        # inherit all the methods of gpib_instrument class
        super().__init__(addr)
    
    ####################
    # DISPLAY SETTINGS #
    ####################
    
    def allocate_channels(self, alloc_str):
        # splits the display into separate windows
        # channel_str = str
        #   options:
        #       '1'    - one graph in full window
        #       '12'   - two graphs split left/right
        #       '1_2'  - two graphs split top/bottom
        #   see manual for more complicated allocations
        # NOTE: the argument given in the manual has a 'D' in front - this is
        #   handled internally by this method
        message = ':disp:spl D' + alloc_str
        self.write(message)

    def set_channel(self,channel):
        # sets active channel
        # channel = int
        message = ':disp:wind'+str(channel)+':act'
        self.write(message)

    def query_channel(self):
        # queries the currently active channel
        # returns the channel as an int
        message = ':serv:chan:act?'
        channel = self.query(message)
        return int(channel)
        
    def set_num_traces(self, num_traces, channel = None):
        # sets the total number of traces present on channel
        # num_traces = int
        # channel = int: if unspecified, defaults to current channel
        if not channel:
            channel = self.query_channel()
        message = ':calc'+str(channel)+':par:coun '+str(num_traces)
        self.write(message)
        
    def query_num_traces(self, channel = None):
        # queries the total number of traces present on channel
        # if channel is unspecified, defaults to the current channel
        if not channel:
            channel = self.query_channel()
        message = ':calc'+str(channel)+':par:coun?'
        num_traces = self.query(message)
        return int(num_traces)   
    
    def allocate_traces(self, alloc_str, channel = None):
        # splits the layout of traces on a given channel
        # if channel is unspecified, defaults to the current channel
        # alloc_str = str
        #   options:
        #       '1'    - one graph in full window
        #       '12'   - two graphs split left/right
        #       '1_2'  - two graphs split top/bottom
        #   see manual for more complicated allocations
        # NOTE: the argument given in the manual has a 'D' in front - this is
        # handled internally by this method
        if not channel:
            channel = self.query_channel()
        message = ':disp:wind'+str(channel)+':spl D'+alloc_str
        self.write(message)
        
    def set_trace(self, trace, channel = None):
        # sets active trace of a given channel
        # if channel is not given, then the current channel is assumed
        # trace = int
        # channel = int
        if not channel:
            channel = self.query_channel()
        message = ':calc'+str(channel)+':par'+str(trace)+':sel'
        self.write(message)
    
    def query_trace(self, channel = None):
        # queries the active trace on channel
        # channel = int
        # if channel unspecified, defaults to current channel
        # returns trace as an int
        if not channel:
            channel = self.query_channel()
        message = ':serv:chan'+str(channel)+':trac:act?'
        trace = self.query(message)
        return int(trace)
    
    def autoscale(self, channel = None, trace = None):
        # autoscales a given trace on a given channel
        # if channel/trace unspecified, defaults to current
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace(channel)
        message = ':disp:wind'+str(channel)+':trac'+str(trace)+':y:auto'
        self.write(message)
    
    ###########
    # MARKERS #
    ###########
    # NOTE: MARKER 10 IS THE REFERENCE MARKER
    
    def toggle_marker(self, marker, state, channel = None):
        # turns marker for a given channel on or off
        # if channel unspecified, defaults to current
        # marker = int
        # state = 0,1 (off,on)
        if not channel:
            channel = self.query_channel()
        message = ':calc'+str(channel)+':mark'+str(marker)+' '+str(state)
        self.write(message)
        
    def move_marker(self, marker, freq, channel = None):
        # move a marker for a given channel to a given frequency
        # if channel unspecified, defaults to current
        # marker = int
        # freq = float (scientific notation OK)
        if not channel:
            channel = self.query_channel()
        message = ':calc'+str(channel)+':mark'+str(marker)+':x '+str(freq)
        self.write(message)
        
    def activate_marker(self, marker, channel = None):
        # activate a marker for a given channel
        # if channel unspecified, defaults to current
        if not channel:
            channel = self.query_channel()
        message = ':calc'+str(channel)+':mark'+str(marker)+':act'
        self.write(message)
        
    def marker_search(self, marker, type_str, channel = None, trace = None):
        # executes marker search type for marker on trace on channel
        # if channel/trace unspecified, defaults to current
        # marker = int
        # type_str = str
        #   options:
        #       'min'   - minimum
        #       'max'   - maximum
        #       'peak'  - peak
        #       'lpe'   - peak to the left
        #       'rpe'   - peak to the right
        #       'targ'  - target
        #       'ltar'  - target to the left
        #       'rtar'  - target to the right
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace()
        message = ':calc'+str(channel)+':trac'+str(trace)+':mark'+str(marker) \
                        +':func' 
        self.write(message+':type '+type_str)
        self.write(message+':exec')
        
    def marker_track(self, marker, type_str, channel = None, trace = None):
        # performs a marker search every sweep according to the type specified
        # if channel/trace unspecified, defaults to current
        # marker = int
        # type_str = str
        #   options:
        #       'min'   - minimum
        #       'max'   - maximum
        #       'peak'  - peak
        #       'lpe'   - peak to the left
        #       'rpe'   - peak to the right
        #       'targ'  - target
        #       'ltar'  - target to the left
        #       'rtar'  - target to the right
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace()
        message = ':calc'+str(channel)+':trac'+str(trace)+':mark'+str(marker) \
                        +':func' 
        self.write(message+':type '+type_str)
        self.toggle_marker_tracking(marker, 1, channel, trace)
        
    def toggle_marker_tracking(self, marker, state, channel = None, \
                               trace = None):
        # toggles tracking for a given marker
        # marker = int
        # state = 0,1 (off,on)
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace()
        message = ':calc'+str(channel)+':trac'+str(trace)+':mark'+str(marker) \
                            +':func:trac '+str(state)
        self.write(message)
        
    def toggle_marker_search_range(self, state, channel = None, trace = None):
        # toggles whether to use a manual search range
        # state = 0,1 (off,on)
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace()
        message = ':calc'+str(channel)+':trac'+str(trace) \
                        +':mark:func:dom '+str(state)
        self.write(message)
    
    def set_marker_search_start(self, freq, channel = None, trace = None):
        # sets the starting frequency of the marker search domain
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace()
        message = ':calc'+str(channel)+':trac'+str(trace) \
                        +':mark:func:dom:star '+str(freq)
        self.write(message)
            
    def set_marker_search_stop(self, freq, channel = None, trace = None):
        # sets the starting frequency of the marker search domain
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace()
        message = ':calc'+str(channel)+':trac'+str(trace) \
                        +':mark:func:dom:stop '+str(freq)
        self.write(message)
        
    def toggle_bandwidth_search(self, state, channel = None, trace = None):
        # toggles bandwidth search mode
        # state = 0,1 (off,on)
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace()
        message = ':calc'+str(channel)+':trac'+str(trace)+':mark:bwid ' \
                    +str(state)
        self.write(message)
        
    def set_bandwidth_threshold(self, marker, threshold, \
                                    channel = None, trace = None):
        # sets the threshold for determining bandwidth
        # threshold = float : +/- 3dB usually
        # marker = int
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace()
        message = ':calc'+str(channel)+':trac'+str(trace)+':mark'+str(marker) \
                    +':bwid:thr '+str(threshold)
        self.write(message)
    
    def track_resonance(self, marker = 1, channel = None, trace = None):
        # track resonance in the current window, find 3dB points and Q
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace()
        self.toggle_bandwidth_search(1, channel, trace)
        self.set_bandwidth_threshold(marker, +3, channel, trace)
        self.toggle_marker(marker, 1, channel)
        self.activate_marker(marker, channel)
        self.marker_track(marker, 'min', channel, trace)

    ########################
    # MEASUREMENT SETTINGS #
    ########################
    
    def toggle_output(self, state):
        # turns RF Out off or on
        # state = 0,1 (off,on)
        message = ':outp '+str(state)
        self.write(message)
    
    def set_measurement(self, meas_str, channel = None, trace = None):
        # sets the measurement carried out by a trace on a channel
        # meas_str = str
        #   options:
        #       'S11' - reflection on port 1
        #       'S21' - transmission to port 2 from port 1
        #       'S12' - transmission to port 1 from port 2
        #       'S22' - reflection on port 2
        #   see manual for others
        # channel = int
        # trace = int
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace()
        message = ':calc'+str(channel)+':par'+str(trace)+':def '+meas_str
        self.write(message)

    def query_measurement(self, channel = None, trace = None):
        # queries the current measurement carried out by a trace on a channel
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace()
        message = ':calc'+str(channel)+':par'+str(trace)+':def?'
        meas_str = self.query(message)
        return meas_str[:-1]
        
    def set_sweep_type(self, type_str, channel = None):
        # sets the type of sweep on a given channel
        # if channel not specified, defaults to current channel
        # type_str = str
        #   options:
        #       'lin' - linear frequency sweep
        #       'log' - logarithmic frequency sweep
        #       'segm' - segment sweep
        #       'pow' - power sweep
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':swe:type '+type_str
        self.write(message)
        
    def query_sweep_type(self, channel = None):
        # queries type of sweep on channel
        # if channel not specified, defaults to current
        # channel = int
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':swe:type?'
        type_str = self.query(message)
        return type_str[:-1]
    
    def set_sweep_mode(self, mode_str, channel = None):
        # sets sweep mode of a channel
        # if channel unspecified, defaults to current
        # channel = int
        # mode_str = str
        #   options (only caps part necessary):
        #       'STEPped'   - stepped mode
        #       'ANALog'    - swept mode
        #   manual specified a couple more options that don't seem to do
        #   anything for this model network analyzer
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':swe:gen '+mode_str
        self.write(message)

    def query_sweep_mode(self, channel = None):
        # queries sweep mode of a channel
        # if channel unspecified, defaults to current
        # channel = int
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':swe:gen?'
        mode_str = self.query(message)
        return mode_str[:-1]

    def set_sweep_points(self, points, channel = None):
        # sets the number of points in the sweep on the specified channel
        # if channel unspecified, defaults to current
        # points = int
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':swe:poin '+str(points)
        self.write(message)

    def set_frequency_start(self, freq, channel = None):
        # sets the start frequency of the sweep on a channel
        # if channel unspecified, defaults to current
        # freq = float: frequency in Hz
        #               scientific notation also OK
        # channel = int
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':freq:star '+str(freq)
        self.write(message)
        
    def set_frequency_stop(self, freq, channel = None):
        # sets the stop frequency of the sweep on a channel
        # if channel unspecified, defaults to current
        # freq = float: frequency in Hz
        #               scientific notation also OK
        # channel = int
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':freq:stop '+str(freq)
        self.write(message)
        
    def set_frequency_center(self, freq, channel = None):
        # sets the center frequency of the sweep on a channel
        # if channel unspecified, defaults to current
        # freq = float: frequency in Hz
        #               scientific notation also OK
        # channel = int
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':freq:cent '+str(freq)
        self.write(message)
        
    def set_frequency_span(self, freq, channel = None):
        # sets the center frequency of the sweep on a channel
        # if channel unspecified, defaults to current
        # freq = float: frequency in Hz
        #               scientific notation also OK
        # channel = int
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':freq:span '+str(freq)
        self.write(message)
        
    def set_freqs(self, freq1, freq2, interval_type = 'range', channel = None):
        # sets a frequency interval according to the type
        # interval_type = str: 'range' or 'span'
        #   if range:
        #       freq1 = start
        #       freq2 = stop
        #   if span:
        #       freq1 = center
        #       freq2 = span
        # freq1,2 = float
        if not channel:
            channel = self.query_channel()
        if interval_type == 'range':
            self.set_frequency_start(freq1,channel)
            self.set_frequency_stop(freq2,channel)
        elif interval_type == 'span':
            self.set_frequency_center(freq1,channel)
            self.set_frequency_span(freq2,channel)
        else:
            print('ERROR: Invalid Interval Type!')
        
    def set_IF_bandwidth(self, bandwidth, channel = None):
        # sets the IF bandwidth of a given channel
        #   -can affect noisiness of measurements - see manual
        # if channel unspecified, defaults to current
        # bandwidth = float (frequency in Hz - scientific notation OK)
        # channel = int
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':band '+str(bandwidth)
        self.write(message)
        
    def set_power(self, power, channel = None):
        # sets the power output of a given channel
        # if channel unspecified, defaults to current
        # power = float: power in dBm
        if not channel:
            channel = self.query_channel()
        message = ':sour'+str(channel)+':pow '+str(power)
        self.write(message)
                
    def set_format(self, format_str, channel = None, trace = None):
        # sets the measurement format of a given trace on a given channel
        # if channel/trace not specified, defaults to current
        # format_str = str
        #   options:
        #       'MLOGarithmic'  - logarithmic magnitude
        #       'PHASe'         - Phase
        #       'UPHase'        - Expanded phase
        #       'SMITh'         - Smith chart: R+jX (resistance/reactance)
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace(channel)
        message = ':calc'+str(channel)+':trac'+str(trace)+':form '+format_str
        self.write(message)
    
    def query_format(self, channel = None, trace = None):
        # queries the format of a given troce on a given channel
        # if channel/trace not specified, defaults to current
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace(channel)
        message = ':calc'+str(channel)+':trac'+str(trace)+':form?'
        format_str = self.query(message)
        return format_str[:-1]
    
    def set_electrical_delay(self, delay, channel = None, trace = None):
        # sets the electrical delay for phase measurements
        # if channel/trace unspecified, defaults to current
        # delay = float: time in seconds (scientific notation OK)
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace(channel)
        message = ':calc'+str(channel)+':trac'+str(trace)+':corr:edel:time ' \
                        + str(delay)
        self.write(message)

    #####################
    # AVERAGING SETINGS #
    #####################
    
    def toggle_averaging(self, state, channel = None):
        # toggle averaging on or off for a given channel
        # if channel unspecified, defaults to current
        # state = int: 0 or 1 (off or on)
        # channel = int
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':aver '+str(state)
        self.write(message)
        
    def set_averaging(self, factor, channel = None):
        # set averaging factor for a given channel
        # if channel unspecified, defaults to current
        # factor = int
        # channel = int
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':aver:coun '+str(factor)
        self.write(message)
        
    def restart_averaging(self, channel = None):
        # restarts averaging on a given channel
        # if channel not specified, defaults to current
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':aver:cle'
        self.write(message)
        
    def toggle_averaging_trigger(self, state):
        # toggles averaging on trigger initiation
        # usage: collect the avg of many traces after a single trigger
        # state = 0,1 (off,on)
        message = ':trig:aver '+str(state)
        self.write(message)
    
    ####################
    # TRIGGER SETTINGS #
    ####################

    def toggle_continuous_triggering(self, state, channel = None):
        # turns continuous triggering mode on or off for a given channel
        # if channel unspecified, defaults to current
        # state = 0,1 (off,on)
        if not channel:
            channel = self.query_channel()
        message = ':init'+str(channel)+':cont '+str(state)
        self.write(message)
        
    def set_trigger_source(self, source_str):
        # sets the source of triggers
        # source_str = str
        #   options:
        #       'int' - internal (always on, I think, so no real control)
        #       'ext' - external (back panel)
        #       'man' - manual (use this one for taking data)
        #       'bus' - bus (just responds to '*TRG' SCPI command - useless?)
        message = ':trig:sour '+source_str
        self.write(message)

    def set_trigger_scope(self, scope_str):
        # sets whether all channels or just the active channel are triggered
        # scope_str = str: 'all' or 'act'
        message = ':trig:scop '+scope_str
        self.write(message)

    def trigger(self, wait = True):
        # triggers a single measurement
        # can be used in conjunction with a query of '*OPC?' to see when
        #   the measurement has completed
        # wait = 0,1 or False,True
        #   if 1: waits for operation to complete before returning
        message = ':trig:sing'
        self.write(message)
        if wait:
            return self.query('*OPC?')

    ################
    # INPUT/OUTPUT #
    ################

    def transfer_data_to_memory(self, channel = None, trace = None):
        # transfers data trace to memory trace (so it is not overwritten by
        #   subsequent datasets until calling this function again)
        # if channel/trace unspecified, default to current
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace(channel)
        message = ':calc'+str(channel)+':trac'+str(trace)+':math:mem'
        self.write(message)
        
    def get_trace_data(self, channel = None, trace = None, \
                               convert = True):
        # gets data from the memory trace on the VNA and returns a local copy
        # if channel/trace unspecified, defaults to current
        # if convert is true, will return the trace data in an array of
        #   floats (or complex numbers in the case of a smith chart)
        # NOTE: DOESN'T NECESSARILY SUPPORT ALL TRACE FORMATS CURRENTLY
        if not channel:
            channel = self.query_channel()
        if not trace:
            trace = self.query_trace(channel)
        message = ':calc'+str(channel)+':trac'+str(trace)+':data:fmem?'
        data_str = self.query(message)

        format_str = self.query_format(channel,trace)
        data_list = data_str.split(',')
        return_list = []
        for ii in range(len(data_list)//2):
            if format_str == 'SMIT':
                resistance = float(data_list[2*ii])
                reactance = float(data_list[((2*ii)+1)])
                if convert:
                    return_list.append(complex(resistance,reactance))
                if not convert:
                    return_list.append(str(complex(resistance,reactance)))
                    return_str = ','.join(return_list)
            else:
                if convert:
                    return_list.append(float(data_list[2*ii]))
                else:
                    return_list.append(data_list[2*ii])
                    return_str = ','.join(return_list)
        if convert:
            return return_list
        else:
            return return_str

            
    def get_frequency_data(self, channel = None, convert = True):
        # gets all the frequency points for a given channel
        # if convert to floats, will return the trace data
        if not channel:
            channel = self.query_channel()
        message = ':sens'+str(channel)+':freq:data?'
        freq_str = self.query(message)
        if convert:
            freq_list = freq_str.split(',')
            freq_list = [float(ii) for ii in freq_list]
            return freq_list
        else:
            return freq_str[:-1]
        
    def get_parameters(self):
        # return all parameters relevant for interpreting trace data
        # power, averaging, electrical delay, format, Sij,
        pass
       
"""
*******************************************************************************
*******************************************************************************
"""      
    
class tektronix_tds7704b(gpib_instrument):
    # OSCILLOSCOPE
    
    def __init__(self, addr):
        super().__init__(addr)

    def toggle_channel(self, channel, state):
        # turns a channel on or off
        # channel = int: 1-4
        # state = 0,1 (off,on)
        message = 'sel:ch' + str(channel) + ' ' + str(state)
        self.write(message)

    def set_coupling(self, channel, coupling_string):
        # sets the coupling for a given channel
        # channel = int: 1-4
        # coupling_string = str: 'dc' or 'gnd'
        message = 'ch' + str(channel) + ':coup ' + coupling_string
        self.write(message)

    #################
    # VERTICAL AXIS #
    #################
    
    def set_vertical_offset(self, channel, offset):
        # sets the offset of a given channel in volts
        # channel = int: 1-4
        # offset = float: in volts, scientific notation OK
        message = 'ch' + str(channel) + ':offs ' + str(offset)
        self.write(message)

    def set_vertical_position(self, channel, divisions):
        # sets the vertical position in divisions
        # channel = int: 1-4
        # divisions = float
        message = 'ch' + str(channel) + ':pos ' + str(divisions)
        self.write(message)

    def set_vertical_scale(self, channel, scale):
        # sets the vertical scale in volts per division
        # channel = int: 1-4
        # scale = float: volts per division, scientific notation OK
        message = 'ch' + str(channel) + ':sca ' + str(scale)
        self.write(message)
        
    ###################
    # HORIZONTAL AXIS #
    ###################
    
    def toggle_horizontal_delay(self, state):
        # turn trigger delay on or off
        # state = 0,1 (off,on)
        message = 'hor:del:mod '+str(state)
        self.write(message)
        
    def set_horizontal_delay(self, delay):
        # sets the trigger delay in seconds
        # delay = float: in seconds, scientific notation OK
        message = 'hor:del:tim '+str(delay)
        self.write(message)
        
    def set_horizontal_position(self, position):
        # sets the horizontal position of the trigger
        # like delay, but when delay is not toggled
        # probably not too useful for actual data collection
        # position = float: percentage of window
        message = 'hor:pos '+str(position)
        self.write(message)
        
    def set_horizontal_reference(self, ref):
        # sets the reference point of the horizontal window
        #   trigger point + delay falls at this point in the horizontal window
        # ref = float: percentage of window, 0 to 100
        message = 'hor:del:pos '+str(ref)
        self.write(message)
        
    def set_horizontal_samplerate(self, rate):
        # NOT INDEPENDENT: AFFECTED BY RECORD LENGTH AND SCALE
        # sets the sample rate in Hz
        # rate = float: in Hz, scientific notation OK
        message = 'hor:mai:sampler '+str(rate)
        self.write(message)
        
    def set_horizontal_scale(self, scale):
        # NOT INDEPENDENT: AFFECTED BY SAMPLE RATE AND RECORD LENGTH
        # sets horizontal scale in seconds per division
        # scale = float: in seconds/division, scientific notation OK
        message = 'hor:sca '+str(scale)
        self.write(message)
        
    def set_horizontal_record_length(self, samples):
        # NOT INDEPENDENT: AFFECTED BY SAMPLE RATE AND SCALE
        # sets number of samples in a record
        # samples = int
        message = 'hor:reco '+str(samples)
        self.write(message)

    ########################
    # ACQUISITION SETTINGS #
    ########################
    
    def toggle_single_acquisition(self, state):
        # turn single acquisition off or on (off means continuous acquisition)
        # state = 0,1 (off,on)
        if state:
            mode_str = 'seq'
        else:
            mode_str = 'runst'
        message = 'acq:stopa '+mode_str
        self.write(message)
    
    def set_acquisition_sampling_mode(self, mode_str):
        # sets the type of sampling
        # mode_str = str:
        #   options:
        #       'rt'    - real time
        #       'it'    - interpolated time
        #       'et'    - equivalent time
        message = 'acq:samp '+mode_str
        self.write(message)

    ######################
    # FASTFRAME SETTINGS #
    ######################
    
    def toggle_fastframe(self, state):
        # turn fastframe off or on
        # state = int: 0,1 (off,on)
        message = 'hor:fast:state '+str(state)
        self.write(message)
    
    def set_frame_count(self, count):
        # sets the number of frames to acquire
        # count: int
        message = 'hor:fast:coun '+str(count)
        self.write(message)

    def set_frame_record_length(self, samples):
        # sets the number of samples in each frame
        # samples = int
        message = 'hor:fast:len '+str(samples)
        self.write(message)

    ####################
    # TRIGGER SETTINGS #
    ####################

    def force_trigger(self):
        # force a trigger event
        message = 'trig forc'
        self.write(message)

    def toggle_auto_trigger(self, state):
        # turn auto trigger off or on
        # state = int: 0,1 (off,on)
        if state:
            mode_str = 'auto'
        else:
            mode_str = 'norm'
        message = 'trig:a:mod '+mode_str
        self.write(message)

    def set_trigger_coupling(self, coupling_str):
        # sets the coupling of the main trigger
        # coupling_str = str
        # options: 'ac','dc', see manual for others
        message = 'trig:a:edge:coup '+coupling_str
        self.write(message)

    def set_trigger_slope(self, slope_str):
        # sets whether the trigger event is on a rising or falling edge
        # slope_str = str: 'rise' or 'fall'
        message = 'trig:a:edge:slo '+slope_str
        self.write(message)
        
    def set_trigger_source(self, channel):
        # sets the channel that is the source of the trigger signal
        #   NOTE: might be useful to trigger on AUX IN eventually, but this
        #           isn't currently supported by this method
        # channel = int: 1-4
        message = 'trig:a:edge:sou ch'+str(channel)
        self.write(message)
        
    def set_trigger_holdoff_mode(self, mode_str):
        # sets the type of trigger holdoff
        # mode_str = str: 'time', 'random', or 'auto'
        message = 'trig:a:hold:by '+mode_str
        self.write(message)
        
    def set_trigger_holdoff(self, delay):
        # sets the trigger holdoff in seconds
        # delay = float: scientific notation OK
        message = 'trig:a:hold:tim '+str(delay)
        self.write(message)
        
    def set_trigger_level(self, level=None):
        # sets trigger level in volts
        # level = float: volts, scientific notation OK
        # default behavior (without level passed): set to 50%
        if level:
            message = 'trig:a:lev '+str(level)
        else:
            message = 'trig:a'
        self.write(message)
        
    ################
    # INPUT/OUTPUT #
    ################

    def set_data_encoding(self, encoding_str):
        # sets the format of the output data
        # encoding_str = str
        #   options:
        #       'ascii'
        #       'rib' - a binary data format
        #       see manual for others
        message = 'dat:enc '+encoding_str
        self.write(message)

    def set_data_source(self, channel):
        # sets the channel from which output data will be obtained
        # channel = int: 1-4
        message = 'dat:sou ch'+str(channel)
        self.write(message)

    def get_data(self, channel=None, encoding_str=None):
        # gets data from a given channel
        # if no channel given, assume the current source channel
        # if no encoding given, assume current encoding
        if channel:
            self.set_data_source(channel)
        if encoding_str:
            self.set_data_encoding(encoding_str)
        message = 'curv?'
        return self.write(message)

"""
*******************************************************************************
*******************************************************************************
"""    

class tektronix_awg7052(gpib_instrument):
    
    def __init__(self,addr):
        super().__init__(addr)

    def force_trigger(self):
        # force a trigger event
        message = '*trg'
        self.write(message)

    def toggle_output(self,channel,state):
        # toggles whether channel is on or off
        # channel   = int: 1 or 2
        # state = 0,1 (off,on)
        message = 'outp'+str(channel)+' '+str(state)
        self.write(message)

    def run(self):
        # initiate output (turns 'run' on)
        message = 'awgc:run'
        self.write(message)
        
    def stop(self):
        # stops output (turns 'run' off)
        message = 'awgc:stop'
        self.write(message)
        
    def toggle_run(self,state):
        # toggles whether the awg is running or not
        # state = 0,1 (off,on)
        if state:
            self.run()
        else:
            self.stop()

    def set_sampling_rate(self,rate):
        # rate = float, scientific notation x.yEz works too, flexible
        message = 'sour:freq '+str(rate)
        self.write(message)

    def set_run_mode(self,mode):
        # sets the run mode, obviously
        # mode = str
        #   -options:
        #       'cont'  -continuous, repeats waveform indefinitely
        #       'trig'  -triggered, outputs one waveform for each trigger
        #       'gat'   -gated, see manual
        #       'seq'   -sequence, see manual
        #       'enh'   -enhanced, see manual
        message = 'awgc:rmode '+mode
        self.write(message)

    def set_frequency_reference(self,source):
        # sets whether to use the internal or an external 10mhz reference
        # source = str: 'int' or 'ext'
        message = 'sour:rosc:sour '+source
        self.write(message)

    #########################
    # WAVEFORM MANIPULATION #
    #########################

    def new_waveform(self, name, size):
        # creates a new (empty) waveform in the current waveform list
        # name = str
        # size = int, number of samples in waveform
        message = 'wlis:wav:new '+'"'+name+'"'+','+str(size)+',REAL'
        self.write(message)
        
    def delete_waveform(self,name):
        # deletes a waveform from the current list
        # name = str
        message = 'wlis:wav:del '+'"'+name+'"'
        self.write(message)
        
    def clear_waveforms(self):
        # deletes all user-defined waveforms from the current list
        message = 'wlis:wav:del ALL'
        self.write(message)
        
    def send_waveform(self, name, w, m1, m2):
        # name = str
        # w = numpy array of floats
        # m1, m2 = numpy arrays containing only 0s and 1s
        n_samples = len(w)
        self.delete_waveform(name)
        self.new_waveform(name,n_samples)
        
        m = ((2**7)*m2) + ((2**6)*m1)
        
        bytes_data = b''
        for ii in range(n_samples):
            bytes_data += struct.pack('fB',w[ii],int(m[ii]))
        
        num_bytes = n_samples*5
        num_bytes = str(num_bytes)
        num_digits = str(len(num_bytes))
        
        num_bytes = num_bytes.encode('ascii')
        num_digits = num_digits.encode('ascii')
        bytes_count = num_digits + num_bytes
        
        bytes_name = name.encode('ascii')
        bytes_samples = str(n_samples)
        bytes_samples = bytes_samples.encode('ascii')
        
        message = b'wlis:wav:data "'+bytes_name+b'",0,'+bytes_samples \
                    +b',#'+bytes_count+bytes_data
        self.write_raw(message)

    def load_waveform(self,channel,name):
        # load a waveform from the current list into channel
        # channel = int: 1 or 2
        # name = str
        message = 'sour'+str(channel)+':wav "'+name+'"'
        self.write(message)

    #######################
    # ANALOG OUT SETTINGS #
    #######################
        
    def set_analog_amplitude(self, channel, amplitude, units='V'):
        # sets the peak to peak voltage amplitude of a given channel
        # channel   = int: 1 or 2
        # amplitude = float
        # units     = str: 'V', 'mV'
        message = 'sour'+str(channel)+':volt '+str(amplitude)+units
        self.write(message)

    ###################
    # MARKER SETTINGS #
    ###################

    def set_marker_low(self, channel, marker, voltage, units='V'):
        # set the low voltage of a given marker on a given channel
        # channel   = int: 1 or 2
        # marker    = int: 1 or 2
        # voltage = float
        # units     = str: 'V', 'mV'
        message = 'sour'+str(channel)+':mark'+str(marker)+':volt:low ' \
                    + str(voltage)+units
        self.write(message)

    def set_marker_high(self, channel, marker, voltage, units='V'):
        # set the low voltage of a given marker on a given channel
        # channel   = int: 1 or 2
        # marker    = int: 1 or 2
        # voltage = float
        # units     = str: 'V', 'mV'
        message = 'sour'+str(channel)+':mark'+str(marker)+':volt:high ' \
                    + str(voltage)+units
        self.write(message)

    def set_marker_delay(self, channel, marker, delay):
        # set the delay for a given channel and marker
        # NOTE: ONLY ACCEPTS DELAY IN PICOSECONDS
        # channel   = int: 1 or 2
        # marker    = int: 1 or 2
        # delay     = float: time in picoseconds
        # units     = str
        message = 'sour' + str(channel) + ':mark' + str(marker) + ':del ' \
                    + str(delay) + 'ps'
        self.write(message)

    #######################
    # FILE SYSTEM METHODS #
    #######################

    def query_cwd(self):
        # return current working directory of awg mass memory
        message = 'mmem:cdir?'
        return self.query(message)

    def mkdir(self, dir_name):
        # makes a new directory in the current working directory
        # dir_name = str
        message = 'mmem:mdir '+'"'+dir_name+'"'
        self.write(message)
        
    def ls(self):
        # query contents of current working directory
        return self.query('mmem:cat?')

    def cd(self,rel_path):
        # change directory relative to current directory
        # rel_path = str
        # '..' moves up one level
        message = 'mmem:cdir '+'"'+rel_path+'"'
        self.write(message)

    def reset_cwd(self):
        message = 'mmem:cdir'
        self.write(message)

    def set_cwd(self,absolute_path):
        # set current working directory of awg mass memory to absolute_path
        # path = str
        self.reset_cwd()
        message = 'mmem:cdir '+'"'+absolute_path+'"'
        self.write(message)

"""
*******************************************************************************
*******************************************************************************
"""

class tektronix_awg520(gpib_instrument):
    
    def __init__(self,addr):
        super().__init__(addr)

    def force_trigger(self):
        # force a trigger event
        message = '*trg'
        self.write(message)

    def toggle_output(self,channel,state):
        # toggles whether channel is on or off
        # channel   = int: 1 or 2
        # state = 0,1 (off,on)
        message = 'outp'+str(channel)+' '+str(state)
        self.write(message)
    
    def set_run_mode(self,mode):
        # sets the run mode, obviously
        # mode = str
        #   -options:
        #       'cont'  -continuous, repeats waveform indefinitely
        #       'trig'  -triggered, outputs one waveform for each trigger
        #       'gat'   -gated, see manual
        #       'enh'   -enhanced, see manual
        message = 'awgc:rmode '+mode
        self.write(message)
        
    def run(self):
        # initiate output (turns 'run' on)
        message = 'awgc:run'
        self.write(message)
        
    def stop(self):
        # stops output (turns 'run' off)
        message = 'awgc:stop'
        self.write(message)
        
    def toggle_run(self,state):
        # toggles whether the awg is running or not
        # state = 0,1 (off,on)
        if state:
            self.run()
        else:
            self.stop()
            
    def set_offset(self, channel, offset, units='V'):
        # set the voltage offset of a given channel
        # channel   = int: 1 or 2
        # offset = float
        # units     = str: 'V', 'mV'
        message = 'sour'+str(channel)+':volt:offs '+str(offset)+units
        self.write(message)
        
    def set_amplitude(self, channel, amplitude, units='V'):
        # sets the peak to peak voltage amplitude of a given channel
        # channel   = int: 1 or 2
        # amplitude = float
        # units     = str: 'V', 'mV'
        message = 'sour'+str(channel)+':volt '+str(amplitude)+units
        self.write(message)

    def set_frequency_reference(self, channel, source):
        # sets the source of the 10MHz reference to use with a channel
        # channel = int: 1 or 2
        # source = str: 'int' or 'ext'
        message = 'sour'+str(channel)+':rosc:sour '+source
        self.write(message)

    def send_waveform(self, w, m1, m2, filename, samplerate):
        # w = array of floats between -1 and 1
        # m1 = array of integers, only 0 and 1 allowed
        # m2 as m1
        # filename = str ending in .wfm
        # samplerate = float up to 1.0E9 (one GS/s)
        
        # need to send a block of bytes data with format
        # cmd + file_counter + header + data_counter + bytes_data + trailer
        
        #converting strings to raw bytes data
        bytes_filename = filename.encode('ascii')
        cmd = b'mmem:data "'+bytes_filename+b'",'
        header = b'MAGIC 1000\r\n'
        
        nsamples = len(w)
        m = m1 + np.multiply(m2, 2)
        
        #packing waveform and markers into bytes data
        bytes_data = b''
        for ii in range(nsamples):
            bytes_data += struct.pack('<fB',w[ii],int(m[ii]))
            
        num_bytes = len(bytes_data)
        num_digits = len(str(num_bytes))
        
        # converting this info into bytes
        num_digits = str(num_digits)
        num_digits = num_digits.encode('ascii')
        num_bytes = str(num_bytes)
        num_bytes = num_bytes.encode('ascii')
        data_counter = b'#'+num_digits+num_bytes
        
        samplerate_str = '{:.2E}'.format(samplerate)
        samplerate_bytes = samplerate_str.encode('ascii')
        trailer = b'CLOCK '+samplerate_bytes+b'\r\n'
        
        file = header + data_counter + bytes_data + trailer
        
        num_file_bytes = len(file)
        num_file_digits = len(str(num_file_bytes))
        
        num_file_digits = str(num_file_digits)
        num_file_digits = num_file_digits.encode('ascii')
        num_file_bytes = str(num_file_bytes)
        num_file_bytes = num_file_bytes.encode('ascii')
        file_counter = b'#'+num_file_digits+num_file_bytes
        
        message = cmd + file_counter + file
        self.write_raw(message)

    def load_waveform(self, channel, filename):
        # loads the waveform at filename into a channel
        # channel   = int: 1 or 2
        # filename  = str
        #   - can be a path, always relative to current working directory
        message = 'sour'+str(channel)+':func:user '+'"'+filename+'"'
        self.write(message)

    ###################
    # MARKER SETTINGS #
    ###################

    def set_marker_low(self, channel, marker, voltage, units='V'):
        # set the low voltage of a given marker on a given channel
        # channel   = int: 1 or 2
        # marker    = int: 1 or 2
        # voltage = float
        # units     = str: 'V', 'mV'
        message = 'sour'+str(channel)+':mark'+str(marker)+':volt:low ' \
                    + str(voltage)+units
        self.write(message)

    def set_marker_high(self, channel, marker, voltage, units='V'):
        # set the low voltage of a given marker on a given channel
        # channel   = int: 1 or 2
        # marker    = int: 1 or 2
        # voltage = float
        # units     = str: 'V', 'mV'
        message = 'sour'+str(channel)+':mark'+str(marker)+':volt:high ' \
                    + str(voltage)+units
        self.write(message)

    def set_marker_delay(self, channel, marker, delay, units='s'):
        # set the delay for a given channel and marker
        # channel   = int: 1 or 2
        # marker    = int: 1 or 2
        # delay     = float
        # units     = str
        message = 'sour' + str(channel) + ':mark' + str(marker) + ':del ' \
                    + str(delay) + units
        self.write(message)

    #######################
    # FILE SYSTEM METHODS #
    #######################

    def set_mass_storage(self, device = 'MAIN'):
        #sets mass storage device
        #device = str
        #options: 'MAIN', 'FLOP', 'NET1', 'NET2', 'NET3'
        message = 'mmem:msis '+'"'+device+'"'
        self.write(message)

    def query_cwd(self):
        # return current working directory of awg mass memory
        message = 'mmem:cdir?'
        return self.query(message)

    def mkdir(self, dir_name):
        # makes a new directory in the current working directory
        # dir_name = str
        message = 'mmem:mdir '+'"'+dir_name+'"'
        self.write(message)
        
    def ls(self):
        # query contents of current working directory
        return self.query('mmem:cat?')

    def cd(self,rel_path):
        # change directory relative to current directory
        # rel_path = str
        # '..' moves up one level
        message = 'mmem:cdir '+'"'+rel_path+'"'
        self.write(message)

    def reset_cwd(self):
        message = 'mmem:cdir'
        self.write(message)

    def set_cwd(self,absolute_path):
        # set current working directory of awg mass memory to absolute_path
        # path = str
        self.reset_cwd()
        message = 'mmem:cdir '+'"'+absolute_path+'"'
        self.write(message)
        
"""
*******************************************************************************
*******************************************************************************
"""

class national_instruments_bnc2090:

    def __init__(self):
        self.output_voltages = []
        for ii in range(2):
            task = nidaqmx.Task()
            ch_str = 'Dev1/ao' + str(ii)
            task.ao_channels.add_ao_voltage_chan(ch_str)
            self.output_voltages.append(0.0)
            task.write(0.0)
            task.close()

    def set_voltage(self, output_ind, voltage):
        task = nidaqmx.Task()
        ch_str = 'Dev1/ao' + str(output_ind)
        task.ao_channels.add_ao_voltage_chan(ch_str)
        self.output_voltages[output_ind] = voltage
        task.write(voltage)
        task.close()

    def get_voltage(self, input_ind, samples=None):
        task = nidaqmx.Task()
        ch_str = 'Dev1/ai' + str(input_ind)
        task.ai_channels.add_ai_voltage_chan(ch_str)
        if samples:
            result = task.read(samples)
        else:
            result = task.read()
        task.close()
        return result

    def get_mean_voltage(self, input_ind, samples, return_stdev=False):
        voltages = self.get_voltage(input_ind, samples)
        mean = statistics.mean(voltages)
        if return_stdev:
            stdev = statistics.stdev(voltages)
            return (
             mean, stdev)
        else:
            return mean
