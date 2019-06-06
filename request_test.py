from __future__ import print_function
import os
import requests

def ChromeToDict( infilename ):
	result = {}
	with open(infilename, 'r') as infile:
		for line in infile:
			data = line.strip().split()
			key = data[0].replace(':', '')
			value = " ".join( data[1:] )
			result[key] = value
	return result

auth_url = "http://course.suraasa.com/authenticate"
auth_header_file = "auth.header"
auth_data_file = "auth.data"
auth_header = ChromeToDict( auth_header_file )
auth_data = ChromeToDict( auth_data_file  )
#auth_response = requests.post(auth_url, headers=auth_header, data=auth_data)

purchase_url = "http://course.suraasa.com/purchaseHistory"
purchase_header_file = "purchase.header"
purchase_header = ChromeToDict( purchase_header_file )
purchase_header['Cookie'] = purchase_header['Cookie'] + '; ' + auth_response.headers['Set-Cookie'] 
#purchase_response = requests.get(purchase_url, headers=purchase_header)
