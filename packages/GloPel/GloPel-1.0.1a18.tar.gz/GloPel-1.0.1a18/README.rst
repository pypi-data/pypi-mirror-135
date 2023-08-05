GloPel
======

GloPel is a Python3-based program for the processing and (global) analysis of PELDOR/DEER traces. GloPel provides a user-friendly GUI based on the PyQt5 GUI framework.

GloPel has been developed in the group of Prof. Dr. Stefan Weber at the University of Freiburg, Freiburg im Breisgau, Germany, during the last couple of years. GloPel was developed by Stephan Rein for the global analysis of PELDOR data and was published in:


[1] S. Rein, P. Lewe, S. L. Andrade, S. Kacprzak, and S. Weber.  *J. Magn. Reson.*, 295 (**2018**) 17–26.


If you use GloPel for your own research and publish results accordingly, please give credits
citing the appropriate reference.

Find the full documentation at the link below:
https://www.radicals.uni-freiburg.de/de/software



Installation
------------

Install GloPel via pip:

$ pip install glopel


Run GloPel
----------

Run GloPel on the console via:

$ GloPel


Alternatively, call it as package when running Python:


>>> from GloPel.GloPel import run
>>> run()



Various subfunctions of GloPel can be used modulary.

Generate a discrete 5x5 second derivative operator:


>>> from GloPel.Regularization import second_order_diffential_operator
>>> diffop = second_order_diffential_operator(5)
>>> print(diffop)
[[-2.  1.  0.  0.  0.]
 [ 1. -2.  1.  0.  0.]
 [ 0.  1. -2.  1.  0.]
 [ 0.  0.  1. -2.  1.]
 [ 0.  0.  0.  1. -2.]]


Generate a PELDOR kernel matrix for t = 0 to t = 2000 ns, using 131 points in the distance domain:


>>> import numpy as np
>>> from GloPel.Regularization import kernel_matrix
>>> time = np.linspace(0, 2000, 500)
>>> points = 131
>>> kernel = kernel_matrix(time, points)


Properties
----------

GloPel provides:

- PELDOR/DEER data processing
- Tikhonov regularization
- Model-based fitting
- Global analysis (Tikhonov and fitting) of two time traces
- Validation tools
- User friendly graphical user interface
- Automatically generated reports


Feedback
--------

We are eager to hear about your experiences with GloPel. You can
email me at stephan.rein@physchem.uni-freiburg.de.  


Acknowledgement
---------------

A number of people have helped shaping GloPel and the ideas behind. First and foremost, Prof. Dr. Stefan Weber and Dr. Sylwia Kacprzak (now Bruker Biospin) were for years the driving force behind GloPel due to the need for advanced analysis of PELDOR/DEER data with limited signal-to-noise ratio. Dr. Till Biskup (now Saarland University) contributed ideas for programming and details of the implementation that make all the difference between a program useful for a larger audience and a simple in-house solution.


Bugfixes
--------
31.08.2020 (Error message appearing for global validation without additive noise)

