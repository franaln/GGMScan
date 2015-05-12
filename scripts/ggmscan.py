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
import pyslha

## Suspect
def writeSuspectPar(m1, m3, mu, msq, at, tanbeta):

    #arguments: M1, M3, mu, At
    Msf12 = msq #5E+03
    Msf3  = msq #5E+03

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
#  2     1.16639000E-05  # G_mu [GeV^-2]
   3     1.17200000E-01  # alpha_s(MZ)^MSbar
#  4     9.11876000E+01  # m_Z(pole)
   5     4.25000000E+00  # m_b(m_b), MSbar
   6     1.72900000E+02  # m_t(pole)
   7     1.77700000E+00  # m_tau(pole)
Block MINPAR                 # Input parameters
#   input for GMSB models (! comment (#) all other (mSUGRA,AMSB) lines):
Block EXTPAR                 # Input parameters
   0     9.11876000E+01   # EWSB_scale
   1     ${M1}      # M_1
   2     5.0E+03    # M_2
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
    parser.add_argument('--count', action='store_true', help='Count number of jobs')

    parser.add_argument('-v', '--verbose', action='store_true', help='verbose')

    parser.add_argument('--scan', action='store_true', help='Scan')
    parser.add_argument('--m1mu', action='store_true', help='Find best m1/mu relation')
    parser.add_argument('--grid', action='store_true', help='Create grid: use M1/mu dict relation')
    parser.add_argument('--tunemu', action='store_true', help='Tune mu using bisection method')


    args = parser.parse_args()

    try:
        execfile(args.configfile, globals())

        # check needed vectors
        v_mu, v_M3, v_At, v_Gmass, v_Msq, v_tanbeta, v_M1

        if args.grid:
            m3mu_dict
            mum1_dict

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

    if args.grid:
        v_M1_copy = [-99,]
    else:
        v_M1_copy = v_M1

    # Count total jobs
    njobs = 0
    for at in v_At:
        for tanb in v_tanbeta:
            for msq in v_Msq:
                for m3 in v_M3:
                    for m1 in v_M1_copy:
                        for mu in v_mu:
                            for Gmass in v_Gmass:
                                if filter_fn_copy(at, tanb, msq, m3, m1, mu, Gmass):
                                    continue

                                njobs += 1

    if args.count:
        print 'Number of jobs: %i' % njobs
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
    def generate_slha(at, tanb, msq, m3, m1, mu, Gmass, outfile=None):

        if outfile is None:
            outfile = 'at_%s_tanb_%s_msq_%s_m3_%s_m1_%s_mu_%s_Gmass_%s.slha' % (at, tanb, msq, m3, m1, mu, Gmass)

        if outfile in os.listdir('.'):
            return outfile

        # Create Suspect input
        writeSuspectPar(m1, m3, mu, msq, at, tanb)

        # Run Suspect
        st = os.system('./suspect2 > /dev/null')

        if st != 0:
            return None

        # Copy Suspect output to SUSYHIT input
        os.system('mv suspect2_lha.out slhaspectrum.in')

        # hack MODSEL (to make it 'look like' GMSB)
        os.system("sed -i 's/.*general MSSM.*/     1   2    #GMSB/' slhaspectrum.in")

        # add the gravitino by hand!
        os.system('AddGravitino slhaspectrum.in %s' % Gmass)

        # Run SUSYHIT
        os.system('./runSUSYHIT > /dev/null')

        os.system('mv susyhit_slha.out %s' % os.path.join(outdir, outfile))

        return outfile


    outdir = '.'

    if args.scan:

        bar = ProgressBar(njobs, len(done_files))

        progress = len(done_files) + 1
        for at in v_At:
            for tanb in v_tanbeta:
                for msq in v_Msq:
                    for m3 in v_M3:
                        for m1 in v_M1_copy:
                            for mu in v_mu:
                                for Gmass in v_Gmass:
                                    if filter_fn_copy(at, tanb, msq, m3, m1, mu, Gmass):
                                        continue

                                    # if args.grid:
                                    #     m1 = m1mu_dict.get(mu)

                                    outfile = 'at_%s_tanb_%s_msq_%s_m3_%s_m1_%s_mu_%s_Gmass_%s.slha' % (at, tanb, msq, m3, m1, mu, Gmass)

                                    if outfile in done_files:
                                        continue

                                    generate_slha(at, tanb, msq, m3, m1, mu, Gmass)

                                    ##
                                    masses = pyslha.read(outfile).blocks['MASS']
                                    m_gl = masses[1000021]
                                    m_n1 = masses[1000022]

                                    if m_n1 > m_gl:
                                        os.system('rm %s' % outfile)


                                    bar.print_bar(progress)
                                    progress += 1
        # end of loops


    # Find M1/mu relation using bisection method :D
    def get_br_n1_Gy(slhafile):
        br_n1_Gy = 0
        for dc in pyslha.read(slhafile).decays[1000022].decays:
            if abs(dc.ids[0]) == 1000039 and abs(dc.ids[1]) == 22:
                br_n1_Gy += dc.br

        return br_n1_Gy

    if args.grid:

        at = v_At[0]
        tanb = v_tanbeta[0]
        msq = v_Msq[0]
        Gmass = v_Gmass[0]

        for m3, mulist in m3mu_dict.iteritems():

            for mu in mulist:

                factor = (1E-07/(float(m3)-150))*(float(mu)-150)
                Gmass = 1E-09 + (1E-07/(float(m3)-150))*(float(mu)-150)

                m1 = mum1_dict.get(mu)

                outfile = 'm3_%s_m1_%s_mu_%s.slha' % (m3, m1, mu)

                outfile = generate_slha(at, tanb, msq, m3, m1, mu, Gmass, outfile=outfile)

                print outfile
                print get_br_n1_Gy(outfile)


        # end of loops



    def find_best_m1(at, tanb, msq, m3, mu, Gmass, m1_min, m1_max, precision=0.005):

        if args.verbose:
            print 'find best m1 for m3 = %f, mu = %f with below %f %%' % (m3, mu, precision*100)

        m1_a = m1_min
        m1_b = m1_max

        br_p = 99

        iteration = 0

        while abs(br_p) > precision and iteration < 100:

            m1_p = (m1_a + m1_b) / 2

            # A
            outfile = generate_slha(at, tanb, msq, m3, m1_a, mu, Gmass)

            br_n1_Gy = get_br_n1_Gy(outfile)

            br_a = br_n1_Gy - 0.5

            # B
            outfile = generate_slha(at, tanb, msq, m3, m1_b, mu, Gmass)

            br_n1_Gy = get_br_n1_Gy(outfile)

            br_b = br_n1_Gy - 0.5

            # P
            outfile = generate_slha(at, tanb, msq, m3, m1_p, mu, Gmass)

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


    if args.m1mu:

        at = v_At[0]
        tanb = v_tanbeta[0]
        msq = v_Msq[0]
        m3 = v_M3[0]
        Gmass = v_Gmass[0]

        m1_min = v_M1[0]
        m1_max = v_M1[-1]

        for mu in v_mu:

            print 'Processing mu =', mu

            best_m1, best_br = find_best_m1(at, tanb, msq, m3, mu, Gmass, m1_min, m1_max)

            print 'best m1 = %f with BR(N1->~Gy) = %f' % (best_m1, best_br)


    ## Diagonal
    # at = v_At[0]
    # tanb = v_tanbeta[0]
    # msq = v_Msq[0]
    # Gmass = v_Gmass[0]

    # m1_min = 10
    # m1_max = 2000

    # mu_min = v_mu[0]
    # mu_max = v_mu[-1]


    # def F(slhafile):
    #     try:
    #         masses = pyslha.read(slhafile).blocks['MASS']

    #         m_gl = masses[1000021]
    #         m_n1 = masses[1000022]

    #         return (m_gl - m_n1 - 20)
    #     except:
    #         return 10000

    # for m3 in v_M3:

    #     mu_a = m3-200
    #     mu_b = m3+200

    #     F_p = 99

    #     while abs(F_p) > 5:

    #         print 'Processing m3 = %i, mu between %f and %f, F(p) = %f' % (m3, mu_a, mu_b, F_p)

    #         mu_p = (mu_a + mu_b) / 2

    #         # A
    #         mu = mu_a
    #         m1 = find_best_m1(at, tanb, msq, m3, mu, Gmass, m1_min, m1_max, 0.1)

    #         outfile = generate_slha(at, tanb, msq, m3, m1, mu, Gmass)

    #         F_a = F(outfile)

    #         # B
    #         mu = mu_b
    #         m1 = find_best_m1(at, tanb, msq, m3, mu, Gmass, m1_min, m1_max, 0.1)

    #         outfile = generate_slha(at, tanb, msq, m3, m1, mu, Gmass)

    #         F_b = F(outfile)

    #         # P
    #         mu = mu_p
    #         m1 = find_best_m1(at, tanb, msq, m3, mu, Gmass, m1_min, m1_max, 0.1)

    #         outfile = generate_slha(at, tanb, msq, m3, m1, mu, Gmass)

    #         F_p = F(outfile)

    #         ###
    #         if F_a * F_p < 0:
    #             mu_a = mu_a
    #         else:
    #             mu_a = mu_p

    #         if F_b * F_p < 0:
    #             mu_b = mu_b
    #         else:
    #             mu_b = mu_p

    #     print 'm3 =', m3, ' best mu =', mu_p, 'best m1 =', m1




if __name__ == '__main__':
    main()
