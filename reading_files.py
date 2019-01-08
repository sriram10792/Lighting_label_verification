#Read dataset and the e-files

import numpy as np
import pandas as pd
#from pandas import ExcelWriter
#from pandas import ExcelFile

#Read the model number and fixture codes from the efile
def reading_efile(path):
    global modelslist
    global fixtureslist
    
    modelsdf= pd.read_excel(path, 'Step 3 - Lighting Fixtures', parse_cols = "k")
    modelsdf=pd.DataFrame(modelsdf)
    modelsdf.columns=['model']
    modelslist=modelsdf['model'].tolist()
    modelslist=[str(i) for i in modelslist]
	
    
    fixturesdf=pd.read_excel(path, 'Step 3 - Lighting Fixtures', parse_cols = "I")
    fixturesdf=pd.DataFrame(fixturesdf)
    fixturesdf.columns=['fixture']
    fixtures=fixturesdf['fixture'].tolist()
    fixtureslist=list(fixtures)
    del fixtureslist[:2]
    fixtureslist=[str(i) for i in fixtureslist]
    
    return modelslist,fixtureslist
 
#Read the dataset
def read_data(path2,path3):
    global dataset
    
    #Reading DLC dataset
    cols_to_use1=['Product Id','Model No.','Reported Wattage','Reported CCT','Category']
    dataset_dlc=pd.read_csv(path2,usecols=cols_to_use1)[cols_to_use1]
    dataset_dlc=dataset_dlc.rename(columns = {'Model No.':'Model'})
    dataset_dlc['Reported Wattage']=dataset_dlc['Reported Wattage'].fillna(0)
    dataset_dlc['Reported Wattage']=np.ceil(dataset_dlc['Reported Wattage']).astype(int)
    
    #Reading Energystar dataset
    cols_to_use2=['ENERGY STAR Unique ID','Model Number','Total Input Power (Watts)','Appearance/Correlated Color Temperature (K)','Indoor/Outdoor']
    dataset_energystar=pd.read_csv(path3,usecols=cols_to_use2)[cols_to_use2]
    dataset_energystar.columns=['Product Id','Model','Reported Wattage','Reported CCT','Category']
    dataset_energystar['Reported Wattage']=dataset_energystar['Reported Wattage'].fillna(0)
    dataset_energystar['Reported Wattage']=np.ceil(dataset_energystar['Reported Wattage']).astype(int)
    
    #Combine the two datasets
    dataset_list=[dataset_dlc,dataset_energystar]
    dataset=pd.concat(dataset_list)
    
    dataset['Reported CCT'].fillna(0, inplace=True)
    dataset.reset_index(drop=True, inplace=True)
    #dataset.to_csv("combined_dataset.csv",index=True)
    return dataset
