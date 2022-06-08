import requests
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

from flask import Flask, render_template, url_for, flash, redirect, request, session, make_response
import xlrd, datetime
import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import date
from sharepoint import SharePointSite, basic_auth_opener

test_url = "https://msa2.sharepoint.com/sites/mmlleerlingen/Planner/HAVO%204.xlsx?web=1"
HAVO3_link = "https://msa2.sharepoint.com/sites/mmlleerlingen/Planner/HAVO%203.xlsx?web=1"
HAVO4_link = "https://msa2.sharepoint.com/sites/mmlleerlingen/Planner/HAVO%204.xlsx?web=1"
HAVO5_link = "https://msa2.sharepoint.com/sites/mmlleerlingen/Planner/HAVO%205.xlsx?web=1"
VWO4_link = "https://msa2.sharepoint.com/sites/mmlleerlingen/Planner/VWO%204.xlsx?web=1"
VWO5_link = "https://msa2.sharepoint.com/sites/mmlleerlingen/Planner/VWO%205.xlsx?web=1"
VWO6_link = "https://msa2.sharepoint.com/sites/mmlleerlingen/Planner/VWO%206.xlsx?web=1"

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

def HAVO3():
    ctx_auth = AuthenticationContext(HAVO3_link)
    ctx_auth.acquire_token_for_user(username, word)
    ctx = ClientContext(HAVO3_link, ctx_auth)
    response = File.open_binary(ctx, "/Shared Documents/User Guide2.xlsx")
    with open("./excelfiles/3H planner.xlsx", "wb") as local_file:
        local_file.write(response.content)

def HAVO4():
    ctx_auth = AuthenticationContext(HAVO4_link)
    ctx_auth.acquire_token_for_user(username, word)
    ctx = ClientContext(HAVO4_link, ctx_auth)
    response = File.open_binary(ctx, "/Shared Documents/User Guide2.xlsx")
    with open("./excelfiles/4H planner.xlsx", "wb") as local_file:
        local_file.write(response.content)

def HAVO5():
    ctx_auth = AuthenticationContext(HAVO5_link)
    ctx_auth.acquire_token_for_user(username, word)
    ctx = ClientContext(HAVO5_link, ctx_auth)
    response = File.open_binary(ctx, "/Shared Documents/User Guide2.xlsx")
    with open("./excelfiles/5H planner.xlsx", "wb") as local_file:
        local_file.write(response.content)

def VWO4():
    ctx_auth = AuthenticationContext(VWO4_link)
    ctx_auth.acquire_token_for_user(username, word)
    ctx = ClientContext(VWO4_link, ctx_auth)
    response = File.open_binary(ctx, "/Shared Documents/User Guide2.xlsx")
    with open("./excelfiles/4V planner.xlsx", "wb") as local_file:
        local_file.write(response.content)

def VWO5():
    ctx_auth = AuthenticationContext(VWO5_link)
    ctx_auth.acquire_token_for_user(username, word)
    ctx = ClientContext(VWO5_link, ctx_auth)
    response = File.open_binary(ctx, "/Shared Documents/User Guide2.xlsx")
    with open("./excelfiles/5V planner.xlsx", "wb") as local_file:
        local_file.write(response.content)

def VWO6():
    ctx_auth = AuthenticationContext(VWO6_link)
    ctx_auth.acquire_token_for_user(username, word)
    ctx = ClientContext(VWO6_link, ctx_auth)
    response = File.open_binary(ctx, "/Shared Documents/User Guide2.xlsx")
    with open("./excelfiles/6V planner.xlsx", "wb") as local_file:
        local_file.write(response.content)

def get_all_files():
    HAVO3()
    HAVO4()
    HAVO5()
    VWO4()
    VWO5()
    VWO6()
