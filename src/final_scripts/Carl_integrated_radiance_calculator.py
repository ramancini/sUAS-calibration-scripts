#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 10:44:29 2025

@author: danny
"""

import math
import numpy
import scipy.interpolate
import numpy as np

def load_first_column_csv(file_path, header_rows=1):
    # Read just the first column, skipping headers
    data = np.genfromtxt(file_path, delimiter=',', skip_header=header_rows, 
                         usecols=(0), dtype='U', encoding=None)
    return data

target_label = load_first_column_csv('/Users/danny/Desktop/School/Spyder/Carl_UAS/No_Emissivity_RSR/Labels_120.csv')
# target_label = load_first_column_csv('/Users/danny/Desktop/School/Spyder/Carl_UAS/No_Emissivity_RSR/target_labels_240.csv')


def read_2_column_csv_to_numpy(file_path, header_rows=1):
   # Load data, skipping the header row(s)
   data = numpy.loadtxt(file_path, delimiter=',', skiprows=header_rows)

   # Split into two separate arrays
   column1 = data[:, 0]
   column2 = data[:, 1]
    
   return column1, column2

def read_1_column_csv_to_numpy(file_path, header_rows=1):
    """Read 1-column CSV file into numpy array."""
    data = numpy.loadtxt(file_path, delimiter=',', skiprows=header_rows)
    
    return data.flatten()  # Ensure 1D array

def interp1(x, y, xp, order=1, extrapolate=False):
   """
   title::
      interp1

   description::
      This method will compute linear interpolants (and extrapolants if
      desired) for a provided set of locations.  This method wraps the 
      scipy.interpolate.splrep and scipy.interpolate.splev B-spline
      interpolation routines into a more compact (but more limited) 
      calling syntax.

   attributes::
      x, y
         Array-like objects defining the sampled function y = f(x)
      xp
         A scalar or an array-like object defining the locations to
         interpolate/extrapolate at
      order
         The order of the B-splines to use to fit the original function
         [default is 1 (linear interpolation/extrapolation)]
      extrapolate
         A boolean indicating whether extrapolation should be carried 
         out, if not desired, NaN will be returned corresponding to the
         locations that fall outside the original data range along the 
         horizontal axis [default is False]

   returns::
      A scalar or array-like object (matching the object type for y)
      containing the interpolant(s)/extrapolant(s)

   author::
      Carl Salvaggio

   copyright::
      Copyright (C) 2015, Rochester Institute of Technology

   license::
      GPL

   version::
      1.0.0

   disclaimer::
      This source code is provided "as is" and without warranties as to 
      performance or merchantability. The author and/or distributors of 
      this source code may have made statements about this source code. 
      Any such statements do not constitute warranties and shall not be 
      relied on by the user in deciding whether to use this source code.
      
      This source code is provided without any express or implied warranties 
      whatsoever. Because of the diversity of conditions and hardware under 
      which this source code may be used, no warranty of fitness for a 
      particular purpose is offered. The user is advised to test the source 
      code thoroughly before relying on it. The user must assume the entire 
      risk of using the source code.
   """

   # Make sure that the provided data set consists of numpy ndarrays, if
   # not, convert them for use within the scope of this method
   if type(x).__module__ != numpy.__name__:
      xN = numpy.asarray(x, dtype=float)
   else:
      xN = x

   if type(y).__module__ != numpy.__name__:
      yN = numpy.asarray(y, dtype=float)
   else:
      yN = y

   # Make sure the elements of the provided data set are the same length
   if xN.size != yN.size:
      raise ValueError('Provided datasets must have the same size')

   # Compute the vector of knots and the B-spline coefficients for the
   tck = scipy.interpolate.splrep(xN, yN, k=order, s=0)

   # Given the knots and B-spline coefficients, evaluate the ordinate 
   # value(s) of the spline at the provided abscissa location(s)
   yp = scipy.interpolate.splev(xp, tck)

   # If extrapolation is not desired, return NaN for abscissa value(s)
   # outside the range of the original data provided
   if extrapolate is False:
      index = numpy.where(xp < xN[0])
      if len(index[0]) > 0:
         yp[index[0]] = float('NaN')

      index = numpy.where(xp > xN[-1])
      if len(index[0]) > 0:
         yp[index[0]] = float('NaN')

   # Return the interpolated/extrapolated ordinate value(s) using the same
   # array-like structure as the provided data
   if type(y).__module__ != numpy.__name__:
      return yp.tolist()
   else:
      return yp

def spectral_radiance(absolute_temperature, wavelengths):
   c1 = 3.74151e08   # [W / m^2 / micron]
   c2 = 1.43879e04   # [micron K]
   radiances = []
   for wavelength in wavelengths:
      radiance = c1 / wavelength**5 / \
            (math.exp(c2 / wavelength / absolute_temperature) - 1) / math.pi
      radiances.append(radiance)
   return numpy.array(radiances)

def integrate(x, y):
   area = 0
   for idx in range(x.size - 1):
      dx = x[idx+1] - x[idx]
      area += y[idx] * dx
   return area




import argparse
import matplotlib.pyplot
import sys

description = 'Compute integrated radiance for the product of a blackbody '
description += 'at a specified temperature, a target emissivity, and a sensor '
description += 'relative spectral response -OR- the blackbody temperature '
description += 'given an integrated radiance'
parser = argparse.ArgumentParser(description=description)

help_message = 'target emissivity filename'
parser.add_argument('emissivity_file_path', 
                    help=help_message)

help_message = 'sensor relative spectral response filename'
parser.add_argument('rsr_file_path', 
                    help=help_message)

help_message = 'target absolute temperature [K]'
parser.add_argument('-t', '--absolute_temperature',
                    dest='absolute_temperature',
                    type=float,
                    default=None,
                    help=help_message)

help_message = 'target intergated radiance [W/m^2/sr]'
parser.add_argument('-r', '--integrated_radiance',
                    dest='integrated_radiance',
                    type=float,
                    default=None,
                    help=help_message)

help_message = 'csv file or radiance values to be searched through'
help_message += '[default is False]'
parser.add_argument('-rl', '--radiance_list',
                    dest='radiance_list',
                    type=str,
                    help=help_message)

help_message = 'display plot of spectral radiance that was integrated '
help_message += '[default is False]'
parser.add_argument('-p', '--display_plot',
                    dest='display_plot',
                    action='store_true',
                    help=help_message)

help_message = 'label for filing svaing'
help_message += '[default is False]'
parser.add_argument('-l', '--label',
                    dest='label',
                    type = str,
                    default='results',
                    help=help_message)

args = parser.parse_args()
emissivity_file_path = args.emissivity_file_path
rsr_file_path = args.rsr_file_path
absolute_temperature = args.absolute_temperature
integrated_radiance = args.integrated_radiance
display_plot = args.display_plot
radiance_list = args.radiance_list
label = args.label

# if absolute_temperature and integrated_radiance:
#    msg = '\n'
#    msg += 'EXITING: '
#    msg += 'Specify either absolute temperature or integrated radiance, '
#    msg += 'not both'
#    msg += '\n'
#    print(msg)
#    sys.exit()

# if absolute_temperature is None and integrated_radiance is None:
#    msg = '\n'
#    msg += 'EXITING: '
#    msg += 'Either absolute temperature or integrated radiance must '
#    msg += 'be specified'
#    msg += '\n'
#    print(msg)
#    sys.exit()

rsr_wavelengths, rsr_data = read_2_column_csv_to_numpy(rsr_file_path)

emissivity_wavelengths, emissivity = \
      read_2_column_csv_to_numpy(emissivity_file_path)

rsr = interp1(rsr_wavelengths, rsr_data, emissivity_wavelengths)
rsr = numpy.nan_to_num(rsr, nan=0)
rsr = rsr / numpy.max(rsr)

wavelengths = emissivity_wavelengths

if absolute_temperature:
   spectral_bb_radiance = spectral_radiance(absolute_temperature, wavelengths)
   sensed_spectral_radiance = spectral_bb_radiance * emissivity # * rsr
   integrated_radiance = integrate(wavelengths, sensed_spectral_radiance, )

   msg = 'Integrated radiance [W/m^2/sr] = {0}'.format(integrated_radiance)
   print(msg)

   if display_plot:
      matplotlib.pyplot.plot(wavelengths,
                             sensed_spectral_radiance,
                             linestyle='-')
      matplotlib.pyplot.title(msg)
      matplotlib.pyplot.xlabel('Wavelength [microns]')
      matplotlib.pyplot.ylabel('Radiance [W/m^2/sr/micron]')
      matplotlib.pyplot.xlim([3, 20])
      matplotlib.pyplot.show()

   sys.exit()


if radiance_list:
    radiance_csv = read_1_column_csv_to_numpy(radiance_list)
    # target_label, radiance_csv = read_2_column_csv_to_numpy(radiance_list)

    temperature_list = []

    
    for radiance in radiance_csv:
        search_integrated_radiance = 0
        search_temperature = 250
        number_of_decimal_places = 1
        
        integrated_rsr = integrate(wavelengths, rsr)
        
        
        while search_integrated_radiance < radiance:
            
            search_temperature += 10**(-number_of_decimal_places)
            search_spectral_bb_radiance = \
                spectral_radiance(search_temperature, wavelengths) 
                
            search_sensed_spectral_radiance = \
                search_spectral_bb_radiance * emissivity * rsr
                
            search_integrated_radiance = \
                integrate(wavelengths, search_sensed_spectral_radiance)
                
            search_integrated_radiance = \
                search_integrated_radiance / integrated_rsr

        msg = 'Derived temperature [K] = {0:.{1}f}'.format(search_temperature,
                                                          number_of_decimal_places)
        temperature_list.append(search_temperature)
        print(msg)
        
    # Create array from radiance_csv and temperature_list
    final_csv = np.column_stack((radiance_csv, temperature_list))
    
    np.savetxt("/Users/danny/Desktop/School/Spyder/Carl_UAS/No_Emissivity_RSR/target_csv.csv", 
               final_csv, 
               delimiter=',', 
               header='Radiance [W/(m² sr)],Temperature [K]', 
               fmt=['%.6f', '%.2f'],
               comments='')

if integrated_radiance:
   search_integrated_radiance = 0
   search_temperature = 250
   number_of_decimal_places = 1
   
   integrated_rsr = integrate(wavelengths, rsr)

   while search_integrated_radiance < integrated_radiance:
      search_temperature += 10**(-number_of_decimal_places)
      search_spectral_bb_radiance = \
            spectral_radiance(search_temperature, wavelengths)
      search_sensed_spectral_radiance = \
            search_spectral_bb_radiance * emissivity * rsr
      search_integrated_radiance = \
            integrate(wavelengths, search_sensed_spectral_radiance)
      search_integrated_radiance = \
          search_integrated_radiance / integrated_rsr

   msg = 'Derived temperature [K] = {0:.{1}f}'.format(search_temperature,
                                                      number_of_decimal_places)
   print(msg)

   if display_plot:
      matplotlib.pyplot.plot(wavelengths,
                             search_sensed_spectral_radiance,
                             linestyle='-')
      matplotlib.pyplot.title(msg)
      matplotlib.pyplot.xlabel('Wavelength [microns]')
      matplotlib.pyplot.ylabel('Radiance [W/m^2/sr/micron]')
      matplotlib.pyplot.xlim([3, 20])
      matplotlib.pyplot.show()

   sys.exit()
   
   
   