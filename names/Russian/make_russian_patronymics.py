#!/usr/bin/python2

VOWELS = ['A', 'E', 'I', 'O', 'U']

def get_patronymics(name):
    res = {'masc': [], 'fem': []}
    last = name[-2]
    if last in VOWELS:
        n = name[:-2]
        res['masc'] = [n + "ICH\n"]
        res['fem'] = [n + "INICHNA\n"]
    else:
        n = name[:-1]
        res['masc'] = [
                n + "ICH\n",
                n + "OVICH\n",
                n + "EVICH\n"
            ]
        res['fem'] = [
                n + "YEVNA\n",
                n + "OVNA\n",
                n + "ICHNA\n"
            ]
    return res


f = open('forenames_masc', 'r')
names = f.readlines()
f.close()
pm = open('patronymics_masc', 'w')
pf = open('patronymics_fem', 'w')
for n in names:
    p = get_patronymics(n)
    for m in p['masc']:
        pm.write(m)
    for f in p['fem']:
        pf.write(f)
pm.close()
pf.close()
