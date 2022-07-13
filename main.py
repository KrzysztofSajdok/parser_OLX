#!/home/krzychu/PycharmProjects/parser_OLX/venv/bin/python

from db_con import DbConnect
from sel_source import SelRequest
import logging
import time
import csv
from datetime import date


def removeaccents(input_text):
    strange = 'ĄĆĘÓŁŚŻŹŃąćęółśżźń'
    ascii_replacements = 'ACEOLSZZNaceolszzn'
    translator = str.maketrans(strange, ascii_replacements)
    return input_text.translate(translator)


logger = logging.getLogger(__name__)
logging.FileHandler('logfile.log')
logging.basicConfig(filename='logfile.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')


con = DbConnect("olx_data.db")
con.get_connection()

cities = con.get_data("""select city_id, name, is_dubble 
                        from custom where city_id not in 
                        (select city_id from olx_data 
                        where date = date('now'));""")

url_base = 'https://www.olx.pl/d/nieruchomosci/mieszkania/'
cities_list = [(url_base + removeaccents(i[1]).lower().replace(" ", "-") + i[2] + '/', i[0]) for i in cities]


for i in cities_list:
    start = time.time()
    curTime = date.today()
    row = SelRequest(i[0]).get_olx_stats()
    row.append(i[1])
    row.append(curTime)
    record = """
                INSERT INTO
                    olx_data(adv_rent_count, adv_sale_count, adv_exchange_count, city_id, date)
                VALUES
                    (?, ?, ?, ?, ?); """
    con.run_query(record, row)
    end = time.time()
    logger.info(f'executed in {end-start}')


# with open('first.csv', 'rb') as inp, open('first_edit.csv', 'wb') as out:
#     writer = csv.writer(out)
#     for row in csv.reader(inp):
#         if row[2] != "0":
#             writer.writerow(row)

# add_record = """
# INSERT INTO
#    olx_data(city_id, adv_sale_count, adv_rent_count, adv_exchange_count)
# VALUES
#    (4548, 629, 837, 7);
# """


# cities_div_urls = {}
# url_base = 'https://www.olx.pl/d/nieruchomosci/mieszkania/'
#
# for el in regions:
# cities_list = [(url_base+removeaccents(i[1]).lower().replace(" ", "-")+'/', i[0]) for i in cities if i[2] == el[1]]
# cities_div_urls[el[0]] = cities_list
#
# reg_urls = [(url_base+removeaccents(el[0]).lower()+'/', el[1]) for el in regions]

# select c.city_id, o.city_id from cities c left join
# (select city_id from olx_data where date = date('now')) o on o.city_id=c.city_id;

# select name, city_id from cities where city_id not in
# (select city_id from olx_data where date=date('now'));

# select name from olx_data join cities on olx_data.city_id = cities.city_id where date = date('now');

# select c.city_id, c.name, c.is_dubble
#                         from custom c left join
#                         (select city_id from olx_data where date = date('now')) o
#                         on o.city_id=c.city_id;
