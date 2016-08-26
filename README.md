GGMScan
========

To scan the GGM phase space:

* Run:

```
ggmscan.py
```

* The configfile must have the following vectors defining the phase space to scan:

```
v_mu, v_m1, v_m2, v_m3, v_at, v_gmass, v_msq, v_tanb
```

* It can also contain a filter function. If return true the point is skipped.

```
def filter_fn(m1, m2, m3, mu, tanb, msq, at, gmass):
     ...
```
