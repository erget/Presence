import netCDF4 as cdf
import numpy as np
import os
import re

"""
folder paths should end with a forward slash
src: root path of product
dst: destination of product
bounds: bounds of the subset given as [latmin, latmax, longmin, longmax]
"""
def subSetFolder(src, dst, bounds):

  FILE_COORDS = "geo_coordinates.nc"
  
  #map the bounds in lat/long onto indexes
  geoFile = cdf.Dataset(src+FILE_COORDS)
  
  lats = geoFile.variables['latitude'][:]
  longs = geoFile.variables['longitude'][:]
  
  mask = np.logical_and(np.logical_and(lats >= bounds[0], lats <= bounds[1]), np.logical_and(longs >= bounds[2], longs <= bounds[3]))
    
  #subset all files in folder
  for subdir, dirs, files in os.walk(src):
    for f in files:
      if re.match('[a-zA-Z0-9]{3}[0-9]_[a-z0-9]*\.nc', f) or re.match('geo_coordinates.nc', f):
	print(f)
	subSetCDF(src+f, dst+f, mask)
  

"""
creates a subset of the provided netCDF4 file,
that only contains the values with indexes inside the given bounds. 
bounds: dictionary specifiying the bounds for each dimensions
  key: dimension dimName
  value: array [latmin, latmax, longmin, longmax] bound
"""
def subSetCDF(src, dst, mask):
    
  orig = cdf.Dataset(src);
  copy = cdf.Dataset(dst, "w");
  
  for attr in orig.ncattrs():
    copy.setncattr(attr, orig.getncattr(attr))
    
  copyVars = {}
  
  for var in orig.variables:
    copyVars[var] = np.extract(mask[:], orig.variables[var][:])
  
  for var in copyVars:
    
    copy.createDimension('dim'+var, copyVars[var].size)
    
    v = copy.createVariable(var, orig.variables[var].datatype, 'dim'+var)
    
    for attr in orig.variables[var].ncattrs():
      v.setncattr(attr, orig.variables[var].getncattr(attr))
    
    v[:] = copyVars[var][:]
  
def testSubSetCDF():
  
  latmin = 39.0
  latmax = 43.0
  longmin = -21.0
  longmax = -19.0
  
  src = "/home/wegner/Documents/testData/testIn/"
  dst = "/home/wegner/Documents/testData/testOut/"
  
  subSetFolder(src, dst, [latmin, latmax, longmin, longmax])
  
testSubSetCDF()
