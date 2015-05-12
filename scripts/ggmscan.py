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


def get_br_n1_Gy(slhafile):
    br_n1_Gy = 0
    for dc in pyslha.read(slhafile).decays[1000022].decays:
        if abs(dc.ids[0]) == 1000039 and abs(dc.ids[1]) == 22:
            br_n1_Gy += dc.br

    return br_n1_Gy


def find_best_m1(at, tanb, msq, m3, mu, Gmass, m1_min, m1_max, precision=0.005):

    """
    Find M1/mu relation using bisection method :D
    """

    if args.verbose:
        print 'find best m1 for m3 = %f, mu = %f with below %f %%' % (m3, mu, precision*100)

    m1_a = m1_min
    m1_b = m1_max

    br_p = 99

    iteration = 0

    while abs(br_p) > precision and iteration < 100:

        m1_p = (m1_a + m1_b) / 2

        # A
        outfile = susyhituitls.generate_slha(at, tanb, msq, m3, m1_a, mu, Gmass)

        br_n1_Gy = get_br_n1_Gy(outfile)

        br_a = br_n1_Gy - 0.5

        # B
        outfile = susyhituitls.generate_slha(at, tanb, msq, m3, m1_b, mu, Gmass)

        br_n1_Gy = get_br_n1_Gy(outfile)

        br_b = br_n1_Gy - 0.5

        # P
        outfile = susyhituitls.generate_slha(at, tanb, msq, m3, m1_p, mu, Gmass)

        br_n1_Gy = get_br_n1_Gy(outfile)

        br_p = br_n1_Gy - 0.5

        ###
        if br_a * br_p < 0:
            m1_a = m1_a
        else:
            m1_a = m1_p

        if br_b * br_p < 0:
            m1_b = m1_b
        else:
            m1_b = m1_p

        iteration += 1

    return m1_p, br_n1_Gy


##--
def main():

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-c', dest='configfile', required=True, help='Configfile')
    parser.add_argument('-o', dest='outputdir', help='Output directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose')
    parser.add_argument('--count', action='store_true', help='Count number of jobs')
    parser.add_argument('--scan', action='store_true', help='Scan')
    #parser.add_argument('--m1mu', action='store_true', help='Find best m1/mu relation')

    global args
    args = parser.parse_args()

    try:
        execfile(args.configfile, globals())

        # check needed vectors
        v_mu, v_M3, v_At, v_Gmass, v_Msq, v_tanbeta, v_M1

    except:
        print 'Error in the configile. exit...'
        raise

    def default_filter_fn(at, tanb, msq, m3, m1, mu, Gmass):
        pass

    try:
        filter_fn_copy = filter_fn
    except:
        print 'No filter function defined in config file'
        filter_fn_copy = default_filter_fn

    # Count total jobs
    njobs = 0
    for at in v_At:
        for tanb in v_tanbeta:
            for msq in v_Msq:
                for m3 in v_M3:
                    for m1 in v_M1:
                        for mu in v_mu:
                            for Gmass in v_Gmass:
                                if filter_fn_copy(at, tanb, msq, m3, m1, mu, Gmass):
                                    continue

                                njobs += 1

    if args.count:
        print 'Number of jobs: %i' % njobs
        return

    # Run directory
    if args.outputdir is None:
        t = datetime.datetime.now()
        datestr = '%s-%s-%s_%s.%s.%s' % (t.year, t.month, t.day, t.hour, t.minute, t.second)
        run_dir = 'SusyGridRun_%s' % datestr
    else:
        run_dir = args.outputdir

    susyhitutils.create_run_directory(run_dir)

    if args.scan:

        # Check scan status
        slha_files = glob.glob('at*.slha')
        if len(slha_files) > 0:
            done_files = filter(os.path.isfile, slha_files)
            done_files.sort(key=lambda x: os.path.getmtime(x))
            done_files = done_files[:-1] # FIX: check for errors in done_files
            print 'Found %i slha files already done. Continue with the remaining jobs...' % len(done_files)
        else:
            done_files = []


        bar = ProgressBar(njobs, len(done_files))

        rm_files = 0

        progress = len(done_files) + 1
        for at in v_At:
            for tanb in v_tanbeta:
                for msq in v_Msq:
                    for m3 in v_M3:
                        for m1 in v_M1:
                            for mu in v_mu:
                                for Gmass in v_Gmass:
                                    if filter_fn_copy(at, tanb, msq, m3, m1, mu, Gmass):
                                        continue

                                    outfile = 'at_%s_tanb_%s_msq_%s_m3_%s_m1_%s_mu_%s_Gmass_%s.slha' % (at, tanb, msq, m3, m1, mu, Gmass)

                                    if outfile in done_files:
                                        continue

                                    susyhitutils.generate_slha(at, tanb, msq, m3, m1, mu, Gmass, outfile)

                                    ## Check that the n1 mass is below gluino mass, otherwise remove slha file
                                    masses = pyslha.read(outfile).blocks['MASS']
                                    m_gl = masses[1000021]
                                    m_n1 = masses[1000022]

                                    if m_n1 > m_gl:
                                        rm_files += 1
                                        os.system('rm %s' % outfile)

                                    bar.print_bar(progress)
                                    progress += 1
        # end of loops
        print '%i files removed beacuse m_n1 > m_gl' % rm_files

    susyhitutils.clean_run_directory()







if __name__ == '__main__':
    main()
