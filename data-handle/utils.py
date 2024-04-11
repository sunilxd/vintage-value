from bs4 import BeautifulSoup as bs
import pandas as pd
import json, pickle, requests
import agmarknetOptions
import datetime as dt



def agmarknet(from_dt:str,
              to_dt:str,
              pricearrival:tuple,
              commodity:tuple,
              state:tuple,
              )->pd.DataFrame:

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://agmarknet.gov.in/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    params = {
        'Tx_Commodity': commodity[1],
        'Tx_State': state[1],
        'Tx_District': '0',
        'Tx_Market': '0',
        'DateFrom': from_dt,
        'DateTo': to_dt,
        'Fr_Date': from_dt,
        'To_Date': to_dt,
        'Tx_Trend': pricearrival[1],
        'Tx_CommodityHead': commodity[0],
        'Tx_StateHead': state[0],
        'Tx_DistrictHead': '--Select--',
        'Tx_MarketHead': '--Select--',
    }

    response = requests.get('https://agmarknet.gov.in/SearchCmmMkt.aspx', params=params, headers=headers)

    soup = bs(response.text, 'html.parser')
    value = soup.find('input', id='__VIEWSTATE')['value']

    data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': value,
        '__VIEWSTATEGENERATOR': 'B5EE7E14',
        '__VIEWSTATEENCRYPTED': '',
        'ctl00$ddlLanguages': 'en',
        'ctl00$ddlArrivalPrice': pricearrival[1],
        'ctl00$ddlCommodity': commodity[1],
        'ctl00$ddlState': state[1],
        'ctl00$ddlDistrict': '0',
        'ctl00$ddlMarket': '0',
        'ctl00$txtDate': from_dt,
        'ctl00$ValidatorExtender1_ClientState': '',
        'ctl00$txtDateTo': to_dt,
        'ctl00$ValidatorCalloutExtender2_ClientState': '',
        'ctl00$cphBody$ButtonExcel': 'Export To Excel',
    }
    response = requests.post('https://agmarknet.gov.in/SearchCmmMkt.aspx', params=params, headers=headers, data=data).text

    response = response[response.find('<div>'):response.find('</div>')]
    soup = bs(response, 'html.parser')
    table = soup.find('table')
    rows = []
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all(['td', 'th']):
            row_data.append(cell.get_text(strip=True))
        rows.append(row_data)

    return rows

    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df