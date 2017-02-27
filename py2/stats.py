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

def get_bin_mean(n, p):
    return n * p

def get_bin_var(n, p):
    return n * p * (1 - p)

def get_bin_dev(n, p):
    return m.sqrt(n * p * (1 - p))

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

def stat3(stat_args):
    for stat_arg in stat_args:
        add_flag = True
        s = [0,0,0,0]
        for a in stat_arg:
            if len(a) == 2:
                s[0] += get_mean(int(a[1]), int(a[0]))
                s[1] += get_dev(int(a[1]), int(a[0]))
            elif len(a) == 1:
                if a[0] == '+':
                    add_flag = True
                elif a[0] == '-':
                    add_flag = False
                else:
                    if add_flag:
                        s[0] += int(a[0])
                    else:
                        s[0] -= int(a[0])
            s[2] = s[0] - s[1]
            s[3] = s[0] + s[1]
        print "EV: %0.2f\tSD: %0.2f\tEV - SD: %0.2f\tEV + SD: %0.2f" % (s[0], s[1], s[2], s[3])

def stat_d6check(check, min_hit, pool_num):
    if check > pool_num:
        print "check larger than pool -- no success"
        return
    elif min_hit > 6:
        print "minimum hit larger than 6 -- no success"
        return
    elif min_hit < 1:
        print "minimum hit value less than one"
        return
    success = 0
    print "Rolled %dd6,\tminimum hit: %d\t check value: %d" % (pool_num, min_hit, check)
    prob = float(7 - min_hit) / 6
    print "hit%%  per roll:\t%0.4f%%" % (prob)
    for k in xrange(check, pool_num + 1):
        temp = m.pow(prob, k) * m.pow(1 - prob, pool_num - k)
        temp = temp / (m.factorial(k) * m.factorial(pool_num - k))
        success += temp
    success *= m.factorial(pool_num)
    print "pool%% success:\t%0.4f%%" % (success)
    s = [get_bin_mean(pool_num, prob), get_bin_dev(pool_num, prob), 0, 0]
    s[2] = s[0] - s[1]
    s[3] = s[0] + s[1]
    print "EV: %0.2f\tSD: %0.2f\tEV - SD: %0.2f\tEV + SD: %0.2f" % (s[0], s[1], s[2], s[3])

def stat_d6pool(min_hit, pool):
    if min_hit < 1:
        print "minimum hit value less than one"
        return
    elif min_hit > 6:
        print "minimum hit value greater than six"
        return
    prob = float(7 - min_hit) / 6
    stats = [get_bin_mean(pool, prob), get_bin_dev(pool, prob), 0, 0]
    stats[2] = stats[0] - stats[1]
    stats[3] = stats[0] + stats[1]
    print "Rolled %dd6\tmin hit : %d\thit%% per roll: %0.4f%%" % (pool, min_hit, prob)
    print "EV: %0.2f\tSD: %0.2f\tEV - SD: %0.2f\tEV + SD: %0.2f" % (stats[0], stats[1], stats[2], stats[3])

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
    elif args[0] == 'd6pool':
        stat_d6pool(int(args[1]), int(args[2]))
    elif args[0] == 'd6check':
        stat_d6check(int(args[1]), int(args[2]), int(args[3]))
    else:
        stat3(p.roll_parse2(args))

if __name__=='__main__':
    stat_main(sys.argv[1:])
