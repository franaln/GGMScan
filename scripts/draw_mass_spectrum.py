#! /usr/bin/env python
# Code to draw mass spectrum from slha input file

import os
import sys
import string
import math
import argparse
import ROOT

from rootutils import set_default_style, get_color

lwidth = 1.1   # line width

def get_line(mass, number=1, color=1):

    if mass < 0.:
        return None

    xmin = number * lwidth

    line = ROOT.TLine(xmin, mass, xmin+lwidth, mass)
    line.SetLineWidth(1)
    line.SetLineColor(color)

    return line

def get_label(text="", mass=0, number=1):

    if mass < 0.:
        return None

    xmin = number * lwidth
    shift = lwidth/4

    mytext = ROOT.TLatex(xmin+shift, mass+45, text)
    mytext.SetTextSize(0.025)
    mytext.SetTextFont(132)

    return mytext

def draw_mass_spectrum(particles, min_=-9999, max_=-9999, output_name='plot.pdf'):

    print "GENERATING MASS SPECTRUM..."

    color1 = get_color('red')
    color2 = get_color('yellow')
    color3 = get_color('green')
    color4 = get_color('blue')
    color5 = get_color('turquoise')
    color6 = get_color('purple')
    color7 = get_color('gray')

    # Get Lines
    N = 0
    lines = dict()
    lines['gl']      = get_line(particles['gl'],       1, color6)
    lines['G']       = get_line(particles['G'],        2, color7)
    lines['h0']      = get_line(particles['h0'],       3, color5)
    lines['H']       = get_line(particles['H'],        4, color5)
    lines['Hp']      = get_line(particles['Hp'],       5, color5)
    lines['A']       = get_line(particles['A'],        6, color5)
    lines['chi10']   = get_line(particles['chi10'],    7, color1)
    lines['chi20']   = get_line(particles['chi20'],    8, color1)
    lines['chi30']   = get_line(particles['chi30'],    9, color1)
    lines['chi40']   = get_line(particles['chi40'],   10, color1)
    lines['chi1p']   = get_line(particles['chi1p'],   11, color2)
    lines['chi2p']   = get_line(particles['chi2p'],   12, color2)
    lines['uL']      = get_line(particles['uL'],      13, color3)
    lines['uR']      = get_line(particles['uR'],      14, color3)
    lines['dL']      = get_line(particles['dL'],      15, color3)
    lines['dR']      = get_line(particles['dR'],      16, color3)
    lines['sL']      = get_line(particles['sL'],      17, color3)
    lines['sR']      = get_line(particles['sR'],      18, color3)
    lines['cL']      = get_line(particles['cL'],      19, color3)
    lines['cR']      = get_line(particles['cR'],      20, color3)
    lines['t1']      = get_line(particles['t1'],      21, color3)
    lines['t2']      = get_line(particles['t2'],      22, color3)
    lines['b1']      = get_line(particles['b1'],      23, color3)
    lines['b2']      = get_line(particles['b2'],      24, color3)
    lines['eL']      = get_line(particles['eL'],      25, color4)
    lines['eR']      = get_line(particles['eR'],      26, color4)
    lines['nu_eL']   = get_line(particles['nu_eL'],   27, color4)
    lines['muL']     = get_line(particles['muL'],     28, color4)
    lines['muR']     = get_line(particles['muR'],     29, color4)
    lines['nu_muL']  = get_line(particles['nu_muL'],  30, color4)
    lines['tau1']    = get_line(particles['tau1'],    31, color4)
    lines['tau2']    = get_line(particles['tau2'],    32, color4)
    lines['nu_tauL'] = get_line(particles['nu_tauL'], 33, color4)

    # Get Labels
    N = 0
    labels = dict()
    labels['gl']      = get_label("#tilde{g}",           particles['gl']     ,   1)
    labels['G']       = get_label("#tilde{G}",           particles['G']      ,   2)
    labels['h0']      = get_label("h^{0}",               particles['h0']     ,   3)
    labels['H']       = get_label("H^{0}",               particles['H']      ,   4)
    labels['Hp']      = get_label("H^{#pm}",             particles['Hp']     ,   5)
    labels['A']       = get_label("A^{0}",               particles['A']      ,   6)
    labels['chi10']   = get_label("#tilde{#chi}^{0}_{1}",        particles['chi10']  ,   7)
    labels['chi20']   = get_label("#tilde{#chi}^{0}_{2}",        particles['chi20']  ,   8)
    labels['chi30']   = get_label("#tilde{#chi}^{0}_{3}",        particles['chi30']  ,   9)
    labels['chi40']   = get_label("#tilde{#chi}^{0}_{4}",        particles['chi40']  ,  10)
    labels['chi1p']   = get_label("#tilde{#chi}^{#pm}_{1}",      particles['chi1p']  ,  11)
    labels['chi2p']   = get_label("#tilde{#chi}^{#pm}_{2}",      particles['chi2p']  ,  12)
    labels['uL']      = get_label("#tilde{u}_{L}",       particles['uL']     ,  13)
    labels['uR']      = get_label("#tilde{u}_{R}",       particles['uR']     ,  14)
    labels['dL']      = get_label("#tilde{d}_{L}",       particles['dL']     ,  15)
    labels['dR']      = get_label("#tilde{d}_{R}",       particles['dR']     ,  16)
    labels['sL']      = get_label("#tilde{s}_{L}",       particles['sL']     ,  17)
    labels['sR']      = get_label("#tilde{s}_{R}",       particles['sR']     ,  18)
    labels['cL']      = get_label("#tilde{c}_{L}",       particles['cL']     ,  19)
    labels['cR']      = get_label("#tilde{c}_{R}",       particles['cR']     ,  20)
    labels['t1']      = get_label("#tilde{t}_{1}",       particles['t1']     ,  21)
    labels['t2']      = get_label("#tilde{t}_{2}",       particles['t2']     ,  22)
    labels['b1']      = get_label("#tilde{b}_{1}",       particles['b1']     ,  23)
    labels['b2']      = get_label("#tilde{b}_{2}",       particles['b2']     ,  24)
    labels['eL']      = get_label("#tilde{e}_{L}",       particles['eL']     ,  25)
    labels['eR']      = get_label("#tilde{e}_{R}",       particles['eR']     ,  26)
    labels['nu_eL']   = get_label("#tilde{#nu}_{eL}",    particles['nu_eL']  ,  27)
    labels['muL']     = get_label("#tilde{#mu}_{L}",     particles['muL']    ,  28)
    labels['muR']     = get_label("#tilde{#mu}_{R}",     particles['muR']    ,  29)
    labels['nu_muL']  = get_label("#tilde{#nu}_{#muL}",  particles['nu_muL'] ,  30)
    labels['tau1']    = get_label("#tilde{#tau}_{1}",    particles['tau1']   ,  31)
    labels['tau2']    = get_label("#tilde{#tau}_{2}",    particles['tau2']   ,  32)
    labels['nu_tauL'] = get_label("#tilde{#nu}_{#tauL}", particles['nu_tauL'],  33)

    # count valid particles
    Nparts = 0
    for name, mass in particles.iteritems():
        if mass > 0:
            Nparts += 1

    # Drawall spectrum lines
    set_default_style()

    cmass = ROOT.TCanvas("cmass", "", 800, 600)
    cmass.SetLeftMargin(0.09)
    cmass.SetRightMargin(0.05)
    cmass.SetTopMargin(0.05)
    cmass.SetBottomMargin(0.08)
    cmass.SetTicks()

    frame = ROOT.TH2F("frame", "", 1, -1, Nparts+6, 100, min_, max_)

    frame.GetXaxis().SetLabelSize(0);
    frame.GetXaxis().SetTickLength(0);
    frame.GetXaxis().SetTitle("SUSY PARTICLES");
    frame.GetXaxis().CenterTitle();
    frame.GetXaxis().SetTitleOffset(0.6);

    frame.GetYaxis().SetTitle("Mass [GeV]");
    frame.GetYaxis().SetTitleOffset(1.2);
    frame.GetYaxis().SetRangeUser(min_, max_);

    frame.Draw()

    for name, mass in particles.iteritems():
        if mass > 0:
            lines[name].Draw()
            labels[name].Draw()

    cmass.SaveAs(output_name)


def main():

    parser = argparse.ArgumentParser(description='input options handler')

    parser.add_argument('ifile', metavar='INFILE', nargs='?', help='slha formatted file to be read')

    args = parser.parse_args()

    ifile = args.ifile

    if not os.path.exists(ifile):
        print "\nFile \'"+ifile+"\' seems not to exist. Please check and come back...\n"
        sys.exit(1)


    #Load input file
    spectrum = open(ifile)

    ### Get mass of susy particles
    particles = dict()

    #Neutralinos
    particles['chi10'] = -9999
    particles['chi20'] = -9999
    particles['chi30'] = -9999
    particles['chi40'] = -9999

    #Charginos
    particles['chi1p'] = -9999
    particles['chi2p'] = -9999

    #Squarks
    particles['uL'] = -9999
    particles['uR'] = -9999
    particles['dL'] = -9999
    particles['dR'] = -9999
    particles['sL'] = -9999
    particles['sR'] = -9999
    particles['cL'] = -9999
    particles['cR'] = -9999
    particles['t1'] = -9999
    particles['t2'] = -9999
    particles['b1'] = -9999
    particles['b2'] = -9999

    #Sleptons
    particles['eL'] = -9999
    particles['eR'] = -9999
    particles['nu_eL'] = -9999
    particles['muL'] = -9999
    particles['muR'] = -9999
    particles['nu_muL'] = -9999
    particles['tau1'] = -9999
    particles['tau2'] = -9999
    particles['nu_tauL'] = -9999

    #Higgses
    particles['h0'] = -9999
    particles['H'] = -9999
    particles['Hp'] = -9999
    particles['A'] = -9999

    #gluino
    particles['gl'] = -9999

    #gravitino
    particles['G']=-9999

    def find_max(lst):
        max_ = 0
        for item in lst:
            if float(item) > max_:
                max_ = float(item)
        return max_

    def find_min(lst):
        min_ = 9999999
        for item in lst:
            if float(item) < min_:
                min_ = float(item)
        return min_

    def format_line(line):
        line.replace(" ","$")
        sl = ''
        add = False
        for ch in line:
            if ch == "$":
                add = True
                continue
            else:
                if add:
                    sl = sl+" "+ch
                    add = False
        return sl

    #Extract masses from file
    mlist = []
    for line in spectrum:
        fields = line.split()

        if "decays" in line: #to avoid overwritten values
            continue

        if "# ~chi_10" in line:
            particles['chi10'] = math.fabs(float(fields[1]))
            mlist.append(particles['chi10'])
            continue
        if "# ~chi_20" in line:
            particles['chi20'] = math.fabs(float(fields[1]))
            mlist.append(particles['chi20'])
            continue
        if "# ~chi_30" in line:
            particles['chi30'] = math.fabs(float(fields[1]))
            mlist.append(particles['chi30'])
            continue
        if "# ~chi_40" in line:
            particles['chi40'] = math.fabs(float(fields[1]))
            mlist.append(particles['chi40'])
            continue
        if "# ~chi_1+" in line:
            particles['chi1p'] = math.fabs(float(fields[1]))
            mlist.append(particles['chi1p'])
            continue
        if "# ~chi_2+" in line:
            particles['chi2p'] = math.fabs(float(fields[1]))
            mlist.append(particles['chi2p'])
            continue
        if "# ~u_L" in line:
            particles['uL'] = math.fabs(float(fields[1]))
            mlist.append(particles['uL'])
            continue
        if "# ~u_R" in line:
            particles['uR'] = math.fabs(float(fields[1]))
            mlist.append(particles['uR'])
            continue
        if "# ~d_L" in line:
            particles['dL'] = math.fabs(float(fields[1]))
            mlist.append(particles['dL'])
            continue
        if "# ~d_R" in line:
            particles['dR'] = math.fabs(float(fields[1]))
            mlist.append(particles['dR'])
            continue
        if "# ~s_L" in line:
            particles['sL'] = math.fabs(float(fields[1]))
            mlist.append(particles['sL'])
            continue
        if "# ~s_R" in line:
            particles['sR'] = math.fabs(float(fields[1]))
            mlist.append(particles['sR'])
            continue
        if "# ~c_L" in line:
            particles['cL'] = math.fabs(float(fields[1]))
            mlist.append(particles['cL'])
            continue
        if "# ~c_R" in line:
            particles['cR'] = math.fabs(float(fields[1]))
            mlist.append(particles['cR'])
            continue
        if "# ~t_1" in line:
            particles['t1'] = math.fabs(float(fields[1]))
            mlist.append(particles['t1'])
            continue
        if "# ~t_2" in line:
            particles['t2'] = math.fabs(float(fields[1]))
            mlist.append(particles['t2'])
            continue
        if "# ~b_1" in line:
            particles['b1'] = math.fabs(float(fields[1]))
            mlist.append(particles['b1'])
            continue
        if "# ~b_2" in line:
            particles['b2'] = math.fabs(float(fields[1]))
            mlist.append(particles['b2'])
            continue
        if "# ~e_L" in line:
            particles['eL'] = math.fabs(float(fields[1]))
            mlist.append(particles['eL'])
            continue
        if "# ~e_R" in line:
            particles['eR'] = math.fabs(float(fields[1]))
            mlist.append(particles['eR'])
            continue
        if "# ~nu_eL" in line:
            particles['nu_eL'] = math.fabs(float(fields[1]))
            mlist.append(particles['nu_eL'])
            continue
        if "# ~mu_L" in line:
            particles['muL'] = math.fabs(float(fields[1]))
            mlist.append(particles['muL'])
            continue
        if "# ~mu_R" in line:
            particles['muR'] = math.fabs(float(fields[1]))
            mlist.append(particles['muR'])
            continue
        if "# ~nu_muL" in line:
            particles['nu_muL'] = math.fabs(float(fields[1]))
            mlist.append(particles['nu_muL'])
            continue
        if "# ~tau_1" in line:
            particles['tau1'] = math.fabs(float(fields[1]))
            mlist.append(particles['tau1'])
            continue
        if "# ~tau_2" in line:
            particles['tau2'] = math.fabs(float(fields[1]))
            mlist.append(particles['tau2'])
            continue
        if "# ~nu_tauL" in line:
            particles['nu_tauL'] = math.fabs(float(fields[1]))
            mlist.append(particles['nu_tauL'])
            continue
        if "# h" in line and fields[0] == "25":
            particles['h0'] = math.fabs(float(fields[1]))
            mlist.append(particles['h0'])
            continue
        if "# H" in line and fields[0] == "35":
            particles['H'] = math.fabs(float(fields[1]))
            mlist.append(particles['H'])
            continue
        if "# H+" in line and fields[0] == "37":
            particles['Hp'] = math.fabs(float(fields[1]))
            mlist.append(particles['Hp'])
            continue
        if "# A" in line and fields[0] == "36":
            particles['A'] = math.fabs(float(fields[1]))
            mlist.append(particles['A'])
            continue
        if "# ~g" in line and fields[0] == "1000021":
            particles['gl'] = math.fabs(float(fields[1]))
            mlist.append(particles['gl'])
            continue
        if "# ~gravitino" in line:
            particles['G'] = math.fabs(float(fields[1]))
            mlist.append(particles['G'])
            continue

    xmax = find_max(mlist)*1.1
    xmin = find_min(mlist)*0.8

    #Call Drawing code for read spectrum
    output_name = os.path.basename(ifile).replace('slha', 'pdf')
    draw_mass_spectrum(particles, xmin, xmax, output_name)

if __name__ == '__main__':
    main()
