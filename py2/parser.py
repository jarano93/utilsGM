#!/usr/bin/python2

# string_obj.split(char_delimiter)
# string_obj1 in string_obj2

# DEPRECATED
def arg_parse(args):
    roll_args = []
    temp = []
    for a in args:
        if ',' in a:
            temp.append(a.split(','))
            # roll_args.append(temp)
            if len(temp) != 1:
                if temp[0] != '':
                    temp.append("deprecated")
            for t in temp:
                if t == ',':
                    pass
                elif t == '':
                    pass
                else:
                    roll_args.append(temp)
            temp = []
        else:
            temp.append(a)
    if len(temp) > 0:
        roll_args.append(temp)
    return roll_args

def arg_parse2(args):
    roll_args = []
    scope = []
    for a in args:
        if ',' in a:
            temp = a.split(',')
            if len(temp) != 1:
                if temp[0] != '':
                    scope.append(temp[0])
                roll_args.append(scope)
                scope = []
                if temp[1] != '':
                    scope.append(temp[1])
            else:
                roll_args.append(scope)
                scope = []
        else:
            scope.append(a)
    if len(scope) > 0:
        roll_args.append(scope)
    return roll_args

# DEPRECATED
def roll_parse(args):
    res = []
    roll_args = arg_parse2(args)
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
            elif a == '-':
                pass
            else:
                res_part.append([a])
        res.append(res_part)
    print res
    return res

def roll_parse2(args):
    res = []
    roll_args = arg_parse2(args)
    for r in roll_args:
        res_part = []
        for a in r:
            if 'd' in a:
                vals = a.split('d')
                if vals[0] == '':
                    vals[0] = 1
                res_part.append(vals)
            else:
                res_part.append([a])
        res.append(res_part)
    return res

