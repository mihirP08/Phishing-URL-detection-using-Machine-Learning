# data collection

import requests as re
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

# unstructured to structured data

import pandas as pd
from bs4 import BeautifulSoup
import feature_extraction as fe

disable_warnings(InsecureRequestWarning)

# 1 CSV to dataframe

URL_file_name = "tranco_list.csv"
data_frame = pd.read_csv(URL_file_name)
# print(data_frame)

URL_list = data_frame['url'].to_list()