#!/usr/bin/python

from wellcompare.graph import app

if __name__ == "__main__":
    print("Enter name of screen directory (Ex. 'Screen1')")
    inp = input("- ")
    app.grph("Screens/" + inp + "/")
