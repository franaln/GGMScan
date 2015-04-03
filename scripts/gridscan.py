#! /usr/bin/env python2.7

import os
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
parser = argparse.ArgumentParser(description='')
#parser.add_argument('slhapath', nargs='?', help='Path to slha files')
parser.add_argument('-o', dest='output_dir', help='Output directory', required=True)
parser.add_argument('-n', dest='ncores', type=int, default=1, help='Cores to use')

args = parser.parse_args()

# if args.slhapath is None:
#     parser.print_usage()
#     sys.exit()


# Run directory
t = datetime.datetime.now()
datestr = '%s-%s-%s_%s.%s.%s' % (t.year, t.month, t.day, t.hour, t.minute, t.second)

run_dir = os.path.join(args.output_dir, 'SusyGridRun_%s' % datestr)
os.system('mkdir %s' % run_dir)

# Copy SUSYHIT executables
shutil.copy2(os.environ['SUSYGRID'] + '/SuSpect/suspect2', '%s/suspect2' % run_dir)
shutil.copy2(os.environ['SUSYGRID'] + '/SUSYHIT/run', '%s/runSUSYHIT' % run_dir)
shutil.copy2(os.environ['SUSYGRID'] + '/SUSYHIT/susyhit.in', '%s/susyhit.in' % run_dir)

os.chdir(run_dir)

# SUSYHIT scan
## Parameter values
mu_min = 50
mu_max = 2000
mu_step = 50

m1_min = 50
m1_max = 2000
m1_step = 50

m1mu_min = 0.98
m1mu_max = 1.0

m3_min = 50
m3_max = 2000
m3_step = 50

msq_min = 800
msq_max = 1500
msq_step = 50

v_At = [0] #At possible values

hmass = 125
tanbeta = 1.5

iN_m1  = (m1_max - m1_min)/m1_step
iN_m3  = (m3_max - m3_min)/m3_step
iN_mu  = (mu_max - mu_min)/mu_step
iN_msq = (msq_max - msq_min)/msq_step

grid_type = '0'

if grid_type == "0":
    iN_msq = 1
    msq_min = 2.5E+03
else:
    iN_m3 = 1
    m3_min = 2.5E+03

# Construct vectors
v_M1 = [ m1_min + ir_m1 * m1_step for ir_m1 in xrange(iN_m1) ]
v_mu = [ mu_min + ir_mu * mu_step for ir_mu in xrange(iN_mu) ]

v_M3  = [ m3_min  + ir_m3 * m3_step for ir_m3 in xrange(iN_m3) ]
v_Msq = [ msq_min + ir_msq * msq_step for ir_msq in xrange(iN_msq) ]

v_Gmass = [1E-09,]

useM1muRelation = False
useFixedMu = True
useMuPositive = True

vbos = False


# Count jobs
njobs = 0
for at in v_At:
    for mu in v_mu:
        for m3 in v_M3:
            for msq in v_Msq:
                for Gmass in v_Gmass:
                    for m1 in v_M1:
                        # make sure that the (aprox) M(chi10) is greater than M(gluino)
                        if mu > m3 or mu > msq:
                            continue

                        njobs += 1


bar = ProgressBar(njobs)

# SUSY-HIT: generate SLHA files one by one
def worker(i, m1, m3, mu, at, tanbeta, Gmass):

    # if (Progress % 10 == 0):

    outfile = 'M1_%s_M3_%s_mu_%s_At_%s_tanB_%s_Gmass_%s.out' % (m1, m3, mu, at, tanbeta, Gmass)

    # Create Suspect input
    writeSuspectPar(m1, m3, mu, msq, at, tanbeta)

    # Run Suspect
    #print 'Running Suspect'
    os.system('./suspect2 > /dev/null')

    # Save suspect output
    #os.system('cp suspect2_lha.out suspect2_lha_%s' % '

    # Copy Suspect output to SUSYHIT input
    shutil.copy2('suspect2_lha.out', 'slhaspectrum.in')

    # #hack MODSEL (to make it 'look like' GMSB)
    os.system("sed -i 's/.*general MSSM.*/     1   2    #GMSB/' slhaspectrum.in")

    #Fix ~t_1 mass (if needed)
    #if [ "$gtype" == "1" ];then
    #     ./FixT1mass slhaspectrum.in $msq
    # fi

    #add the gravitino by hand!
    os.system('AddGravitino slhaspectrum.in 1E-9')

    #Fix Higgs mass (if needed)
    #if [ "$customHmass" -eq 1 ];then
    #     ./FixHiggs slhaspectrum.in $Hmass
    # fi

    #run SUSYHIT
    # echo ' Launching SUSYHIT ...'
    #print 'Running SUSYHIT'
    os.system('./runSUSYHIT > /dev/null')

    shutil.copy2('susyhit_slha.out', outfile)

    bar.print_bar(i)



pool = multiprocessing.Pool(processes=args.ncores)

progress = 0
jobs = []
for at in v_At:

    for mu in v_mu:

        for m3 in v_M3:

            for msq in v_Msq:

                for Gmass in v_Gmass:

                    for m1 in v_M1:

                        # make sure that the (aprox) M(chi10) is greater than M(gluino)
                        if mu > m3 or mu > msq:
                            continue

                        pool.apply(worker, args=(progress, m1, m3, mu, at, tanbeta, Gmass,))

                        progress += 1


# end of loops

pool.close()
