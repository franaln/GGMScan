import ROOT
from rootutils import *

def draw_boxlegend(x, y, color, text):

    box = ROOT.TBox(x, y+2, x+30, y+28)
    box.SetFillColor(get_color(color))

    label = ROOT.TLatex(x+40, y, text)
    label.SetTextSize(0.025)

    ROOT.SetOwnership(box, False)
    ROOT.SetOwnership(label, False)

    box.Draw()
    label.Draw()

def draw_boxpie(m3, mu, *brs):

    y1 = mu
    y2 = mu + 25

    colors = ['purple', 'blue', 'green', 'orange', 'pink']

    x2 = m3
    for i, br in enumerate(brs):
        x1 = x2 + 0.001
        x2 = x1 + round(br*25,1)

        box = ROOT.TBox(x1, y1, x2, y2)
        box.SetFillColor(get_color(colors[i]))
        ROOT.SetOwnership(box, False)
        box.Draw()

def draw_grid_frame():

    canvas = ROOT.TCanvas('', '', 800,800)
    canvas.SetTickx(0)
    canvas.SetTicky(0)

    ROOT.SetOwnership(canvas, False)

    m3_min = 800
    m3_max = 1500

    mu_min = 150
    mu_max = 1500

    nx = (m3_max - m3_min) / 25
    ny = (mu_max - mu_min) / 25

    dx = 25
    dy = 25

    frame = ROOT.TH2F('h2', 'h2', nx, m3_min, m3_max, ny, mu_min, mu_max)
    ROOT.SetOwnership(frame, False)
    frame.SetTitle('')

    canvas.SetTicks()
    canvas.SetLeftMargin(0.120)
    canvas.SetRightMargin(0.120)
    canvas.SetBottomMargin(0.120)
    canvas.SetTopMargin(0.120)

    frame.SetLabelOffset(0.012, "X") # label offset on x axis
    frame.SetLabelOffset(0.012, "Y") # label offset on x axis
    frame.SetXTitle('M_{3} [GeV]')
    frame.SetYTitle('#mu [GeV]')
    frame.GetXaxis().SetTitleSize(0.03)
    frame.GetYaxis().SetTitleSize(0.03)
    frame.GetXaxis().SetLabelSize(0.03)
    frame.GetYaxis().SetLabelSize(0.03)
    frame.GetXaxis().SetTitleOffset(1.4)
    frame.GetYaxis().SetTitleOffset(1.8)

    frame.GetXaxis().SetNdivisions(10, 3, 0)
    frame.GetYaxis().SetNdivisions(10, 5, 0)

    frame.Draw("hist")
    ROOT.gROOT.ForceStyle()

    #hack for GGM . The physics limit is not in M3-mu but in m_gl-m_chi10. So transform one into the other!
    f_m3mg = ROOT.TF1("f_m3mg", "170.511+x*0.896509", 0, 2000)
    f_m3mg.SetRange(f_m3mg.Eval(frame.GetXaxis().GetXmin()), f_m3mg.Eval(frame.GetXaxis().GetXmax()))

    f_mumn = ROOT.TF1("f_mumn", "-16.9058+x*1.01732", 0, 2000)
    f_mumn.SetRange(f_mumn.Eval(frame.GetYaxis().GetXmin()), f_mumn.Eval(frame.GetYaxis().GetXmax()))

    xc = min(f_m3mg.Eval(m3_max), m3_max)
    yc = min(f_m3mg.Eval(mu_max), mu_max)

    lmg = ROOT.TLine(m3_min, f_m3mg.Eval(m3_min), xc, yc)
    ROOT.SetOwnership(lmg, False)
    lmg.SetLineStyle(2)
    lmg.SetLineColor(1)
    lmg.Draw()

    valText = ROOT.TLatex()
    valText.SetNDC()
    valText.SetTextAlign(11)
    valText.SetTextSize(0.02)
    valText.SetTextColor(ROOT.TColor.GetColor("#555555"))
    valText.SetTextAngle(25)
    valText.DrawLatex(0.6,0.79, "m_{#tilde{g}} < m_{#tilde{#chi}_{1}^{0}}")
    valText.AppendPad()
    ROOT.gPad.SetTicks(0, 0)

    # m_gluino axis
    mg_axis = ROOT.TGaxis(frame.GetXaxis().GetXmin(), frame.GetYaxis().GetXmax(), frame.GetXaxis().GetXmax(), frame.GetYaxis().GetXmax(), "f_m3mg", 510, "-")
    ROOT.SetOwnership(mg_axis, False)
    mg_axis.ImportAxisAttributes(frame.GetXaxis())
    mg_axis.SetTitle("m_{#tilde{g}} [GeV]")
    mg_axis.SetTitleOffset(1.2)
    mg_axis.SetLabelOffset(0.001)
    mg_axis.Draw()

    # m_chi10 axis
    mu_axis = ROOT.TGaxis(frame.GetXaxis().GetXmax(), frame.GetYaxis().GetXmin(), frame.GetXaxis().GetXmax(), frame.GetYaxis().GetXmax(), "f_mumn", 510, "+L")
    ROOT.SetOwnership(mu_axis, False)
    mu_axis.ImportAxisAttributes(frame.GetYaxis())
    mu_axis.SetTitle("m_{#tilde{#chi}^{0}_{1}} [GeV]")
    mu_axis.SetLabelOffset(0.01)
    mu_axis.SetTitleOffset(2)
    mu_axis.Draw()

    # Redraw axis and update canvas
    canvas.RedrawAxis()

    return canvas
