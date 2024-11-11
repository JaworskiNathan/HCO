from neuron import h
import numpy as np
import matplotlib.pyplot as plt

class Cell():
        def __init__(self,stim=0,num=0,dur=0,d=0,name = 'Template'):
                self.name = name
                self.s = []
                self.soma = h.Section(name='soma',cell=self)
                self.soma.nseg = 1	
                self.soma.L = 1000 		 
                self.soma.diam = 9.99593  
                self.soma.cm = 1
                self.soma.insert('leak')
                self.soma.eleak = -60
                self.soma.gbar_leak = 0.03e-3 
                if stim == 0:
                        self.syn = h.inhsyn(.5,sec=self.soma)
                        self.syn.esyn = -80
                        self.syn.gmax = 0.04  
                        self.syn.tau1 = 10   
                        self.syn.tau2 = 20 
                if stim == 1:
                        self.current_clamp(num,dur,d)
                if stim == 2:
                        self.synaptic_stim(num,dur,d)
                surf_area = (self.soma.L * 10**-4) * (np.pi * self.soma.diam * 10**-4) 
                self.sarea = round(surf_area,7)
                self.spikecounter = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)
                self.spikecounter.threshold = 0
                print(f'Initialized Template Cell with Surface Area = {self.sarea}cm^2')

        def setup(self,num):
                self.t = h.Vector()
                self.t.record(h._ref_t)
                self.vars = ['ileak_leak','ina_na','ik_kdr','ica_cas','ica_cat','ik_ka','ik_kca','ih_hyper','v','cai',
                             'ja_cas','k_cas','u_cat','z_cat','a_ka','b_ka','n_kdr','m_na','hm_hyper','h_na','c_kca',
                             'g_cas','g_cat','g_ka','g_kdr','g_na','g_kca']
                self.clrs = ['k','y','r','orange','brown','pink','g','c']
                self.record = {}
                for v in self.vars:
                        vec = h.Vector()
                        try:
                                vec.record(getattr(self.soma(.5),'_ref_'+v))
                        except AttributeError:
                                pass
                        self.record[v] = vec
                self.spike_times = h.Vector()      
                self.spikecounter.record(self.spike_times) 
                print(f"( {num} / {num} ) : Created vars for {self}")
                print("----------------------------------------")

        def make_motor(self):
                self.dsyn1 = h.inhsyn(.5,sec=self.soma)
                self.dsyn1.esyn=-20
                self.dsyn1.gmax = 0.01  
                self.dsyn1.tau1 = 10   
                self.dsyn1.tau2 = 20
                self.setup(0)

        def make_spike(self,num=2):
                self.name = name
                self.soma.insert('na')
                self.soma.ena = 50 
                self.soma.gbar_na = 0.3  
                self.soma.insert('kdr')
                self.soma.ek = -80 
                self.soma.gbar_kdr = 0.15
                print(f'( 1 / {num} ) : {self} can Spike: Added Na , K Channels')
                if num == 2:
                        self.setup(num)

        def make_adapt(self,num=3):
                self.make_spike(num=num)
                self.name = name
                self.soma.insert('capool')
                self.soma.cao = 3 
                self.soma.cai = 50e-6   
                self.soma.tauca_capool = 200           
                self.soma.insert('cas')
                self.soma.gbar_cas = .008 
                self.soma.insert('ka')
                self.soma.gbar_ka = .07
                self.soma.insert('kca')
                self.soma.gbar_kca = .02
                print(f'( 2 / {num} ) : {self} can Adapt: Added Capool and Cas , Ka , KCa Channels')
                if num == 3:
                        self.setup(num)

        def make_burst(self,num=4):
                self.make_adapt(name,num=num)
                self.name = name
                self.soma.insert('cat')
                self.soma.gbar_cat = .007 
                print(f'( 3 / {num} ) : {self} can Burst: Added CaT Channels')
                if num == 4:
                        self.setup(num)

        def make_HCO(self,num=5):
                self.make_burst(name,num=num)
                self.name = name
                self.soma.insert('hyper')
                self.soma.eh = -20 
                self.soma.gbar_hyper = .002 
                print(f'( 4 / {num} ) : {self} can Oscillate: Added H Channels')
                self.setup(num)

        def plot_cell(self,xmin,xmax,cellid):
                plt.subplot(4,1,1)
                spk = 1
                clro = ['slategray','bo','go','mo']
                clr = ['dimgray','gray','darkgray','lightgray']
                self.v = self.record['v']
                self.xmin = xmin
                self.xmax = xmax
                plt.plot(self.t, self.v, clr[cellid],linewidth=1, label=f'{self}')
                plt.xlim([xmin,xmax])
                plt.ylim(min(self.v)-25,max(self.v)+25)
                plt.xlabel('t (ms)')
                plt.ylabel('Vm (mV)')
                plt.title('Membrane Voltage')
                plt.legend()

                for i in self.record:
                        if i.startswith('i') and len(self.record[i]) != 0:
                                plt.subplot(4,1,2)
                                plt.plot(self.t, self.record[i],linewidth=1, label=f'{self} : {i}')
                                plt.xlim([xmin,xmax])
                                plt.xlabel('t (ms)')
                                plt.ylabel('I (nA)')
                                plt.title('Ion Currents')
                        if i.startswith('c') and len(self.record[i]) != 0:
                                plt.subplot(4,1,3)
                                spk = 0
                                plt.plot(self.t, self.record[i],linewidth=1, label=f'{self} : {i}')
                                plt.xlim([xmin,xmax])
                                plt.ylabel('Concentration (mM)')
                                plt.xlabel('t (ms)')
                                plt.title('Intracellular Calcium')
                                plt.legend()

                plt.subplot(4,1,4 - spk)
                plt.xlim([xmin , xmax])
                self.spikecount = len(self.spike_times)
                if self.spikecount > 1:
                        self.isi = np.diff(self.spike_times)
                        st = np.array(self.spike_times)
                        for sp in st:
                                if sp > 1000:
                                        self.s.append(round(sp,1))
                        self.isf = 1000 / self.isi
                        plt.ylim([0, max(self.isf) + 5])
                        plt.vlines(st,0+(cellid * 5),5+(cellid * 5))
                        notfirst = st[1:]
                        for i,spike in enumerate(notfirst):
                                if self.isf[i] > 5:
                                        plt.plot(spike,self.isf[i],clro[cellid])      
                plt.xlabel('t (ms)')
                plt.ylabel('f (Hz)')
                plt.title('Spikes')
                plt.show()
                
        def current_clamp(self, num, dur, d):
                self.ccl = h.IClamp(self.soma(.5))
                self.ccl.delay = d
                self.ccl.dur = dur
                self.ccl.amp = num

        def synaptic_stim(self,num,dur,d):
                self.syn = h.inhsyn(.5,sec=self.soma)
                self.spk_train = h.NetStim() 
                self.spk_train.noise = 0
                self.spk_train.start=d
                self.spk_train.interval=dur
                self.spk_train.number=num
                self.nc = h.NetCon(self.spk_train,self.syn,sec=self.soma) 
                self.nc.weight[0] = 1
                self.syn.esyn = -80
                self.syn.gmax = 0.04  
                self.syn.tau1 = 10   
                self.syn.tau2 = 20 

        def __repr__(self):
                return f"{self.name}"

