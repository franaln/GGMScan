#! /usr/bin/env python2.7
# Code to draw mass spectrum from slha input file

import os
import sys
import string
import math
import argparse
import ROOT
import pyslha

from rootutils import set_default_style, get_color

color1 = get_color('red')
color2 = get_color('yellow')
color3 = get_color('green')
color4 = get_color('blue')
color5 = get_color('turquoise')
color6 = get_color('purple')
color7 = get_color('gray')

colors = {
    1000022:  color1,
    1000023:  color1,
    1000025:  color1,
    1000035:  color1,
    1000024:  color2,
    1000037:  color2,
    1000002:  color3,
    2000002:  color3,
    1000001:  color3,
    2000001:  color3,
    1000003:  color3,
    2000003:  color3,
    1000004:  color3,
    2000004:  color3,
    1000006:  color3,
    2000006:  color3,
    1000005:  color3,
    2000005:  color3,
    1000011:  color4,
    2000011:  color4,
    1000012:  color4,
    1000013:  color4,
    2000013:  color4,
    1000014:  color4,
    1000015:  color4,
    2000015:  color4,
    1000016:  color4,
    25     :  color5,
    35     :  color5,
    37     :  color5,
    36     :  color5,
    1000021:  color6,
    1000039:  color7,
}

labels = {

    1000022: '#tilde{#chi}^{0}_{1}',
    1000023: '#tilde{#chi}^{0}_{2}',
    1000025: '#tilde{#chi}^{0}_{3}',
    1000035: '#tilde{#chi}^{0}_{4}',
    1000024: '#tilde{#chi}^{#pm}_{1}',
    1000037: '#tilde{#chi}^{#pm}_{2}',

    1000001: "#tilde{q}_{L}",
    2000001: "#tilde{q}_{R}",

    # 1000002: "#tilde{u}_{L}",
    # 2000002: "#tilde{u}_{R}",
    # 1000001: "#tilde{d}_{L}",
    # 2000001: "#tilde{d}_{R}",
    # 1000003: "#tilde{s}_{L}",
    # 2000003: "#tilde{s}_{R}",
    # 1000004: "#tilde{c}_{L}",
    # 2000004: "#tilde{c}_{R}",
    1000006: "#tilde{t}_{1}",
    2000006: "#tilde{t}_{2}",
    1000005: "#tilde{b}_{1}",
    2000005: "#tilde{b}_{2}",

    1000011: "#tilde{l}_{L}",
    2000011: "#tilde{l}_{R}",
    1000012: "#tilde{#nu}_{L}",

    # 1000011: "#tilde{e}_{L}",
    # 2000011: "#tilde{e}_{R}",
    # 1000012: "#tilde{#nu}_{eL}",
    # 1000013: "#tilde{#mu}_{L}",
    # 2000013: "#tilde{#mu}_{R}",
    # 1000014: "#tilde{#nu}_{#muL}",
    # 1000015: "#tilde{#tau}_{1}",
    # 2000015: "#tilde{#tau}_{2}",
    # 1000016: "#tilde{#nu}_{#tauL}",

    25     : "h^{0}",
    35     : "H^{0}",
    36     : "A^{0}",
    37     : "H^{#pm}",
    1000021: "#tilde{g}",
    1000039: "#tilde{G}",
}


class Particle:
    def __init__(self, pdgid, mass=0.):

        self.pdgid = pdgid
        self.mass = mass

        self.label = labels[pdgid]
        self.color = colors[pdgid]

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
    try:
        doc = pyslha.read(ifile)
        masses = doc.blocks['MASS']
    except pyslha.ParseError, pe:
        print str(pe) + "... exiting"
        sys.exit(1)


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
        Particle(1000039),

        #Higgses
        Particle(25),
        Particle(35),
        Particle(37),
        Particle(36),

        #gluino
        Particle(1000021),

        #Neutralinos
        Particle(1000022),
        Particle(1000023),
        Particle(1000025),
        Particle(1000035),

        #Charginos
        Particle(1000024),
        Particle(1000037),

        #Squarks
        Particle(1000001),
        Particle(2000001),
        # Particle(1000002),
        # Particle(2000002),
        # Particle(1000003),
        # Particle(2000003),
        # Particle(1000004),
        # Particle(2000004),
        Particle(1000006),
        Particle(2000006),
        Particle(1000005),
        Particle(2000005),

        #Sleptons
        Particle(1000011),
        Particle(2000011),
        Particle(1000012),
        # Particle(1000013),
        # Particle(2000013),
        # Particle(1000014),
        # Particle(1000015),
        # Particle(2000015),
        # Particle(1000016),

    ]

    for i, p in enumerate(particles):
        particles[i].mass = abs(float(masses[p.pdgid]))


    max_ = find_max(particles) * 1.1 if args.maxmass is None else float(args.maxmass)
    min_ = find_min(particles) * 0.8

    #Call Drawing code for read spectrum
    output_name = os.path.basename(ifile).replace('slha', 'pdf')

    print "GENERATING MASS SPECTRUM..."

    # count valid particles
    Nparts = 0
    for p in particles:
        if p.mass > 0 and p.mass < max_:
            Nparts += 1

    # Drawall spectrum lines
    set_default_style()

    cmass = ROOT.TCanvas("cmass", "", 800, 600)
    cmass.SetLeftMargin(0.09)
    cmass.SetRightMargin(0.05)
    cmass.SetTopMargin(0.05)
    cmass.SetBottomMargin(0.08)
    cmass.SetTicks()

    frame = ROOT.TH2F("frame", "", 1, -1, Nparts+1, 100, min_, max_)

    frame.GetXaxis().SetLabelSize(0)
    frame.GetXaxis().SetTickLength(0)
    frame.GetXaxis().SetTitle("")
    frame.GetXaxis().CenterTitle()
    frame.GetXaxis().SetTitleOffset(0.6)

    frame.GetYaxis().SetTitle("Mass [GeV]")
    frame.GetYaxis().SetTitleOffset(1.2)
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

            label = ROOT.TLatex(xmin+shift, p.mass+50, p.label)
            ROOT.SetOwnership(label, False)
            label.SetTextSize(0.025)
            label.SetTextFont(132)
            label.Draw()

            np += 1

    cmass.SaveAs(output_name)



if __name__ == '__main__':
    main()
