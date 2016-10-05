from matplotlib import pyplot as plt
malt = [line.strip("\n").split(";") for line in open("malt_learning_curve.csv", "r")]
udp = [line.strip("\n").split(";") for line in open("udpipe_learning_curve.csv", "r")]
#TODO: rechange to this when I've run something with fix
#sizes = udp[0][1:]
sizes = udp[0]
#and rm this
udp[0][0] = udp[0][0].strip("language")

maltd = {}
udpd = {}

for i in range(1,len(malt)):
    maltd[malt[i][0]] = [float(n) for n in malt[i][1:]]

for i in range(1,len(udp)):
    udpd[udp[i][0]] = [float(n) for n in udp[i][1:]]

#import ipdb;ipdb.set_trace()

for language in udpd:
    sizes_l = sizes[:len(udpd[language])]
    n_sizes = [i for i in range(len(sizes_l))]
    plt.xticks(n_sizes,sizes_l, rotation='vertical')
    plt.plot(n_sizes, udpd[language], label="udpipe")
    plt.plot(n_sizes, maltd[language], label="maltparser")
    plt.legend(loc='lower right')
    plt.savefig("./Figures/learning_curve_%s.png"%language)
    plt.clf()
