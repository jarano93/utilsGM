#!/usr/bin/python2

# string_obj.split(char_delimiter)
# string_obj1 in string_obj2

def arg_parse(args):
    roll_args = []
    temp = []
    for a in args:
        if ',' in a:
            temp.append(a.split(','))
            roll_args.append(temp)
            temp = []
        else:
            temp.append(a)
    if len(temp) > 0:
        roll_args.append(temp)
    return roll_args

def roll_parse(args):
    res = []
    roll_args = arg_parse(args)
    for r in roll_args: 
        res_part = []
        for a in r:
            if 'd' in a:
                vals = a.split('d')
                if vals[0] == '':
                    vals[0] = 1
                res_part.append(vals)
            elif a == '+':
                pass
            else:
                res_part.append([a]) 
        res.append(res_part)
    return res
