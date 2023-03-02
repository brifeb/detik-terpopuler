import os
import app
import pathlib
import datetime

print('Update Detik Populer starting..')

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


kategori = ['detikcom', 'news', 'finance', 'hot', 'inet', 'sport', 'oto', 'travel', 'sepakbola',
            'food', 'health', 'wolipop', 'edu', 'jateng', 'jatim', 'jabar', 'sulsel', 'sumut', 'bali', 'hikmah']

for kat in kategori:
    app.get_populer(kat)
print('update done!')

#cek
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data/")
data_file = '{}detik-{}.json'.format(DATA_DIR, kategori[0])
fname = pathlib.Path(data_file)
mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
update_time = mtime.strftime("%d %b %X")
print("Check \nFile: {}\nLast update: {}".format(data_file, update_time))