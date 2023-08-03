#Megan Cuevas, 4/11/23, "JD_conversions.py"

from astropy import time, coordinates as coord, units as u
import numpy as np
from optparse import OptionParser

parser = OptionParser()
(options,args) = parser.parse_args()

data = np.loadtxt(open(args[0]),
                  delimiter=",", skiprows=1)

MJD = data[:,0]

#print('MJD:',MJD)
#print('length of MJD:',len(MJD))

RA = args[1]
DEC = args[2]

def MJD2BJD(MJD,ra,dec,verbose=False):
    target = coord.SkyCoord(ra,dec,unit=(u.deg, u.deg), frame='icrs')
    
    #observatory = coord.EarthLocation.of_site('Palomar')
    observatory = coord.EarthLocation.from_geodetic(243.137,33.356,1706)  #Palomar
    #observatory = coord.EarthLocation.from_geodetic(204.5253,19.8260,4145) #Keck
    #observatory = coord.EarthLocation.from_geodetic(342.118,28.761,2332) #WHT
    #observatory = coord.EarthLocation.from_geodetic(203.7432,20.7082,3052) #Haleakala (OGG)
    #observatory = coord.EarthLocation.from_geodetic(149.0685,-31.2749,1165) #Siding Springs (COJ)

    times = time.Time(MJD+0.0001736111, format='mjd', scale='utc', location=observatory)
    #0.0001736111 is 15 seconds since BJD is a 'mid-time' exposure
    ltt_bary = times.light_travel_time(target)
    time_barycentre = times.tdb + ltt_bary
    
    return time_barycentre.mjd

bjd = MJD2BJD(MJD,RA,DEC,verbose=False)

#goes through the array of MJD times per target, and converts them to BJD
newjd = bjd+2400000.5
#print('newjd:',newjd)
#print('length of newjd:',len(newjd))

newjd = np.reshape(newjd, (data.shape[0],1))   # adjust dimension of the new array
result = np.append(data, newjd, 1)             #add column to data
np.savetxt(args[0], result, delimiter=',', fmt="%s", header = "MJD, R, R_error, BJD")
