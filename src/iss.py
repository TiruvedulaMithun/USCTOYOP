import time
import csv
import sys
import os
import json
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import re
from fuzzywuzzy import fuzz

# Sample raw cookie data as a string, each line is a separate cookie entry
raw_cookie_data = """
BIGipServerpac8-group1-op	!ph083HXSIpxr1CkVm4fmsw0VJ1sI0T9EOudM600XMRLwI5hbrdvx7i8OJHvoQW9hEHfV9RiIPs5ptg==	client.paciolan.com	/	Session	106		✓			Medium	
BIGipServerpac8-weo	!BgC4/AEVcGk1kwoVm4fmsw0VJ1sI0cXSxcoY/DKoea2E17CSI+g3XXmwzvvrX/A1bhs5+Bn5dDi2qt0=	client.paciolan.com	/	Session	100		✓			Medium	
BOCA_PRINTER_NAME	Boca%20BIDI%20FGL%2026%2F46%20300%20DPI	client.paciolan.com	/	Session	56		✓			Medium	
BusOrgId	31855	client.paciolan.com	/app	Session	13					Medium	
BusOrgId	31855	client.paciolan.com	/	Session	13		✓			Medium	
CurrentLivingBusOrgId	jNEZyevnz4SHF3dN0ql4bg%3D%3D	client.paciolan.com	/app	Session	49		✓			Medium	
CurrentLivingBusOrgId	jNEZyevnz4SHF3dN0ql4bg%3D%3D	client.paciolan.com	/	Session	49		✓			Medium	
CurrentLivingServerId	l2mLkHmWfEM6WglL540AbxcbS18WKgSoJmLdiYNrHxQ%3D	client.paciolan.com	/app	Session	67		✓			Medium	
CurrentLivingServerId	l2mLkHmWfEM3azxhheIujORl2PG1TJa%2BV17FzuSDnjo%3D	client.paciolan.com	/	Session	69		✓			Medium	
CurrentLivingUserId	jNEZyevnz4SHF3dN0ql4bg%3D%3D	client.paciolan.com	/	Session	47		✓			Medium	
CurrentLivingUserId	jNEZyevnz4SHF3dN0ql4bg%3D%3D	client.paciolan.com	/app	Session	47		✓			Medium	
JSESSIONID	E9twTJ0UylwScmP-6SCd-dCN4kf0avzdz86ORvoF.pus-ca01-r29c5-def-h152-app4	client.paciolan.com	/app	Session	79		✓			Medium	
JSESSIONID	s3txAQf1akAA6tHJ-rHHDbIpMNlHzE8tiXiOEC-4.pus-ca01-r29c1-def-h122-app3	client.paciolan.com	/	Session	79		✓			Medium	
LASER_PRINTER_NAME	Microsoft%20Print%20to%20PDF	client.paciolan.com	/	Session	46		✓			Medium	
Location	31856	client.paciolan.com	/app	Session	13					Medium	
Location	31856	client.paciolan.com	/	Session	13		✓			Medium	
PrinterType	BOCA%2CLASER	client.paciolan.com	/	Session	23		✓			Medium	
SorderGrid	%7B%22state%22%3A%7B%22widthfeePrc%22%3A%22i%3A74%22%2C%20%22widthselPriceLevelCd%22%3A%22i%3A50%22%2C%20%22widthseatBlocks%22%3A%22i%3A117%22%2C%20%22widthitemName%22%3A%22i%3A327%22%7D%7D	client.paciolan.com	/	2024-05-14T23:35:17.000Z	199		✓			Medium	
TerminalCd	51-8f-55-69-42-68	client.paciolan.com	/app	Session	27					Medium	
TerminalCd	51-8d-9f-21-7a-a6	client.paciolan.com	/	Session	27		✓			Medium	
_BEAMER_BOOSTED_ANNOUNCEMENT_DATE_vchiLcpV22713	2024-05-01T21:57:14.458Z	client.paciolan.com	/	Session	71		✓			Medium	
_BEAMER_DATE_vchiLcpV22713	2024-04-17T16:02:26.000Z	client.paciolan.com	/	Session	50		✓			Medium	
_BEAMER_FILTER_BY_URL_vchiLcpV22713	false	.paciolan.com	/	2024-05-07T23:54:28.000Z	40		✓	None		Medium	
_BEAMER_FILTER_BY_URL_vchiLcpV22713	false	.client.paciolan.com	/	2024-05-07T23:54:28.000Z	40		✓	None		Medium	
_BEAMER_FILTER_BY_URL_vchiLcpV22713	false	client.paciolan.com	/	Session	40		✓			Medium	
_BEAMER_FIRST_VISIT_vchiLcpV22713	2023-10-26T21:16:09.589Z	.paciolan.com	/	2025-03-03T23:35:15.000Z	57		✓	None		Medium	
_BEAMER_FIRST_VISIT_vchiLcpV22713	2023-10-26T21:16:09.589Z	client.paciolan.com	/	Session	57		✓			Medium	
_BEAMER_LAST_POST_SHOWN_vchiLcpV22713	65634267	client.paciolan.com	/	Session	45		✓			Medium	
_BEAMER_LAST_PUSH_PROMPT_INTERACTION_vchiLcpV22713	1704503365577	client.paciolan.com	/	Session	63		✓			Medium	
_BEAMER_LAST_UPDATE_vchiLcpV22713	1715124915684	.paciolan.com	/	2025-03-03T23:35:15.000Z	46		✓	None		Medium	
_BEAMER_LAST_UPDATE_vchiLcpV22713	1715112148242	client.paciolan.com	/	Session	46		✓			Medium	
_BEAMER_NPS_LAST_SHOWN_vchiLcpV22713	1714862331902	client.paciolan.com	/	Session	49		✓			Medium	
_BEAMER_USER_ID_vchiLcpV22713	687e7d1f-23a4-4aaf-b593-283427405c45	.paciolan.com	/	2025-03-03T23:35:15.000Z	65		✓	None		Medium	
_BEAMER_USER_ID_vchiLcpV22713	687e7d1f-23a4-4aaf-b593-283427405c45	client.paciolan.com	/	Session	65		✓			Medium	
_ga	GA1.2.1264575802.1698354957	client.paciolan.com	/	Session	30		✓			Medium	
_ga	GA1.2.1264575802.1698354957	.paciolan.com	/	2025-06-11T23:35:17.579Z	30					Medium	
_ga_088FTVYN0L	GS1.2.1715124905.398.1.1715124912.0.0.0	.paciolan.com	/	2025-06-11T23:35:12.933Z	53					Medium	
_ga_088FTVYN0L	GS1.2.1715112099.397.1.1715112120.0.0.0	client.paciolan.com	/	Session	53		✓			Medium	
_ga_N22E0KCT4K	GS1.3.1715098401.464.1.1715099124.60.0.0	client.paciolan.com	/	Session	54		✓			Medium	
_ga_N22E0KCT4K	GS1.2.1715124917.465.0.1715124917.60.0.0	.paciolan.com	/	2025-06-11T23:35:17.735Z	54					Medium	
_gat	1	client.paciolan.com	/	Session	5		✓			Medium	
_gid	GA1.3.1198247623.1714950412	client.paciolan.com	/	Session	31		✓			Medium	
_gid	GA1.2.1198247623.1714950412	.paciolan.com	/	2024-05-08T23:35:17.000Z	31					Medium	
amplitude_id_07f03cbad2c0f198cae5714559f4d029paciolan.com	eyJkZXZpY2VJZCI6ImZhYjU4MzBhLTNlODMtNGQ3OC1iY2Q3LWIwN2QxMWI2YTg2Y1IiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTcxNTEyNDI1Mjg4OCwibGFzdEV2ZW50VGltZSI6MTcxNTEyNDI1ODgxMCwiZXZlbnRJZCI6MSwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjF9	client.paciolan.com	/	Session	301		✓			Medium	
amplitude_id_07f03cbad2c0f198cae5714559f4d029paciolan.com	eyJkZXZpY2VJZCI6ImZhYjU4MzBhLTNlODMtNGQ3OC1iY2Q3LWIwN2QxMWI2YTg2Y1IiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTcxNTEyNDI1Mjg4OCwibGFzdEV2ZW50VGltZSI6MTcxNTEyNDkxNDgzMywiZXZlbnRJZCI6MiwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjJ9	.paciolan.com	/	2025-06-11T23:35:14.834Z	301					Medium	
et.op.PACUSC.locale	en_US	client.paciolan.com	/	Session	24		✓			Medium	
et.op.PACUSC.locales	%5B%22en_US%22%2C%22fr%22%5D	client.paciolan.com	/	Session	48		✓			Medium	
et.op.PACUSC.poolId	pac8-group1-op	client.paciolan.com	/	Session	33		✓			Medium	
et.op.clientId	PACUSC	client.paciolan.com	/	Session	20					Medium	
et.op.display	page	client.paciolan.com	/	Session	17					Medium	
pac-authz	6e7e41f0-0cca-11ef-bab2-0000c0a83607	client.paciolan.com	/	Session	45		✓			Medium	
"""

raw_local_storage_data = """
CD  51-8d-9f-21-7a-a6  
TERMINAL_CD 81-8f-55-66-93-e8  
SELLER_LOCA_PAIR [{"orgId":31855,"locationId":31856,"accessTime":1715124737166}]    
_BEAMER_SELECTOR_COLOR_vchiLcpV22713  #3f7be1  
amplitude_unsent_430dc24551adca351d6dd9d9383050bf  []  
_BEAMER_LAST_POST_SHOWN_vchiLcpV22713  null    
LOCATION_ID  31856  
amplitude_unsent_07f03cbad2c0f198cae5714559f4d029 [{"device_id":"fab5830a-3e83-4d78-bcd7-b07d11b6a86cR","user_id":null,"timestamp":1715124741281,"event_id":2,"session_id":1715124252888,"event_type":"load_page_ticketing","version_name":null,"platform":"Web","os_name":"Chrome","os_version":"124","device_model":"Windows","language":"en-US","api_properties":{},"event_properties":{},"user_properties":{},"uuid":"fb345462-831d-4c28-b621-b3639a0583de","library":{"name":"amplitude-js","version":"4.5.2"},"sequence_number":2,"groups":{},"group_properties":{},"user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}]  
pa_enabled 1  
_BEAMER_DATE_vchiLcpV22713 2024-05-07T16:32:18-07:00  
BEAMER_USER_ID_vchiLcpV22713 687e7d1f-23a4-4aaf-b593-283427405c45  
_BEAMER_FIRST_VISIT_vchiLcpV22713 2023-10-26T21:16:09.589Z  
_BEAMER_NPS_LAST_SHOWN_vchiLcpV22713 1714862331902  
_BEAMER_HEADER_COLOR_vchiLcpV22713 #2a69b7  
PRINTER_TYPE BOCA,LASER  
BOCA_PRINTER_NAME Boca BIDI FGL 26/46 300 DPI  
_BEAMER_FILTER_BY_URL_vchiLcpV22713 false  
PRINTAGENT_HOST localhost:8091  
_BEAMER_LAST_UPDATE_vchiLcpV22713 1715124732364  
LASER_PRINTER_NAME Microsoft Print to PDF  
_BEAMER_BOOSTED_ANNOUNCEMENT_DATE_vchiLcpV22713 2024-05-01T21:57:14.458Z
"""

# Function to parse the raw cookie data into a list of dictionaries
def parse_cookies(raw_data):
    cookies = []
    lines = raw_data.strip().split('\n')
    for line in lines:
        parts = line.split('\t')
        if len(parts) >= 2:
            cookie = {
                'name': parts[0].strip(),
                'value': parts[1].strip()
            }
            cookies.append(cookie)
    return cookies

def parse_raw_to_dict(raw_data):
    data_dict = {}
    lines = raw_data.strip().split('\n')  # Split the raw data into lines
    for line in lines:
        parts = line.split('\t')  # Split each line into parts using the tab character as a delimiter
        if len(parts) >= 2:
            key = parts[0].strip()  # Clean up any leading/trailing whitespace
            value = parts[1].strip()
            data_dict[key] = value  # Add to dictionary
        else:
            print(f"Skipping malformed line: {line}")
    return data_dict



APP_LOCAL_STORAGE = {
"CD": "51-8d-9f-21-7a-a6", 
"SELLER_LOCA_PAIR": "[{\"orgId\":31855,\"locationId\":31856,\"accessTime\":1715112120480}]", 
"_BEAMER_SELECTOR_COLOR_vchiLcpV22713": "#3f7be1", 
"amplitude_unsent_430dc24551adca351d6dd9d9383050bf": "[]", 
"_BEAMER_LAST_POST_SHOWN_vchiLcpV22713": "65634267", 
"LOCATION_ID": "31856", 
"amplitude_unsent_07f03cbad2c0f198cae5714559f4d029": "[]", 
"amplitude_unsent_identify_fc60ef617af1d2497fbf611e5aa6da33_pac-library": "[]", 
"amplitude_unsent_identify_07f03cbad2c0f198cae5714559f4d029": "[]", 
"pa_enabled": "1", 
"_BEAMER_DATE_vchiLcpV22713": "2024-04-17T16:02:26.000Z", 
"amplitude_unsent_fc60ef617af1d2497fbf611e5aa6da33_pac-library": "[]", 
"1586305:recentTransactions:eventAdded": "true", 
"pa": "sid=554gfvne&sst=1715112099&sis=6&rv=1", 
"_BEAMER_FIRST_VISIT_vchiLcpV22713": "2023-10-26T21:16:09.589Z", 
"amplitude_unsent_identify_430dc24551adca351d6dd9d9383050bf": "[]", 
"_BEAMER_NPS_LAST_SHOWN_vchiLcpV22713": "1714862331902", 
"_BEAMER_HEADER_COLOR_vchiLcpV22713": "#2a69b7", 
"PRINTER_TYPE": "BOCA,LASER", 
"BOCA_PRINTER_NAME": "Boca BIDI FGL 26/46 300 DPI", 
"_BEAMER_FILTER_BY_URL_vchiLcpV22713": "false", 
"PRINTAGENT_HOST": "localhost:8091", 
"_BEAMER_LAST_UPDATE_vchiLcpV22713": "1715112148242", 
"LASER_PRINTER_NAME": "Microsoft Print to PDF", 
"_BEAMER_BOOSTED_ANNOUNCEMENT_DATE_vchiLcpV22713": "2024-05-01T21:57:14.458Z"
}

APP_COOKIES = [
    {"name": "BIGipServerapigateway", "value": "!j6LNfO+Loh8xjF8Vm4fmsw0VJ1sI0a7FXT2PtrGt0cGYOPEuM9yvVAtKU854oH7nOwfpTXXJ9Fb3/X4="},
    {"name": "BIGipServerpac8-group1-op", "value": "!Df7ympJRd4VqIhAVm4fmsw0VJ1sI0dxi0v52RQZZS+kXJr8k/wiWvoMrLwBZlZ5zHmCG8jzyqvhgEw=="},
    {"name": "BIGipServerpac8-weo", "value": "!HOLmu2k7yWz+nmwVm4fmsw0VJ1sI0cWOXC3xKCq07N3fkzsuh1V74eOwLaSFEOruYVWCf7N0nSOj26E="},
    {"name": "BOCA_PRINTER_NAME", "value": "Boca%20BIDI%20FGL%2026%2F46%20300%20DPI"},
    {"name": "BusOrgId", "value": "31855"},
    {"name": "JSESSIONID", "value": "s3txAQf1akAA6tHJ-rHHDbIpMNlHzE8tiXiOEC-4.pus-ca01-r29c1-def-h122-app3"},
    {"name": "LASER_PRINTER_NAME", "value": "Microsoft%20Print%20to%20PDF"},
    {"name": "Location", "value": "31856"},
    {"name": "PrinterType", "value": "BOCA%2CLASER"},
    {"name": "SorderGrid", "value": "%7B%22state%22%3A%7B%22widthfeePrc%22%3A%22i%3A74%22%2C%20%22widthselPriceLevelCd%22%3A%22i%3A50%22%2C%20%22widthseatBlocks%22%3A%22i%3A117%22%2C%20%22widthitemName%22%3A%22i%3A327%22%7D%7D"},
    {"name": "TerminalCd", "value": "51-8d-9f-21-7a-a6"},
    {"name": "_BEAMER_BOOSTED_ANNOUNCEMENT_DATE_vchiLcpV22713", "value": "2024-05-01T21:57:14.458Z"},
    {"name": "_BEAMER_DATE_vchiLcpV22713", "value": "2024-04-17T16:02:26.000Z"},
    {"name": "_BEAMER_FILTER_BY_URL_vchiLcpV22713", "value": "false"},
    {"name": "_BEAMER_FIRST_VISIT_vchiLcpV22713", "value": "2023-10-26T21:16:09.589Z"},
    {"name": "_BEAMER_LAST_POST_SHOWN_vchiLcpV22713", "value": "65634267"},
    {"name": "_BEAMER_LAST_PUSH_PROMPT_INTERACTION_vchiLcpV22713", "value": "1704503365577"},
    {"name": "_BEAMER_LAST_UPDATE_vchiLcpV22713", "value": "1715112148242"},
    {"name": "_BEAMER_NPS_LAST_SHOWN_vchiLcpV22713", "value": "1714862331902"},
    {"name": "_BEAMER_USER_ID_vchiLcpV22713", "value": "687e7d1f-23a4-4aaf-b593-283427405c45"},
    {"name": "_ga", "value": "GA1.2.1264575802.1698354957"},
    {"name": "_ga_088FTVYN0L", "value": "GS1.2.1715112099.397.1.1715112120.0.0.0"},
    {"name": "_ga_N22E0KCT4K", "value": "GS1.3.1715098401.464.1.1715099124.60.0.0"},
    {"name": "_gid", "value": "GA1.3.1198247623.1714950412"}
]


EVENT_MAP = {
    "COMM1": {
        "name": "Phi Kappa Phi",
        "date": "5/8/2024",
        "location": "Bing Theatre",
        "keywords": ["Phi","Kappa"],
        "event_id": 1
    },
    "COMM2": {
        "name": "Dornsife Ph.D. Hooding Ceremony",
        "date": "5/8/2024",
        "location": "Allyson Felix Field",
        "keywords": ["Dornsife"],
        "event_id": 2
    },
    "COMM6": {
        "name": "Black Graduate Celebration ",
        "date": "5/8/2024",
        "location": "Allyson Felix Field",
        "keywords": ["Black"],
        "event_id": 6
    },
    "COMM3": {
        "name": "Rossier School of Education Ph.D. and Ed.D. Hooding",
        "date": "5/8/2024",
        "location": "McCarthy Quad",
        "keywords": ["Rossier","Education"],
        "event_id": 3
    },
    "COMM4": {
        "name": "Annenberg Ph.D. Hooding",
        "date": "5/8/2024",
        "location": "Wallis Annenberg Hall, Room L105A",
        "keywords": ["Annenberg"],
        "event_id": 4
    },
    "COMM5": {
        "name": "Veterans/ROTC Grad",
        "date": "5/8/2024",
        "location": "RTCC Ballroom",
        "keywords": ["Veterans","ROTC"],
        "event_id": 5
    },
    "COMM7": {
        "name": "Viterbi Ph.D. Hooding and Awards Ceremony",
        "date": "5/8/2024",
        "location": "Bovard Auditorium",
        "keywords": ["Viterbi"],
        "event_id": 7
    },
    "COMM8": {
        "name": "Marshall School of Business Ph.D. Ceremony",
        "date": "5/8/2024",
        "location": "Davidson Conference Center",
        "keywords": ["Marshall","Business"],
        "event_id": 8
    },
    "COMM9": {
        "name": "Mark's Foundation Student Athlete Awards",
        "date": "5/9/2024",
        "location": "Galen Center - Founders Room",
        "keywords": ["Mark's","Marks","Mark"],
        "event_id": 9
    },
    "COMM21": {
        "name": "Athlete Student Recognition",
        "date": "5/9/2024",
        "location": "Galen Center",
        "keywords": ["Athlete"],
        "event_id": 21
    },
    "COMM17": {
        "name": "Dworak-Peck School of Social Work",
        "date": "5/10/2024",
        "location": "Coliseum",
        "keywords": ["Dworak","Peck","Social","Dworak-Peck"],
        "event_id": 17
    },
    "COMM18": {
        "name": "Marshall School of Business",
        #"name": "Marshall School of Business (undergrad)",
        #"name": "Marshall School of Business (Grad)",
        "date": "5/10/2024",
        "location": "Coliseum",
        "keywords": ["Marshall","Business"],
        "event_id": 18
    },
    "COMM20": {
        "name": "Trojan Family Graduate Celebration",
        "date": "5/9/2024",
        "location": "Coliseum",
        "keywords": ["Trojan","Family"],
        "event_id": 20
    },
    "COMM22": {
        "name": "Public Policy",
        "date": "5/10/2024",
        "location": "Shrine Auditorium",
        "keywords": ["Public","Policy"],
        "event_id": 22
    },
    "COMM11": {
        "name": "School of Cinematic Arts",
        "date": "5/10/2024",
        "location": "Shrine Auditorium",
        "keywords": ["Cinematic","Arts"],
        "event_id": 11
    },
    "COMM12": {
        "name": "Gould School of Law - Undergrad and JD ",
        "date": "5/10/2024",
        "location": "USC Village Great Lawn",
        "keywords": ["Gould","Law", "Undergrad","JD"],
        "event_id": 12
    },
    "COMM23": {
        "name": "Gould School of Law - Graduate and International Programs",
        "date": "5/10/2024",
        "location": "USC Village Great Lawn",
        "keywords": ["Gould","Law", "Graduate","International"],
        "event_id": 23
    },
    "COMM13": {
        "name": "Viterbi School of Engineering Undergraduate Degree Programs",
        "date": "5/10/2024",
        "location": "Galen Center",
        "keywords": ["Viterbi","Engineering", "Undergraduate"],
        "event_id": 13
    },
    "COMM24": {
        "name": "Viterbi School of Engineering Graduate #1",
        "date": "5/10/2024",
        "location": "Galen Center",
        "keywords": ["Viterbi","Engineering","Graduate", "1", "One", "#1", "grad"],
        "event_id": 24
    },
    "COMM25": {
        "name": "Viterbi School of Engineering Graduate #2",
        "date": "5/10/2024",
        "location": "Galen Center",
        "keywords": ["Viterbi","Engineering","Graduate", "2", "Two", "#2", "grad"],
        "event_id": 25
    },
    "COMM26": {
        "name": "Keck School of Medicine - M.D.",
        "date": "5/11/2024",
        "location": "Galen Center",
        "keywords": ["Keck","Medicine","M.D.", "MD"],
        "event_id": 26
    },
    "COMM15": {
        "name": "Keck School of Medicine -Ph.D.,DNAP,MPH,M.S.",
        "date": "5/11/2024",
        "location": "Galen Center",
        "keywords": ["Keck","Medicine","Ph.D.","DNAP","MPH","M.S.", "PhD", "MS"],
        "event_id": 15
    },
    "COMM19": {
        "name": "Mann School of Pharmacy and Pharmaceutical Sciences",
        "date": "5/11/2024",
        "location": "McCarthy Quad",
        "keywords": ["Mann","Pharmacy","Pharmaceutical"],
        "event_id": 19
    },
    "COMM10": {
        "name": "USC Commencement",
        "date": "5/9/2024",
        "location": "UPC Campus",
        "keywords": ["USC","Commencement"],
        "event_id": 10
    },
    "COMM14": {
        "name": "USC Commencement",
        "date": "5/10/2024",
        "location": "UPC Campus",
        "keywords": ["USC","Commencement"],
        "event_id": 14
    },
}

DATE_TO_EVENT_MAP = {
    "5/08/2024": ["COMM1","COMM2","COMM6","COMM3","COMM4","COMM5","COMM7","COMM8"],
    "5/09/2024": ["COMM9","COMM21","COMM10","COMM20"],
    "5/10/2024": ["COMM17","COMM18","COMM22","COMM11","COMM12","COMM23","COMM13","COMM24","COMM25","COMM14"],
    "5/11/2024": ["COMM26","COMM15","COMM19"],
}

COMPLIMENTATRY_EVENTS = {
    "COMM21": ["COMM10"],
    "COMM17": ["COMM14"], 
    "COMM18": ["COMM14"], 
    "COMM18": ["COMM14"], 
    "COMM22": ["COMM14"], 
    "COMM11": ["COMM14"], 
    "COMM12": ["COMM14"], 
    "COMM23": ["COMM14"], 
    "COMM13": ["COMM14"], 
    "COMM24": ["COMM14"], 
    "COMM25": ["COMM14"], 
}

def findEvent(event, date=None, location=None):
    formatted_date = None
    # parse date "Friday, May 10th" to "5/10/2024"
    day, rest = date.split(",")
    empty, month, day = rest.split(" ")
    day = day[:-2]
    if month == "May":
        formatted_date = "5/"+day+"/2024"
    all_possible_events = DATE_TO_EVENT_MAP[formatted_date]
    # print("Date:", formatted_date, all_possible_events)
    potential_event = None
    match_scores = []
    event_name_normalized = event.lower()

    for possible_event in all_possible_events:
        match_score = 0
        event_details = EVENT_MAP[possible_event]
        for keyword in event_details["keywords"]:
            # Check for both exact and fuzzy matches, weighted slightly towards exact matches
            if keyword.lower() in event_name_normalized:
                match_score += 10  # Exact match found
            else:
                # Fuzzy match - using token set ratio for better handling of mixed words
                match_score += (fuzz.token_set_ratio(keyword.lower(), event_name_normalized) / 10)
        match_scores.append({"event": possible_event, "score": match_score})
    
    match_scores = sorted(match_scores, key=lambda x: x["score"], reverse=True)
    # print("Match Scores:", match_scores)
    potential_event = match_scores[0]["event"]
    return potential_event

def getAllEventsToBook(event):
    if event in COMPLIMENTATRY_EVENTS:
        return [event] + COMPLIMENTATRY_EVENTS[event]
    return [event]

def enter_text_in_element_by_id(driver, text, element_id):
    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    print("[INFO] Entering text in field:", text)
    input_field.clear()
    input_field.send_keys(text)

def double_click_first_entry(driver):
    try:
        # Wait for the grid body to be visible
        highlight_row = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.x-grid3-highlightrow'))
        )

        print("[INFO] Double-clicking on the first entry in the grid")
        
        # Locate the first <tr> within the table of the highlighted row
        # first_tr = highlight_row.find_element_by_css_selector('.x-grid3-row-table > tbody > tr')
        # print("[INFO] found the sfirst entry in the grid", first_tr.get_attribute("innerHTML")[:1000])
        # Create an ActionChain to perform double click
        actions = ActionChains(driver)
        actions.double_click(highlight_row).perform()
        
    except Exception as e:
        traceback.print_exc()
        print("Error during double-clicking on the first entry: ", e)
        raise e

def click_element_by_id(driver, element_id):
    try:
        # Wait for the element to be clickable
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        
        # Click on the element
        element.click()
        print(f"[INFO] Successfully clicked on element with ID: {element_id}")
        
    except Exception as e:
        traceback.print_exc()
        print(f"[ERROR] Failed to click on element with ID: {element_id}. Error: {e}")
        raise e
    
def click_element_by_attribute(driver, attribute_name, attribute_value):
    try:
        # Extract the unique part of the URL
        unique_part = attribute_value.split('/')[-1].split(')')[0]  # Extract the filename from URL
        safe_attribute_value = unique_part.replace("'", "\\'")
        
        # Construct XPath using contains() to match the simpler, unique part
        xpath = f"//*[contains(@{attribute_name}, '{safe_attribute_value}')]"
        print(f"[INFO] Constructed XPath now: {xpath}")

        # Find all elements that match the XPath
        elements = driver.find_elements(By.XPATH, xpath)
        print(f"[INFO] Number of elements found: {len(elements)}")

        # Print a snippet of each found element for verification
        for i, element in enumerate(elements):
            print(f"[INFO] Element {i+1}: {element.get_attribute('outerHTML')[:200]}")

        # Proceed to click the first element if any are found
        if elements:
            elements[0].click()
            print(f"[INFO] Successfully clicked on the first element with part of {attribute_name}='{safe_attribute_value}'")
        else:
            print("[INFO] No elements found to click on.")

    except Exception as e:
        traceback.print_exc()
        print(f"[ERROR] Failed to click on element with {attribute_name}='{attribute_value}'. Error: {e}")
        raise e

def click_image_in_add_button(driver):
    try:
        print("[INFO] 'add' button start.")
       # Find the element with the ID 'add'
        add_button = driver.find_element(By.ID, "add")
        
        # Within the 'add' element, find the image tag
        img_element = add_button.find_element(By.TAG_NAME, "img")
        
        # Click on the image
        img_element.click()
        print("[INFO] Successfully clicked on the image within the 'add' button.")
        
    except Exception as e:
        print(f"[ERROR] Failed to click on the image within the 'add' button. Error: {e}")

def fillAndForward(driver, text):
    # Wait for the grid body to load
    x_editor_div = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.x-editor'))
    )
    
    print("[INFO] Found the XEDITOR DIV.", x_editor_div.get_attribute("outerHTML")[:1000])
    
    x_form_field = x_editor_div.find_element(By.CSS_SELECTOR, '.x-form-field')
    
    x_form_field.send_keys(text)
    ActionChains(driver).send_keys(Keys.TAB).perform()
    time.sleep(0.5)
    return x_form_field

def parseCSV(driver):
    try:
        # read csv file
        firstFlag = True
        HAS_ACTIVITY_COL = True
        HAS_COLUMN_NAMES = True
        FILE_NAME = "./data.csv"
        input("[ACTION] Please put PAC7 and this window side by side and Press Enter to continue...")
        with open(FILE_NAME, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                if HAS_COLUMN_NAMES:
                    HAS_COLUMN_NAMES = False
                    continue
                CRUE_Approved, Tickets_Delivered, Notes, Submission_Date, Guest, Email, USC_ID, School, Count, Day, Event, Location, Time, Guest_1, Guest_2, Guest_3, Guest_4, Guest_5, Guest_6, Guest_7, Guest_8, Guest_9, Guest_10, Guest_11, Guest_12, Comments = row
                
                calculated_events = []
                print("-----------------------------------------")
                print("[INFO] Trying to issue", Count, "tickets to the event:\"", Event, "on", Day, "\"for", Email,"-",  USC_ID )
                eventinQuestion = findEvent(Event, Day, Location)
                print("Potential Event Identified:", eventinQuestion,"-", EVENT_MAP[eventinQuestion]["name"])
                calculated_events = getAllEventsToBook(eventinQuestion)
                print("The following events will be issued: ", calculated_events)
                
                event_accept = input("[ACTION] Press enter to accept or enter the eventIDs (x in COMMx) seperated by commas")
                new_temp_arr = []
                if event_accept:
                    calculated_events = event_accept.split(",")
                    err_index = 0
                    for calculated_event in calculated_events:
                        calculated_event = calculated_event.strip()
                        new_temp_arr.append(calculated_event)
                        if calculated_event not in EVENT_MAP:
                            print("[ERROR] Invalid Event ID:", calculated_event)
                            err_index += 1
                            break
                    if err_index > 0:
                        print("[ERROR] Invalid Event ID(s) found. Please correct and try again.")
                        continue
                    calculated_events = new_temp_arr
                print(Count, "Tickets being issued for the followign events", calculated_events)
                enter_text_in_element_by_id(driver, USC_ID, 'x-auto-36-input')
                click_element_by_id(driver, 'x-auto-37')
                time.sleep(0.5)
                double_click_first_entry(driver)
                time.sleep(0.5)        
                click_element_by_id(driver, "x-auto-47")
                for calculated_event in calculated_events:
                    print("$$$$$ Issuing tickets for event:", calculated_event)
                    time.sleep(0.5)
                    click_image_in_add_button(driver)
                    time.sleep(1)
                    
                    ActionChains(driver).send_keys(calculated_event).perform()
                    ActionChains(driver).send_keys(Keys.TAB).perform()
                    time.sleep(1)
                    # enter_text_in_element_by_id(driver, Count, 'x-auto-542-input')
                    ActionChains(driver).send_keys(Count).perform()
                    ActionChains(driver).send_keys(Keys.TAB).perform()
                    time.sleep(1)
                    # enter_text_in_element_by_id(driver, Count, 'x-auto-530-input')
                    # ActionChains(driver).send_keys("1").perform()
                    # ActionChains(driver).send_keys(Keys.TAB).perform()
                    # time.sleep(1)
                    # enter_text_in_element_by_id(driver, "GADD", 'x-auto-1066-input')
                    ActionChains(driver).send_keys("GADD").perform()
                    ActionChains(driver).send_keys(Keys.TAB).perform()
                    time.sleep(1)
                    # enter_text_in_element_by_id(driver, "MD", 'Disposition-input')
                    ActionChains(driver).send_keys("MD").perform()
                    ActionChains(driver).send_keys(Keys.TAB).perform()
                click_element_by_id(driver, 'x-auto-89')
                time.sleep(1)
                input("----------------------------------------- GO next?")
                try:
                    click_element_by_id(driver, 'x-auto-2423')
                    time.sleep(0.5)
                except:
                    print("NO FINISH")
                try:
                    click_element_by_id(driver, 'x-auto-2504')
                except:
                    print("NO FINISH 2")
                

                
    except Exception as e:
        # print stack trace
        traceback.print_exc()
        print("[ERROR] Something went wrong", e)
        input("Press Enter to quit. Don't forget to CHANGE THE DATA FILE FOR NEXT ITERATION.")
    input("[INFO] Done. Press Enter to quit. Don't forget to CHANGE THE DATA FILE FOR NEXT ITERATION.")

def save_cookies(driver, path):
    cookies = driver.get_cookies()
    with open(path, 'w') as file:
        json.dump(cookies, file)

def load_cookies(driver, path):
    with open(path, 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def save_local_storage(driver, path):
    local_storage = driver.execute_script("var items = {}; for (var i = 0; i < localStorage.length; i++) {var key = localStorage.key(i); items[key] = localStorage.getItem(key);} return items;")
    with open(path, 'w') as file:
        json.dump(local_storage, file)

def load_local_storage(driver, path):
    with open(path, 'r') as file:
        items = json.load(file)
        for key, value in items.items():
            driver.execute_script(f"window.localStorage.setItem('{key}','{value}');")

def openBrowser():
    driver = webdriver.Chrome()
    driver.get("https://client.paciolan.com")

    cookies_path = './cookies.json'
    local_storage_path = './local_storage.json'
    if os.path.exists(cookies_path):
        load_cookies(driver, cookies_path)
    else:
        for key, value in APP_LOCAL_STORAGE.items():
            driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
    
    if os.path.exists(local_storage_path):
        load_local_storage(driver, local_storage_path)
    else:
        for cok in APP_COOKIES:
            name, value = cok["name"], cok["value"]
            cookie = {'name': name, 'value': value}
            driver.add_cookie(cookie)
        
    if os.path.exists(cookies_path) and os.path.exists(local_storage_path):
        load_cookies(driver, cookies_path)
    
    driver.get("https://client.paciolan.com/app/orderMgmt.do#sorder")
    
    return driver

def ensureLoginAndNavToHome(driver):
    # Assuming there's a check for a login element or redirect to login page
    if not driver.find_elements(By.ID, "x-auto-36-input"):
        print("[INFO] PLEASE LOG IN AND NAVIGATE TO HOME...")
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "x-auto-36-input")))
    print("[INFO] LOGGED IN AND NAVIGATED TO HOME...")
    save_local_storage(driver, './local_storage.json')
    save_cookies(driver, './cookies.json')
    pass

def experiment(driver):
    # print the number of img tags with class=" x-btn-image"
    print("1", len(driver.find_elements(By.CSS_SELECTOR, "img.x-btn-image")))
    
    elems = driver.find_elements(By.CSS_SELECTOR, "img.x-btn-image")
    
    
    input("Press Enter to continue...")
    

if __name__ == "__main__":
    # print(parse_cookies(raw_cookie_data))
    driver = openBrowser()
    ensureLoginAndNavToHome(driver)
    parseCSV(driver)
    # parseCSV(None)
    pass