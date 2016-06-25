#!/usr/bin/python2
# -*- coding: utf-8 -*-

import copy
import sys
import namer as na
import random as r
import math as m

class Person:
    def __init__(self, name, alive, gender, parents):
        self.name = name
        self.alive = alive
        self.gender = gender
        self.parents = parents
        self.couple_flag = False

    def get_name(self):
        return self.name

    def has_couple(self):
        return self.couple_flag

    def set_couple(self, couple):
        self.couple_flag = True
        self.couple = couple

    def get_pair(self):
        return self.couple if self.has_couple() else False

    def get_parents(self):
        return self.parents

    def descriptor(self):
        desc = " ".join(self.name)
        desc += " (" + self.gender[0] + ")"
        if not self.alive:
            desc += " (DECEASED)"
        return desc

    def adopt_surname(self, surname):
        name = copy.deepcopy(self.name[:-1])
        maiden_name = copy.deepcopy(self.name[-1])
        maiden_name = "(" + maiden_name + ")"
        name.append(maiden_name)
        name.append(surname)
        self.name = name

class Couple:
    def __init__(self, type, father, mother):
        self.type = type
        self.father = father
        self.mother = mother
        self.children = []

    def make_children(self, genders):
        patronymics = ['Russian', 'Arabic', 'Maghreb']
        if self.type in patronymics:
            res = self.children_patronymic(genders)
        elif self.type == 'Somali':
            res = self.children_somali(genders)
        else:
            res = self.children_general(genders)
        self.children = res
        return self.children

    def childless(self):
        return len(self.children) == 0

    def children_patronymic(self, genders):
        surname = self.father.name[-1]
        f_name = self.father.name[0]
        res = []
        for g in genders:
            name = [na.get_forename(self.type, g)]
            if self.type == "Russian":
                name.append(na.get_russian_patronymic(f_name, g))
            elif self.type == "Arabic":
                name.append(na.get_arabic_patronymic(f_name, g))
            elif self.type == "Maghreb":
                name.append(na.get_maghreb_patronymic(f_name, g))
            name.append(surname)
            p = Person(name, True, g, self)
            res.append(p)
        return res

    def children_somali(self, genders):
        patronymics = self.father.name[:-1]
        res = []
        for g in genders:
            name = [na.get_forename(self.type, g)]
            for pa in patronymics:
                name.append(pa)
            p = Person(name, True, g, self)
            res.append(p)
        return res

    def children_general(self, genders):
        surname = self.father.name[-1]
        res = []
        for g in genders:
            name = [
                    na.get_forename(self.type, g),
                    surname
                ]
            p = Person(name, True, g, self)
            res.append(p)
        return res

    def get_children(self):
        return self.children

    def num_children(self):
        return len(self.children)

    def get_child(self, i):
        return self.children[i]

    def descriptor(self):
        return self.father.descriptor() + " - " + self.mother.descriptor()

    @classmethod
    def complete(cls, type, person):
        if person.gender == 'masc':
            father = person
            m_name = na.gen_names(type, 'fem', 1)[0]
            mother = Person(m_name, True, 'fem', None)
            if type != 'Somali':
                surname = copy.deepcopy(father.name[-1])
                mother.adopt_surname(surname)
        elif person.gender == 'fem':
            mother = person
            f_name = na.gen_names(type, 'masc', 1)[0]
            if type != 'Somali':
                surname = copy.deepcopy(f_name[-1])
                mother.adopt_surname(surname)
            father = Person(f_name, True, 'masc', None)
        c = cls(type, father, mother)
        father.set_couple(c)
        mother.set_couple(c)
        return c

    @classmethod
    def persons(cls, type, father, mother):
        surname = father.get_name()[-1]
        mother.adopt_surname(surname)
        c = cls(type, father, mother)
        father.set_couple(c)
        mother.set_couple(c)
        return c

    @classmethod
    def rand(cls, type):
        m_name = na.gen_names(type, 'masc', 1)[0]
        f_name = na.gen_names(type, 'fem', 1)[0]
        father = Person(m_name, True, 'masc', None)
        mother = Person(f_name, True, 'fem', None)
        mother.adopt_surname(copy.deepcopy(f_name[-1]))
        c = cls(type, father, mother)
        father.set_couple(c)
        mother.set_couple(c)
        return c


class Clan:
    def __init__(self, type, ch_floor, ch_ceil, ch_mort, mort):
        self.type = type
        self.ch_floor = ch_floor
        self.ch_ceil = ch_ceil
        self.ch_mort = ch_mort
        self.mort = mort
        self.persons_p = {}
        self.persons_m = {}
        self.couples_p = {}
        self.couples_m = {}
        self.final = {}

    def make_tree(self):
        self.root_gen(0)
        while True:
            if self.mid_gen(1):
                break
        self.merge_gen(2)
        self.final_gen(3)

    def root_gen(self, depth):
        paternal = Couple.rand(self.type)
        maternal = Couple.rand(self.type)
        paternal.father.alive = self.mortality(depth)
        paternal.mother.alive = self.mortality(depth)
        maternal.father.alive = self.mortality(depth)
        maternal.mother.alive = self.mortality(depth)
        self.root_p = paternal
        self.root_m = maternal

    def handle_children(self, children, depth):
        persons = []
        couples = []
        for ch in children:
            alive = self.ch_mortality()
            ch.alive = alive
            if alive:
                couple = Couple.complete(self.type, ch)
                couples.append(couple)
            else:
                persons.append(ch)
        for c in couples:
            c.father.alive = self.mortality(depth)
            c.mother.alive = self.mortality(depth)
        return persons, couples

    def handle_final_children(self, children, depth):
        persons_live = []
        persons_dead = []
        for ch in children:
            alive = self.ch_mortality()
            ch.alive = alive
            if alive:
                persons_live.append(ch)
            else:
                persons_dead.append(ch)
        return persons_live + persons_dead

    def mid_gen(self, depth):
        children_p = self.root_p.make_children(self.child_genders())
        persons_p, couples_p = self.handle_children(children_p, depth)
        children_m = self.root_m.make_children(self.child_genders())
        persons_m, couples_m = self.handle_children(children_m, depth)

        if couples_p == [] and couples_m == []:
            return False

        self.persons_p[self.root_p] = persons_p
        self.couples_p[self.root_p] = couples_p
        self.persons_m[self.root_m] = persons_m
        self.couples_m[self.root_m] = couples_m
        return True

    def merge_gen(self, depth):
        for c in self.couples_p[self.root_p][:-1]:
            children_p = c.make_children(self.child_genders())
            persons_p, couples_p = self.handle_children(children_p, depth)
            self.persons_p[c] = persons_p
            self.couples_p[c] = couples_p
        couple_p = self.couples_p[self.root_p][-1]
        children_p = couple_p.make_children(self.ensure_masc())
        persons_p, couples_p = self.handle_children(children_p[:-1], depth)
        self.persons_p[couple_p] = persons_p
        self.couples_p[couple_p] = couples_p
        father = children_p[-1]
        couple_m = self.couples_m[self.root_m][0]
        children_m = couple_m.make_children(self.ensure_fem())
        mother = children_m[0]
        merge_couple = Couple.persons(self.type, father, mother)
        self.couples_p[couple_p].append(merge_couple)
        persons_m, couples_m = self.handle_children(children_m[1:], depth)
        self.persons_m[couple_m] = persons_m
        self.couples_m[couple_m] = couples_m
        for c in self.couples_m[self.root_m][1:]:
            children_m = c.make_children(self.child_genders())
            persons_m, couples_m = self.handle_children(children_m, depth)
            self.persons_m[c] = persons_m
            self.couples_m[c] = couples_m

    def final_gen(self, depth):
        for cp in self.couples_p.values():
            for c in cp:
                if c.childless():
                    children = c.make_children(self.child_genders())
                    persons = self.handle_final_children(children, depth)
                    self.persons_p[c] = persons
        for cm in self.couples_m.values():
            for c in cm:
                if c.childless():
                    children = c.make_children(self.child_genders())
                    persons = self.handle_final_children(children, depth)
                    self.persons_m[c] = persons

    # └ ─ ├ ┌ │
    def print_tree(self):
        self.print_paternal()
        mid_string = ""
        for i in xrange(19):
            mid_string += "*   "
        mid_string += "*"
        print mid_string
        self.print_maternal()

    def print_paternal(self):
        self.recurse_paternal(self.root_p, "", 0)

    def recurse_paternal(self, couple, lead, depth):
        print lead + couple.descriptor()
        # i_lead, i_end, p_lead, p_end = self.new_lead(lead, heads)
        i_lead, i_end, p_lead, p_end = "", "", "", ""
        for d in xrange(depth + 1):
            i_lead += "    "
            p_lead += "    "
        for p in self.persons_p[couple]:
            print i_lead + p.descriptor()
        try:
            for c in self.couples_p[couple]:
                self.recurse_paternal(c, p_lead, depth + 1)
        except: pass

    def print_maternal(self):
        self.recurse_maternal(self.root_m, "", 0)

    def recurse_maternal(self, couple, lead, depth):
        i_lead, i_end, p_lead, p_end = "", "", "", ""
        for d in xrange(depth + 1):
            i_lead += "    "
            p_lead += "    "
        try:
            for c in self.couples_m[couple]:
                self.recurse_maternal(c, p_lead, depth + 1)
        except: pass
        for p in self.persons_m[couple]:
            print i_lead + p.descriptor()
        print lead + couple.descriptor()

    def new_lead(self, lead, heads):
        # TODO handle the merge
        print heads
        if lead == "":
            i_lead = heads[1]
            i_end = heads[3]
            p_lead = heads[1]
            p_end = heads[3]
        else:
            leads = [lead[i:i+4] for i in xrange(0, len(lead), 4)]
            i_lead = ""
            i_end = ""
            p_lead = ""
            p_end = ""
            for l in leads[:-1]:
                print l
                if l == heads[0]:
                    i_lead += heads[0]
                    i_end += heads[0]
                    p_lead += heads[0]
                    p_ends += heads[0]
                elif l == heads[1]:
                    i_lead += heads[2]
                    i_end += heads[2]
                    p_lead += heads[2]
                    p_ends += heads[2]
                elif l == heads[2]:
                    i_lead += heads[2]
                    i_end += heads[2]
                    p_lead += heads[2]
                    p_ends += heads[2]
            tail = leads[-1]
            if tail == heads[0]:
                i_lead += heads[0] + heads[0]
                i_end += heads[0] + heads[0]
                p_lead += heads[0] + heads[0]
                p_ends += heads[0] + heads[0]
            elif tail == heads[1]:
                print "TAIL"
                i_lead += heads[2] + heads[1]
                i_end += heads[2] + heads[3]
                p_lead += heads[2] + heads[1]
                p_ends += heads[2] + heads[3]
            elif tail == heads[3]:
                i_lead += heads[0] + heads[1]
                i_end += heads[0] + heads[3]
                p_lead += heads[0] + heads[1]
                p_ends += heads[0] + heads[3]
        print i_lead
        print i_end
        print p_lead
        print p_end
        return i_lead, i_end, p_lead, p_end

    def child_genders(self):
        num = r.randint(self.ch_floor, self.ch_ceil)
        genders = []
        for n in xrange(num):
            if r.random() < 0.5:
                genders.append("masc")
            else:
                genders.append("fem")
        return genders

    def ensure_masc(self):
        genders = self.child_genders()
        genders[-1] = 'masc'
        return genders

    def ensure_fem(self):
        genders = self.child_genders()
        genders[0] = 'fem'
        return genders

    def mortality(self, depth):
        return r.random() > m.pow(self.mort, m.pow(2, depth - 2))

    def ch_mortality(self):
        return r.random() > self.ch_mort

def make_clan(type, ch_floor, ch_ceil, ch_mort, mort):
    c = Clan(type, ch_floor, ch_ceil, ch_mort, mort)
    c.make_tree()
    c.print_tree()

def clan_main(args):
    make_clan(args[0], int(args[1]), int(args[2]), float(args[3]), float(args[4]))

if __name__=='__main__':
    clan_main(sys.argv[1:])
