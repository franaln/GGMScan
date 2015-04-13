#! /usr/bin/env python2.7

import os
import sys
import glob
import math
import shutil
import string
import datetime
import argparse
import multiprocessing
from progressbar import ProgressBar

## Suspect
def writeSuspectPar(m1, m3, mu, msq, at, tanbeta):

    #arguments: M1, M3, mu, At
    Msf12 = 2.5E+03
    Msf3 = 2.5E+03

    # inputs remaining constant through the scan:
    SLHAInputTemplate = string.Template("""\
Block MODSEL                 # Select model
   1    ${MODSEL}            # general MSSM low scale
Block SU_ALGO  # !Optional SUSPECT v>=2.3* block: algorithm control parameters
# !IF block absent (or if any parameter undefined), defaut values are taken
   2    21  # 2-loop RGE (defaut, 1-loop RGE is: 11 instead)
   3    1   # 1: g_1(gut) = g_2(gut) consistently calculated from input
#   (other possibility is 0: High scale input =HIGH in block EXTPAR below)
   4    2   # RGE accuracy: 1: moderate, 2: accurate (but slower)
   6    1   #  1: M_Hu, M_Hd input (default in constrained models)
#        (other possibility 0: MA_pole, MU(EWSB) input instead)
   7    2   #  choice for sparticles masses rad. corr. (=/= h):
#               2 ->all (recommended, defaut); 1->no R.C. in squarks & gauginos.
   8    0   # 1 (default): EWSB scale=(mt_L*mt_R)^(1/2)
#         (Or = 0: arbitrary EWSB scale: give EWSB in Block EXTPAR below)
   9    2   # Final spectrum accuracy: 1 -> 1% acc.; 2 -> 0.01 % acc.(defaut)
   10   2   # Higgs boson masses rad. corr. calculation options:
#             A simple (but very good) approximation (advantage=fast)  : 0
#             Full one-loop calculation                                : 1
#             One-loop  + dominant DSVZ 2-loop (defaut,recommended)    : 2
   11   0   # Higher order Higgs 'scheme' choice in rad. corr. at mZ:
#          RUNNING DRbar Higgs masses at loop-level at mZ (defaut)    : 0
#          POLE          Higgs masses at loop-level at mZ             : 1
Block SMINPUTS               # Standard Model inputs
   1     1.27932904E+02  # alpha_em^-1(MZ)^MSbar
#   2     1.16639000E-05  # G_mu [GeV^-2]
   3     1.17200000E-01  # alpha_s(MZ)^MSbar
#   4     9.11876000E+01  # m_Z(pole)
   5     4.25000000E+00  # m_b(m_b), MSbar
   6     1.72900000E+02  # m_t(pole)
   7     1.77700000E+00  # m_tau(pole)
Block MINPAR                 # Input parameters
#   input for GMSB models (! comment (#) all other (mSUGRA,AMSB) lines):
Block EXTPAR                 # Input parameters
   0     9.11876000E+01   # EWSB_scale
   1     ${M1}      # M_1
   2     2.5E+03    # M_2
   3     ${M3}      # M_3
   11    ${At}      # A_t
   12    0.00E+00   # A_b
   13    0.00E+00   # A_tau
   14    0.00E+00   # A_u
   15    0.00E+00   # A_d
   16    0.00E+00   # A_e
   23    ${mu}      # mu(EWSB)
   26    2.00E+03   # MA_pole
   25    ${tanBeta} # tanbeta(MZ)
   31    ${Msf12}   # M_eL
   32    ${Msf12}   # M_muL
   33    ${Msf3}    # M_tauL
   34    ${Msf12}   # M_eR
   35    ${Msf12}   # M_muR
   36    ${Msf3}    # M_tauR
   41    ${Msq}     # M_q1L
   42    ${Msq}     # M_q2L
   43    ${Msq}     # M_q3L
   44    ${Msf12}   # M_uR
   45    ${Msf12}   # M_cR
   46    ${Msf3}    # M_tR
   47    ${Msq}     # M_dR
   48    ${Msq}     # M_sR
   49    ${Msq}     # M_bR
""")

    SLHAInput = SLHAInputTemplate.substitute({
        'MODSEL' : 0,
        'M1' : m1,
        'M3' : m3,
        'mu' : mu,
        'Msq': msq,
        'At' : at,
        'Msf12' : Msf12,
        'Msf3' : Msf3,
        'tanBeta' : tanbeta,
    })

    InFile = open('suspect2_lha.in', 'w')
    InFile.write(SLHAInput)
    InFile.close()


##--
def main():

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-c', dest='configfile', required=True, help='Configfile')
    parser.add_argument('-o', dest='outputdir', help='Output directory')
    #parser.add_argument('-n', dest='ncores', type=int, default=1, help='Cores to use')
    parser.add_argument('--count', action='store_true', help='Count number of jobs')

    args = parser.parse_args()

    try:
        execfile(args.configfile, globals())

        # check needed vectors
        v_M1, v_mu, v_M3, v_At, v_Gmass, v_Msq, v_tanbeta

    except:
        print 'Error in the configile. exit...'
        sys.exit(1)


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
        #print 'Aprox. time (at 1 Hz): %s days, %s hours, %s minutes, %s seconds' % (
        sys.exit(1)

    # Run directory
    if args.outputdir is None:
        t = datetime.datetime.now()
        datestr = '%s-%s-%s_%s.%s.%s' % (t.year, t.month, t.day, t.hour, t.minute, t.second)

        run_dir = 'SusyGridRun_%s' % datestr
        os.system('mkdir -p %s' % run_dir)

    else:
        run_dir = args.outputdir

        if not os.path.exists(run_dir):
            os.system('mkdir -p %s' % run_dir)

    # Copy SUSYHIT executables
    shutil.copy2(os.environ['SUSYGRID'] + '/SuSpect/suspect2', '%s/suspect2' % run_dir)
    shutil.copy2(os.environ['SUSYGRID'] + '/SUSYHIT/run', '%s/runSUSYHIT' % run_dir)
    shutil.copy2(os.environ['SUSYGRID'] + '/SUSYHIT/susyhit.in', '%s/susyhit.in' % run_dir)

    os.chdir(run_dir)

    # Check scan status
    slha_files = glob.glob('at*.slha') + glob.glob('0/at*.slha')

    if len(slha_files) > 0:
        done_files = filter(os.path.isfile, slha_files)
        done_files.sort(key=lambda x: os.path.getmtime(x))

        print 'Found %i slha files already done. Continue with the remaining jobs...' % len(done_files)

        # FIX: check for errors in done_files
        done_files = done_files[:-1]
    else:
        done_files = []

    # SUSY-HIT: generate SLHA files one by one
    bar = ProgressBar(njobs, len(done_files))

    # pool = multiprocessing.Pool(processes=args.ncores)
    # jobs = []
    outdir = '.'

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

                                if (progress % 1000) == 0:
                                    outdir = '%i' % (progress % 1000)
                                    os.system('mkdir -p %s' % outdir)

                                outfile = 'at_%s_tanb_%s_msq_%s_m3_%s_m1_%s_mu_%s_Gmass_%s.slha' % (at, tanb, msq, m3, m1, mu, Gmass)

                                if outfile in done_files:
                                    continue

                                # pool.apply(worker, args=(progress, m1, m3, mu, at, tanbeta, Gmass,))
                                #worker(progress, at, tanb, msq, m3, m1, mu, Gmass)

                                # Create Suspect input
                                writeSuspectPar(m1, m3, mu, msq, at, tanb)

                                # Run Suspect
                                #log.write('Running Suspect\n')
                                os.system('./suspect2 > /dev/null')

                                # Copy Suspect output to SUSYHIT input
                                os.system('mv suspect2_lha.out slhaspectrum.in')

                                # hack MODSEL (to make it 'look like' GMSB)
                                os.system("sed -i 's/.*general MSSM.*/     1   2    #GMSB/' slhaspectrum.in")

                                # add the gravitino by hand!
                                os.system('AddGravitino slhaspectrum.in 1E-9')

                                # Fix Higgs mass (if needed)
                                # if [ "$customHmass" -eq 1 ];then
                                #     ./FixHiggs slhaspectrum.in $Hmass
                                # fi

                                # Run SUSYHIT
                                #log.write('Running SUSYHIT\n')
                                os.system('./runSUSYHIT > /dev/null')

                                os.system('mv susyhit_slha.out %s' % os.path.join(outdir, outfile))

                                bar.print_bar(progress)
                                progress += 1


# end of loops

# pool.close()

if __name__ == '__main__':
    main()
