import config
def write_n_lines(infile,outfile, n):
    """
    append n lines of infile to outfile where after n lines, lines are written
    until an empty line is found
    """
    out = open(outfile, 'a')
    stop = False
    for i, line in enumerate(open(infile, 'r')):
        if i == n:
            stop = True
        if line == "\n" and stop:
            out.write(line)
            out.close()
            return
        else:
            out.write(line)
    out.close() #if I don't do this I discard Tamil and Kazakh # I think
    return


exp = config.exp
gold = 'dev_gold.conll'
malt = 'dev_parsed_maltOpt.conll'
udp = 'dev_parsed_udpipe.conll'
concatdir = exp + 'UD_concat/'
cgold = concatdir+gold
cmalt = concatdir+malt
cudp = concatdir+udp
nlines = 9000

l_considered = [line.strip("\n") for line in open("selection.txt", "r")]
for ln, language in enumerate(l_considered):
    ldir = exp + language + "/"
    write_n_lines(ldir+gold,cgold,nlines)
    write_n_lines(ldir+malt,cmalt,nlines)
    write_n_lines(ldir+udp,cudp,nlines)
