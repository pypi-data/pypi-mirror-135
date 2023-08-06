# TruSD

**Tr**ajectories **u**nder **S**election and **D**rift is an implementation of a method that co-infers selection coefficients and genetic drift from allele trajectories using a maximum-likelihood framework.

If you find the software useful in your research please cite this package.


## Installation

TruSD needs Python 3.6 or newer. Python 2 is *not* supported! TruSD was only
tested on Linux (Ubuntu), but *should* work on Mac and Windows as well.

We suggest to use a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
for use of TruSD. To install TruSD, run:

```sh
pip3 install trusd
```

This will install TruSD as importable module and three command line tools,
`trusd`, `trusd-plot`, and `trusd-sim`.


## Update

If you later want to update TruSD, use the pip command:

```sh
pip3 install --upgrade trusd
```


## Running TruSD from within a Python script

Import the `trusd` module from your Python 3 script:

```python
# inside python3 script or interactive prompt
import trusd
help(trusd.trusd) # gives package content
```

For an example, download two files (for example with `wget`):

```sh
wget https://github.com/mathiasbockwoldt/TruSD/blob/master/examples/min_working_example.py
wget https://github.com/mathiasbockwoldt/TruSD/blob/master/examples/traj_example.txt
```

You can start an example run with

```sh
python3 min_working_example.py
```

The `min_working_example.py` is documented to explain the basic steps.
It uses `traj_example.txt` as input and produces `outfile.txt` (the results),
`outfile.json` (the metadata) and `outfile.pdf` (the plot).


## Running TruSD as command line program

The command line programs are self-explanatory using the `--help` flag.

```sh
trusd --help
trusd-plot --help
trusd-sim --help
```

The parameters are the same as in the Python modules.
