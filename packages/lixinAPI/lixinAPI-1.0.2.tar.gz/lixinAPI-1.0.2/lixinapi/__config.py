import pandas as pd
import datetime
from lixinapi.secret import *
#solr地址
stockurl='http://39.97.160.135:8092/StockData/get_history_data?security=%s&startdate=%s&enddate=%s'
incomeurl='http://39.97.160.135:8092/StockData/get_Income_data?security=%s&startdate=%s&enddate=%s'
cashflowurl='http://39.97.160.135:8092/StockData/get_CashFlow_data?security=%s&startdate=%s&enddate=%s'
balanceurl='http://39.97.160.135:8092/StockData/get_Balance_data?security=%s&startdate=%s&enddate=%s'
loginurl='http://39.97.160.135:8092/Login/ressetLogin?loginname=%s&loginpwd=%s'
contenturl='http://39.97.160.135:8092/StockData/get_Content_data?code=%s&type=%s&tname=%s&year=%s'
