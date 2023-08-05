
pyPipe3D
========

This is the repository for pyPipe3D, a Python implementation of the Pipe3D pipeline. pyPipe3D is a spectroscopy analysis pipeline which produces coherent, easy to distribute and compare, parameters of the stellar populations and the ionized gas, suited in particular for data from the most recent optical IFS surveys. The pipeline is build using ``pyFIT3D``, which is the main spectral fitting module included in this package.

Main scripts of analysis and plots are located in directory `bin`. The package also contains a set of examples at the sub-directory `examples`. ``pyFIT3D`` is located with the following structure::

	pyFIT3D
	├── common
	│   ├── __init__.py
	│   ├── auto_ssp_tools.py
	│   ├── constants.py
	│   ├── gas_tools.py
	│   ├── io.py
	│   ├── stats.py
	│   └── tools.py
	├── __init__.py
	└── modelling
	    ├── __init__.py
	    ├── dust.py
	    ├── gas.py
	    └── stellar.py

Documentation
-------------

**pyPipe3D** Documentation is under construction. The present version of the documentation can be found `here <http://ifs.astroscu.unam.mx/pyPipe3D>`.

Installation
------------

If you want to use the modules distributed in this project on your system, you will need a working installation of `Python 3.7` and `pip`. Then you can simply run from the terminal::

	$ pip install pyPipe3D

Instead, if you want to clone this repository, run::

	$ git clone https://gitlab.com/pipe3d/pyPipe3D.git

or if you have configured an SSH access key::

	$ git clone git@gitlab.com:pipe3d/pyPipe3D.git

This will create a directory containing the source code and data sets in `pyPipe3D`, then you install the packages running::

	$ cd pyPipe3D
	$ pyPipe3D> pip install .

And you are done.

Run emission lines fit test example
-----------------------------------

`fit_elines.py` example::

	$ pyPipe3D> cd examples
	$ pyPipe3D/examples> source fit_elines_example.sh

or::

	$ pyPipe3D/examples> fit_elines.py NGC5947.cen.gas.txt notebooks/Ha_NII.config none 6600 6800 2 20 5 0 0.15 fit_elines.NII_Ha.NGC5947.out

or::

	$ pyPipe3D/examples> python fit_elines_example.py

Example of the pipeline procedure of analysis for a CALIFA data cube
--------------------------------------------------------------------

We prepare an example of the pyPipe3D pipeline analysis of a CALIFA data cube. For the full description of the execution of the pipeline `read this <examples/IFS_analysis/README.txt>`.

Contact us: `pipe3d@astro.unam.mx <mailto:pipe3d@astro.unam.mx>`
