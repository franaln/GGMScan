#! /usr/bin/env python2.7

import sys
import argparse
import ROOT
from rootutils import *
from drawutils import *


def get_min(tree, var):
    var_min = 999
    for row in tree:
        v = getattr(row, var)
        if v < var_min:
            var_min = v
    return int(var_min)

def get_max(tree, var):
    var_max = -999
    for row in tree:
        v = getattr(row, var)
        if v > var_max:
            var_max = v
    return int(var_max)

# config
parser = argparse.ArgumentParser(description='draw particles decays from grid slha files')
parser.add_argument('slhafile', nargs='?', help='Path to slha files')
#parser.add_argument('-o', dest='output_file', help='Output file')

args = parser.parse_args()

if args.slhafile is None:
    parser.print_usage()
    sys.exit()

# outfile = ROOT.TFile(args.output_file, 'recreate')

slha = ROOT.TChain('slha')
slha.Add(args.slhafile)

mu_min = get_min(slha, 'mu')
mu_max = get_max(slha, 'mu') + 200
mu_bins = (mu_max - mu_min)

m3_min = get_min(slha, 'm3')
m3_max = get_max(slha, 'm3') + 50
m3_bins = (m3_max - m3_min)

gl_min = get_min(slha, 'm_gl')
gl_max = get_max(slha, 'm_gl') + 200

n1_min = get_min(slha, 'm_n1')
n1_max = get_max(slha, 'm_n1') + 50

def get_m3_bin(m3):
    return int((m3 - m3_min)/25) + 1

def get_mu_bin(mu):
    return int((mu - mu_min)/25) + 1

h_gl_n1g = ROOT.TH2F('h_gl_n1g', 'h_gl_n1g', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_gl_n2g = ROOT.TH2F('h_gl_n2g', 'h_gl_n2g', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_gl_n3g = ROOT.TH2F('h_gl_n3g', 'h_gl_n3g', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)

h_gl_n1qq = ROOT.TH2F('h_gl_n1qq', 'h_gl_n1qq', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_gl_n2qq = ROOT.TH2F('h_gl_n2qq', 'h_gl_n2qq', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_gl_n3qq = ROOT.TH2F('h_gl_n3qq', 'h_gl_n3qq', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_gl_c1qq = ROOT.TH2F('h_gl_c1qq', 'h_gl_c1qq', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)

h_gl_Gg = ROOT.TH2F('h_gl_Gg', 'h_gl_Gg', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)

h_gl_n1 = ROOT.TH2F('h_gl_n1', 'h_gl_n1', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_gl_n2 = ROOT.TH2F('h_gl_n2', 'h_gl_n2', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_gl_n3 = ROOT.TH2F('h_gl_n3', 'h_gl_n3', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_gl_c1 = ROOT.TH2F('h_gl_c1', 'h_gl_c1', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)

h_n1_Gy = ROOT.TH2F('h_n1_Gy', 'h_n1_Gy', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_n1_GZ = ROOT.TH2F('h_n1_GZ', 'h_n1_GZ', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_n1_Gh = ROOT.TH2F('h_n1_Gh', 'h_n1_Gh', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)

h_n2_n1 = ROOT.TH2F('h_n2_n1', 'h_n2_n1', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_n2_c1 = ROOT.TH2F('h_n2_c1', 'h_n2_c1', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_n2_GX = ROOT.TH2F('h_n2_GX', 'h_n2_GX', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)

h_n3_n1 = ROOT.TH2F('h_n3_n1', 'h_n3_n1', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_n3_n2 = ROOT.TH2F('h_n3_n2', 'h_n3_n2', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_n3_c1 = ROOT.TH2F('h_n3_c1', 'h_n3_c1', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_n3_GX = ROOT.TH2F('h_n3_GX', 'h_n3_GX', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)

h_c1_n1 = ROOT.TH2F('h_c1_n1', 'h_c1_n1', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
h_c1_GW = ROOT.TH2F('h_c1_GW', 'h_c1_GW', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)

points = []

for row in slha:

    # gl decays
    h_gl_n1.Fill(row.m3, row.mu, row.br_gl_n1)
    h_gl_n2.Fill(row.m3, row.mu, row.br_gl_n2)
    h_gl_n3.Fill(row.m3, row.mu, row.br_gl_n3)
    h_gl_c1.Fill(row.m3, row.mu, row.br_gl_c1)
    h_gl_Gg.Fill(row.m3, row.mu, row.br_gl_Gg)

    # n1 decays
    h_n1_Gy.Fill(row.m3, row.mu, row.br_n1_Gy)
    h_n1_GZ.Fill(row.m3, row.mu, row.br_n1_GZ)
    h_n1_Gh.Fill(row.m3, row.mu, row.br_n1_Gh)

    # n2 decays
    h_n2_n1.Fill(row.m3, row.mu, row.br_n2_n1)
    h_n2_c1.Fill(row.m3, row.mu, row.br_n2_c1)
    h_n2_GX.Fill(row.m3, row.mu, row.br_n2_GX)

    # n3 decays
    h_n3_n1.Fill(row.m3, row.mu, row.br_n3_n1)
    h_n3_n2.Fill(row.m3, row.mu, row.br_n3_n2)
    h_n3_c1.Fill(row.m3, row.mu, row.br_n3_c1)
    h_n3_GX.Fill(row.m3, row.mu, row.br_n3_GX)

    # c1 decays
    h_c1_n1.Fill(row.m3, row.mu, row.br_c1_n1)
    h_c1_GW.Fill(row.m3, row.mu, row.br_c1_GW)

    points.append((row.m3, row.mu))



# Plots
set_default_style()

# Draw total gl->X BR
frame = draw_m3mu_frame(m3_min, m3_max, mu_min, mu_max) ##, gl_min, gl_max, n1_min, n1_max)

for m3, mu in points:

    bin_ = h_gl_n1.FindBin(m3, mu)

    br1 = h_gl_n1.GetBinContent(bin_)
    br2 = h_gl_n2.GetBinContent(bin_)
    br3 = h_gl_n3.GetBinContent(bin_)
    br4 = h_gl_c1.GetBinContent(bin_)
    br5 = h_gl_Gg.GetBinContent(bin_)

    draw_boxpie(m3, mu, br1, br2, br3, br4, br5)

draw_boxlegend(m3_min+50, 1850, 'purple', 'BR(#tilde{g} #rightarrow #tilde{#chi}^{0}_{1} g / #tilde{#chi}^{0}_{1} qq)')
draw_boxlegend(m3_min+50, 1750,   'blue', 'BR(#tilde{g} #rightarrow #tilde{#chi}^{0}_{2} g / #tilde{#chi}^{0}_{2} qq)')
draw_boxlegend(m3_min+50, 1650,  'green', 'BR(#tilde{g} #rightarrow #tilde{#chi}^{0}_{3} g / #tilde{#chi}^{0}_{3} qq)')
draw_boxlegend(m3_min+50, 1550, 'orange', 'BR(#tilde{g} #rightarrow #tilde{#chi}^{#pm}_{1} qq)')
draw_boxlegend(m3_min+50, 1450,   'pink', 'BR(#tilde{g} #rightarrow #tilde{G} g)')

frame.RedrawAxis()

frame.Print('br_gl_X.pdf')

# Draw N1->X BR
frame3 = draw_m3mu_frame(m3_min, m3_max, mu_min, mu_max) ##, gl_min, gl_max, n1_min, n1_max)

for m3, mu in points:

    bin_ = h_n1_Gy.FindBin(m3, mu)

    br1 = h_n1_Gy.GetBinContent(bin_)
    br2 = h_n1_GZ.GetBinContent(bin_)
    br3 = h_n1_Gh.GetBinContent(bin_)

    draw_boxpie(m3, mu, br1, br2, br3)

draw_boxlegend(m3_min+50, mu_max-200, 'purple', 'BR(#tilde{#chi}^{0}_{1} #rightarrow #tilde{G} #gamma)')
draw_boxlegend(m3_min+50, mu_max-300,  'blue', 'BR(#tilde{#chi}^{0}_{1} #rightarrow #tilde{G} Z)')
draw_boxlegend(m3_min+50, mu_max-400, 'green', 'BR(#tilde{#chi}^{0}_{1} #rightarrow #tilde{G} h)')

frame3.RedrawAxis()

frame3.Print('br_n1_X.pdf')

# Draw N2->X BR
frame4 = draw_m3mu_frame(m3_min, m3_max, mu_min, mu_max) ##, gl_min, gl_max, n1_min, n1_max)

for m3, mu in points:

    bin_ = h_n2_n1.FindBin(m3, mu)

    br1 = h_n2_n1.GetBinContent(bin_)
    br2 = h_n2_c1.GetBinContent(bin_)
    br3 = h_n2_GX.GetBinContent(bin_)

    draw_boxpie(m3, mu, br1, br2, br3)

draw_boxlegend(m3_min+50, mu_max-200, 'purple', 'BR(#tilde{#chi}^{0}_{2} #rightarrow #tilde{#chi}^{0}_{1})')
draw_boxlegend(m3_min+50, mu_max-300,   'blue', 'BR(#tilde{#chi}^{0}_{2} #rightarrow #tilde{#chi}^{#pm}_{1})')
draw_boxlegend(m3_min+50, mu_max-400,  'green', 'BR(#tilde{#chi}^{0}_{2} #rightarrow #tilde{G} X)')

frame4.RedrawAxis()

frame4.Print('br_n2_X.pdf')

# Draw N3->X BR
frame5 = draw_m3mu_frame(m3_min, m3_max, mu_min, mu_max) ##, gl_min, gl_max, n1_min, n1_max)

for m3, mu in points:

    bin_ = h_n3_n1.FindBin(m3, mu)

    br1 = h_n3_n1.GetBinContent(bin_)
    br2 = h_n3_n2.GetBinContent(bin_)
    br3 = h_n3_c1.GetBinContent(bin_)
    br4 = h_n3_GX.GetBinContent(bin_)

    draw_boxpie(m3, mu, br1, br2, br3, br4)

draw_boxlegend(m3_min+50, mu_max-200, 'purple', 'BR(#tilde{#chi}^{0}_{3} #rightarrow #tilde{#chi}^{0}_{1})')
draw_boxlegend(m3_min+50, mu_max-300,   'blue', 'BR(#tilde{#chi}^{0}_{3} #rightarrow #tilde{#chi}^{0}_{2})')
draw_boxlegend(m3_min+50, mu_max-400,  'green', 'BR(#tilde{#chi}^{0}_{3} #rightarrow #tilde{#chi}^{#pm}_{1})')
draw_boxlegend(m3_min+50, mu_max-500, 'orange', 'BR(#tilde{#chi}^{0}_{3} #rightarrow #tilde{G} X)')

frame5.RedrawAxis()
frame5.SaveAs('br_n3_X.pdf')

# Draw C1->X BR
frame6 = draw_m3mu_frame(m3_min, m3_max, mu_min, mu_max) ##, gl_min, gl_max, n1_min, n1_max)

for m3, mu in points:

    bin_ = h_c1_n1.FindBin(m3, mu)

    br1 = h_c1_n1.GetBinContent(bin_)
    br2 = h_c1_GW.GetBinContent(bin_)

    draw_boxpie(m3, mu, br1, br2)

draw_boxlegend(m3_min+50, mu_max-200, 'purple', 'BR(#tilde{#chi}^{#pm}_{1} #rightarrow #tilde{#chi}^{0}_{1})')
draw_boxlegend(m3_min+50, mu_max-300,   'blue', 'BR(#tilde{#chi}^{#pm}_{1} #rightarrow #tilde{G} W)')


frame6.RedrawAxis()

frame6.Print('br_c1_X.pdf')
