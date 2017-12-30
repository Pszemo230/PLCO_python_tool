import pandas
import pymysql
from sklearn.preprocessing import MinMaxScaler

from query_loader import QueryLoader


class MySqlFetcher:
    def __init__(self, scaler=MinMaxScaler(), query_loader=QueryLoader()):
        self.db_connection = self.open_connection()
        self.data_set = pandas.DataFrame()
        self.data_set_normalized = pandas.DataFrame()
        self.scaler = scaler
        self.query_loader = query_loader

    def open_connection(self):
        return pymysql.connect(host='localhost',
                               user='root',
                               password='root',
                               db='prostate_screening',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

    def close_connection(self):
        self.db_connection.close()

    def run_select_query(self, query, arguments=None):
        query_result = pandas.read_sql_query(query, self.db_connection, params=arguments)
        query_result = query_result.apply(pandas.to_numeric)
        self.data_set = query_result
        self.normalize_data_set()
        return self.data_set

    def print_data_set_stats(self):
        print("DataSet Shape:")
        print(self.data_set.shape)
        print("DataSet Stats:")
        print(self.data_set.describe(include='all'))

    def print_scaled_data_set_stats(self):
        print("DataSet Shape:")
        print(self.data_set_normalized.shape)
        print("DataSet Stats:")
        print(self.data_set_normalized.describe())

    def normalize_data_set(self):
        self.data_set_normalized = pandas.DataFrame(self.scaler.fit_transform(self.data_set.iloc[:, 0:-1]))

    def get_X(self):
        return self.data_set_normalized.values

    def get_Y(self):
        return self.data_set.values[:, -1]

    def run_select_query_from_file(self, file_name):
        query = self.query_loader.load_query(file_name)
        self.run_select_query(query)