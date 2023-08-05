#!/usr/bin/env python3

import sys
import json
import time
import random
import logging
import requests
import argparse
from pprint import pprint
from datetime import datetime


colors = True
machine = sys.platform # Detecting the os
if machine.lower().startswith(("os", "win", "darwin","ios")): 
    colors = False # Colors will not be displayed

if not colors:
	reset = red = white = green  = ""

else:                                                 
    white = "\033[97m"
    red = "\033[91m"    
    reset = "\033[0m"
    green = "\033[92m"



user_agents = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4091.2 Safari/537.36",
                           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
                           "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.90 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                           "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
                           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71",
                           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
                           "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
                           "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36,gzip(gfe)",
                           "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
                           "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/7.0.185.1002 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 OPR/52.0.2871.99",
                           "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
                           "Mozilla/5.0 (Linux; Android 11; SM-M115F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
                           "Mozilla/5.0 (Linux; Android 8.0.0; SM-A750GN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
                           "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/169.1.385914506 Mobile/15E148 Safari/604.1",
                           "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1",
                           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
                           "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36/swoLZb83-26"]
                           
                           

def devilseye():
	parser = argparse.ArgumentParser(description=f"{red}The Devil's Eye:{white} is a  darkweb OSINT tool, that extracts information (.onion links, descriptions) from the darkweb without requiring a Tor network.  developed by {green}Richard Mwewa {white}| https://github.com/{red}rlyonheart{reset}")
	parser.add_argument("query", help=f"{white}search query. {red}Note{white}: if search query contains spaces, put it inside quote ('') symbols{reset}")
	parser.add_argument("-p","--page",help=f"{white}page number ({red}default is 1{white}){reset}", metavar=f"{white}NUMBER{reset}", dest="page", default=1)
	parser.add_argument("-r", "--raw", help=f"{white}return output in raw {red}json{white} format{reset}", dest="raw", action="store_true")
	parser.add_argument("-o", "--output", help=f"{white}write output to a specified {red}file{reset}", metavar=f"{white}FILENAME{reset}", dest="output")
	parser.add_argument("-v", "--verbose", help=f"{white}run thelordseye in {red}verbose{white} mode{reset}", dest="verbose", action="store_true")
	args = parser.parse_args()
	start = datetime.now()
	
	if args.verbose:
		logging.basicConfig(format=f"{white}* %(message)s{reset}",level=logging.DEBUG)
	
	while True:
		try:
			headers = {"User-Agent": f"{random.choice(user_agents)}"}
			base = f"https://darksearch.io/api/search?query={args.query}&page={int(args.page)}"
			response = requests.get(base, headers=headers).json()
			count=0
			for result in response["data"]:
			    count+=1
			    results = f"""
{red}{args.query}{white}
├ total results: {red}{response['total']}{white}
└╼ result number: {red}{count}{white}

{result['title']}
├ .onion url: {red}{result['link']}{white}
└╼ description: {red}{result['description']}{white}{reset}\n"""
			    if args.raw:
			    	pprint(response)
			    		
			    else:
			    	print(results)
			    	
			    if args.output:
			    	output(args,results,response)  					
				
			page = input(f"\n{white}* Next page ({green}1-{response['total']}{white}) ->>  ")
			args.page = page					
			
		except KeyboardInterrupt:
			if args.verbose:
				print(f"\n{white}* Process interrupted with {red}Ctrl{white}+{red}C{reset}")
				exit(f"{white}* Stopped in {red}{datetime.now()-start} {white}seconds.{reset}\n")		
			break
			
		except Exception as e:
			if args.verbose:
				print(f"{white}* Error: {red}{e}{reset}")
				print(f"{white}* Reconnecting...{reset}")


				
def output(args,results,response):
	if args.raw:
		object = json.dumps(response, indent=4)
		with open(args.output, "a") as raw:
			raw.write(object)
			raw.close()
			
	else:
		with open(args.output, "a") as file:
			file.write(results)
			file.close()
	if args.verbose:
	    print(f"\n{white}* Output written to ./{green}{args.output}{reset}")
	    	
		
if __name__=="__main__":
    devilseye()