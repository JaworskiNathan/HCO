from neuron import h
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from ModFiles.SimpleSpiking import Cell

h.load_file('stdrun.hoc')
plt.rcParams.update({
    "font.family": "Times New Roman",
})
cmap = mpl.colormaps['plasma']
h.dt = 0.025 
h.v_init= -60 
AMP = 1
DUR = 200
DELAY = 5
test_ena_values = np.linspace(60, 40, 5, endpoint=True) 
test_ek_values = np.linspace(-90, -70, 5, endpoint=True) 
colors = cmap(np.linspace(0.8, 0, len(test_ek_values)))

cells = [Cell(AMP, DUR, DELAY) for _ in range(len(test_ena_values))]
for i,[ena,ek] in enumerate(zip(test_ena_values,test_ek_values)):
    cells[i].spike(ena=ena, ek=ek)

plot_start = DELAY - 25
h.tstop = DUR + DELAY + 25 

_ = h.run()

fig = plt.figure(figsize=[14,6],layout='constrained')

for i, cell in enumerate(cells):
    plt.plot(cell.t, cell.v, color=colors[i], linewidth=3, label=f"{round(cell.soma.ena,1)}mV : {round(cell.soma.ek,1)}mV")
plt.xlim(plot_start, h.tstop)
plt.ylim(-100, 75)
plt.xlabel('t (ms)', fontsize=25)
plt.ylabel('Membrane Voltage (mV)', fontsize=25)
plt.title('Sodium and Potassium Reversals on Membrane Potential', fontsize=25, pad=0.5)
fig.legend(title='       ENa  :  EKdr', title_fontsize=30, loc='outside center right', fontsize=25 )
fig.get_layout_engine().set(w_pad=0.2, h_pad=0.2)
plt.show()

