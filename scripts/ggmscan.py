#! /usr/bin/env python

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


def main():

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-c', dest='configfile', required=True, help='Configfile')
    parser.add_argument('-o', dest='outputdir', help='Output directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose')

    parser.add_argument('--count', action='store_true', help='Count number of jobs')
    parser.add_argument('--scan', action='store_true', help='Do parameters scan')


    global args
    args = parser.parse_args()

    try:
        execfile(args.configfile, globals())

        # check needed vectors
        v_mu, v_m1, v_m2, v_m3, v_at, v_gmass, v_msq, v_tanb

    except:
        print('Error in the configile. exit...')
        print('Configfile must have the following vectors: v_m1, v_m2, v_m3, v_mu, v_msq, v_tanb, v_at, v_gmass')
        raise

    def default_filter_fn(m1, m2, m3, mu, tanb, msq, at, gmass):
        pass

    global filter_fn_copy
    try:
        filter_fn_copy = filter_fn
    except:
        print('No filter function defined in config file')
        filter_fn_copy = default_filter_fn

    # Count total jobs
    njobs = 0
    for at in v_at:
        for tanb in v_tanb:
            for msq in v_msq:
                for m3 in v_m3:
                    for m2 in v_m2:
                        for m1 in v_m1:
                            for mu in v_mu:
                                for Gmass in v_gmass:
                                    if filter_fn_copy(at, tanb, msq, m3, m1, mu, Gmass):
                                        continue
                                    njobs += 1

    if args.count:
        print('Number of jobs: %i' % njobs)
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
            print('Found %i slha files already done. Continue with the remaining jobs...' % len(done_files))
        else:
            done_files = []


        bar = ProgressBar(njobs, len(done_files))

        rm_files = 0

        progress = len(done_files) + 1
        for at in v_at:
            for tanb in v_tanb:
                for msq in v_msq:
                    for m3 in v_m3:
                        for m2 in v_m2:
                            for m1 in v_m1:
                                for mu in v_mu:
                                    for Gmass in v_Gmass:
                                        if filter_fn_copy(at, tanb, msq, m3, m1, mu, Gmass):
                                            continue

                                        outfile = 'at_%s_tanb_%s_msq_%s_m3_%s_m1_%s_mu_%s_Gmass_%s.slha' % (at, tanb, msq, m3, m1, mu, Gmass)

                                        if outfile in done_files:
                                            continue

                                        susyhitutils.generate_slha(m1, m2, m3, mu, tanb, msq, at, Gmass, outfile)


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
        print('%i files removed beacuse m_n1 > m_gl' % rm_files)


    # Clean directory
    susyhitutils.clean_run_directory()



if __name__ == '__main__':
    main()
