# GGM scan (gluino neutralino grid)

import pyslha

## Parameter values
mu_min = 1000
mu_max = 2000
mu_step = 100

m1_min = 1000
m1_max = 2000
m1_step = 100

m3_min = 1000
m3_max = 2000
m3_step = 100

# Construct vectors
v_m1 = range(m1_min, m1_max, m1_step)
v_mu = range(mu_min, mu_max, mu_step)
v_m3 = range(m3_min, m3_max, m3_step)
v_tanb = [1.5, 5., 10., 25., 50.]

v_msq = [2.5E+03,]
v_gmass = [1E-09,]
v_at = [0,]
v_m2 = [3E+03]

def filter_slha_fn(slha_path):
    masses = pyslha.read(slha_path).blocks['MASS']
    m_gl = masses[1000021]
    m_n1 = masses[1000022]
    if m_n1 > m_gl:
        return True

    return False
