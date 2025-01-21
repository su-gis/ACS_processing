import sys, getopt
#import csv
import datetime
from datetime import datetime
import pandas as pd
from pytz import timezone
import pytz
import json
import math

# Enter  your desidred no data value in your output
NO_DATA_VALUE = -9999


def main(inputFile, codebook, ouputDir):
    
    df_input = pd.read_csv(inputFile)
    df_codebook = pd.read_excel(codebook)
    #print(df_input)
    #print(df_codebook)
    
    outputFile = inputFile.split('/')[-1]        # get a file name from the inputFile full path
    p = outputFile.rfind('.')                    # get start position of the file surfix
    if (p > 1): outputFile = outputFile[:p]      # delete the file surfix
    
    CBGIDs = []
    for i in range(len(df_input)):
        #geoid = "{:02d}{:05d}".format(df_input.loc[i, 'state'], df_input.loc[i, 'zipcode'])    
        geoid = "{:02d}{:03d}{:06d}{:01d}".format(df_input.loc[i, 'state'], df_input.loc[i, 'county'], df_input.loc[i, 'tract'], df_input.loc[i, 'block group'])
        #if (len(geoid) != 7):        
        if (len(geoid) != 12): 
            print("Invalid length of CBGid in {}    line-no: {} [{}]  {} bytes ".format(inputFile, i, geoid, len(geoid)))
        CBGIDs.append(geoid)
    df_byCBG = df_input.copy(deep=True)
    df_byCBG.insert(loc=0, column='geoid', value=CBGIDs)
    #print(df_byCBG)
    create_output(df_byCBG, df_codebook, ouputDir+"/"+outputFile+"_byCBG")
    '''
    # create summary of df_input by county
    dataSP = 3                                   # Data Start Position in the columns of df_input
    summaryDict = {}                             # key: countyID, value: summary of df_input (array)
    summaryHeader = ["geoid", "nCBGs", "dummy"] + list(df_input.columns)[dataSP:]
    #print(summaryHeader)
    for i in range(len(df_input)):
        #if (i > 21): break
        geoid = "{:02d}{:03d}".format(df_input.loc[i, 'state'], df_input.loc[i, 'county'])
        if (len(geoid) != 5): 
            print("Invalid length of countyid in {}    line-no: {} [{}]  {} bytes ".format(inputFile, i, geoid, len(geoid)))
        if (geoid in summaryDict):
            values = summaryDict[geoid]
            values[1] += 1
            for j in range(dataSP, len(list(df_input.columns))):
                if (math.isnan(df_input.iat[i, j]) or df_input.iat[i, j] == -666666666): 
                    continue
                if (values[j] == -666666666): values[j] = df_input.iat[i, j]
                else:                         values[j] += df_input.iat[i, j]
            summaryDict[geoid] = values
        else:
            values = [geoid, 1, ""] + [-666666666]*(len(list(df_input.columns))-dataSP)
            for j in range(dataSP, len(list(df_input.columns))):
                if (math.isnan(df_input.iat[i, j]) or df_input.iat[i, j] == -666666666): 
                    continue
                values[j] = df_input.iat[i, j]
            summaryDict[geoid] = values
    #print(summaryDict)
    summaryList = list(summaryDict.values())
    summaryList = sorted(summaryList, key=lambda k: k[0])
    #print(summaryList)
    df_byCounty = pd.DataFrame(columns=summaryHeader, data=summaryList)
    #print(df_byCounty)
    create_output(df_byCounty, df_codebook, ouputDir+"/"+outputFile+"_byCounty")
    '''
    return

 
def create_output(df_input, df_codebook, outputFile):
    
    header_summarized = ["GEOID"]
    header_normalized = ["GEOID"]
    for j in range(len(df_codebook)):
        if (df_codebook.loc[j, 'use'] != 1): continue
        if isinstance(df_codebook.loc[j, 'CODE'], float): continue
        header_summarized.append(df_codebook.loc[j, 'Short_name'])
        header_normalized.append(df_codebook.loc[j, 'Name_normalized'])
    #print(len(header_summarized), header_summarized)
    #print(len(header_normalized), header_normalized)
    
    list_summarized = []
    list_normalized = []
    for i in range(len(df_input)):
        #if (i > 0): break
        geoid = df_input.loc[i, 'geoid']
        aSeries = df_input.loc[i]
        #print(type(aSeries), aSeries)
        #print(type(aSeries), aSeries.values.tolist())
        
        record_summarized = [geoid]
        record_normalized = [geoid]
        for j in range(len(df_codebook)):
            if (df_codebook.loc[j, 'use'] != 1): continue
            if isinstance(df_codebook.loc[j, 'CODE'], float): continue
            codes = df_codebook.loc[j, 'CODE'].split(",")
            #print(j, codes, df_codebook.loc[j, 'denominator'], type(df_codebook.loc[j, 'denominator']))
            value = 0
            isNaN = True
            for k in range(len(codes)):
                code = codes[k].strip()
                if code not in aSeries.index:
                    print(f"Warning: '{code}' not found in input data. Skipping...")
                    continue
                if math.isnan(aSeries.at[code]) or aSeries.at[code] == -666666666:
                #if (math.isnan(aSeries.at[code]) or aSeries.at[code] == -666666666): 
                    #print(i, j, k, code, aSeries.at[code], df_codebook.loc[j, 'Original_Name'])
                    continue
                value += aSeries.at[code]
                isNaN = False
            if (isNaN): value = NO_DATA_VALUE 
            #print(j, value, codes)
            record_summarized.append(value)
            
            isNaN = True
            denominator = df_codebook.loc[j, 'denominator']
            #if (isinstance(denominator, str) and denominator not in aSeries):
            #    print(j, codes, denominator, "not in " + inputFile)
            if (isinstance(denominator, str) and denominator in aSeries and 
                aSeries.at[denominator] != 0 and aSeries.at[denominator] != -666666666 ):
                if (value is NO_DATA_VALUE): value = NO_DATA_VALUE
                else:
                    #print(j, codes, value, aSeries.at[denominator])
                    isNaN = False
                    value = value / aSeries.at[denominator]*100
            if (isNaN): value = value            
            record_normalized.append(value)
            
        #print(i, record_summarized)
        list_summarized.append(record_summarized)
        list_normalized.append(record_normalized)
    #print(list_summarized)
    df_summarized = pd.DataFrame(columns=header_summarized, data=list_summarized)
    df_normalized = pd.DataFrame(columns=header_normalized, data=list_normalized)
    #print(df_summarized)
    #print(df_normalized)
    
    df_summarized.to_csv(outputFile+"_summarized.csv", index=False)
    print("outputFile  file is {}".format(outputFile+"_summarized.csv"))
    df_normalized.to_csv(outputFile+"_normalized.csv", index=False)
    print("outputFile  file is {}".format(outputFile+"_normalized.csv"))
    
    return

 
def getParameter(argv):
    inputFile = ''
    codebook = ''
    ouputDir = ''
    
    try:
        opts, args = getopt.getopt(argv, "hi:c:o:", ["inputFile=", "codebook=", "ouputDir="])
    except getopt.GetoptError:
        print("ACS_selection.py -i <inputFile> -c <codebook> -o <ouputDir>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("ACS_selection.py -i <inputFile> -c <codebook> -o <ouputDir>")
            sys.exit()
        elif opt in ("-i", "--inputFile"):
            inputFile = arg
        elif opt in ("-c", "--codebook"):
            codebook = arg
        elif opt in ("-o", "--ouputDir"):
            ouputDir = arg
    
    print("inputFile   file is {}".format(inputFile))
    print("codebook    file is {}".format(codebook))
    print("output directory is {}".format(ouputDir))
    
    return [inputFile, codebook, ouputDir]


if __name__ == '__main__':
# python ACS_selection_blockgroup.py -i data/ACS_2023_5year__cbg_CA.csv -c data/ACS_2023_5year_codebook_all.xlsx -o data/output_California

# python ACS_selection_blockgroup.py -i data/ACS_2020_5year__block_Texas.csv -c data/ACS_2020_5year_codebook_all.xlsx -o data/output_Texas
# python ACS_selection_tract.py -i data/ACS_2019_5year__tract_Texas.csv -c data/ACS_2019_5year_codebook_all.xlsx -o data/output_Texas
# python ACS_selection_tract.py -i data/ACS_2018_5year__tract_IL.csv -c data/ACS_2018_5year_codebook_all.xlsx -o data/output_tract_IL/all
# python ACS_selection_tract.py -i data/ACS_2018_5year__tract_IL.csv -c data/ACS_2018_5year_codebook.xlsx -o data/output/20variables
# python ACS_selection_tract.py -i data/ACS_2018_5year__tract_IL.csv -c data/ACS_2018_5year_codebook_all_for_VNE.xlsx -o data/output_tract/all

    started_datetime = datetime.now()
    print('ACS_selection start at {}'.format(started_datetime.strftime('%Y-%m-%d %H:%M:%S')))
    
    # Get parameter from console
    parameter = getParameter(sys.argv[1:])
    inputFile = parameter[0]
    codebook  = parameter[1]
    ouputDir  = parameter[2]
    
    main(inputFile, codebook, ouputDir)
    
    ended_datetime = datetime.now()
    elapsed = ended_datetime - started_datetime
    total_seconds = int(elapsed.total_seconds())
    hours, remainder = divmod(total_seconds,60*60)
    minutes, seconds = divmod(remainder,60)	
    print('ACS_selection ended at {}    Elapsed {:02d}:{:02d}:{:02d}'.format(ended_datetime.strftime('%Y-%m-%d %H:%M:%S'), hours, minutes, seconds))