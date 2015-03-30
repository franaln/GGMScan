#!/usr/bin/env python2.7

import sys, os, argparse
from array import array
import ROOT

def get_gluino_mass(m3):
    p0 = 166.071
    p1 = 0.89076
    return p0+p1*m3

def get_chi1_mass(mu):
    p0 = -29.3908
    p1 = 1.01192
    return p0+p1*mu

def get_m3(m_gl):
    p0 = 166.071
    p1 = 0.89076
    return (m_gl-p0)/p1

def get_mu(m_chi1):
    p0 = -29.3908
    p1 = 1.01192
    return (m_chi1-p0)/p1

if __name__ == '__main__':

    # config
    parser = argparse.ArgumentParser(description='draw particles decays from grid slha files')
    parser.add_argument('--infile', dest='infile', action='store', help='File with the list of slha files to consider.', default='slhafiles.txt')
    parser.add_argument('--fullbr', action='store_true', help='Do full (sgl ...> n1) br calculation')
    parser.add_argument('--fpath', dest='fpath', action='store', help='Path to slha files to be read.')

    config = parser.parse_args()

    #open parameters file
    if os.path.isfile(config.infile):
        with open(config.infile,'r') as fin:
            slha_files = fin.read().split('\n')

    else:
        print 'File not found! Try again...'
        sys.exit(1)

    m3 = []
    mu = []
    gl_n1g = []   #  BR(~g -> ~chi_10 g)
    gl_n2g = []   #  BR(~g -> ~chi_20 g)
    gl_n3g = []   #  BR(~g -> ~chi_30 g)
    gl_Gg = [] #  BR(~g -> ~G      g)

    gl_n1qq = []  # BR(~g -> ~chi_10 q  qb)
    gl_n2qq = []  # BR(~g -> ~chi_20 q  qb)
    gl_n3qq = []  # BR(~g -> ~chi_30 q  qb)
    gl_c1qq = []  # BR(~g -> ~chi_10 q  qb)

    n1_Ggam = [] # BR(~chi_10 -> ~G        gam)
    n1_Gz = []   # BR(~chi_10 -> ~G        Z)
    n1_Gh = []   # BR(~chi_10 -> ~G        h)

    n2_n1 = [] # BR(~chi_20 -> ~chi10 ...
    n2_c1 = [] # BR(~chi_20 -> ~chi1+ ...
    n3_n1 = [] # BR(~chi_30 -> ~chi10 ...
    n3_n2 = [] # BR(~chi_30 -> ~chi20 ...
    n3_c1 = [] # BR(~chi_30 -> ~chi1+ ...
    c1_n1 = [] # BR(~chi_1+ -> ~chi10 ...

    outfile = ROOT.TFile('decays.root', 'recreate')

    for f in slha_files:

        if not f:
            continue

        path = os.path.join(config.fpath, f)

        print 'Processing', path

        try:
            fin =  open(path,'r')
            rows = fin.read().split('\n')
            fin.close()
        except:
            print 'File ',config.fpath+f,' not found! Skipping...'
            continue

        m3.append(float(f.split('_')[4]))
        mu.append(float(f.split('_')[-1].split('.')[0]))

        #gluino->...
        n1g = 0
        n2g = 0
        n3g = 0
        Gg = 0
        Ggam = 0
        Gz = 0
        Gh = 0
        n1qq = 0
        n2qq = 0
        n3qq = 0
        c1qq = 0

        #secondary decays to n1
        n2n1 = 0
        n2c1 = 0
        n3n1 = 0
        n3n2 = 0
        n3c1 = 0
        c1n1 = 0

        for r in rows:

            if "# BR(" not in r:  #just look at gluino decays for now
                    continue

            dp = float(r.split()[0])

            if "BR(~g -> ~G      g)" in r:
                Gg = dp

            if "BR(~g -> ~chi_10" in r:
                if "g)" in r:
                    n1g = dp
                elif ("d  db)" in r) or ("u  ub)" in r) or ("s  sb)" in r) or ("c  cb)" in r) or ("b  bb)" in r) or ("t  tb)" in r):
                    n1qq += dp

            if "BR(~g -> ~chi_20 " in r:
                if "g)" in r:
                    n2g = dp
                elif ("d  db)" in r) or ("u  ub)" in r) or ("s  sb)" in r) or ("c  cb)" in r) or ("b  bb)" in r) or ("t  tb)" in r):
                    n2qq += dp

            if "BR(~g -> ~chi_30 " in r:
                if "g)" in r:
                    n3g += dp
                elif ("d  db)" in r) or ("u  ub)" in r) or ("s  sb)" in r) or ("c  cb)" in r) or ("b  bb)" in r) or ("t  tb)" in r):
                    n3qq += dp

            if ("BR(~g -> ~chi_1+" in r) or ("BR(~g -> ~chi_1-" in r):
                c1qq += dp

            if "BR(~chi_10 -> ~G        gam)" in r:
                Ggam = dp

            if "BR(~chi_10 -> ~G        Z)" in r:
                Gz = dp

            if "BR(~chi_10 -> ~G        h)" in r:
                Gh = dp

            if "BR(~chi_1+ -> ~chi_10 " in r:
                #if ("u    db)" in r) or ("c    sb)" in r) or ("e+   nu_e)" in r) or ("mu+  nu_mu)" in r) or ("tau+ nu_tau)" in r): #not needed
                c1n1 += dp

            if "BR(~chi_20 -> ~chi_10 " in r:
                n2n1 += dp

            if ("BR(~chi_20 -> ~chi_1+ " in r) or ("BR(~chi_20 -> ~chi_1- " in r):
                n2c1 += dp

            if "BR(~chi_30 -> ~chi_10 " in r:
                n3n1 += dp

            if "BR(~chi_30 -> ~chi_20 " in r:
                n3n2 += dp

            if ("BR(~chi_30 -> ~chi_1+ " in r) or ("BR(~chi_30 -> ~chi_1- " in r):
                n3c1 += dp

        gl_n1g.append(n1g)
        gl_n2g.append(n2g)
        gl_n3g.append(n3g)
        gl_Gg.append(Gg)

        gl_n1qq.append(n1qq)
        gl_n2qq.append(n2qq)
        gl_n3qq.append(n3qq)
        gl_c1qq.append(c1qq)

        n1_Ggam.append(Ggam)
        n1_Gz.append(Gz)
        n1_Gh.append(Gh)

        c1_n1.append(c1n1)
        n2_n1.append(n2n1)
        n2_c1.append(n2c1)
        n3_n1.append(n3n1)
        n3_n2.append(n3n2)
        n3_c1.append(n3c1)


    mu_min = 150
    mu_max = 1300
    mu_bins = (mu_max - mu_min) / 25

    m3_min = 800
    m3_max = 1500
    m3_bins = (m3_max - m3_min) / 25

    h_gl_n1g = ROOT.TH2F('h_gl_n1g', ';M_{3} [GeV];#mu [GeV]', m3_bins, m3_min, m3_max, mu_bins, mu_min, mu_max)
    h_gl_n2g   = h_gl_n1g.Clone("h_gl_n2g")
    h_gl_n3g   = h_gl_n1g.Clone("h_gl_n3g")
    h_gl_n1qq  = h_gl_n1g.Clone("h_gl_n1qq")
    h_gl_n2qq  = h_gl_n1g.Clone("h_gl_n2qq")
    h_gl_n3qq  = h_gl_n1g.Clone("h_gl_n3qq")
    h_gl_c1qq  = h_gl_n1g.Clone("h_gl_c1qq")
    h_gl_Gg = h_gl_n1g.Clone("h_gl_Gg")

    h_gl_n1g_full  = h_gl_n1g.Clone("h_gl_n1g_full")
    h_gl_n2g_full  = h_gl_n1g.Clone("h_gl_n2g_full")
    h_gl_n3g_full  = h_gl_n1g.Clone("h_gl_n3g_full")
    h_gl_n1qq_full = h_gl_n1g.Clone("h_gl_n1qq_full")
    h_gl_n2qq_full = h_gl_n1g.Clone("h_gl_n2qq_full")
    h_gl_n3qq_full = h_gl_n1g.Clone("h_gl_n3qq_full")
    h_gl_c1qq_full = h_gl_n1g.Clone("h_gl_c1qq_full")
    h_gl_Gg_full = h_gl_n1g.Clone("h_gl_Gg_full")

    h_gl_n1 = h_gl_n1g.Clone("h_gl_n1")
    h_gl_n2 = h_gl_n1g.Clone("h_gl_n2")
    h_gl_n3 = h_gl_n1g.Clone("h_gl_n3")
    h_gl_c1 = h_gl_n1g.Clone("h_gl_c1")

    h_gl_n1_full = h_gl_n1g.Clone("h_gl_n1_full")
    h_gl_n2_full = h_gl_n1g.Clone("h_gl_n2_full")
    h_gl_n3_full = h_gl_n1g.Clone("h_gl_n3_full")
    h_gl_c1_full = h_gl_n1g.Clone("h_gl_c1_full")

    h_n1_Ggam = h_gl_n1g.Clone("h_n1_Ggam")
    h_n1_Gz = h_gl_n1g.Clone("h_n1_Gz")
    h_n1_Gh = h_gl_n1g.Clone("h_n1_Gh")

    #fill histos
    for i in xrange(len(m3)):

        #print n2_n1[i] + n2_c1[i]*c1_n1[i]
        print m3[i], mu[i],  (n3_n2[i]*((n2_n1[i] + n2_c1[i]*c1_n1[i])) + n3_c1[i]*c1_n1[i])

        h_gl_n1g_full.Fill(m3[i], mu[i], gl_n1g[i])
        h_gl_n2g_full.Fill(m3[i], mu[i], gl_n2g[i] * (n2_n1[i] + n2_c1[i]*c1_n1[i]))
        h_gl_n3g_full.Fill(m3[i], mu[i], gl_n3g[i] * (n3_n2[i]*((n2_n1[i] + n2_c1[i]*c1_n1[i])) + n3_c1[i]*c1_n1[i]))
        h_gl_Gg_full .Fill(m3[i], mu[i], gl_Gg[i])

        h_gl_n1qq_full.Fill(m3[i], mu[i],gl_n1qq[i])
        h_gl_n2qq_full.Fill(m3[i], mu[i],gl_n2qq[i] * (n2_n1[i] + n2_c1[i]*c1_n1[i]))
        h_gl_n3qq_full.Fill(m3[i], mu[i],gl_n3qq[i] * (n3_n2[i]*((n2_n1[i] + n2_c1[i]*c1_n1[i])) + n3_c1[i]*c1_n1[i]))
        h_gl_c1qq_full.Fill(m3[i], mu[i],gl_c1qq[i] * c1_n1[i])

        h_gl_n1_full.Fill(m3[i], mu[i], gl_n1qq[i]+gl_n1g[i])
        h_gl_n2_full.Fill(m3[i], mu[i], (gl_n2qq[i]+gl_n2g[i]) * (n2_n1[i] + n2_c1[i]*c1_n1[i]))
        h_gl_n3_full.Fill(m3[i], mu[i], (gl_n3qq[i]+gl_n3g[i]) * ( n3_n2[i]*((n2_n1[i] + n2_c1[i]*c1_n1[i])) + n3_c1[i]*c1_n1[i] ))
        h_gl_c1_full.Fill(m3[i], mu[i], gl_c1qq[i] * c1_n1[i])

        h_gl_n1g.Fill(m3[i], mu[i], gl_n1g[i])
        h_gl_n2g.Fill(m3[i], mu[i], gl_n2g[i])
        h_gl_n3g.Fill(m3[i], mu[i], gl_n3g[i])
        h_gl_Gg .Fill(m3[i], mu[i], gl_Gg[i])
        h_gl_n1qq.Fill(m3[i], mu[i], gl_n1qq[i])
        h_gl_n2qq.Fill(m3[i], mu[i], gl_n2qq[i])
        h_gl_n3qq.Fill(m3[i], mu[i], gl_n3qq[i])
        h_gl_c1qq.Fill(m3[i], mu[i], gl_c1qq[i])

        h_gl_n1.Fill(m3[i], mu[i], gl_n1qq[i]+gl_n1g[i])
        h_gl_n2.Fill(m3[i], mu[i], gl_n2qq[i]+gl_n2g[i])
        h_gl_n3.Fill(m3[i], mu[i], gl_n3qq[i]+gl_n3g[i])
        h_gl_c1.Fill(m3[i], mu[i], gl_c1qq[i])

        h_n1_Ggam.Fill(m3[i], mu[i], n1_Ggam[i])
        h_n1_Gz.Fill(m3[i], mu[i], n1_Gz[i])
        h_n1_Gh.Fill(m3[i], mu[i], n1_Gh[i])

    # save hsitograms
    outfile.Write()
