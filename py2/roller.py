#!/usr/bin/python2

import sys
import random as r
import parser as p

def roll(roll_args):
    for roll_arg in roll_args:
        rolls = []
        for a in roll_arg:
            temp = 0
            if len(a) == 2:
                for n in xrange(int(a[0])):
                    temp += r.randint(1, int(a[1]))
            elif len(a) == 1:
                temp = int(a[0])
            rolls.append(temp)
        print "Rolled: %d %s" % (sum(rolls), rolls)

def roll_main(args):
    roll(p.roll_parse(args))

if __name__=='__main__':
    roll_main(sys.argv[1:])
