from matplotlib import pyplot as plt
import numpy as np
malt = [line.strip("\n").split(";") for line in open("RES/learning_curve/zoom/malt_learning_curve.csv", "r")]
udp = [line.strip("\n").split(";") for line in open("RES/learning_curve/zoom/udpipe_learning_curve.csv", "r")]

sizes = malt[0][1:]
maltd = {}
udpd = {}
fig, axes = plt.subplots(2, 4, sharey='row')
((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = axes

all_axes = [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]

axes[0][0].set_ylim([1,100])
axes[1][0].set_ylim([1,100])

for i in range(1,len(malt)):
    maltd[malt[i][0]] = [float(n) for n in malt[i][1:]]

for i in range(1,len(udp)):
    udpd[udp[i][0]] = [float(n) for n in udp[i][1:]]


for n, language in enumerate(udpd):
    sizes_l = sizes[:len(udpd[language])]
    n_sizes = [i for i in range(len(sizes_l))]
    plt.sca(all_axes[n])
    plt.xticks(n_sizes,sizes_l, rotation=45)
    all_axes[n].set_title(language)
    #for full thing
    #if language=="UD_Czech":
    for label in all_axes[n].get_xticklabels()[::2]:
        label.set_visible(False)
    try:
        if n == len(udpd) -1:
            plt.plot(n_sizes, udpd[language], label='udpipe')
            plt.plot(n_sizes, maltd[language], label='maltparser')
        else:
            plt.plot(n_sizes, udpd[language])
            plt.plot(n_sizes, maltd[language])

    except:
        KeyError

plt.legend(bbox_to_anchor=(-1.8, 2.4), loc=2, borderaxespad=0.)
fig.text(0.5, 0.04, 'Training size', ha='center')
fig.text(0.04, 0.5, 'LAS', va='center', rotation='vertical')
plt.show()
fig.savefig("./Figures/learning_curve/zoom_learning_curve.png")
