import pandas as pd
from bs4 import BeautifulSoup
import importlib
import numpy as np

pd.options.display.max_rows = 1000

state_code_dict = importlib.import_module("state_codes").state_dict
state_code_dict = {v: int(k) for k, v in state_code_dict.items()}
state_code_dict = {v: k for k, v in state_code_dict.items()}


def create_dataframe_from_html_file(file_name):
    alcohol_soup = BeautifulSoup(open(file_name, encoding = "ISO-8859-1"), features="html.parser")  # noqa
    all_rows = alcohol_soup.find_all('tr')

#  print(len(all_rows))

    alcohol_data_list = []
    started = True

    for r in all_rows:
        found_2014 = True
        tlist = []
        ths = r.find_all('th')
        for th in ths:
            if not started and th.get_text().strip() != 'Alabama':
                continue
            else:
                started = True

            if th.has_attr('colspan'):
                current_state = th.get_text().strip()
            if not th.has_attr('colspan'):
                if th.get_text().strip() != '2014':
                    found_2014 = False
                    break
                # print("th     " + current_state)
                tlist.append(current_state)
                # print("th     " + th.get_text())
                tlist.append(th.get_text())
        if found_2014:
            for td in r.find_all('td'):
                #  print("td     " + td.get_text())
                tlist.append(td.get_text())
            if len(tlist) != 0:
                alcohol_data_list.append(tlist)
    df = pd.DataFrame(alcohol_data_list, columns=['STATE', 'YEAR', 'BEER', 'WINE', 'SPIRITS', 'ALL BEVERAGES', 'US DECILE FOR ALL BEVERAGES'])  # noqa
    return df

df = create_dataframe_from_html_file("alcohol_consumption_by_state+_and_time.htm")  # noqa

df2 = create_dataframe_from_html_file("alcohol_consumption_by_state+_and_time2.htm")  # noqa
# print(df.concat(df2))
con_df = pd.concat([df, df2])

df3 = create_dataframe_from_html_file("alcohol_consumption_by_state+_and_time3.htm")  # noqa
#  print(df3)
con_df = pd.concat([con_df, df3])
df4 = create_dataframe_from_html_file("alcohol_consumption_by_state+_and_time4.htm")  # noqa
#  print(df4)
con_df = pd.concat([con_df, df4])

df5 = create_dataframe_from_html_file("alcohol_consumption_by_state+_and_time5.htm")  # noqa
#  print(df5)
con_df = pd.concat([con_df, df5])
#  print(con_df)
# this is for regions - not needed
#  df6 = create_dataframe_from_html_file("alcohol_consumption_by_state+_and_time6.htm")  # noqa
#  print(df6)


def slices(s, *args):
    position = 0
    for length in args:
        yield s[position:position + length]
        position += length

#  list(slices('abcdefghijklmnopqrstuvwxyz0123456789', 2, 10, 50))


def readInDataFrame(file_name, col_suffix):
    global state_code_dict

    with open(file_name, "r") as file_handle:
            rows = file_handle.readlines()

    df_rows = []
    for row in rows:
        r = list(slices(row, 2, 2, 2, 4, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7))
        df_rows.append(r)

    df = pd.DataFrame.from_records(df_rows, columns=['STATE-CODE', 'DIVISION-NUMBER', 'ELEMENT CODE', 'YEAR', # noqa
        'JAN-VALUE'+col_suffix,
        'FEB-VALUE'+col_suffix,
        'MAR-VALUE'+col_suffix,
        'APR-VALUE'+col_suffix,
        'MAY-VALUE'+col_suffix,
        'JUNE-VALUE'+col_suffix,
        'JULY-VALUE'+col_suffix,
        'AUG-VALUE'+col_suffix,
        'SEPT-VALUE'+col_suffix,
        'OCT-VALUE'+col_suffix,
        'NOV-VALUE'+col_suffix,
        'DEC-VALUE'+col_suffix])  # noqa

    #  print(sprecip_df)
    df = df.astype({'STATE-CODE': 'int64', 'YEAR': 'int64'})
    df['STATE-CODE'].replace(to_replace=state_code_dict, inplace=True)# noqa
    #  print(df)

    return df


sprecip_df = readInDataFrame("state+precipitation.wsv", '-PRECIP')
sprecip_df2 = readInDataFrame("state+precipitation2.wsv", '-PRECIP')

stemp_df = readInDataFrame("state+temperature.wsv", '-TEMPERATURE')
stemp_df2 = readInDataFrame("state+temperature2.wsv", '-TEMPERATURE')

sprecip_df = pd.concat([sprecip_df, sprecip_df2])
stemp_df = pd.concat([stemp_df, stemp_df2])


print("sprecip_df_concated------------")
print(sprecip_df)

merged_df = sprecip_df.merge(stemp_df, left_on=['STATE-CODE', 'DIVISION-NUMBER', 'YEAR'], right_on=['STATE-CODE', 'DIVISION-NUMBER', 'YEAR']) # noqa


sliced_df = merged_df[['STATE-CODE', 'YEAR', 'JAN-VALUE-PRECIP', 'JAN-VALUE-TEMPERATURE']]  # noqa
sliced_df = sliced_df[sliced_df['YEAR'] == 2014]
#  print(sliced_df)  # noqa
print("sliced up---------------------")
print(sliced_df)
sliced_df['STATE-CODE'] = sliced_df['STATE-CODE'].str.strip()

grped = sliced_df.astype({'STATE-CODE': 'str', 'JAN-VALUE-TEMPERATURE': 'float64', 'JAN-VALUE-PRECIP': 'float64'}).groupby(['YEAR', 'STATE-CODE']) # noqa

grped_agg_df = grped.aggregate(np.mean)
grped_agg_df.reindex(level=['YEAR', 'STATE-CODE'])
#  grped_agg_df['STATE-CODE'] = grped_agg_df['STATE-CODE'].str.strip()

print("grouped----------------------")
print(grped_agg_df)
#  print(con_df)

totally_merged = con_df.merge(grped_agg_df, left_on=['STATE'], right_on=['STATE-CODE'])  # noqa

totally_merged = totally_merged.sort_values(by=['ALL BEVERAGES'], ascending=False)  # noqa
print("totally--------------------")
print(totally_merged[['STATE', 'JAN-VALUE-TEMPERATURE', 'JAN-VALUE-PRECIP', 'ALL BEVERAGES']])  # noqa
