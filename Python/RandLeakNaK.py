from neuron import h
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from ModFiles.SimpleSpiking import Cell
import random


h.load_file('stdrun.hoc')
plt.rcParams.update({
    "font.family": "Times New Roman",
})
cmap = mpl.colormaps['plasma']
h.dt = 0.025 
h.v_init= -60 
AMP = 5
DUR = 3
DELAY = 1000
GAP = 25

_enav = np.linspace(60, 40, 10, endpoint=True) 
_ekv = np.linspace(-90, -70, 10, endpoint=True) 
_elv = np.linspace(-50, -90, 10, endpoint=True) 
enav = [random.choice(_enav) for _ in _enav]
ekv = [random.choice(_ekv) for _ in _ekv]
elv = [random.choice(_elv) for _ in _elv]

cells = [Cell(AMP, DUR, DELAY+(x*GAP)) for x in range(10)]
for i,[ena,ek,el] in enumerate(zip(enav,ekv,elv)):
    cells[i].spike(ena=ena, ek=ek, el=el)

colors = cmap(np.linspace(0.9, 0, len(cells)))
plot_start = 900
h.tstop = 1350

_ = h.run()

fig = plt.figure(figsize=[14,6],layout='constrained')

for i,cell in enumerate(cells):
    plt.plot(cell.t, cell.v, color=colors[i], linewidth=3, label=f"{round(cell.soma.ena,1)}mV : {round(cell.soma.ek,1)}mV : {round(cell.soma.eleak,1)}mV")
plt.xlim(plot_start, h.tstop)
plt.ylim(-100, 75)
plt.xlabel('t (ms)', fontsize=25)
plt.ylabel('Membrane Voltage (mV)', fontsize=25)
plt.title('Sodium and Potassium Reversals on Membrane Potential', fontsize=25, pad=0.5)
fig.legend(title='       ENa  :  EKdr  :  Eleak', title_fontsize=30, loc='outside center right', fontsize=25 )
fig.get_layout_engine().set(w_pad=0.2, h_pad=0.2)
plt.show()

