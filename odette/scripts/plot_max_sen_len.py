from matplotlib import pyplot as plt
#TODO: erm how did I do those? #ah yes using error anal in main
malt = [line.strip("\n").split(";") for line in open("senlen_malt.csv", "r")]
udp = [line.strip("\n").split(";") for line in open("senlen_udpipe.csv", "r")]

sizes = udp[0][1:]

maltd = {}
udpd = {}

for i in range(1,len(malt)):
    maltd[malt[i][0]] = [float(n) for n in malt[i][1:]]

for i in range(1,len(udp)):
    udpd[udp[i][0]] = [float(n) for n in udp[i][1:]]

tot_sizes = len(sizes)
#import numpy as np
#ys = np.arange(1,100,1)

for language in udpd:
    #TODO: add legend to axes
    size_l = len(udpd[language])
    start_l = tot_sizes - size_l
    sizes_l = sizes[start_l:]
    n_sizes = [i for i in range(len(sizes_l))]
    axes = plt.gca()
    axes.set_ylim([1,100])
    plt.xticks(n_sizes,sizes_l, rotation='vertical')
    #plt.yticks(ys)
    plt.plot(n_sizes, udpd[language], label="udpipe")
    plt.plot(n_sizes, maltd[language], label="maltparser")
    plt.legend(loc='upper right')
    plt.savefig("./Figures/max_sen_len_%s.png"%language)
    plt.clf()
