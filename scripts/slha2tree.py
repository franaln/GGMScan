#! /usr/bin/env python

import os
import sys
import pyslha
import ROOT
import array
import argparse

# config
parser = argparse.ArgumentParser(description='create tree from slha files')
parser.add_argument('slhapath', nargs='?', help='path to slha files')
parser.add_argument('-r', dest='recursive', action='store_true', help='recursive search slha files')
parser.add_argument('-o', dest='output_file', help='Output file', required=True)

args = parser.parse_args()

if args.slhapath is None:
    parser.print_usage()
    sys.exit()

outfile = ROOT.TFile(args.output_file, 'recreate')

def get_slha_files(dir_):

    for fname in os.listdir(dir_):

        path = os.path.join(dir_, fname)

        if os.path.isdir(path) and args.recursive:
            for rpath in get_slha_files(path):
                yield rpath

        elif os.path.isfile(path) and fname.endswith('.slha'):
            yield path


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
    'tanb',
    'at',

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

    'lsp',
    'nlsp',

    # neutralino mixing matrix
    'n11',
    'n12',
    'n13',
    'n14',
    'n21',
    'n22',
    'n23',
    'n24',
    'n31',
    'n32',
    'n33',
    'n34',
    'n41',
    'n42',
    'n43',
    'n44',

    # chargino mixing matrix
    'c11',
    'c12',
    'c21',
    'c22',

    # decay length
    'ctau_gl',
    'ctau_n1',
    'ctau_n2',

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

    'br_c1_n1',
    'br_c1_GW',
]

ntuple = ROOT.TNtuple('slha', 'slha', ':'.join(variables))

# Loop over input spectrum files
for evt, infile in enumerate(get_slha_files(args.slhapath)):

    if evt % 1000 == 0:
        print('Processing %i ...' % evt)

    ## Read spectrum file
    BLOCKS, DECAYS = None, None
    try:
        doc = pyslha.read(infile)
        BLOCKS, DECAYS = doc.blocks, doc.decays
    except (pyslha.ParseError, pe):
        print(str(pe) + " (%s) ... exiting" % infile)
        continue

    ## SUSY parameters
    params = BLOCKS['EXTPAR']

    m1   = params[1]
    m2   = params[2]
    m3   = params[3]
    mu   = params[23]
    msq  = params[41]
    tanb = params[25]
    at   = params[11]

    ## Masses
    masses = { k: abs(v) for k, v in BLOCKS['MASS'].items() }

    m_h  = masses[25]
    m_gl = masses[1000021]
    m_n1 = masses[1000022]
    m_n2 = masses[1000023]
    m_n3 = masses[1000025]
    m_n4 = masses[1000035]
    m_c1 = masses[1000024]
    m_c2 = masses[1000037]
    m_G  = masses[1000039]

    sorted_masses = sorted(masses.keys(), key=masses.get)
    sparticles = [i for i in sorted_masses if i>1000000]

    lsp  = sparticles[0]
    nlsp = sparticles[1]

    ## N mixing matrix
    nmix = BLOCKS['NMIX']
    n11 = nmix[(1,1)]
    n12 = nmix[(1,2)]
    n13 = nmix[(1,3)]
    n14 = nmix[(1,4)]
    n21 = nmix[(2,1)]
    n22 = nmix[(2,2)]
    n23 = nmix[(2,3)]
    n24 = nmix[(2,4)]
    n31 = nmix[(3,1)]
    n32 = nmix[(3,2)]
    n33 = nmix[(3,3)]
    n34 = nmix[(3,4)]
    n41 = nmix[(4,1)]
    n42 = nmix[(4,2)]
    n43 = nmix[(4,3)]
    n44 = nmix[(4,4)]

    ## Chargino mixing matrix
    umix = BLOCKS['UMIX']
    c11 = umix[(1,1)]
    c12 = umix[(1,2)]
    c21 = umix[(2,1)]
    c22 = umix[(2,2)]


    ## Decays
    hbar = 6.582E-25      # GeV.s
    cspeed = 2.99792458E8 # m.s

    ## gluino decays
    gluino = DECAYS[1000021]

    ctau_gl = hbar * cspeed / gluino.totalwidth * 1000.

    br_gl_n1qq = 0
    br_gl_n2qq = 0
    br_gl_n3qq = 0
    br_gl_c1qq = 0

    br_gl_n1g = 0
    br_gl_n2g = 0
    br_gl_n3g = 0

    br_gl_c1 = 0
    br_gl_Gg = 0
    br_gl_other = 0
    for dc in gluino.decays:

        pid0 = abs(dc.ids[0])
        pid1 = abs(dc.ids[1])
        pid2 = abs(dc.ids[2]) if len(dc.ids) > 2 else 0

        # ~g -> N1 X
        if pid0 == 1000022:
            if pid1 == 21:
                br_gl_n1g += dc.br
            elif (pid1 > 0 and pid1 < 9) and (pid2 > 0 and pid2 < 9):
                br_gl_n1qq += dc.br

        # ~g -> N2 X
        elif pid0 == 1000023:
            if pid1 == 21:
                br_gl_n2g += dc.br
            elif (pid1 > 0 and pid1 < 9) and (pid2 > 0 and pid2 < 9):
                br_gl_n2qq += dc.br

        # ~g -> N3 X
        elif pid0 == 1000025:
            if pid1 == 21:
                br_gl_n3g += dc.br
            elif (pid1 > 0 and pid1 < 9) and (pid2 > 0 and pid2 < 9):
                br_gl_n3qq += dc.br

        # ~g -> C1 X
        elif pid0 == 1000024:
            br_gl_c1qq += dc.br
            br_gl_c1   += dc.br

        # ~g -> ~G g
        elif pid0 == 1000039 and pid1 == 21:
            br_gl_Gg += dc.br

        else:
            br_gl_other += dc.br

    br_gl_n1 = br_gl_n1g + br_gl_n1qq
    br_gl_n2 = br_gl_n2g + br_gl_n2qq
    br_gl_n3 = br_gl_n3g + br_gl_n3qq


    # Fix files modified by hand
    br_total = br_gl_n1 + br_gl_n2 + br_gl_n3 + br_gl_c1 + br_gl_Gg + br_gl_other

    print(infile, br_total)
    if br_total < 0.99:
        br_gl_n1g  = br_gl_n1g/br_total
        br_gl_n1qq = br_gl_n1qq/br_total
        br_gl_n2g  = br_gl_n2g/br_total
        br_gl_n2qq = br_gl_n2qq/br_total
        br_gl_n3g  = br_gl_n3g/br_total
        br_gl_n3qq = br_gl_n3qq/br_total
        br_gl_c1   = br_gl_c1/br_total
        br_gl_c1qq = br_gl_c1qq/br_total
        br_gl_Gg   = br_gl_Gg/br_total
        br_gl_other   = br_gl_other/br_total

    br_gl_n1 = br_gl_n1g + br_gl_n1qq
    br_gl_n2 = br_gl_n2g + br_gl_n2qq
    br_gl_n3 = br_gl_n3g + br_gl_n3qq

    br_total = br_gl_n1 + br_gl_n2 + br_gl_n3 + br_gl_c1 + br_gl_Gg + br_gl_other
    print(br_total)


    # neutralino1 decays
    n1 = DECAYS[1000022]

    ctau_n1 = hbar * cspeed / n1.totalwidth * 1000.

    br_n1_GZ = 0
    br_n1_Gy = 0
    br_n1_Gh = 0
    for dc in n1.decays:

        pid0 = abs(dc.ids[0])
        pid1 = abs(dc.ids[1])

        # N1 -> ~G Z
        if pid0 == 1000039 and pid1 == 23:
            br_n1_GZ += dc.br

        # N1 -> ~G y
        elif pid0 == 1000039 and pid1 == 22:
            br_n1_Gy += dc.br

        # N1 -> ~G h0
        elif pid0 == 1000039 and pid1 == 25:
            br_n1_Gh += dc.br


    # neutralino2 decays
    n2 = DECAYS[1000023]

    ctau_n2 = hbar * cspeed / n2.totalwidth * 1000.

    br_n2_n1 = 0
    br_n2_c1 = 0
    br_n2_GX = 0
    for dc in n2.decays:

        pid0 = abs(dc.ids[0])
        pid1 = abs(dc.ids[1])

        # N2 -> N1
        if pid0 == 1000022:
            br_n2_n1 += dc.br

        # N2 -> C1
        elif pid0 == 1000024:
            br_n2_c1 += dc.br

        # N2 -> ~G X
        elif pid0 == 1000039:
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

        # N3 -> N1
        if pid0 == 1000022:
            br_n3_n1 += dc.br

        # N3 -> N2
        elif pid0 == 1000023:
            br_n3_n2 += dc.br

        # N3 -> C1
        elif pid0 == 1000024:
            br_n3_c1 += dc.br

        # N3 -> ~G X
        elif pid0 == 1000039:
            br_n3_GX += dc.br


    # chargino1 decays
    c1 = DECAYS[1000024]

    br_c1_n1 = 0
    br_c1_GW = 0
    for dc in c1.decays:

        pid0 = abs(dc.ids[0])
        pid1 = abs(dc.ids[1])

        # C1 -> N1
        if pid0 == 1000022:
            br_c1_n1 += dc.br

        # C1 -> ~G W
        elif pid0 == 1000039 and pid1 == 24:
            br_c1_GW += dc.br

    values = [
        # parameters
        m1,
        m2,
        m3,
        mu,
        msq,
        tanb,
        at,

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

        # LSP, NLSP
        lsp,
        nlsp,

        # neut mixing matrix
        n11,
        n12,
        n13,
        n14,
        n21,
        n22,
        n23,
        n24,
        n31,
        n32,
        n33,
        n34,
        n41,
        n42,
        n43,
        n44,

        # chargino mixing matrix
        c11,
        c12,
        c21,
        c22,

        # decay length
        ctau_gl,
        ctau_n1,
        ctau_n2,

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

        br_c1_n1,
        br_c1_GW,
    ]

    ntuple.Fill(array.array("f", values))


ntuple.Write()
output_file.Close()
print('done -> %s created' % args.output_file)
