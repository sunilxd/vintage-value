# %%
import requests
from pathlib import Path
from datetime import datetime, timedelta
import logging

from utils import *
from tqdm.auto import tqdm


logger = logging.getLogger("tn-download")
handler = logging.FileHandler("data_download.log")


logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


pricearrival = agmarknetOptions.price_arrival.Both
state = agmarknetOptions.state.__Select__


crop_name = dir(agmarknetOptions.commodities)
fol_path = Path('TN')


for crop in tqdm(crop_name):
    
    commodity = eval(f'agmarknetOptions.commodities.{crop}')
    file_path = fol_path / f"{commodity[0].replace('/', '-')}.feather"
    from_dt = dt.date(2010, 1, 1)
    to_dt = dt.date(2024, 4, 11)

    if file_path.is_file():
        continue

    try:

        df = []

        while from_dt < to_dt:
            cur_to_date = min(from_dt.replace(year=from_dt.year + 5), to_dt)
            response = agmarknet(from_dt.strftime('%Y-%m-%d'), cur_to_date.strftime('%Y-%m-%d'), pricearrival, commodity, state)
            
            if df:
                df += response[1:]
            else:
                df += response


            from_dt = cur_to_date + dt.timedelta(days=1)

        if df:
            df = pd.DataFrame(df[1:], columns=df[0])
            df.to_feather(file_path)
            logger.info(f'{crop}, {df.shape[0]}')
        else:
            with open(file_path, 'wb') as f:
                f.write("")
    
    except Exception as e:
        logging.error(f'{crop}, {e}')
