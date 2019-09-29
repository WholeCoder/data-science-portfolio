# Load the Pandas libraries with alias 'pd'
import pandas as pd
# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
data = pd.read_csv("NUT_DATA.txt", sep='^', header=None)
# Preview the first 5 lines of the loaded data
data = data.rename(columns={0: 'NDB_No', 1: 'Nutr_No', 2: 'Nutr_Val', 3: 'Num_Data_Pts', 4: 'Std_Error', 5: 'Src_Cd', 6: 'Deriv_Cd', 7: 'Ref_NDB_No', 8: 'Add_Nutr_Mark', 9: 'Num_Studies', 10: 'Min', 11: 'Max', 12: 'DF', 13: 'Low_EB', 14: 'Up_EB', 15: 'Stat_cmt', 16: 'AddMod_Date', 17: 'CC'}) # noqa

#  print(data)


nut_def_data = pd.read_csv("NUTR_DEF.txt", sep='^', header = None,  encoding  =  "ISO-8859-1")  # noqa
# Preview the first 5 lines of the loaded data
nut_def_data = nut_def_data.rename(columns={0: 'Nutr_No', 1: 'Units', 2: 'Tagname', 3: 'NutrDesc', 4: 'Num_Dec', 5: 'SR_Order'}, errors="raise")  # noqa
#  usecols=['Nutr_No', 'Units', 'Tagname', 'NutrDesc', 'Num_Dec', 'SR_Order'],
#  print(nut_def_data[['Nutr_No', 'Tagname', 'NutrDesc']])


print("Merged dataframe")
merged_df = data.merge(nut_def_data, left_on=['Nutr_No'], right_on=['Nutr_No']) # noqa
print(merged_df[['NutrDesc', 'NDB_No']])

food_des_data = pd.read_csv("FOOD_DES.txt", sep='^', header = None,  encoding  =  "ISO-8859-1")  # noqa
# Preview the first 5 lines of the loaded data
food_des_data = food_des_data.rename(columns={0: 'NDB_No', 1: 'FdGrp_Cd', 2: 'Long_Desc', 3: 'Shrt_Desc', 4: 'ComName', 5: 'ManufacName', 6: 'Survey', 7: 'Ref_desc', 8: 'Refuse', 9: 'SciName', 10: 'N_Factor', 11: 'Pro_Factor', 12: 'Fat_Factor', 13:'CHO_Factor'}, errors="raise")  # noqa
#  usecols=['Nutr_No', 'Units', 'Tagname', 'NutrDesc', 'Num_Dec', 'SR_Order'],
#  print(food_des_data[['NDB_No', 'Long_Desc']])'


print("Merged dataframe")
merged_df = merged_df.merge(food_des_data, left_on=['NDB_No'], right_on=['NDB_No']) # noqa
print(merged_df[['NutrDesc', 'Long_Desc', 'Nutr_Val', 'Nutr_No']])

print(merged_df.groupby(['Nutr_No']).corr())
