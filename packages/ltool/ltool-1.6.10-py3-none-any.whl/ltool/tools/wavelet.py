# -*- coding: utf-8 -*-
"""
Created on Thu May  5 15:19:16 2016

@author: nick
"""
import numpy as np

def wavelet(sig, sig_err, step, alpha):
    
    ihalf = int(alpha/(2.*step))
    wsig = np.nan*np.zeros(len(sig))
    wsig_err = np.nan*np.zeros(len(sig))
    
    for i in range(ihalf+1,len(sig)-ihalf-1):
        int_d = np.trapz(sig[(i-ihalf):i],dx=step)
        int_u = np.trapz(sig[i+1:(i+ihalf)+1],dx=step)
        
        if (int_u == int_u) and (int_d == int_d):
            wsig[i]=(int_u - int_d)/alpha
            N = np.floor(alpha/step)
            sum2 = np.sum(np.power(sig_err[(i-ihalf+1):i],2)) +\
                np.sum(np.power(sig_err[i+1:(i+ihalf)],2))
            err2_d = np.power(sig_err[(i-ihalf)],2)
            err2_u = np.power(sig_err[(i+ihalf)+1],2)
            err2_md = np.power(sig_err[i-1],2)
            err2_mu = np.power(sig_err[i+1],2)
            wsig_err[i] = (1./N)*np.sqrt(sum2 + \
                            (err2_mu + err2_md + err2_d + err2_u)/4.)
      
    return(wsig, wsig_err)
