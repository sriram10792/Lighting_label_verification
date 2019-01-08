#To execute lighting Label verification and return results as JSON from the function


def lighting_verification(path):
    import pandas as pd
    import numpy as np
    import json

    #Import user defined funcitons
    import reading_files
    import dataset_operations_regex
    import regex_operations
    import specialcharacters
    import calculate_results
    import wattage_check    
    
   #To accept files from the user
    #from argparse import ArgumentParser
    #parser = ArgumentParser()
    #parser.add_argument("file", help='enter file name')
    #args = parser.parse_args()
    #file_path = args.file

    #DLC and Energystar Datasets and combine them into a single dataset
    dataset1_path='https://s3.us-east-2.amazonaws.com/anb-lighting-label-verification/dlc_dataset.csv'
    dataset2_path='https://s3.us-east-2.amazonaws.com/anb-lighting-label-verification/energystar.csv'
    dataset=reading_files.read_data(dataset1_path,dataset2_path)
    
    
    #Pass file path as argument
    file_path=str(path)
    #To extract model numbers from the e-file
    modelslist,fixtureslist=reading_files.reading_efile(file_path)
    
    modelslist=[str(x) for x in modelslist]
    models=len(modelslist)
    
    #Store all results (dataframe results) for each model number in the e-file
    all_results=[]
    #To store the result status  - for model number - of each model
    results_list=[]
    #To store wattage result status of each model
    wattage_results=[]
    #To store wattage check
    wattage_status=[]
    #To modify the dataset to fit regular expression operations if needed    
    dataset_regex=dataset_operations_regex.regex_replacements(dataset)
   
    for i in range(models):
        test_model=modelslist[i]
        test_fixture=fixtureslist[i]
        #print('\n\n Test model',test_model)

        matches_1=dataset[dataset['Model'].str.match(test_model,case=False)]
        results_case1=len(matches_1)
        
        if results_case1==1:
            #print("One exact model matched for model",i+1,"\n\n")
            #print(matches_1)
            results_df=matches_1
            all_results.append(results_df)
            # To store the output of each model and its corresponding result
            outcome='one match found'
            results_list.append(outcome)
            
            #To check the wattage match for that model
            watt_check,watt_outcome=wattage_check.watt_compare(results_df,test_fixture)
            wattage_status.append(watt_check)
            wattage_results.append(watt_outcome)
        
        #If one exact match, display results. If more than one match, display a message
        #If no match found, clean the data and check for one exact match
        
        elif results_case1>1:
            #print("Many direct matches found",results_case1, ".Enter a full model number for model ",i+1,"\n\n")
            results_df=matches_1
            all_results.append(results_df)
        
            #To print the model match results
            outcome='many matches found'
            results_list.append(outcome)
            #To print the wattage results
            watt_check=0
            wattage_status.append(watt_check)
            watt_outcome="model match not complete"
            wattage_results.append(watt_outcome)
        
        elif results_case1==0:
            test_model,matches_2=specialcharacters.specialcharcheck(dataset,test_model)
            results_case2=len(matches_2)
            
            if results_case2==1:
                #print('One exact model match found after fixing punctuations for model',i+1,"\n\n")
                #print(matches_2)
                results_df=matches_2
                all_results.append(results_df)
            
                #To print model match results
                outcome='one match found'
                results_list.append(outcome)
                #To check the wattage match for that model
                watt_check,watt_outcome=wattage_check.watt_compare(results_df,test_fixture)
                wattage_status.append(watt_check)
                wattage_results.append(watt_outcome)
                
                
            elif results_case2>1:
                #print("Many matches found,",results_case2,",after fixing punctuations and spaces, please enter a full model number for model ",i+1,"\n \n")
                results_df=matches_2
                all_results.append(results_df)
            
                #To print model match results
                outcome='many matches found'
                results_list.append(outcome)
                #To print the wattage results
                watt_check=0
                wattage_status.append(watt_check)
                watt_outcome="model match not complete"
                wattage_results.append(watt_outcome)
            
            
            elif results_case2==0:
                results_reg=regex_operations.reg_compare(dataset_regex,test_model)
                results_df=results_reg
                all_results.append(results_df)
                if results_df is None:
                    #To print model match results and wattage results
                    outcome='no match found'
                    watt_check=0
                    watt_outcome="model not matched"
                elif len(results_df)>1:
                    #To print model match results and wattage results
                    outcome='many matches found'
                    watt_check=0
                    watt_outcome="model match not complete"
                
                elif len(results_df)==1:
                    #To print model match results and wattage results
                    outcome='one match found'
                    #To check the wattage match for that model
                    watt_check,watt_outcome=wattage_check.watt_compare(results_df,test_fixture)
            
                results_list.append(outcome)
                wattage_status.append(watt_check)
                wattage_results.append(watt_outcome)   

    
    #To create the results dataframe
    result_dataframe=pd.DataFrame(np.column_stack([modelslist,results_list,wattage_results]),columns=['model','dlc_result','wattage_output'])
    result_json=result_dataframe.to_json(orient='records')
    #result_json=result_json.replace("\\","")
    

    #To check if all wattage are matched. If all wattage matched, all elements in wattage_status will be 1
    if all(i==1 for i in wattage_status):
        watt_pass=1
    else:
            watt_pass=0
    
    #To print results
    overall_status=calculate_results.calculate_output(all_results,models,watt_pass)

    #Print results only if all model numbers does not match
    if overall_status==1:
        final_output={'body': 'e-file OK', 'status':True,'errors': result_json}
        #final_output=json.dumps(final_output)
        #final_output = json.loads(final_output)
        #final_output=final_output.replace("\\","")
        return final_output
    
    if overall_status==0:
        final_output={'body': 'Not all models are verified', 'status':False,'errors': result_json}
        #final_output=json.dumps(final_output)
        #final_output=final_output.replace("\\","")
        return final_output
        
    if overall_status==2:
        final_output={'body': 'All models verified, but wattage does not match', 'status':False,'errors': result_json}
        #final_output=json.dumps(final_output)
        #final_output=final_output.replace("\\","")
        return final_output
 
