#To check for model match after accounting for special characters and spaces

import re

def specialcharcheck(data,model_number):
    global matches_case2
    global test_model
    dataset_2=data.copy()
    test_model=str(model_number)
    #print(test_model)
    dataset_2['Model']=dataset_2['Model'].str.replace('\W', '')

    #Remove all spaces from new dataset
    dataset_2['Model']=dataset_2['Model'].str.replace(' ', '')
    
    #Remove all special characters and spaces from the search model number
    test_model=re.sub('[^a-zA-Z0-9 \n\.]', '', test_model)
    #test_model=test_model.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
    test_model= re.sub(r'\s+', '',test_model)
    
    matches_case2=dataset_2[dataset_2['Model'].str.match(test_model,case=False)]
    #results_case2=len(matches_case2)
    
    return test_model,matches_case2
        
    
