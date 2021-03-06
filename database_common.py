# Creates a decorator to handle the database connection/cursor opening/closing.
# Creates the cursor with RealDictCursor, thus it returns real dictionaries, where the column names are the keys.
import os

import psycopg2
import psycopg2.extras

connection_string = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(
    "postgres://wfcewjcymznnur:b39d50024622c1fdd6e5bed138e4c46181c6c6eec0690a18e4dd9d289104c614@ec2-54-78-36-245.eu-west-1.compute.amazonaws.com:5432/dfupb3jad2bns9",
    sslmode="require",
)

# os.environ['PSQL_USER_NAME'] ='keitkalon'
# os.environ['PSQL_PASSWORD'] ='0000'
# os.environ['PSQL_HOST'] ='localhost'
# os.environ['PSQL_DB_NAME'] ='yolp_db'

# def get_connection_string():
#     # setup connection string
#     # to do this, please define these environment variables first
#     user_name = os.environ.get('PSQL_USER_NAME')
#     password = os.environ.get('PSQL_PASSWORD')
#     host = os.environ.get('PSQL_HOST')
#     database_name = os.environ.get('PSQL_DB_NAME')
#
#     env_variables_defined = user_name and password and host and database_name
#
#     if env_variables_defined:
#         # this string describes all info for psycopg2 to connect to the database
#         return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
#             user_name=user_name,
#             password=password,
#             host=host,
#             database_name=database_name
#         )
#     else:
#         raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection = psycopg2.connect(
            "postgres://wfcewjcymznnur:b39d50024622c1fdd6e5bed138e4c46181c6c6eec0690a18e4dd9d289104c614@ec2-54-78-36-245.eu-west-1.compute.amazonaws.com:5432/dfupb3jad2bns9",
            sslmode="require",
        )

        connection.autocommit = True
        return connection
    except psycopg2.DatabaseError as exception:
        print("Database connection problem")
        raise exception


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper
