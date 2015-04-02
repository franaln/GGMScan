import ROOT
from rootutils import *
from drawutils import *
from SUSY_GGM_M3_mu_mc12points import pointdict


def get_m3_bin(m3):
    return int((m3 - 800)/25) + 1

def get_mu_bin(mu):
    return int((mu - 150)/25) + 1


# Decays histograms
f = ROOT.TFile('decays.root')

h_gl_n1 = f.Get('h_gl_n1')
h_gl_n2 = f.Get('h_gl_n2')
h_gl_n3 = f.Get('h_gl_n3')
h_gl_c1 = f.Get('h_gl_c1')
h_gl_Gg = f.Get('h_gl_Gg')

# h_gl_n1_full = f.Get('h_gl_n1_full')
# h_gl_n2_full = f.Get('h_gl_n2_full')
# h_gl_n3_full = f.Get('h_gl_n3_full')
# h_gl_c1_full = f.Get('h_gl_c1_full')
# h_gl_Gg_full = f.Get('h_gl_Gg_full')

h_n1_Gy = f.Get('h_n1_Gy')
h_n1_Gz = f.Get('h_n1_GZ')
h_n1_Gh = f.Get('h_n1_Gh')

h_n2_n1 = f.Get('h_n2_n1')
h_n2_c1 = f.Get('h_n2_c1')
h_n2_GX = f.Get('h_n2_GX')

h_n3_n1 = f.Get('h_n3_n1')
h_n3_n2 = f.Get('h_n3_n2')
h_n3_c1 = f.Get('h_n3_c1')
h_n3_GX = f.Get('h_n3_GX')

# Plots
set_default_style()

# Draw total gl->X BR
frame = draw_grid_frame()

for m3, mu in pointdict.itervalues():

    bin_m3 = get_m3_bin(m3)
    bin_mu = get_mu_bin(mu)

    br1 = h_gl_n1.GetBinContent(bin_m3, bin_mu)
    br2 = h_gl_n2.GetBinContent(bin_m3, bin_mu)
    br3 = h_gl_n3.GetBinContent(bin_m3, bin_mu)
    br4 = h_gl_c1.GetBinContent(bin_m3, bin_mu)
    br5 = h_gl_Gg.GetBinContent(bin_m3, bin_mu)

    draw_boxpie(m3, mu, br1, br2, br3, br4, br5)

draw_boxlegend(830, 1400, 'purple', 'BR(#tilde{g} #rightarrow #tilde{#chi}^{0}_{1} g / #tilde{#chi}^{0}_{1} qq)')
draw_boxlegend(830, 1325,   'blue', 'BR(#tilde{g} #rightarrow #tilde{#chi}^{0}_{2} g / #tilde{#chi}^{0}_{2} qq)')
draw_boxlegend(830, 1250,  'green', 'BR(#tilde{g} #rightarrow #tilde{#chi}^{0}_{3} g / #tilde{#chi}^{0}_{3} qq)')
draw_boxlegend(830, 1175, 'orange', 'BR(#tilde{g} #rightarrow #tilde{#chi}^{#pm}_{1} qq)')
draw_boxlegend(830, 1100,   'pink', 'BR(#tilde{g} #rightarrow #tilde{G} g)')

frame.RedrawAxis()

frame.Print('br_gl_X.pdf')

# # Draw total gl->X BR (full)
# frame2 = draw_grid_frame()

# for m3, mu in pointdict.itervalues():

#     bin_m3 = get_m3_bin(m3)
#     bin_mu = get_mu_bin(mu)

#     br1 = h_gl_n1_full.GetBinContent(bin_m3, bin_mu)
#     br2 = h_gl_n2_full.GetBinContent(bin_m3, bin_mu)
#     br3 = h_gl_n3_full.GetBinContent(bin_m3, bin_mu)
#     br4 = h_gl_c1_full.GetBinContent(bin_m3, bin_mu)
#     br5 = h_gl_Gg_full.GetBinContent(bin_m3, bin_mu)

#     draw_boxpie(m3, mu, br1, br2, br3, br4, br5)

# draw_boxlegend(830, 1400, 'purple', 'BR(#tilde{g} #rightarrow #tilde{#chi}^{0}_{1} g / #tilde{#chi}^{0}_{1} qq)')
# draw_boxlegend(830, 1325,   'blue', 'BR(#tilde{g} #rightarrow #tilde{#chi}^{0}_{2} g / #tilde{#chi}^{0}_{2} qq)')
# draw_boxlegend(830, 1250,  'green', 'BR(#tilde{g} #rightarrow #tilde{#chi}^{0}_{3} g / #tilde{#chi}^{0}_{3} qq)')
# draw_boxlegend(830, 1175, 'orange', 'BR(#tilde{g} #rightarrow #tilde{#chi}^{#pm}_{1} qq)')
# draw_boxlegend(830, 1100,   'pink', 'BR(#tilde{g} #rightarrow #tilde{G} g)')

# frame2.RedrawAxis()

# frame2.Print('br_gl_X_full.pdf')


# Draw N1->X BR
frame3 = draw_grid_frame()

for m3, mu in pointdict.itervalues():

    bin_m3 = get_m3_bin(m3)
    bin_mu = get_mu_bin(mu)

    br1 = h_n1_Gy.GetBinContent(bin_m3, bin_mu)
    br2 = h_n1_Gz.GetBinContent(bin_m3, bin_mu)
    br3 = h_n1_Gh.GetBinContent(bin_m3, bin_mu)

    draw_boxpie(m3, mu, br1, br2, br3)

draw_boxlegend(830, 1400, 'purple', 'BR(#tilde{#chi}^{0}_{1} #rightarrow #tilde{G} #gamma)')
draw_boxlegend(830, 1325,  'blue', 'BR(#tilde{#chi}^{0}_{1} #rightarrow #tilde{G} Z)')
draw_boxlegend(830, 1250, 'green', 'BR(#tilde{#chi}^{0}_{1} #rightarrow #tilde{G} h)')

frame3.RedrawAxis()

frame3.Print('br_N1_X.pdf')

# Draw N2->X BR
frame4 = draw_grid_frame()

for m3, mu in pointdict.itervalues():

    bin_m3 = get_m3_bin(m3)
    bin_mu = get_mu_bin(mu)

    br1 = h_n2_n1.GetBinContent(bin_m3, bin_mu)
    br2 = h_n2_c1.GetBinContent(bin_m3, bin_mu)
    br3 = h_n2_GX.GetBinContent(bin_m3, bin_mu)

    draw_boxpie(m3, mu, br1, br2, br3)

draw_boxlegend(830, 1400, 'purple', 'BR(#tilde{#chi}^{0}_{2} #rightarrow #tilde{#chi}^{0}_{1})')
draw_boxlegend(830, 1325,   'blue', 'BR(#tilde{#chi}^{0}_{2} #rightarrow #tilde{#chi}^{#pm}_{1})')
draw_boxlegend(830, 1250,  'green', 'BR(#tilde{#chi}^{0}_{2} #rightarrow #tilde{G} X)')

frame4.RedrawAxis()

frame4.Print('br_N2_X.pdf')

# Draw N3->X BR
frame5 = draw_grid_frame()

for m3, mu in pointdict.itervalues():

    bin_m3 = get_m3_bin(m3)
    bin_mu = get_mu_bin(mu)

    br1 = h_n3_n1.GetBinContent(bin_m3, bin_mu)
    br2 = h_n3_n2.GetBinContent(bin_m3, bin_mu)
    br3 = h_n3_c1.GetBinContent(bin_m3, bin_mu)
    br4 = h_n3_GX.GetBinContent(bin_m3, bin_mu)

    draw_boxpie(m3, mu, br1, br2, br3, br4)

draw_boxlegend(830, 1400, 'purple', 'BR(#tilde{#chi}^{0}_{3} #rightarrow #tilde{#chi}^{0}_{1})')
draw_boxlegend(830, 1325,   'blue', 'BR(#tilde{#chi}^{0}_{3} #rightarrow #tilde{#chi}^{0}_{2})')
draw_boxlegend(830, 1250,  'green', 'BR(#tilde{#chi}^{0}_{3} #rightarrow #tilde{#chi}^{#pm}_{1})')
draw_boxlegend(830, 1175, 'orange', 'BR(#tilde{#chi}^{0}_{3} #rightarrow #tilde{G} X)')

frame5.RedrawAxis()

frame5.Print('br_N3_X.pdf')
