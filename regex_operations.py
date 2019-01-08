#To check for model match after performing few regex operations

import re

def reg_compare(data,model_number):
    global rows_found
    global results_df
    global a
    
    dataset=data
    test_model=model_number
    dataset_3=dataset.copy()
    
    row_count=len(dataset_3)
    rows_found=[]
        
    for row in range (row_count):
        dataset_model = dataset_3["Model"][row]
        dataset_model=str(dataset_model)
                       
        #To remove | if they are at the end, or beginning which will match anything
        if (dataset_model[-1]=='|') or (dataset_model[0]=='|'):
            dataset_model=dataset_model.rstrip('|')
            dataset_model=dataset_model.lstrip('|')
            
        #To remove | that does not lie inside parentheses
        dataset_model = re.sub(r'\|(?![^(]*\))','', dataset_model)
                    
        #Check if all parentheses are balanced
        left_parts=dataset_model.split('(')
        left_parts = list(filter(None, left_parts))
        left_parts_count = len(left_parts)
        right_parts=dataset_model.split(')')
        right_parts=list(filter(None, right_parts))
        right_parts_count = len(right_parts)
        dataset_diff = abs(left_parts_count - right_parts_count)
                           
        #Proceed only if dataset_diff is 0, indicating all parentheses match
        if dataset_diff == 0:
            try:
                search=re.search(dataset_model,test_model,re.IGNORECASE)
                if search is not None:
                    row_number=row
                    rows_found.append(row)
                                               
            except:
                pass
            #Not returning exceptions because errors occur when model is not found in a certain row in dataset
                                
    total_count=len(rows_found)
        
    if total_count ==0:
        return None
                                     
    if total_count>1:
        results_df=dataset_3.iloc[rows_found]
        return results_df
        
    if total_count==1:
        results_df=dataset_3.iloc[rows_found]
        return results_df
