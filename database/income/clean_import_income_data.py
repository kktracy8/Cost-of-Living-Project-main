# # Code for cleaning OES Income by Occupation Data (May 2022) and creating income comparison dataset
# # Original dataset can be accessed here: "https://www.bls.gov/oes/special-requests/oesm22ma.zip"
#
# # Import Packages
# import pandas as pd
# import sqlalchemy
# import sqlite3
#
# pd.set_option('display.max_columns', None)
#
# # Read income data
# # income = pd.read_excel("oesm22ma/MSA_M2022_dl.xlsx")
#
# #income = pd.read_excel("/Users/zachgeesing/Documents/Documents - Zach’s MacBook Pro/OMS Analytics/CSE 6242 Data and Visual Analytics/Group Project/oesm22ma/MSA_M2022_dl.xlsx")
#
# # Preview raw data
# # print(income.head())
#
# # Get unique MSA locations
# income_locs = income.AREA_TITLE.unique()
#
# # Filter for selected cities
# locs = ['Denver-Aurora-Lakewood, CO', 'Las Vegas-Henderson-Paradise, NV', 'Los Angeles-Long Beach-Anaheim, CA',
#         'Boston-Cambridge-Nashua, MA-NH', 'Dallas-Fort Worth-Arlington, TX', 'Chicago-Naperville-Elgin, IL-IN-WI',
#         'New York-Newark-Jersey City, NY-NJ-PA']
#
# income = income[income['AREA_TITLE'].isin(locs)]
#
# # Convert columns to numeric
# numcols = ['TOT_EMP', 'EMP_PRSE', 'JOBS_1000', 'LOC_QUOTIENT', 'PCT_TOTAL',
#            'PCT_RPT', 'H_MEAN', 'A_MEAN', 'MEAN_PRSE', 'H_PCT10', 'H_PCT25',
#            'H_MEDIAN', 'H_PCT75', 'H_PCT90', 'A_PCT10', 'A_PCT25', 'A_MEDIAN',
#            'A_PCT75', 'A_PCT90']
#
# income[numcols] = income[numcols].apply(pd.to_numeric, errors='coerce')
#
# # Filter for detailed occupation types only
# income = income[income["O_GROUP"] == "detailed"]
#
# # Remove occupations that do not have data in all selected cities
# n = len(pd.unique(income['AREA']))
# income = income.groupby('OCC_TITLE').filter(lambda x: len(x) == n)
#
# # print(len(income))
#
# # Select subset of columns needed for income comparison
# income = income[['AREA', 'AREA_TITLE', 'OCC_CODE', 'OCC_TITLE', 'O_GROUP', 'TOT_EMP', 'JOBS_1000', 'LOC_QUOTIENT',
#                  'H_MEAN', 'A_MEAN', 'MEAN_PRSE', 'H_PCT10', 'H_PCT25', 'H_MEDIAN', 'H_PCT75', 'H_PCT90', 'A_PCT10',
#                  'A_PCT25', 'A_MEDIAN', 'A_PCT75', 'A_PCT90']].copy()
#
# # Impute missing income data with average of other locations for the same occupation
# impute_cols = ['TOT_EMP', 'JOBS_1000', 'LOC_QUOTIENT', 'H_MEAN', 'A_MEAN', 'MEAN_PRSE',
#                'H_PCT10', 'H_PCT25', 'H_MEDIAN', 'H_PCT75', 'H_PCT90', 'A_PCT10', 'A_PCT25',
#                'A_MEDIAN', 'A_PCT75', 'A_PCT90']
#
# for col in impute_cols:
#     income[col] = income[col].fillna(income.groupby('OCC_TITLE')[col].transform('mean'))
#
# # Check for missing data after imputation
# # print(income.isna().sum())
#
# # Impute missing annual income with hourly and vice versa if available for the same occupations / locations
# # Using standard 2080 hour work year
# cols = ['_MEAN', '_PCT10', '_PCT25', '_MEDIAN', '_PCT75', '_PCT90']
#
# for col in cols:
#     income['H' + col] = income['H' + col].fillna(income['A' + col] / 2080)
#     income['A' + col] = income['A' + col].fillna(income['H' + col] * 2080)
#
# # Final cleaned datasets for import
# income_clean = income[['AREA', 'AREA_TITLE', 'OCC_CODE', 'OCC_TITLE', 'O_GROUP',
#                        'TOT_EMP', 'JOBS_1000', 'LOC_QUOTIENT', 'H_MEAN', 'A_MEAN']].copy()
#
# # Create copies so we can compare relative wages for each location
# # Join all locations to each other on occupation title
# src = income_clean.copy()
# dest = income_clean.copy()
#
# # Add prefix to column headers
# src = src.add_prefix('src_')
# dest = dest.add_prefix('dest_')
#
# # convert column headers to lowercase
# src.columns = [x.lower() for x in src.columns]
# dest.columns = [x.lower() for x in dest.columns]
#
# income_comp = pd.merge(src, dest, left_on='src_occ_code', right_on='dest_occ_code', how='left')
#
# # Add calculated columns to compare location wages by occupation
# income_comp['jobs_1000_dif'] = income_comp['dest_jobs_1000'] - income_comp['src_jobs_1000']
# income_comp['loc_quotient_dif'] = income_comp['dest_loc_quotient'] - income_comp['src_loc_quotient']
# income_comp['h_mean_dif'] = income_comp['dest_h_mean'] - income_comp['src_h_mean']
# income_comp['a_mean_dif'] = income_comp['dest_a_mean'] - income_comp['src_a_mean']
#
# # print(len(income_comp))
#
# # Add city columns based on MSA
# income = income_clean.copy()
# income_comparison = income_comp.copy()
#
# # Convert cols to lowercase
# income.columns = [x.lower() for x in income.columns]
#
# # Add City abbrev - for joining with other datasets
# cities = {'Chicago-Naperville-Elgin, IL-IN-WI': 'Chicago, IL', 'Dallas-Fort Worth-Arlington, TX': 'Dallas, TX',
#           'Denver-Aurora-Lakewood, CO': 'Denver, CO', 'Las Vegas-Henderson-Paradise, NV': 'Las Vegas, NV',
#           'Los Angeles-Long Beach-Anaheim, CA': 'Los Angeles, CA','New York-Newark-Jersey City, NY-NJ-PA': 'New York City, NY',
#           'Boston-Cambridge-Nashua, MA-NH': 'Boston, MA'}
#
# # Add state mapping to income tables
# income['city'] = income['area_title'].map(cities)
# income_comparison['src_city'] = income_comparison['src_area_title'].map(cities)
# income_comparison['dest_city'] = income_comparison['dest_area_title'].map(cities)
#
# # print(income_comparison.head())
# # print(income.head())
#
# # Add income tables to db
# # engine = sqlalchemy.create_engine('sqlite:///database/data.db', echo=False)
#
# # income.to_sql('income', con=engine, if_exists='replace', index=False)
# # income_comparison.to_sql('income_comparison', con=engine, if_exists='replace')
#
# conn = sqlite3.connect('../data.db')
# print(conn)
#
# # Add data to db
# income.to_sql('income', con=conn, if_exists='replace', index=False)
#
# #conn.execute("""create table income as select * from income""")
#
# income_comparison.to_sql('income_comparison', con=conn, if_exists='replace')
#
# #conn.execute("""create table income_comparison as select * from income_comparison""")
#
# conn.close()
#
# # Test accessing new tables
# # df1 = pd.read_sql_table('income_comparison', con=engine)
# # df2 = pd.read_sql_table('income', con=engine)
# # print(df1.head())
# # print(df2.head())
#
# # print(engine)
