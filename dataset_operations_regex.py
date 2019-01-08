#To make changes to the dataset to run regex

import re


def regex_replacements(dataset):
    
    dataset_case3=dataset.copy()
    
    def allratingwildcardreplace(model):
        model=re.sub('All Rating','\w+',model,flags=re.IGNORECASE)
        model=re.sub(r'X{2,15}','\w+',model,flags=re.IGNORECASE)
        return model
    dataset_case3['Model']=dataset_case3['Model'].apply(allratingwildcardreplace)
    
    def specialcharactersspacereplace(model):
        model=re.sub('[-!@#$]', ' ',model)
        model=re.sub('blank','',model,flags=re.IGNORECASE)               
        model=re.sub('\[','(',model)
        model=re.sub('\]',')',model)
        model=re.sub(',','|',model)
        model=re.sub(' ','',model)
        model='^'+model+'$'
        return model
    dataset_case3['Model']=dataset_case3['Model'].apply(specialcharactersspacereplace)
        
    return dataset_case3