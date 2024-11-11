
from neuron import h
from ModFiles.Template import Cell
import matplotlib.pyplot as plt
import numpy as np
h.load_file('stdrun.hoc')

h.dt = 0.025 
h.v_init= -60 

s = Cell(1,10,500,1000);s.make_spike(name='Spiking Cell')
a = Cell(1,10,500,1000);a.make_adapt(name='Adapting Cell')
b = Cell(1,10,500,1000);b.make_burst(name='Bursting Cell')
lvls = [s,a,b]

mcells = [Cell(),Cell(),Cell(),Cell()]
hcocells = [Cell(2,1,1,0),Cell(),Cell(2,1,1,120),Cell()]

for i,cell in enumerate(mcells):
    cell.make_motor(name=f"Motor {i+1}")
for i,cell in enumerate(hcocells):
    cell.make_HCO(name=f"HCO {i+1}")

nc12 = h.NetCon(hcocells[0].soma(0.5)._ref_v,hcocells[1].syn,0,0,10,sec=hcocells[0].soma) 
nc21 = h.NetCon(hcocells[1].soma(0.5)._ref_v,hcocells[0].syn,0,0,10,sec=hcocells[1].soma) 
nc34 = h.NetCon(hcocells[2].soma(0.5)._ref_v,hcocells[3].syn,0,0,10,sec=hcocells[2].soma) 
nc43 = h.NetCon(hcocells[3].soma(0.5)._ref_v,hcocells[2].syn,0,0,10,sec=hcocells[3].soma) 
ncs=[nc12,nc21,nc34,nc43]

for i in range(4):
    nc = h.NetCon(hcocells[i].soma(0.5)._ref_v,mcells[i].dsyn1,sec=hcocells[i].soma)
    nc.weight[0] = 1
    ncs.append(nc)
plot_start = 950
h.tstop = 4000
_ = h.run()
t = s.t

for lvl in lvls:
    plt.figure(figsize=[8,8],layout='constrained')
    lvl.plot_cell(plot_start,1600,0)
    plt.suptitle(f"{lvl}",fontsize=20)

plt.figure(figsize=[8,8],layout='constrained')
for i,[m,hco] in enumerate(zip(mcells,hcocells)):
        mv = h.Vector()
        mv = m.record['v']
        hcov = h.Vector()
        hcov = hco.record['v']
        plt.subplot(4,1,i+1)
        plt.ylim(-80,50)
        plt.plot(t, hcov, 'teal', label=f'{hco}',linewidth=1)
        plt.plot(t, mv, 'darkslategray', label=f'{m}',linewidth=3)
        plt.xlim(500,h.tstop)
        plt.legend()
plt.show()
