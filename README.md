# [GarciaLab](https://www.garcialab.org)

## Info-
Code developed for research on modeling prion growth dynamics in budding yeast.
This package is used to compare two 96 well plates well by well, for example
comparing A1 of one plate to A1 or another plate, and so on. This code generates
graphs, heatmaps, and sumarries of your data, while also performing some basic
statistics.

## Usage -
Begin by creating a directory for your screens called 'Screens'. Next, 
make a directory inside of that for every screen
that you run (Ex. "Screen1"). Inside of your individual screen directory, 
create another folder called 'Data' and put the excel file produce 
from the Epoch2 plate reader inside. Then, from the outer directory, 
run the package ($ python -m wellcompare) on the terminal. The program 
will create several directories for you. Some notable ones are 'Graphs',
which contains graphs and data summaries, and 'Heatmaps' (if -hm flag added).

Example Directory Structure: 

|- Outer_folder    <- run python -m wellcompare inside this outer directory  
|      |-Screen  
|            |- Screen1  
|                  |- Data    
|                       |- screen1.xslx   
|            |- Screen2   
|                  |- Data  
|                       |- screen2.xslx   
    
    
## Requirements -
Also outlined in requirements.txt:
1. Python3
2. Pip3
3. Pandas
4. Numpy
5. Maplotlib
6. Scipy
7. Seaborn
8. ArgParse
9. xlrd

## Setup & Installation (MacOS)-
Download Package (recommended):
- Type the following commands into terminal
1. $ pip install wellcombine
2. $ python -m wellcompare \[options\]

-- OR --

Clone Repo:
- Type the following commands into terminal
1. $ git clone https://github.com/jacobian0208/well_compare.git
2. $ pip install -r requirements.txt
3. $ python -m wellcompare \[options\]

## Files & Directories -
1. graph.py : module to graph cleaned data
2. extract.py : module to extract and clean data from Epoch2 microplate reader output
3. combine.py : module to combine and further clean extracted data
4. __main__.py : main file to run package as script
5. requirements.txt : a list of required packages to install to run this program correctly
6. LICENSE : an MIT license to allow use of this program

