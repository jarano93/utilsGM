#!/usr/bin/python2

import sys
import random as r
import parser as p

def roll(roll_args):
    for roll_arg in roll_args:
        add_flag = True
        rolls = []
        for a in roll_arg:
            temp = 0
            if len(a) == 2:
                for n in xrange(int(a[0])):
                    if add_flag:
                        temp += r.randint(1, int(a[1]))
                    else:
                        temp -= r.randint(1, int(a[1]))
            elif len(a) == 1:
                if a[0] == '+':
                    add_flag = True
                    continue
                elif a[0] == '-':
                    add_flag = False
                    continue
                else:
                    if add_flag:
                        temp = int(a[0])
                    else:
                        temp = -int(a[0])
            rolls.append(temp)
        print "Rolled: %d %s" % (sum(rolls), rolls)

def roll_fate(num_rolls):
    for n in xrange(int(num_rolls)):
        rolls = []
        for i in xrange(4):
            rolls.append(r.randint(-1,1))
        print "Rolled %d: %s" % (sum(rolls), rolls)

def roll_pool(roll_args):
    for roll_arg in roll_args:
        add_flag = True
        rolls = []
        for a in roll_arg:
            temp = 0
            if len(a) == 2:
                for n in xrange(int(a[0])):
                    if add_flag:
                        rolls.append(r.randint(1, int(a[1])))
                    else:
                        rolls.append(r.randint(1, int(a[1])))
            elif len(a) == 1:
                if a[0] == '+':
                    add_flag = True
                    continue
                elif a[0] == '-':
                    add_flag = False
                    continue
                else:
                    if add_flag:
                        for n in xrange(int(a[0])):
                            rolls.append("hit")
                    else:
                        for n in xrange(int(a[0])):
                            rolls.append("miss")
        print "Rolled: %s" % (rolls)

def roll_main(args):
    if args[0] == 'fate':
        if len(args) == 1:
            roll_fate(1)
        else:
            roll_fate(args[1])
    elif args[0] == 'pool':
        roll_pool(p.roll_parse2(args[1:]))
    else:
        roll(p.roll_parse2(args))

if __name__=='__main__':
    roll_main(sys.argv[1:])
