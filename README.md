# get_sql

function get_df -> return pandas dataframe:
parameters:
- user_query (query or link to .sql)
- replacement (dictionary where key = old text to be replaced, value = new text)
- connection (connection object to be used in pandas.read_sql function: default OLAP-DWH-02:OlapDataSourceTemp2017 sqlalchemy.engine.base.Connection)
- kwargs (any parameters of pandas.read_sql function)

function save_me:
mirror to pandas.to_excel

function create_fn -> text:
creates filename from text of query
