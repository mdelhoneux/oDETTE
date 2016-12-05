from matplotlib import pyplot as plt
malt = [line.strip("\n").split(";") for line in open("RES/learning_curve/malt_learning_curve.csv", "r")]
udp = [line.strip("\n").split(";") for line in open("RES/learning_curve/udpipe_learning_curve.csv", "r")]
#TODO: rechange to this when I've run something with fix
sizes = malt[0][1:]
#sizes = udp[0]
#import ipdb;ipdb.set_trace()
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
    #to get the full scale
    axes = plt.gca()
    axes.set_ylim([1,100])
    plt.xticks(n_sizes,sizes_l, rotation='vertical')
    try:
        plt.plot(n_sizes, udpd[language], label="U")
        plt.plot(n_sizes, maltd[language], label="M")
    except:
        KeyError
        plt.clf()
    plt.ylabel('LAS')
    plt.xlabel('Training size')
    plt.tight_layout()
    plt.legend(loc='lower right')
    plt.savefig("./Figures/learning_curve/learning_curve_%s.png"%language)
    plt.clf()
