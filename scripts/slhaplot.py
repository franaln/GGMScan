#! /usr/bin/env python

import argparse
import ROOT
from rootutils.rootutils import *


labels = {
    'm1': 'M_{1}',
    'm2': 'M_{2}',
    'm3': 'M_{3}',
    'mu': '#mu',
    'msq': 'M_{sq}',

    # masses
    'm_h': 'm_{h}',
    'm_gl': 'm_{#tilde{g}}',
    'm_n1': 'm_{#chi^{0}_{1}}',
    'm_n2': 'm_{#chi^{0}_{2}}',
    'm_n3': 'm_{#chi^{0}_{3}}',
    'm_n4': 'm_{#chi^{0}_{4}}',
    'm_c1': 'm_{#chi^{#pm}_{1}}',
    'm_c2': 'm_{#chi^{#pm}_{2}}',
    'm_G': 'm_{#tilde{G}}',

    # BR
    'br_gl_n1g': 'BR(#tilde{g} #rightarrow #chi^{0}_{1} g)',
    'br_gl_n2g': 'BR(#tilde{g} #rightarrow #chi^{0}_{2} g)',
    'br_gl_n3g': 'BR(#tilde{g} #rightarrow #chi^{0}_{3} g)',
    'br_gl_n1qq': 'BR(#tilde{g} #rightarrow #chi^{0}_{1} qq)',
    'br_gl_n2qq': 'BR(#tilde{g} #rightarrow #chi^{0}_{2} qq)',
    'br_gl_n3qq': 'BR(#tilde{g} #rightarrow #chi^{0}_{3} qq)',
    'br_gl_c1qq': 'BR(#tilde{g} #rightarrow #chi^{#pm}_{1} qq)',
    'br_gl_n1': 'BR(#tilde{g} #rightarrow #chi^{0}_{1})',
    'br_gl_n2': 'BR(#tilde{g} #rightarrow #chi^{0}_{2})',
    'br_gl_n3': 'BR(#tilde{g} #rightarrow #chi^{0}_{3})',
    'br_gl_c1': 'BR(#tilde{g} #rightarrow #chi^{#pm}_{1})',
    'br_gl_Gg': 'BR(#tilde{g} #rightarrow #tilde{G} g)',

    'br_n1_Gy': 'BR(#chi^{0}_{1} #rightarrow #tilde{G} #gamma)',
    'br_n1_GZ': 'BR(#chi^{0}_{1} #rightarrow #tilde{G} Z)',
    'br_n1_Gh': 'BR(#chi^{0}_{1} #rightarrow #tilde{G} h)',

    'br_n2_n1': 'BR(#chi^{0}_{2} #rightarrow #chi^{0}_{1})',
    'br_n2_c1': 'BR(#chi^{0}_{2} #rightarrow #chi^{#pm}_{1})',
    'br_n2_GX': 'BR(#chi^{0}_{2} #rightarrow #tilde{G} X)',

    'br_n3_n1': 'BR(#chi^{0}_{3} #rightarrow #chi^{0}_{1})',
    'br_n3_n2': 'BR(#chi^{0}_{3} #rightarrow #chi^{0}_{2})',
    'br_n3_c1': 'BR(#chi^{0}_{3} #rightarrow #chi^{#pm}_{1})',
    'br_n3_GX': 'BR(#chi^{0}_{3} #rightarrow #tilde{G} X)',

    'ctau_n1': 'c#tau_{#chi^{0}_{1}}',

    'n1_bino': '#tilde{B}',
    'n1_wino': '#tilde{W}_{3}',
    'n1_hino1': '#tilde{H}^{0}_{1}',
    'n1_hino2': '#tilde{H}^{0}_{2}',

    'n2_bino': '#tilde{B}',
    'n2_wino': '#tilde{W}_{3}',
    'n2_hino1': '#tilde{H}^{0}_{1}',
    'n2_hino2': '#tilde{H}^{0}_{2}',

    'n3_bino': '#tilde{B}',
    'n3_wino': '#tilde{W}_{3}',
    'n3_hino1': '#tilde{H}^{0}_{1}',
    'n3_hino2': '#tilde{H}^{0}_{2}',

    'n4_bino': '#tilde{B}',
    'n4_wino': '#tilde{W}_{3}',
    'n4_hino1': '#tilde{H}^{0}_{1}',
    'n4_hino2': '#tilde{H}^{0}_{2}',

}


def get_histogram(filename, x, y, z=False, selection=''):

    tree = ROOT.TChain('slha')
    tree.Add(filename)

    if not z:
        varstr = '%s:%s' % (y, x)

        tree.Draw(varstr, selection)
        g = ROOT.gPad.GetPrimitive("Graph")

        g = sort_graph(g)

    else:
        varstr = '%s:%s:%s>>htmp' % (y, x, z)

        tree.SetMarkerStyle(21)
        tree.SetMarkerSize(1)

        tree.Draw(varstr, selection, 'col goff')

        g = ROOT.gDirectory.Get('htmp')
        g.SetDirectory(0)
        g.SetStats(0)

    ROOT.SetOwnership(g, False)

    g.SetTitle('')
    g.SetMarkerStyle(20)
    g.SetMarkerSize(0.5)

    return g.Clone()


def slhaplot2(filename, x, y, z, selection='', outname='x.pdf', xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None, text=''):

    g = get_histogram(filename, x, y, z, selection)

    g.GetXaxis().SetTitle(labels.get(x, x))
    g.GetYaxis().SetTitle(labels.get(y, y))
    g.GetYaxis().SetTitleOffset(1.7)

    g.GetZaxis().SetTitle(labels.get(z, z))
    g.GetZaxis().SetTitleOffset(1.7)

    if xmin is not None and xmax is not None:
        g.GetXaxis().SetRangeUser(xmin, xmax)
    if ymin is not None and ymax is not None:
        g.GetYaxis().SetRangeUser(ymin, ymax)

    c = ROOT.TCanvas('', '', 800, 800)
    c.SetLeftMargin(0.12)
    c.SetTopMargin(0.06)
    if z is not None:
        c.SetRightMargin(0.18)

    if z:
        g.SetContour(999)
        if zmin is not None and zmax is not None:
            g.SetContour(999)
            g.GetZaxis().SetRangeUser(zmin, zmax)

        g.Draw('colz')
    else:
        g = sort_graph(g)
        g.Draw('pa')

    if text is not None:
        t = ROOT.TLatex(0.14, 0.96, text)
        t.SetNDC()
        t.SetTextFont(42)
        t.SetTextSize(0.035)
        t.Draw()

    c.SaveAs(outname)

    return g

def slhaplot(filename, x, y, scanvar, scanvalues=[], selection='', outname='x.pdf', xmin=None, xmax=None, ymin=None, ymax=None, text=''):

    colors = ['purple', 'blue', 'green', 'orange', 'pink', 'yellow', 'gray']

    graphs = []

    if scanvalues > 4:
        leg = create_legend(0.5, 0.8, 0.7, 0.85, 2)
    else:
        leg = create_legend(0.5, 0.8, 0.7, 0.85)

    i = 0
    for cut in scanvalues:

        tag = '%s = %i' % (labels.get(scanvar, scanvar), cut)

        g = get_histogram(filename, x, y, '', selection+' && %s == %i' % (scanvar, cut))

        g.SetMarkerColor(get_color(colors[i]))

        leg.AddEntry(g, tag, 'p')

        graphs.append(g)

        i += 1

    graphs[0].GetXaxis().SetTitle(labels.get(x, x))
    graphs[0].GetYaxis().SetTitle(labels.get(y, y))
    graphs[0].GetXaxis().SetRangeUser(xmin, xmax)
    graphs[0].GetYaxis().SetRangeUser(ymin, ymax)

    graphs[0].GetXaxis().SetLimits(xmin, xmax)

    can = ROOT.TCanvas()

    graphs[0].Draw('pa')

    for g in graphs[1:]:
        g.Draw('p same')

    leg.Draw()

    if text:
        t = ROOT.TLatex(0.1, 0.92, text)
        t.SetNDC()
        t.SetTextFont(132)
        t.SetTextSize(0.035)
        t.Draw()

    can.SaveAs(outname)


def slhaplot1(filename, x, y, selection='', outname='x.pdf', xmin=None, xmax=None, ymin=None, ymax=None, logy=False, text=''):

    g = get_histogram(filename, x, y, '', selection)

    g.SetMarkerColor(get_color('blue'))

    g.GetXaxis().SetTitle(labels.get(x, x))
    g.GetYaxis().SetTitle(labels.get(y, y))

    if xmin is not None and xmax is not None:
        g.GetXaxis().SetRangeUser(xmin, xmax)
        g.GetXaxis().SetLimits(xmin, xmax)

    if ymin is not None and ymax is not None:
        g.GetYaxis().SetRangeUser(ymin, ymax)

    can = ROOT.TCanvas()

    if logy:
        can.SetLogy()

    g.Draw('pa')

    if text:
        t = ROOT.TLatex(0.1, 0.92, text)
        t.SetNDC()
        t.SetTextFont(132)
        t.SetTextSize(0.035)
        t.Draw()

    can.SaveAs(outname)


def main():

    parser = argparse.ArgumentParser(description='create plots from slha tree')
    parser.add_argument('treepath', nargs='?', help='Path to slha tree')
    parser.add_argument('-o', dest='output_file', help='Output file', required=True)

    parser.add_argument('-x', help='X variable')
    parser.add_argument('-y', help='Y variable')
    parser.add_argument('-z', help='Z variable')
    parser.add_argument('-s', default='', help='Selection')

    parser.add_argument('--text', help='')

    args = parser.parse_args()

    if args.z is None:
        slhaplot1(args.treepath, args.x, args.y, outname=args.output_file)
    else:
        slhaplot2(args.treepath, args.x, args.y, args.z, args.s, outname=args.output_file, text=args.text)


if __name__ == '__main__':

    ROOT.gROOT.SetBatch()

    # set_default_style()
    ROOT.gStyle.SetPalette(57)


    main()
