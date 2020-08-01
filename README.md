[GarciaLab](https://www.garcialab.org)

Code developed for research on modeling prion growth dynamics in budding yeast.
This package is used to compare two 96 well plates well by well, for example
comparing A1 of one plate to A1 or another plate, and so on. This code generates
graphs, heatmaps, and sumarries of your data, while also performing some basic
statistics.

# Usage -
Begin by creating a directory for your screen (Ex. "Screen1"). Inside of 
your screen directory, create another folder called 'Data' and put the 
excel file produce from the Epoch2 plate reader inside. Then, from the 
RME_Screen directory, run the file graph.py ($ python graph.py) on the 
terminal.
    
# Requirements -
Also outlined in requirements.txt:
1. Python3
2. Pip3
3. Python3 Pandas
4. Python3 Numpy
5. Python3 Maplotlib
6. Python3 Scipy
7. Python3 Seaborn

# Setup -
1. $ git clone https://github.com/jacobian0208/well_compare.git
3. $ pip install -r requirements.txt
2. $ python setup.py

# Files & Directories -

