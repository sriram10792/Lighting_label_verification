#To check if the wattage matches the fixture code, only when model numbers matched

def watt_compare(resultsdf,fixture_code):
    global output_text
    results_df=resultsdf
    test_fixture=fixture_code
    
    #Extract the wattage from the result
    dlc_watt=results_df.iloc[0]['Reported Wattage']
    
    #Extract the wattage from the fixture code
    try:    
        fixture_watt=int("".join(filter(str.isdigit,test_fixture)))
    except:
        ValueError
        fixture_watt=None
        #When the fixture code does not have numbers
    
    if fixture_watt==dlc_watt:
        output_text="wattage matched"
        return 1,output_text
    else:
        output_text="wattage does not match"
        return 0,output_text

