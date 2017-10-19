GGMScan
========

To download and compile SUSYHIT package:

    bash install.sh



To scan the GGM parameter space:

* Usage:

```
ggmscan.py -c CONFIGFILE [-o OUTPUTDIR] [-v] [--count] [--scan]
```

* The configfile must have the following lists defining the phase space to scan:

```
v_mu, v_m1, v_m2, v_m3, v_at, v_gmass, v_msq, v_tanb
```

* It can also contain a filter function (based on parameters or the slha parameters). If return true the point is skipped.

```
def filter_par_fn(m1, m2, m3, mu, tanb, msq, at, gmass):
    ...

def filter_slha_fn(slha_path):
    ...
```


* To create an ntuple from slha files:

```
slha2tree.py -r -o OUTPUT_FILE SLHA_DIR
```
