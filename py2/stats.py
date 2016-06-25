#!/usr/bin/python2

import sys
import math as m
import parser as p

def get_mean(n, k):
    return k * float(n + 1) / 2

def get_var(n, k):
    return m.pow(k, 2) * (m.pow(n, 2) - 1) / 12

def get_dev(n, k):
    return k * m.sqrt((m.pow(n, 2) - 1) / 12)

def stat(stat_args):
    for stat_arg in stat_args:
        s = [0,0,0]
        for a in stat_arg:
            if len(a) == 2:
                s[0] += get_mean(int(a[1]), int(a[0]))
                s[1] += get_var(int(a[1]), int(a[0]))
                s[2] += get_dev(int(a[1]), int(a[0]))
                pass
            elif len(a) == 1:
                s[0] += int(a[0])
        print "Mean: %f\tVar: %f\tDev: %f" % (s[0], s[1], s[2])

def stat_sixes(N):
    for n in xrange(N):
        val = n+1
        s = []
        s.append(get_mean(6, val))
        s.append(get_var(6, val))
        s.append(get_dev(6, val))
        print "Die: %d\tMean: %f\tVar: %f\tDev: %f" % (val, s[0], s[1], s[2])

def stat_main(args):
    if args[0] == 'sixes':
        stat_sixes(int(args[1]))
    else:
        stat(p.roll_parse(args))

if __name__=='__main__':
    stat_main(sys.argv[1:])
