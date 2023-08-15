
import PIC_lab_control as PIC
import time
from datetime import datetime 
import pylab as pl
import numpy as np
import os, os.path



chip_no     = 'ST0-Old_run'
struct_no   = '980_paperclip_4'
input_left  = 'power_30_mW_center_980nm_step_1nm'
input_right = ''

set_power   = [30]                        # in mW



center_wavelength = 945 #958.3                # in nm
bandwidth = 70                         # in nm

step0            = 1.0               # in nm
set_to_get_time0 = 0.1                # in sec
num_spectra      = 1


sweep = False
set_power_sweep  = [20,30]
wavelength_sweep = [912, 920, 930, 940, 950, 960, 970, 978]

bandwidth_sweep        = 3
step0_sweep            = 0.02          # in nm



CTL = PIC.TOPTICA_CTL950()

CTL.SetPowerStabilizationStatus(True)
CTL.SetPowerStabilizationParameters(0.3,15,0,1)





    

if sweep == False:
        
    
    start0 = center_wavelength - 0.5*bandwidth 
    stop0 = center_wavelength + 0.5*bandwidth 
    
    Power_meter = PIC.PM100USB(center_wavelength)
    
    Nsteps = round((stop0-start0)/step0)+1
    lambdaIN=[i*step0+start0 for i in range(Nsteps)]
    
    DataAvg = [[[0] for i in range(len(lambdaIN))] for i in range(2)]
    
    
    for power_curr in set_power:
    
        CTL.SetPower(power_curr)
        
        
        now = datetime.now()
        datestring =  now.strftime("%Y-%m-%d_%H-%M-%S")
        file_name  =  datestring +'_MPW850_3-photon_chip_' + str(chip_no) + '_struct_' + str(struct_no)  
        comment    =  'Input left: ' + input_left + '\nInput right: ' + input_right + '\nSet-to-get time: ' + str(set_to_get_time0) + 'sec\nSet power: ' + str(power_curr)
        filenamePREFIX = './'+file_name+'/'+file_name
        
        os.mkdir(file_name)
        
        
            
        for m in range(num_spectra):
        
            SWEEP0 = PIC.Sweep2D(sweepPar=lambdaIN,
                                 SetFunction=CTL.SetWavelength,
                                 GetFunction=[CTL.GetPower, Power_meter.GetPower],
                                  timeFromSetToGet=set_to_get_time0,
                                 setLabels='Wavelength (nm)',
                                 getLabels= ['Output power CTL (mW)', 'Output power Powermeter (W)'])
                
            SWEEP0.Run(plotting=True)
            
            
            DataAvg = np.add(DataAvg, SWEEP0.Data) 
                
            SWEEP0.SaveTxt(dataSelect=0,x1Select=-1,x2Select=-1,filename=filenamePREFIX + '--' +SWEEP0.outTitle[0] + '_' + str(m) + '.txt',additionalText=comment)
            SWEEP0.SaveTxt(dataSelect=1,x1Select=-1,x2Select=-1,filename=filenamePREFIX + '--' +SWEEP0.outTitle[1] + '_' + str(m) + '.txt',additionalText=comment)
            
        
        if num_spectra > 1:
        
            SWEEP0.Data = np.divide(DataAvg, num_spectra) 
            
            SWEEP0.SaveTxt(dataSelect=0,x1Select=-1,x2Select=-1,filename=filenamePREFIX + '--' +SWEEP0.outTitle[0] + '_average.txt',additionalText=comment)
            SWEEP0.SaveTxt(dataSelect=1,x1Select=-1,x2Select=-1,filename=filenamePREFIX + '--' +SWEEP0.outTitle[1] + '_average.txt',additionalText=comment)
    

else:  
    
    
    Power_meter = PIC.PM100USB(wavelength_sweep[1])
    Nsteps = round(bandwidth_sweep/step0_sweep)+1
    
    
    for power_curr in set_power_sweep:
    
        CTL.SetPower(power_curr)
        
        now = datetime.now()
        datestring =  now.strftime("%Y-%m-%d_%H-%M-%S")
        file_name  =  datestring +'_MPW850_3-photon_chip_' + str(chip_no) + '_struct_' + str(struct_no)   
        comment    =  'Input left: ' + input_left + '\nInput right: ' + input_right + '\nSet-to-get time: ' + str(set_to_get_time0) + 'sec\nSet power: ' + str(power_curr)
        filenamePREFIX = './'+file_name+'/'+file_name
        
        os.mkdir(file_name)
        
        for lambda_curr in wavelength_sweep:
        
        
            Power_meter.SetWavelength(lambda_curr)    
            lambdaIN=[i*step0_sweep+lambda_curr-0.5*bandwidth_sweep for i in range(Nsteps)]
            
            SWEEP0x = PIC.Sweep2D(sweepPar=lambdaIN,
                             SetFunction=CTL.SetWavelength,
                             GetFunction=[CTL.GetPower, Power_meter.GetPower],
                              timeFromSetToGet=set_to_get_time0,
                             setLabels='Wavelength (nm)',
                             getLabels= ['Output power CTL (mW)', 'Output power Powermeter (W)'])
            
            SWEEP0x.Run(plotting=True)
             
            SWEEP0x.SaveTxt(dataSelect=0,x1Select=-1,x2Select=-1,filename=filenamePREFIX + '--' +SWEEP0x.outTitle[0] + '_' + str(lambda_curr) + 'nm.txt',additionalText=comment)
            SWEEP0x.SaveTxt(dataSelect=1,x1Select=-1,x2Select=-1,filename=filenamePREFIX + '--' +SWEEP0x.outTitle[1] + '_' + str(lambda_curr) + 'nm.txt',additionalText=comment)
                
            


Power_meter.close()
CTL.close()






