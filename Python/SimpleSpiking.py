from neuron import h
import numpy as np
import matplotlib.pyplot as plt

class Cell():
        def __init__(self,num=0,dur=0,d=0):
                self.name = 'Template'
                self.soma = h.Section(name='soma',cell=self)
                self.soma.nseg = 1	
                self.soma.L = 1000 		 
                self.soma.diam = 9.99593  
                self.soma.cm = 1 

                self.ccl = h.IClamp(self.soma(.5))
                self.ccl.delay = d
                self.ccl.dur = dur
                self.ccl.amp = num
                self.spikecounter = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)
                self.spikecounter.threshold = 0
                print(f'Initialized Template Cell')

        def setup_v(self):

                self.t = h.Vector()
                self.v = h.Vector()
                self.t.record(h._ref_t)
                self.v.record(self.soma(0.5)._ref_v)

                self.spike_times = h.Vector()     
                self.s = [] 
                self.s = self.spikecounter.record(self.spike_times) 
  
        def spike(self,ena=50,gna=0.5,ek=-80,gk=0.45,el=-60,gl=0.00003):
                self.soma.insert('na')
                self.soma.ena = ena 
                self.soma.gbar_na = gna 
                self.soma.insert('kdr')
                self.soma.ek = ek 
                self.soma.gbar_kdr = gk 
                self.soma.insert('leak')
                self.soma.eleak = el
                self.soma.gbar_leak = gl
                self.setup_v()
       

       


