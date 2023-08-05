#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 21:31:10 2020

@author: nick
"""
import os, sys, datetime
import configparser
from dateutil import parser as parse_date
import netCDF4
import numpy as np

def export_nc(geom, metadata, alpha, wave, snr_factor, wct_peak_margin, ltool_ver, fname, dir_out):
    
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)
    
    geom_dts = geom.to_dataset('features')
    geom_dts = geom_dts.drop_vars('layers')
    geom_dts = geom_dts.fillna(netCDF4.default_fillvals['f8'])
    
    geom_dts.attrs = metadata
    geom_dts.attrs['processor_name'] = 'ltool'
    geom_dts.attrs['processor_version'] = ltool_ver
    
    time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    args = ' '.join(sys.argv[1:])
    geom_dts.attrs['history'] = f"{geom_dts.attrs['history']}; {time}: ltool {args}" 
    geom_dts.attrs['layer_method'] = 'Wavelet Correlation Transform'
    
    if snr_factor != snr_factor:
        snr_factor = netCDF4.default_fillvals['f8']
    geom_dts['snr_factor'] = snr_factor
    geom_dts.snr_factor.attrs['long_name'] = 'Product to noise ratio limit applied to the WCT normalized by the noise vertically. It is used to discern between noise and actual layers.'
    geom_dts.snr_factor.attrs['units'] = ''
    
    if wct_peak_margin != wct_peak_margin:
        wct_peak_margin = netCDF4.default_fillvals['f8']
    geom_dts['wct_peak_margin'] = wct_peak_margin
    geom_dts.wct_peak_margin.attrs['long_name'] = 'Absolute WCT ratio threshold. It represents the WCT values of a number of subsequent features of the same kind (either solely bases or soleley tops) divided by the maximum absolute WCT value among them. Features with values less than this threshold are rejected. It is used to identify most suitable feature among a number of subsequent candidates.'
    geom_dts.wct_peak_margin.attrs['units'] = ''

    if alpha != alpha:
        alpha = netCDF4.default_fillvals['f8']    
    geom_dts['dilation'] = alpha
    geom_dts.dilation.attrs['long_name'] = 'The dilation value (window) used for the WCT calculations.'
    geom_dts.dilation.attrs['units'] = 'km'

    if wave != wave:
        wave = netCDF4.default_fillvals['f8']      
    geom_dts['wavelength'] = float(wave)
    geom_dts.wavelength.attrs['long_name'] = 'The wavelength of the ELDA product used to obtain the geometrical properties'
    geom_dts.wavelength.attrs['units'] = 'nm'

    geom_dts['residual_layer_flag'] = geom_dts['residual_layer_flag'].astype('int32')
    geom_dts.residual_layer_flag.attrs['values'] = '0 for normal layers, 1 for the residual layer'
    geom_dts.residual_layer_flag.attrs['long_name'] = 'Flag for the first layer.It is 1 when its true base is not identified. In this case, the first range bin is used as the base instead and the layer is marked as a potential candidate for the residual layer'
    geom_dts.residual_layer_flag.attrs['units'] = ''

    geom_dts.base.attrs['long_name'] = 'The layer base (ASL)'
    geom_dts.base.attrs['units'] = 'km'
    
    geom_dts.center_of_mass.attrs['long_name'] = 'The layer center of mass. It is the average altitude weighted by the product values (ASL)'
    geom_dts.center_of_mass.attrs['units'] = 'km'
    
    geom_dts.top.attrs['long_name'] = 'The layer top (ASL)'
    geom_dts.top.attrs['units'] = 'km'
    
    geom_dts.peak.attrs['long_name'] = 'The height of the product maximum within the layer (ASL)'
    geom_dts.peak.attrs['units'] = 'km'
    
    geom_dts.thickness.attrs['long_name'] = 'The layer thickness (top - base)'
    geom_dts.thickness.attrs['units'] = 'km'
    
    geom_dts.base_sig.attrs['long_name'] = 'The product value at the base of the layer'
    geom_dts.base_sig.attrs['units'] = 'm-1 sr-1'
    
    geom_dts.top_sig.attrs['long_name'] = 'The product value at the top of the layer'
    geom_dts.top_sig.attrs['units'] = 'm-1 sr-1'
    
    geom_dts.peak_sig.attrs['long_name'] = 'The product value at the peak of the layer'
    geom_dts.peak_sig.attrs['units'] = 'm-1 sr-1'
    
    geom_dts.depth.attrs['long_name'] = 'Integrated product within the layer'
    geom_dts.depth.attrs['units'] = 'm-1 sr-1'

    geom_dts.sharpness.attrs['long_name'] = 'Minimum absolute difference between the product value at the peak and the product value at the base or top'        
    geom_dts.sharpness.attrs['units'] = 'm-1 sr-1'
    
    geom_dts.trend.attrs['long_name'] = 'Difference between the product value at the top and the product value at the base'        
    geom_dts.trend.attrs['units'] = 'm-1 sr-1'

    geom_dts.weight.attrs['long_name'] = 'Fraction of the integrated product within the layer to the whole columnar integral'
    geom_dts.weight.attrs['units'] = ''
    
    geom_dts.to_netcdf(os.path.join(dir_out,fname))
        
    return(geom_dts)

def nc_name(metadata, prod_id, prod_type_id, wave):

    ms_id = metadata['measurement_ID']
    
    st_id = metadata['station_ID']
    
    ver = metadata['scc_version']
    
    prod_id = prod_id.zfill(7)
    
    prod_type_id = prod_type_id.zfill(3)
    
    wave = wave.zfill(4)
    
    start_t = parse_date.parse(metadata['measurement_start_datetime'])\
        .strftime('%Y%m%d%H%M')
    stop_t = parse_date.parse(metadata['measurement_stop_datetime'])\
        .strftime('%Y%m%d%H%M')
        
    fname = f'{st_id}_{prod_type_id}_{wave}_{prod_id}_{start_t}_{stop_t}_{ms_id}_ltool_v{ver}.nc'

    return(fname)
