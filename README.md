# Census and ACS data collection & preprocessing
Python programs to help census or acs data collection, aggregation, normalization at both tract and count level. Initially we made the python programs with ACS 2018 5 year estimate, but the codes should be resuable for both census and acs data in different years.

### Section1: Download tract-level data by using the Census API for all states in the U.S.
- section 1\Data_collection_cbg_tract_ByState\Tract_Join_to_Shp_California_BlockGroup_2023.ipynb how census block group level and tract level ACS data in a particular state were collected and preprocessed.

- The output of Section1 is the input of Section2
- The description of each code is available here: https://api.census.gov/data/2018/acs/acs5/variables.html

- ##### Websites related to CensusAPI
    - https://www.census.gov/data/developers/data-sets.html
    - https://www.census.gov/data/developers/data-sets/acs-5year.html
	- https://api.census.gov/data/2018/acs/acs5/examples.html


### Section2: Data selection, aggregation, and normalization
#### ACS_selection_tract.py and ACS_selection_zipcode.py

- ###### How to run examples:
       python ACS_selection_blockgroup.py -i data/ACS_2023_5year__cbg_CA.csv -c data/ACS_2023_5year_codebook_all.xlsx -o data/output_California
	   
	   python ACS_selection_tract.py -i data/ACS_2023_5year__tract_CA.csv -c data/ACS_2023_5year_codebook_all.xlsx -o data/output_California


 - -i  input: Provide the combined ACS data file downloaded in the previous step. This file is the output generated during the earlier process in the folder 'section 1'. 
 - -c input: This is the control file. In other words, the data you entered above as a parameter -i,  will be selected or calculated based on the rules in this file.

   - colA (CODE) - Required : In order to see the variables in your output file, you need to list it in this column. If you do not list the variable CODE in colA, it will not be printed in the output file. In addition, you need to enter “1” in the colB (use) to print the variable in your outputfile. When you enter multiple variable code in colA, it will sum up the variables.For example, B27011_004E, B27011_009E, B27011_014E → it means all variables will be summed up like this: B27011_004E + B27011_009E + B27011_014E 
   - colB (use) - Required: You need to enter “1” in the colB (use) to print the variable in your outputfile. If colB is empty, the variable will not be printed in the output file. 
  
   - colC (denominator) - Optional: enter the variable code that you want to use to normalize the variable in ColA. If colC is empty, it will use the count without the normalization. For example, for the 3rd in ACS_2018_5year_selected_codebook.xlsx, B06009_004E in col A is divided by B06009_001E and multiplied by 100 in your outputfile. For the 20th row in the same file,
 ((B27011_004E + B27011_009E + B27011_014E) / B27011_001E )*100
   - ColD (Original Name) - Optional: long name of the variables. It will not be shown in your output file.
   - ColE (Short Name) - Required: it will be displayed as column headers in one of your output files (the one for count).
   - ColF (Name_normalized) - Optional: it will be displayed as column headers in one of the output files (the one for normalized data).
   - ColG (GROUP) - Optional: This column is just for your reference and is not used for computation.

  -  -o  output: Enter the folder name. Enter the folder name that exists. 4 csv files will be created
 -     # output of ACS_selection_blockgroup.py.py
        1. XXXX_byTract_summarized.csv: cout in block group level
        2. XXXX_byTract_normalized.csv: Normalized (percentage) in  block group level
		
  -     # output of ACS_selection_tract.py
        1. XXXX_byTract_summarized.csv: cout in tract level
        2. XXXX_byTract_normalized.csv: Normalized (percentage) in tract level

  -     # output of ACS_selection_county.py
        1. XXXX_byTract_summarized.csv: cout in county level
        2. XXXX_byTract_normalized.csv: Normalized (percentage) in county level		

  -     # output of ACS_selection_zipcode.py
        1. XXXXL_byZipcode_summarized.csv: cout in zipcode level
        2. XXXX_byZipcode_normalized.csv: Normalized (percentage) in zipcode level
		
     
- No data value in your output file will be displayed as -9999
-------------
If you have questions, please contact Dr. Su Yeon Han at su.han@txstate.edu
