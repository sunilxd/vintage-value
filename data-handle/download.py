# %%
### Initial request
from utils import *
from pathlib import Path
import logging
from tqdm.auto import tqdm
import pickle


logger = logging.getLogger("my_custom_logger")  # Give your logger a unique name.
handler = logging.FileHandler("data_download.log")  # Specify the log file.

# Configure the log level and format for this custom logger
logger.setLevel(logging.DEBUG)  # Set the desired log level.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the custom logger
logger.addHandler(handler)

from_dt = dt.date(2015, 1, 1).strftime('%Y-%m-%d')
to_dt = dt.date(2023, 9, 20).strftime('%Y-%m-%d')
pricearrival = agmarknetOptions.price_arrival.Price
commodity = agmarknetOptions.commodities.Ajwan
state = agmarknetOptions.state.__Select__


# %%
crop_name = dir(agmarknetOptions.commodities)
fol_path = Path('Data')

# %%
# commodity = crop_name[0]

for crop in tqdm(crop_name):
    if crop.startswith('__'):
        continue

    
    commodity = eval(f'agmarknetOptions.commodities.{crop}')
    pkl_path = fol_path / f"{commodity[0].replace('/', '-')}.pickle"
    file_path = fol_path / f"{commodity[0].replace('/', '-')}.feather"
    print(file_path)

    if pkl_path.is_file() or file_path.is_file():
        continue

    try:
        response = agmarknet(from_dt, to_dt, pricearrival, commodity, state)
        with open(pkl_path, 'wb') as f:
            pickle.dump(response, f)
            
        df = get_df(response)
        df.to_feather(file_path)
        logger.info(f'{crop}, {df.shape[0]}')
    
    except Exception as e:
        logging.error(f'{crop}, {e}')
    


