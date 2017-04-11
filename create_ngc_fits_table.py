#!/usr/bin/python3
#
# Copyright 2017 Christian Dersch <lupinix@mailbox.org>
# All rights reserved.
#
# License: BSD (3 clause, see file LICENSE in top directory)
#

import numpy as np
from astropy.coordinates import Angle
from astropy.io import ascii, fits
from astropy.table import Table
import astropy.units as u

openngc_csv = "OpenNGC/NGC.csv"



def getnum(ngcstr):
    # Function to extract the integer number of an object,
    # returns 0 for non-main objects to avoid duplicates
    if ngcstr[0] == "N":
        if len(ngcstr) == 7:
            return ngcstr[3:7]
        else:
            return "0"
    elif ngcstr[0] == "I":
        if len(ngcstr) == 6:
            return ngcstr[2:6]
        else:
            return "0"
    else:
        return "0"

getnum_vect = np.vectorize(getnum)


def readable_names(ngcstr):
    # Generate better readable names, e.g. NGC 224 instead of NGC0224
    if ngcstr[0] == "N":
        readable_name = "NGC " + ngcstr[3:].lstrip("0")
    elif ngcstr[0] == "I":
        readable_name = "IC " + ngcstr[2:].lstrip("0")
    else:
        # Change nothing if don't know what to do
        readable_name = ngcstr
    return readable_name

readable_names_vect = np.vectorize(readable_names)

###### main program ######
ngcic = ascii.read(openngc_csv,delimiter=";")
# As we have masked table, we have to handle our integer column a bit special,
# get as string first, set int compatible fill value and convert on
# table creation
ngc_numbers = getnum_vect(ngcic["Name"])
ngc_numbers.set_fill_value(0)
#
table = Table([Angle(ngcic["RA"],unit="hourangle").to(u.deg),
    Angle(ngcic["Dec"],unit=u.deg),
    ngcic["Type"],
    # Calculate radius in degrees
    (ngcic["Smax"]*u.arcmin/2).to(u.deg),
    readable_names_vect(ngcic["Name"]),
    ngc_numbers.astype(np.int16)],
    # use the column names as in previous ngc2000 tables from now on
    names=("ra","dec","classification","radius","name","number"))
table.sort("ra")

# split the table into one for NGC and one for IC, sort out sub-objects
# to have a table with only the original ngcic objects
table_ngc = table[np.char.startswith(table["name"],"NGC")]
table_ngc = table_ngc[table_ngc["number"]!=0]
table_ic = table[np.char.startswith(table["name"],"IC")]
table_ic = table_ic[table_ic["number"]!=0]

# Now we are ready to create the FITS tables
# ngc
tbhdu_ngc = fits.BinTableHDU.from_columns(
    [fits.Column(name="ra",format="E",array=table_ngc["ra"]),
     fits.Column(name="dec",format="E",array=table_ngc["dec"]),
     fits.Column(name="classification",format="A10",array=table_ngc["classification"]),
     fits.Column(name="radius",format="E",array=table_ngc["radius"]),
     fits.Column(name="name",format="A8",array=table_ngc["name"]),
     fits.Column(name="ngcnum",format="I",array=table_ngc["number"])])
tbhdu_ngc.writeto('openngc_ngc.fits')

# ic
tbhdu_ic = fits.BinTableHDU.from_columns(
    [fits.Column(name="ra",format="E",array=table_ic["ra"]),
     fits.Column(name="dec",format="E",array=table_ic["dec"]),
     fits.Column(name="classification",format="A10",array=table_ic["classification"]),
     fits.Column(name="radius",format="E",array=table_ic["radius"]),
     fits.Column(name="name",format="A8",array=table_ic["name"]),
     fits.Column(name="icnum",format="I",array=table_ic["number"])])
tbhdu_ic.writeto('openngc_ic.fits')


