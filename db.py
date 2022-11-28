import os

import pyodbc


def sql_execute(query, param):
    # クエリ実行(パラメータがない場合は実行無し)
    if not param:
        return None

    # DB接続文字列生成
    conn_str = _create_connection_string()
    conn = None
    cursor = None
    try:
        # 対象のSQLServerに接続
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # SQL実行
        result = cursor.execute(query, param)
        column_list = [column[0] for column in result.description]
        rows = cursor.fetchall()

    except pyodbc.Error as err:
        print(f'DB Connection Error : {err}')
        raise err
    finally:
        # DB接続のクローズ
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

    return rows, column_list


def _create_connection_string():
    # SQLServer接続の設定
    driver = '{' + os.environ['GXP_ODBC_DRIVER'] + '}'
    server = os.environ['GXP_DB_ENDPOINT']
    db = os.environ['GXP_DB_NAME']
    user = os.environ['GXP_DB_USERNAME']
    password = os.environ['GXP_DB_PASSWORD']
    # 接続情報文字列の生成
    return f'DRIVER={driver};SERVER={server};DATABASE={db};UID={user};PWD={password};'