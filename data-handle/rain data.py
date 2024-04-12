# %%
import requests
from pathlib import Path
from datetime import datetime, timedelta
import pickle

# %%

start_date = datetime(2015, 1, 1)
end_date = datetime.now()

files = {
    'type': (None, '1'),
    'date': (None, '2015-04-01'),
    'submit': (None, 'சமர்ப்பிக்கவும்'),
}

folder = Path('weather_org')

current_date = start_date
while current_date <= end_date:
    cur_date = current_date.strftime("%Y-%m-%d")

    files['date'] = (None, cur_date)
    response = requests.post(
        'https://beta-tnsmart.rimes.int/index.php/Rainfall/daily_data',
        files=files,
    )
    with open(folder / cur_date, 'wb') as f:
        pickle.dump(response.text, f)

    print(cur_date)
    current_date += timedelta(days=1)



