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

folder = Path('../data/weather_org')

current_date = start_date
while current_date <= end_date:
    cur_date = current_date.strftime("%Y-%m-%d")
    print(cur_date)
    file_path = folder / cur_date

    if file_path.is_file():
        current_date += timedelta(days=1)
        continue

    files['date'] = (None, cur_date)
    response = requests.post(
        'https://beta-tnsmart.rimes.int/index.php/Rainfall/daily_data',
        files=files,
    )
    with open(file_path, 'wb') as f:
        pickle.dump(response.text, f)

    current_date += timedelta(days=1)



