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

openngc_csv = "/home/lupinix/OpenNGC/NGC.csv"

ngcic = ascii.read(openngc_csv,delimiter=";")
table = Table([ngcic["Name"],
    Angle(ngcic["RA"],unit="hourangle").degree,
    Angle(ngcic["Dec"],unit=u.deg).degree,
    ngcic["Type"],
    (ngcic["Smax"]*u.arcmin/2).to(u.deg)],
    names=("Name","RA","Dec","Type","Radius"))
table.sort("Dec")
#table_ic = table[(table["Name"])[0]=="I"]
print(table[table["Name"]=="IC1525"])
