#! /usr/bin/env python
# Code to draw mass spectrum from slha input file

import os
import sys
import string
import math
import argparse
import ROOT
import pyslha


color1 = ROOT.TColor.GetColor('#A60628')
color2 = ROOT.TColor.GetColor('#e2a233')
color3 = ROOT.TColor.GetColor('#32b43c')
color4 = ROOT.TColor.GetColor('#348ABD')
color5 = ROOT.TColor.GetColor('#188487')
color6 = ROOT.TColor.GetColor('#7A68A6')
color7 = ROOT.TColor.GetColor('#838283')

# colors = {
#     1000022:  color1,
#     1000023:  color1,
#     1000025:  color1,
#     1000035:  color1,
#     1000024:  color2,
#     1000037:  color2,
#     1000002:  color3,
#     2000002:  color3,
#     1000001:  color3,
#     2000001:  color3,
#     1000003:  color3,
#     2000003:  color3,
#     1000004:  color3,
#     2000004:  color3,
#     1000006:  color3,
#     2000006:  color3,
#     1000005:  color3,
#     2000005:  color3,
#     1000011:  color4,
#     2000011:  color4,
#     1000012:  color4,
#     1000013:  color4,
#     2000013:  color4,
#     1000014:  color4,
#     1000015:  color4,
#     2000015:  color4,
#     1000016:  color4,
#     25     :  ,
#     35     :  color5,
#     37     :  color5,
#     36     :  color5,
#     1000021:  color6,
#     1000039:  ,
# }

# labels = {

#     1000022:
#     1000023:
#     1000025:
#     1000035:
#     1000024:
#     1000037:

#     1000001: "#tilde{q}_{L}",
#     2000001: "#tilde{q}_{R}",

#     1000006: "#tilde{t}_{1}",
#     2000006: "#tilde{t}_{2}",

#     1000011: "#tilde{l}_{L}",
#     2000011: "#tilde{l}_{R}",
#     1000012: "#tilde{#nu}_{L}",


#     25     : ,
#     35     :
#     36     :
#     37     : ,
#     1000021: ,
#     1000039: ,
# }


class Particle:
    def __init__(self, mass, label, color):

        self.mass = mass

        self.label = label
        self.color = color


def main():

    parser = argparse.ArgumentParser(description='input options handler')

    parser.add_argument('ifile', metavar='INFILE', nargs='?', help='slha formatted file to be read')
    parser.add_argument('--maxmass', help='')

    args = parser.parse_args()

    ifile = args.ifile

    if ifile is None or not os.path.exists(ifile):
        parser.print_usage()
        sys.exit(1)

    ## Read spectrum file
    # try:
    #     doc = pyslha.read(ifile)
    #     print (doc.blocks)
    #     masses = [ abs(float(m)) for m in doc.blocks['MASS'] ]
    # except pyslha.ParseError as pe:
    #     print (str(pe) + "... exiting")
    #     sys.exit(1)
    start_reading = False
    masses = {}
    with open(ifile) as f:
        lines  = f.read().split('\n')

        for line in lines:
            if start_reading:
                try:
                    pdgid, mass, _, _ = line.split()

                    pdgid = int(pdgid)
                    mass = abs(float(mass))

                    masses[pdgid] = mass

                except:
                    continue

            elif line.startswith('BLOCK MASS'):
                start_reading = True
            else:
                continue


    def find_max(plst):
        max_ = 0
        for p in plst:
            if p.mass > max_:
                max_ = p.mass
        return max_

    def find_min(plst):
        min_ = 9999999
        for p in plst:
            if p.mass < min_:
                min_ = p.mass
        return min_


    ### Get mass of susy particles
    particles = [
        #gravitino
        Particle(masses[1000039], "#tilde{G}", color7),

        #Higgses
        Particle(masses[25], "h^{0}", color5),
        Particle(masses[35], "H^{0}", color5),
        Particle(masses[37], "A^{0}", color5),
        Particle(masses[36], "H^{#pm}", color5),

        #gluino
        Particle(masses[1000021], "#tilde{g}", color6),

        #Neutralinos
        Particle(masses[1000022], '#tilde{#chi}^{0}_{1}', color1),
        Particle(masses[1000023], '#tilde{#chi}^{0}_{2}', color1),
        Particle(masses[1000025], '#tilde{#chi}^{0}_{3}', color1),
        Particle(masses[1000035], '#tilde{#chi}^{0}_{4}', color1),

        #Charginos
        Particle(masses[1000024], '#tilde{#chi}^{#pm}_{1}', color2),
        Particle(masses[1000037], '#tilde{#chi}^{#pm}_{2}', color2),
    ]

    ## Sleptons
    sleptons = [
        1000011,
        2000011,
        1000013,
        2000013,
    ]

    max_val = max([ masses[pid] for pid in sleptons ])
    min_val = min([ masses[pid] for pid in sleptons ])

    if (max_val - min_val) < 5:
        particles.append(Particle(min_val, "#tilde{l}", color4))
    else:
        particles.append(Particle(masses[1000011], "#tilde{e}_{L}", color4))
        particles.append(Particle(masses[2000011], "#tilde{e}_{R}", color4))
        particles.append(Particle(masses[1000013], "#tilde{#mu}_{L}", color4))
        particles.append(Particle(masses[2000013], "#tilde{#mu}_{R}", color4))


    staus = [
        1000015,
        2000015,
    ]

    max_val = max([ masses[pid] for pid in staus ])
    min_val = min([ masses[pid] for pid in staus ])

    if (max_val - min_val) < 5:
        particles.append(Particle(min_val, "#tilde{#tau}", color4))
    else:
        particles.append(Particle(mmasses[1000015], "#tilde{#tau}_{1}", color4))
        particles.append(Particle(mmasses[2000015], "#tilde{#tau}_{2}", color4))



    snus = [
        1000012,
        1000014,
        1000016,
    ]

    max_val = max([ masses[pid] for pid in snus ])
    min_val = min([ masses[pid] for pid in snus ])

    if (max_val - min_val) < 5:
        particles.append(Particle(min_val, "#tilde{#nu}", color4))
    else:
        particles.append(Particle(mmasses[1000012], "#tilde{#nu}_{eL}",    color4))
        particles.append(Particle(mmasses[1000014], "#tilde{#nu}_{#muL}",  color4))
        particles.append(Particle(mmasses[1000016], "#tilde{#nu}_{#tauL}", color4))


    # Merge squarks/sleptons if are similar
    squarks = [
        1000001,
        2000001,
        1000002,
        2000002,
        1000003,
        2000003,
        1000004,
        2000004,
        1000005,
        2000005,
    ]

    labels = [
        "#tilde{d}_{L}",
        "#tilde{d}_{R}",
        "#tilde{u}_{L}",
        "#tilde{u}_{R}",
        "#tilde{s}_{L}",
        "#tilde{s}_{R}",
        "#tilde{c}_{L}",
        "#tilde{c}_{R}",
        "#tilde{b}_{1}",
        "#tilde{b}_{2}",
    ]

    max_val = max([ masses[pid] for pid in squarks ])
    min_val = min([ masses[pid] for pid in squarks ])

    if (max_val - min_val) < 5:
        particles.append(Particle(min_val, "#tilde{q}", color3))
    else:
        for p, label in zip(squarks, labels):
            particles.append(Particle(masses[p], label, color3))


    stops = [
        1000006,
        2000006,
    ]

    max_val = max([ masses[pid] for pid in stops ])
    min_val = min([ masses[pid] for pid in stops ])

    if (max_val - min_val) < 5:
        particles.append(Particle(min_val, "#tilde{t}", color3))
    else:
        particles.append(Particle(masses[1000006], "#tilde{t}_{1}", color3))
        particles.append(Particle(masses[2000006], "#tilde{t}_{2}", color3))


    max_ = find_max(particles) * 1.1 if args.maxmass is None else float(args.maxmass)
    min_ = find_min(particles) * 0.8

    #Call Drawing code for read spectrum
    output_name = os.path.basename(ifile).replace('slha', 'pdf')

    print ("GENERATING MASS SPECTRUM...")

    # count valid particles
    Nparts = 0
    for p in particles:
        if p.mass > 0 and p.mass < max_:
            Nparts += 1

    # Drawall spectrum lines

    cmass = ROOT.TCanvas("cmass", "", 800, 600)
    cmass.SetLeftMargin(0.09)
    cmass.SetRightMargin(0.05)
    cmass.SetTopMargin(0.05)
    cmass.SetBottomMargin(0.08)
    cmass.SetTicks(1, 1)

    frame = ROOT.TH2F("frame", "", 1, -1, Nparts+1, 100, min_, max_)

    frame.SetStats(0)

    frame.GetXaxis().SetLabelSize(0)
    frame.GetXaxis().SetTickLength(0)
    frame.GetXaxis().SetTitle("")
    frame.GetXaxis().CenterTitle()
    frame.GetXaxis().SetTitleOffset(0.6)

    frame.GetYaxis().SetTitle("Mass [GeV]")
    frame.GetYaxis().SetTitleOffset(1.25)
    frame.GetYaxis().SetRangeUser(min_, max_)

    frame.Draw()

    lwidth = 1

    np = 0
    for p in particles:

        if p.mass > 0 and p.mass < max_:

            # line
            xmin = np * lwidth

            line = ROOT.TLine(xmin, p.mass, xmin+lwidth, p.mass)
            ROOT.SetOwnership(line, False)
            line.SetLineWidth(1)
            line.SetLineColor(p.color)
            line.Draw()

            # label
            xmin = np * lwidth
            shift = lwidth * 0.25

            label = ROOT.TLatex(xmin+shift, p.mass+100, p.label)
            ROOT.SetOwnership(label, False)
            label.SetTextSize(0.025)
            label.SetTextFont(132)
            label.Draw()

            np += 1

    cmass.SaveAs(output_name)



if __name__ == '__main__':
    main()
