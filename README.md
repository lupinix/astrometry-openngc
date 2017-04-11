# astrometry-openngc
OpenNGC catalogue for astrometry.net

This repository contains scripts to create FITS tables etc. to use the OpenNGC catalogue [1] with astrometry.net [2]

Licensing:
  * License for the code is 3-clause BSD, same license as used by astrometry.net, check file LICENSE
  * License for the data is CC-BY-SA-4.0 as for the OpenNGC catalog itself, check file LICENSE-OpenNGC

Content:
  * create_ngc_fits_table.py – script to generate FITS tables from NGC.csv
  * openngc_ic.fits – replacement for ic2000.fits in astrometry
  * openngc_ngc.fits – replacement for ngc2000.fits in astrometry

Requirements:
  * astropy is required to run the Python scripts, we use it for table and FITS handling

[1] https://github.com/mattiaverga/OpenNGC

[2] https://github.com/dstndstn/astrometry.net
