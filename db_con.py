import sqlite3
from sqlite3 import Error
import logging
import time

logger = logging.getLogger(__name__)
logging.FileHandler('logfile.log')
logging.basicConfig(filename='logfile.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')


class DbConnect:

    def __init__(self, db_path):
        self.connection = None
        self.db_path = db_path

    def get_connection(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            print("Database connected successfully.")
            logger.info("database connected successfully")
        except Error as e:
            logger.critical(f"error: {e}")
            # print(f"An Error has occurred: {e}")
        # return connection

    def insert_data(self, sql_query, values): # insert
        cursor = self.connection.cursor()
        try:
            start = time.time()
            cursor.execute(sql_query, values)
            self.connection.commit()
            end = time.time()
            logger.debug(sql_query)
            logger.debug(values)
            logger.info(f"SQL query run successfully in {end-start} s")
        except Error as e:
            print(f" Query Failed……{e}")

    def remove_accents(self, input_text):
        strange = 'ĄĆĘÓŁŚŻŹŃąćęółśżźń'
        ascii_replacements = 'ACEOLSZZNaceolszzn'
        translator = str.maketrans(strange, ascii_replacements)
        return input_text.translate(translator)

    def get_data(self, query):
        records = []
        cursor = self.connection.cursor()
        cursor.execute(query)
        # exception
        rows = cursor.fetchall()
        for row in rows:
            records.append(row)
        return records






# def get_notready(self):
#     col = []
#     cursor = self.connection.cursor()
#     cursor.execute("""SELECT
#                         name, city_id FROM cities
#                         WHERE city_id NOT IN
#                         (SELECT city_id FROM olx_data
#                         WHERE date=date('now'));
#                     """)
#     rows = cursor.fetchall()
#     for row in rows:
#         col.append(row)
#     return col


# con = DbConnect("/home/krzychu/PycharmProjects/OLX_selenium/test_table.db")
# con.get_connection()
# regions = con.get_column("regions", "name, region_id")
# cities = con.get_column("cities", "city_id, name, city_region_id")

# cities_div = {}
#
# for el in regions:
#     # print(el)
#     cities_list = []
#     for i in cities:
#         if i[2] == el[1]:
#             cities_list.append(i[1])
#     cities_div[el[0]] = cities_list
#
# print(cities_div)

# print(regions)
# print(cities)

# add_record = """
# INSERT INTO
#    olx_data(city_id, adv_sale_count, adv_rent_count, adv_exchange_count)
# VALUES
#    (4548, 629, 837, 7);
# """

# run_query(connection=con, sql_query=add_record)
