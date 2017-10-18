#! /usr/bin/env python2.7

import os
import sys
import glob
import math
import shutil
import datetime
import argparse
import susyhitutils
from progressbar import ProgressBar
import pyslha


def get_br(slhafile, br_to='Gy'):

    br = 0
    for dc in pyslha.read(slhafile).decays[1000022].decays:

        if br_to == 'Gy' and abs(dc.ids[0]) == 1000039 and abs(dc.ids[1]) == 22:
            br += dc.br

        if br_to == 'GZ' and abs(dc.ids[0]) == 1000039 and abs(dc.ids[1]) == 23:
            br += dc.br

        if br_to == 'Gh' and abs(dc.ids[0]) == 1000039 and abs(dc.ids[1]) == 25:
            br += dc.br

    return br


def find_best_m1(m1_min, m1_max, m2, m3, mu, tanb, msq, at, Gmass, br_to='Gy', br_eq=0.5, precision=0.001):

    """
    Find M1/mu relation using bisection method :D
    """

    if args.verbose:
        print ('find best m1 for m3 = %f, mu = %f' % (m3, mu))

    m1_a = m1_min
    m1_b = m1_max
    m1_p = (m1_a + m1_b) / 2

    br_p = 99

    iteration = 0
    last_m1_p = 0

    while abs(br_p) > precision and iteration < 100:

        m1_p = (m1_a + m1_b) / 2

        # A
        outfile = susyhitutils.generate_slha(m1_a, m2, m3, mu, tanb, msq, at, Gmass)

        br = get_br(outfile, br_to)

        br_a = br - br_eq

        # B
        outfile = susyhitutils.generate_slha(m1_b, m2, m3, mu, tanb, msq, at, Gmass)

        br = get_br(outfile, br_to)

        br_b = br - br_eq

        # P
        outfile = susyhitutils.generate_slha(m1_p, m2, m3, mu, tanb, msq, at, Gmass)

        br = get_br(outfile, br_to)

        br_p = br - br_eq

        ###
        if br_a * br_p < 0:
            m1_a = m1_a
        else:
            m1_a = m1_p

        if br_b * br_p < 0:
            m1_b = m1_b
        else:
            m1_b = m1_p

        if m1_a == m1_b:
            m1_a = m1_max

        iteration += 1

        last_m1_p = m1_p
        if abs(m1_a - m1_p) <= 1 and abs(m1_b - m1_p) <= 1:
            break

    return m1_p, br



##--
def main():

    parser = argparse.ArgumentParser(description='')

    # parser.add_argument('-c', dest='configfile', required=True, help='Configfile')
    parser.add_argument('-o', dest='outputdir', help='Output directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose')

    parser.add_argument('--m3', type=float, default=2000.)
    parser.add_argument('--vmu',  help='mu values separated by comma')
    parser.add_argument('--tune', help='Tune M1 to get desired N1->X BRs: br_n1_Gy=0.5 (example)')
    parser.add_argument('--precision', type=float, help='Precision')


    global args
    args = parser.parse_args()



    # Run directory
    if args.outputdir is None:
        t = datetime.datetime.now()
        datestr = '%s-%s-%s_%s.%s.%s' % (t.year, t.month, t.day, t.hour, t.minute, t.second)
        run_dir = 'SusyGridRun_%s' % datestr
    else:
        run_dir = args.outputdir

    susyhitutils.create_run_directory(run_dir)


    br_to, br_eq = args.tune.split('=')

    br_to = br_to.replace('br_n1_', '')
    br_eq = float(br_eq)

    at    = 0
    tanb  = 1.5
    msq   = 5.0E+03

    m2 = 3.0E+03
    m3 = args.m3
    gmass = 1E-09

    m1_min = 1
    m1_max = 5000

    v_mu = args.vmu.split(',')

    for mu in v_mu:

        print ('Processing mu =', mu)

        best_m1, best_br = find_best_m1(m1_min, m1_max, m2, m3, mu, tanb, msq, at, gmass, br_to, br_eq, args.precision)

        print ('best m1 = %f with BR(N1->%s) = %f' % (best_m1, br_to, best_br))


    susyhitutils.clean_run_directory()



if __name__ == '__main__':
    main()
