#! /usr/bin/env python2.7

import argparse
import ROOT
from rootutils import set_default_style

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
}


def slhaplot(filename, x, y=None, z=None, selection='', outname='x.pdf', xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None):

    set_default_style()

    # ntotal = tree.GetEntries("1");
    # nselect = tree.GetEntries(cutstr);

    # print "Plotting ", varstr, " with selection ", cutstr, "."
    # print "Selected ", nselect, " out of ", ntotal, " entries. Fraction = ", nselect/ntotal

    tree = ROOT.TChain('slha')
    tree.Add(filename)

    tree.SetMarkerStyle(21)
    tree.SetMarkerSize(1)

    if y is not None and z is not None:
        varstr = '%s:%s:%s>>htmp' % (y, x, z)
    else:
        varstr = '%s>>htmp' % x

    tree.Draw(varstr, selection, 'col goff')

    hist = ROOT.gDirectory.Get('htmp')

    hist.SetTitle('')
    hist.SetStats(0)

    hist.GetXaxis().SetTitle(labels.get(x, x))

    if y is not None:
        hist.GetYaxis().SetTitle(labels.get(y, y))
        hist.GetYaxis().SetTitleOffset(1.5)

    if z is not None:
        hist.GetZaxis().SetTitle(labels.get(z, z))
        hist.GetZaxis().SetTitleOffset(1.5)

    if xmin is not None and xmax is not None:
        hist.GetXaxis().SetRangeUser(xmin, xmax)

    if ymin is not None and ymax is not None:
        hist.GetYaxis().SetRangeUser(ymin, ymax)

    if zmin is not None and zmax is not None:
        hist.GetZaxis().SetRangeUser(zmin, zmax)



    c = ROOT.TCanvas('', '', 800, 800)

    c.SetRightMargin(0.16)

    hist.Draw('colz')
    c.SaveAs(outname)


def main():

    parser = argparse.ArgumentParser(description='create plots from slha tree')
    parser.add_argument('treepath', nargs='?', help='Path to slha tree')
    parser.add_argument('-o', dest='output_file', help='Output file', required=True)

    parser.add_argument('-x')
    parser.add_argument('-y')
    parser.add_argument('-z')

    args = parser.parse_args()

    slhaplot(args.treepath, args.x, args.y, args.z, args.output_file)


if __name__ == '__main__':
    main()
