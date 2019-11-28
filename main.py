import numpy as np
from pprint import pprint

from model import TempestEngine
	
url1 = "https://docs.google.com/spreadsheets/d/14nWdtNCC01mNBeEG_L_UkBbBfuO0tDsQCWk1ekLSxZI/edit#gid=0"	
# url2 = "https://docs.google.com/spreadsheets/d/1aWOaNM5QuqgktEAa_lTsk21w6l6IFUwmF7h1V1j8I3c/edit#gid=0"

tempest = TempestEngine(url1)

while True:
	task = input("Enter a query: ")
	cleaned_query = tempest.clean_query(task)
	tempest.get_query_reply(cleaned_query)