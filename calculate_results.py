#To return results for the e-file based on wattage and model number


def calculate_output(result_list,models,watt_status):
    all_results=result_list
    models_count=models
    watt_pass=watt_status
        
    #To remove Null elements from the list for models not found            
    length_all_results=len(all_results)
    edited_list=[]

    for a in range(length_all_results):
        if all_results[a] is not None:
            edited_list.append(all_results[a])
                
        #To create list where only one exact matches exist
        final_list=[]
        length_edited_list=len(edited_list)
        for l in range(length_edited_list):
            if len(edited_list[l])==1:
                final_list.append(edited_list[l])
                
   #To check whether all 3-file model numbers matched
    length_final_list=len(final_list)
    
    if length_final_list==models_count and watt_pass==1:
        #print("e-file OK")
        return 1
        
    elif length_final_list==models_count and watt_pass==0:
        #print("All models match, but wattage does not")
        return 2
    elif length_final_list!=models_count:
        #print("Check e-file, not all models were verified")
        return 0
