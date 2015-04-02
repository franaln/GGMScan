#! /usr/bin/env python

import os
import sys
import pyslha
import ROOT
import array
import argparse

# config
parser = argparse.ArgumentParser(description='draw particles decays from grid slha files')
parser.add_argument('slhapath', nargs='?', help='Path to slha files')
parser.add_argument('-o', dest='output_file', help='Output file')

args = parser.parse_args()

if args.slhapath is None:
    parser.print_usage()
    sys.exit()

outfile = ROOT.TFile(args.output_file, 'recreate')

def compare(x, y):
    sx = os.path.basename(x).split('.')[0].split('_')
    sy = os.path.basename(y).split('.')[0].split('_')

    for i in xrange(len(x)):
        if sx[i] == sy[i]:
            continue
        try:
            nx = int(sx[i])
            ny = int(sy[i])
            if nx < ny:
                return -1
            elif nx == ny:
                return 0
            else:
                return 1
        except:
            continue

paths = [os.path.join(args.slhapath, f) for f in os.listdir(args.slhapath)]

slha_files = sorted(paths, cmp=compare)


# Output file and output tree
output_file = ROOT.TFile(args.output_file, 'recreate')

# create the ntuple
variables = [
    # parameters
    'm1',
    'm2',
    'm3',
    'mu',
    'msq',

    # masses
    'm_h',
    'm_gl',
    'm_n1',
    'm_n2',
    'm_n3',
    'm_n4',
    'm_c1',
    'm_c2',
    'm_G',

    # BR
    'br_gl_n1g',
    'br_gl_n2g',
    'br_gl_n3g',
    'br_gl_n1qq',
    'br_gl_n2qq',
    'br_gl_n3qq',
    'br_gl_c1qq',
    'br_gl_n1',
    'br_gl_n2',
    'br_gl_n3',
    'br_gl_c1',
    'br_gl_Gg',

    'br_n1_Gy',
    'br_n1_GZ',
    'br_n1_Gh',

    'br_n2_n1',
    'br_n2_c1',
    'br_n2_GX',

    'br_n3_n1',
    'br_n3_n2',
    'br_n3_c1',
    'br_n3_GX',
]

ntuple = ROOT.TNtuple('slha', 'slha', ':'.join(variables))

# Loop over input spectrum files
for infile in slha_files:

    ## Read spectrum file
    BLOCKS, DECAYS = None, None
    try:
        doc = pyslha.read(infile)
        BLOCKS, DECAYS = doc.blocks, doc.decays
    except pyslha.ParseError, pe:
        print str(pe) + "... exiting"
        sys.exit(1)


    ## SUSY parameters
    params = BLOCKS['EXTPAR']

    m1 = params[1]
    m2 = params[2]
    m3 = params[3]
    mu = params[23]
    msq = params[41]
    tanb = params[25]


    ## Masses
    masses = BLOCKS['MASS']

    m_h = abs(masses[25])
    m_gl = abs(masses[1000021])
    m_n1 = abs(masses[1000022])
    m_n2 = abs(masses[1000023])
    m_n3 = abs(masses[1000025])
    m_n4 = abs(masses[1000035])
    m_c1 = abs(masses[1000024])
    m_c2 = abs(masses[1000037])
    m_G = abs(masses[1000039])


    ## Decays

    # hbar = 6.582E-25  # GeV.s
    # cspeed = 2.99792458E8 #m.s

    ## gluino decays
    gluino = DECAYS[1000021]

    br_gl_n1qq = 0
    br_gl_n2qq = 0
    br_gl_n3qq = 0
    br_gl_c1qq = 0

    br_gl_n1g = 0
    br_gl_n2g = 0
    br_gl_n3g = 0

    br_gl_c1 = 0
    br_gl_Gg = 0
    for dc in gluino.decays:

        pid0 = abs(dc.ids[0])
        pid1 = abs(dc.ids[1])
        pid2 = abs(dc.ids[2]) if len(dc.ids) > 2 else 0

        if pid0 == 1000022: # ~g -> chi01 X
            if pid1 == 21:
                br_gl_n1g += dc.br
            elif (pid1 > 0 and pid1 < 9) and (pid2 > 0 and pid2 < 9):
                br_gl_n1qq += dc.br

        if pid0 == 1000023: # ~g -> chi02 X
            if pid1 == 21:
                br_gl_n2g += dc.br
            elif (pid1 > 0 and pid1 < 9) and (pid2 > 0 and pid2 < 9):
                br_gl_n2qq += dc.br

        elif pid0 == 1000025: # ~g -> chi03 X
            if pid1 == 21:
                br_gl_n3g += dc.br
            elif (pid1 > 0 and pid1 < 9) and (pid2 > 0 and pid2 < 9):
                br_gl_n3qq += dc.br

        elif pid0 == 1000024: # ~g -> chipm1 X
            br_gl_c1qq += dc.br
            br_gl_c1 += dc.br

        elif pid0 == 1000039 and pid1 == 21: # ~g -> ~G g
            br_gl_Gg += dc.br

    br_gl_n1 = br_gl_n1g + br_gl_n1qq
    br_gl_n2 = br_gl_n2g + br_gl_n2qq
    br_gl_n3 = br_gl_n3g + br_gl_n3qq


    # neutralino1 decays
    n1 = DECAYS[1000022]

    br_n1_GZ = 0
    br_n1_Gy = 0
    br_n1_Gh = 0
    for dc in n1.decays:

        pid0 = abs(dc.ids[0])
        pid1 = abs(dc.ids[1])

        if pid0 == 1000039 and pid1 == 23: # chi01 -> ~G Z
            br_n1_GZ += dc.br
        elif pid0 == 1000039 and pid1 == 22: # chi01 -> ~G y
            br_n1_Gy += dc.br
        elif pid0 == 1000039 and pid1 == 25: # chi01 -> ~G h0
            br_n1_Gh += dc.br


    # neutralino2 decays
    n2 = DECAYS[1000023]

    br_n2_n1 = 0
    br_n2_c1 = 0
    br_n2_GX = 0
    for dc in n2.decays:

        pid0 = abs(dc.ids[0])
        pid1 = abs(dc.ids[1])

        if pid0 == 1000022: # N2 -> N1
            br_n2_n1 += dc.br
        elif pid0 == 1000024: # N2 -> C1
            br_n2_c1 += dc.br
        elif pid0 == 1000039: # N2 -> ~G X
            br_n2_GX += dc.br

    # neutralino3 decays
    n3 = DECAYS[1000025]

    br_n3_n1 = 0
    br_n3_n2 = 0
    br_n3_c1 = 0
    br_n3_GX = 0
    for dc in n3.decays:

        pid0 = abs(dc.ids[0])
        pid1 = abs(dc.ids[1])

        if pid0 == 1000022: # N3 -> N1
            br_n3_n1 += dc.br
        elif pid0 == 1000023: # N3 -> N2
            br_n3_n2 += dc.br
        elif pid0 == 1000024: # N3 -> C1
            br_n3_c1 += dc.br
        elif pid0 == 1000039: # N3 -> ~G X
            br_n3_GX += dc.br


    values = [
        # parameters
        m1,
        m2,
        m3,
        mu,
        msq,

        # masses
        m_h,
        m_gl,
        m_n1,
        m_n2,
        m_n3,
        m_n4,
        m_c1,
        m_c2,
        m_G,

        # BR
        br_gl_n1g,
        br_gl_n2g,
        br_gl_n3g,
        br_gl_n1qq,
        br_gl_n2qq,
        br_gl_n3qq,
        br_gl_c1qq,
        br_gl_n1,
        br_gl_n2,
        br_gl_n3,
        br_gl_c1,
        br_gl_Gg,

        br_n1_Gy,
        br_n1_GZ,
        br_n1_Gh,

        br_n2_n1,
        br_n2_c1,
        br_n2_GX,

        br_n3_n1,
        br_n3_n2,
        br_n3_c1,
        br_n3_GX,
    ]

    ntuple.Fill(array.array("f", values))


ntuple.Write()
output_file.Close()