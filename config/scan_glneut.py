# GGM scan (gluino neutralino grid)

## Parameter values
mu_min = 50
mu_max = 3000
mu_step = 50

m1_min = 50
m1_max = 3000
m1_step = 50

m1mu_min = 0.98
m1mu_max = 1.0

m3_min = 100
m3_max = 2000
m3_step = 100

iN_m1  = (m1_max - m1_min)/m1_step
iN_m3  = (m3_max - m3_min)/m3_step
iN_mu  = (mu_max - mu_min)/mu_step

# Construct vectors
v_M1 = [ m1_min + ir_m1 * m1_step for ir_m1 in xrange(iN_m1) ]
v_mu = [ mu_min + ir_mu * mu_step for ir_mu in xrange(iN_mu) ]
v_M3  = [ m3_min  + ir_m3 * m3_step for ir_m3 in xrange(iN_m3) ]
v_tanbeta = [1.5, 5., 10., 25., 50.]

v_Msq = [2.5E+03,]
v_Gmass = [1E-09,]
v_At = [0,]
