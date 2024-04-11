# %%

from utils import *
from pathlib import Path
import logging
from tqdm.auto import tqdm
import pickle
import os


logger = logging.getLogger("my_custom_logger")  # Give your logger a unique name.
handler = logging.FileHandler("data_download.log")  # Specify the log file.


logger.setLevel(logging.DEBUG)  # Set the desired log level.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


# %%
pricearrival = agmarknetOptions.price_arrival.Both
commodity = agmarknetOptions.commodities.Ajwan
state = agmarknetOptions.state.__Select__


crop_name = dir(agmarknetOptions.commodities)
fol_path = Path('New')


for crop in tqdm(crop_name):
    # if crop.startswith('__'):
    #     continue
    
    
    commodity = eval(f'agmarknetOptions.commodities.{crop}')
    file_path = fol_path / f"{commodity[0].replace('/', '-')}.feather"
    from_dt = dt.date(2000, 1, 1)
    to_dt = dt.date(2023, 9, 20)

    if file_path.is_file():
        continue

    try:

        df = []

        while from_dt < to_dt:
            cur_to_date = min(from_dt.replace(year=from_dt.year + 2), to_dt)
            response = agmarknet(from_dt.strftime('%Y-%m-%d'), cur_to_date.strftime('%Y-%m-%d'), pricearrival, commodity, state)
            
            if df:
                df += response[1:]
            else:
                df += response


            from_dt = cur_to_date + dt.timedelta(days=1)

        df = pd.DataFrame(df[1:], columns=df[0])
        df.to_feather(file_path)
        logger.info(f'{crop}, {df.shape[0]}')
        print(crop)
    
    except Exception as e:
        logging.error(f'{crop}, {e}')


