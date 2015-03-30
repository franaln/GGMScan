# single photon analysis

import ROOT
from rootutils import Hist2D
#from susyplot import Plot2D

class GridHistogram(Hist2D):

    m3_min = 800
    m3_max = 1450

    mu_min = 150
    mu_max = 1250

    def __init__(self, name):


        self.m3_bins = (self.m3_max - self.m3_min + 50) / 25
        self.mu_bins = (self.mu_max - self.mu_min + 50) / 25

        Hist2D.__init__(self, name, self.m3_bins, self.m3_min, self.m3_max + 50, self.mu_bins, self.mu_min, self.mu_max + 50)

    def load(self, h):
        for bx in xrange(h.GetNbinsX()):
            for by in xrange(h.GetNbinsY()):
                self.SetBinContent(bx+1, by+1, h.GetBinContent(bx+1, by+1))

    def fill(self, m3, mu, value):
        m3_bin = self.get_m3_bin(m3)
        mu_bin = self.get_mu_bin(mu)
        self.SetBinContent(m3_bin, mu_bin, value)

    def get(self, m3, mu):
        m3_bin = self.get_m3_bin(m3)
        mu_bin = self.get_mu_bin(mu)
        return self.GetBinContent(m3_bin, mu_bin)

    # def walk(self):
    #     for

    def get_m3_bin(self, m3):
        return int((m3 - self.m3_min)/25) + 1

    def get_mu_bin(self, mu):
        return int((mu - self.mu_min)/25) + 1

    # def plot(self, name, zmin=0., zmax=1., ztitle='', text=False, add_text=''):

    #     plot = Plot2D(name)
    #     ROOT.gStyle.SetPaintTextFormat('g')
    #     if text:
    #         plot.add('', self, drawopts='colz text')
    #     else:
    #         plot.add('', self, drawopts='colz')
    #     plot.create(zmin=zmin, zmax=zmax, xtitle='M_{3} (GeV)', ytitle='#mu (GeV)', ztitle=ztitle)
    #     if add_text:
    #         plot.draw_text(0.2, 0.8, add_text)
    #     plot.save(name+'.eps')
    #     plot.save(name+'.png')
