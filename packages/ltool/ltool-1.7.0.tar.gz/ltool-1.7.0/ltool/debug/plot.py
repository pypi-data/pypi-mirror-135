#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 20:20:15 2021

@author: nick
"""

from matplotlib import pyplot as plt
import os
import pandas as pd
import numpy as np

def debug_layers(date, i_d, alt, sig, wct, sig_err, wct_err, geom, max_alt, 
                 snr_factor, dir_out, dpi_val):
    
    alt = np.round(alt, decimals=2)
    
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)
    
    ulim_y = 0.5*pd.Series([400., 200., 100., 20., 10., 5., 400., 400., 200., 100., 100., 20., 20., 10., 7., 7.], 
                       index = ['e355', 'e532', 'e1064', 'b355', 'b532', 'b1064', 
                                'e313', 'e351', 'e510', 'e694', 'e817', 'b313', 
                                'b351', 'b510', 'b694', 'b817'])
    
    if len(geom) > 0:
        bases = geom.sel(features = 'base').values
        tops = geom.sel(features = 'top').values
        coms = geom.sel(features = 'center_of_mass').values
    
    # Plots
    plt.figure
    plt.title(f'Product ID {i_d}')
    plt.subplot(122)
    xlims = [-0.05*ulim_y.loc[i_d], ulim_y.loc[i_d]]
    ylims = [0, max_alt]
    plt.title(f'Product ID {i_d}')
    if len(geom) > 0:
        for i in range(geom.shape[0]):
            if geom.sel(features='residual_layer_flag').values[i] == 1:
                clrs = ['gray', 'black', 'grey']
            if geom.sel(features='residual_layer_flag').values[i] == 0:
                clrs = ['purple', 'cyan', 'purple']
            plt.plot(xlims, [bases[i], bases[i]], color = clrs[0])
            plt.plot(xlims, [tops[i], tops[i]], color =  clrs[1])
            plt.plot(xlims, [coms[i], coms[i]], '--', color = 'goldenrod')
            plt.axhspan(bases[i], tops[i], facecolor = clrs[2], alpha = 0.2)
    plt.plot(sig, alt, color = 'tab:blue')
    plt.fill_betweenx(alt, sig - sig_err, 
                      sig + sig_err,
                      alpha = 0.3, color = 'tab:blue')
    plt.plot([0,0], ylims, '--', color = 'tab:brown')

    plt.axis(xlims + ylims)
    plt.xlabel('Aerosol Back. Coef. [$Mm^{-1} \cdot sr^{-1}$]')
    plt.ylabel('Altitude [m]')

    plt.subplot(121)
    xlims = [-0.02*ulim_y.loc[i_d], 0.02*ulim_y.loc[i_d]]
    ylims = [0, max_alt]
    if len(geom) > 0:
        for i in range(geom.shape[0]):
            if geom.sel(features='residual_layer_flag').values[i] == 1:
                clrs = ['gray', 'black', 'grey']
            if geom.sel(features='residual_layer_flag').values[i] == 0:
                clrs = ['purple', 'cyan', 'purple']
            plt.plot(xlims, [bases[i], bases[i]], color = clrs[0])
            plt.plot(xlims, [tops[i], tops[i]], color =  clrs[1])
            plt.plot(xlims, [coms[i], coms[i]], '--', color = 'goldenrod')
            plt.axhspan(bases[i], tops[i], facecolor = clrs[2], alpha = 0.2)
    plt.plot( wct, alt)
    plt.plot( snr_factor*wct_err, alt, '--', color = 'darkgreen')
    plt.plot(-snr_factor*wct_err, alt, '--', color = 'lightgreen')
    plt.axis(xlims + ylims)
    plt.xlabel('Wavelet Cov. Transform [$Mm^{-1} sr^{-1}$]')
    plt.ylabel('Altitude [m]')
    
    ts = pd.to_datetime(str(date)) 
    date_s = ts.strftime("%Y%m%d_%H%M%S")
    
    plt.tight_layout()
    plt.savefig(os.path.join(dir_out,f'{date_s}_{i_d}.png'),
                dpi = dpi_val)
    plt.close()
    
    return()
