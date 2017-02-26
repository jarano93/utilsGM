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

# deprecated
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
        print "Mean: %0.2f\tVar: %0.2f\tDev: %0.2f" % (s[0], s[1], s[2])

def stat2(stat_args):
    for stat_arg in stat_args:
        s = [0,0,0,0]
        for a in stat_arg:
            if len(a) == 2:
                s[0] += get_mean(int(a[1]), int(a[0]))
                s[1] += get_dev(int(a[1]), int(a[0]))
                pass
            elif len(a) == 1:
                s[0] += int(a[0])
        s[2] = s[0] - s[1]
        s[3] = s[0] + s[1]
        print "EV: %0.2f\tSD: %0.2f\tEV - SD: %0.2f\tEV + SD: %0.2f" % (s[0], s[1], s[2], s[3])

def stat_list(die, N):
    for n in xrange(N):
        val = n + 1
        s = []
        s.append(get_mean(die, val))
        # s.append(get_var(die, val))
        s.append(get_dev(die, val))
        s.append(s[0] - s[1])
        s.append(s[0] + s[1])
        if val == 1:
            print "Die: %dd%d\tEV: %0.2f\tSD: %0.2f\tEV - SD: %0.2f\tEV + SD: %0.2f" % (val, die, s[0], s[1], s[2], s[3])
        else:
            print "Dice: %dd%d\tEV: %0.2f\tSD: %0.2f\tEV - SD: %0.2f\tEV + SD: %0.2f" % (val, die, s[0], s[1], s[2], s[3])

# DEPRECATED
def stat_sixes(N):
    die = 6
    for n in xrange(N):
        val = n+1
        s = []
        s.append(get_mean(die, val))
        s.append(get_var(die, val))
        s.append(get_dev(die, val))
        print "Dice: %d\tMean: %f\tVar: %f\tDev: %f" % (val, s[0], s[1], s[2])

def stat_main(args):
    if args[0] == 'list':
        stat_list(int(args[1]), int(args[2]))
    else:
        stat2(p.roll_parse(args))

if __name__=='__main__':
    stat_main(sys.argv[1:])
