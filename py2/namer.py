#!/usr/bin/python2

import sys
import random as r

NAME_DIR = "/home/jon/Projects/utilsGM/names/"
SUR = "surnames"
FORE = "forenames_"
PAT = "patronymics_"

VOWELS = ['A', 'E', 'I', 'O', 'U']

def get_russian_patronymic(name, gender):
    res = {'masc': [], 'fem': []}
    last = name[-1]
    if last in VOWELS:
        n = name[:-1]
        res['masc'] = [n + "ICH"]
        res['fem'] = [n + "INICHNA"]
    else:
        res['masc'] = [
                name + "ICH",
                name + "OVICH",
                name + "EVICH"
            ]
        res['fem'] = [
                name + "YEVNA",
                name + "OVNA",
                name + "ICHNA"
            ]
    return r.choice(res[gender])

def get_arabic_patronymic(name, gender):
    res = []
    if gender == 'masc':
        res = [
                "IBN " + name,
                "BIN " + name,
            ]
    elif gender == 'fem':
        res = [
                "IBNAT " + name,
                "BINT " + name,
            ]
    return r.choice(res)

def get_maghreb_patronymic(name, gender):
    res = []
    if gender == 'masc':
        res = [
                "EBN " + name,
                "BEN " + name,
            ]
    elif gender == 'fem':
        res = [
                "EBNAT " + name,
                "BENT " + name,
            ]
    return r.choice(res)

def rand_name(name_array):
    return r.choice(name_array)[:-1]

def print_name(type, gender, num):
    names = gen_names(type, gender, num)
    for n in names:
        print " ".join(n)

def get_forename(type, gender):
    if type == 'Somali':
        type_dir = NAME_DIR + 'Arabic/'
    else:
        type_dir = NAME_DIR + type + '/'
    fore_file = type_dir + FORE + gender
    f_file = open(fore_file, 'r')
    fores = f_file.readlines()
    f_file.close()
    return rand_name(fores)

def gen_names(type, gender, num):
    res = []
    if type=="Russian" or type=="Arabic" or type=="Maghreb":
        for n in xrange(num):
            res.append(gen_patronymic_name(type, gender))
    elif type=="Somali":
        for n in xrange(num):
            res.append(gen_somali_name(gender))
    else:
        for n in xrange(num):
            res.append(gen_regular_name(type, gender))
    return res

def gen_regular_name(type, gender):
    type_dir = NAME_DIR + type + '/'
    sur_file =  type_dir + SUR
    fore_file = type_dir + FORE + gender
    f_fore = open(fore_file, 'r')
    f_sur = open(sur_file, 'r')
    fores = f_fore.readlines()
    surs = f_sur.readlines()
    name = [rand_name(fores), rand_name(surs)]
    f_fore.close()
    f_sur.close()
    return name

def gen_patronymic_name(type, gender):
    type_dir = NAME_DIR + type + '/'
    sur_file =  type_dir + SUR
    fore_file = type_dir + FORE + gender
    pat_file = type_dir + PAT + gender
    f_fore = open(fore_file, 'r')
    f_sur = open(sur_file, 'r')
    f_pat = open(pat_file, 'r')
    fores = f_fore.readlines()
    surs = f_sur.readlines()
    pats = f_pat.readlines()
    name = [rand_name(fores), rand_name(pats), rand_name(surs)]
    f_fore.close()
    f_sur.close()
    f_pat.close()
    return name

def gen_somali_name(gender):
    type_dir = NAME_DIR + 'Arabic/'
    masc_file = type_dir + FORE + 'masc'
    m = open(masc_file, 'r')
    m_names = m.readlines()
    m.close()
    if gender=="fem":
        fem_file = type_dir + FORE + 'fem'
        f = open(fem_file, 'r')
        f_names = f.readlines()
        forename = rand_name(f_names)
        f.close()
    else:
        forename = rand_name(m_names)
    name = [forename, rand_name(m_names), rand_name(m_names), rand_name(m_names)]
    return name

def name_main(args):
    if len(args) == 3:
        print_name(sys.argv[1], sys.argv[2], 1)
    elif len(args) == 4:
        print_name(sys.argv[1], sys.argv[2], int(sys.argv[3]))

if __name__=='__main__':
    name_main(sys.argv)
