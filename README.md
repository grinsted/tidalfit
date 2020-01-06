Tidalfit for python
===================

A minimal tool for estimating tidal amplitudes and phases from e.g. tide gauge observations. 

There is an example/testcase in the bottom of tidalfit.py.

check also [Utide](https://github.com/wesleybowman/UTide).


This is less full-featured than pytides, but:
* It is much faster for large data sets
* pytides does not appear to be not actively maintained. 
* This is much simpler. I do not attempt to calculate the tidal frequencies, but simply look them up in a table. 
* it uses with numpy/pandas datetime instead of 'old'-style datetime and timestamps. 
* The constituent table with amplitudes and phases are stored in a pandas dataframe.

This is very much still a work in progress.


TODO:
* allow a trend and mean component to be fitted at the same time, or allow user to specify additional "predictors".
* add robust fitting methods. 
* consider fit to be a @classmethod
* avoid overfitting. (Remove constituents that cannot be fitted with the given data.)
* use a standard reference epoch / phase 
* Use singleton to hold master harmonic table.
* more tests...
* ...
