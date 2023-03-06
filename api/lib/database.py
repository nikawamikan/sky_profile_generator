import os
import MySQLdb
from MySQLdb.cursors import Cursor
from typing import Union, Optional


class DBConnection:
    """データベースに接続するためのクラスです。with句によってデータベースの接続を確保する利用法が推奨されます。
    """
    def __get_connection() -> MySQLdb.Connection:
        """コネクションを確保するための関数。内部的にしか利用しません。環境変数から接続に必要な変数を受け取ります。

        Returns:
            MySQLdb.Connection: データベースに接続したコネクション
        """

        host = "db"
        user = os.getenv("MARIADB_USER")
        passwd = os.getenv("MARIADB_PASSWORD")
        db = os.getenv("MARIADB_DATABASE")
        port = 3306
        charset = "utf8"

        connection: MySQLdb.Connection = MySQLdb.connect(
            host=host,
            user=user,
            passwd=passwd,
            db=db,
            port=port,
            charset=charset)
        return connection

    def __init__(self, auto_commit: bool = True) -> None:
        """コンストラクタでDB接続を開始します。

        Args:
            auto_commit (bool, optional): 自動でコミットするかの設定を行います。デフォルトではTrueです。
        """
        self.conn = DBConnection.__get_connection()
        self.auto_commit = auto_commit

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.auto_commit:
            self.commit()
        self.close()

    def commit(self) -> None:
        """コミットを明示的に実行します
        """
        self.conn.commit()

    def close(self) -> None:
        """接続をcloseします
        """
        self.conn.close()

    def execute(self, sql: str, *, values: Optional[tuple] = None) -> Cursor:
        """SQLを実行します
        主に戻り値を受け取らない場合に利用

        Args:
            sql (str): SQLを入力します。このSQLはvalueを%sで指定しSQLインジェクション攻撃に対して耐性を高める利用法が推奨されます
            values (Optional[tuple], optional): SQLに付随するvalueです。 Defaults to None.

        Returns:
            Cursor: カーソルを返します。
        """
        cursor: Cursor = self.conn.cursor()
        cursor.execute(sql, args=values)
        return cursor

    def select(self, sql: str, values: Optional[Union[list, tuple]] = None) -> tuple[tuple]:
        """selectを実行し結果をTupleで受け取ります

        Args:
            sql (str): SQLを入力します。このSQLはvalueを%sで指定しSQLインジェクション攻撃に対して耐性を高める利用法が推奨されます
            values (Optional[Union[list, tuple]], optional): SQLに付随するvalueです。 Defaults to None.

        Returns:
            tuple[tuple]: 行列を格納したtuple
        """
        cursor = self.execute(sql=sql, values=values)
        rows: tuple[tuple] = cursor.fetchall()
        return rows

    def insert(self, table: str, *, columns: str = None,  values: Union[list[Union[list, tuple]], tuple[Union[tuple, list]]]) -> None:
        """insert文を実行します

        Args:
            table (str): テーブル名を指定します。
            values (Union[list[Union[list, tuple]], tuple[Union[tuple, list]]]): 
                指定したテーブルに対してTupleもしくはListでデータを挿入します。
                これは複数形になるため、単一のデータでもネストする必要があります。
            columns (str, optional): カラム名を指定します。省略した場合はすべてのカラムにデータを挿入する必要があります。 Defaults to None.
        """
        column = len(values[0])
        row = len(values)
        value_str = ",".join(["%s" for _ in range(column)])
        value_str = ",".join([f"({value_str})" for _ in range(row)])

        if columns == None:
            sql = f"insert into {table} values" + value_str
        else:
            sql = f"insert into {table}({columns}) values" + value_str
        self.execute(
            sql=sql,
            values=(val for sub in values for val in sub),
        )

    def last_insert_id(self) -> int:
        """insert文で最後に入力したIDを取得します。
        Auto incrimentに設定されてない場合取得できません。

        Returns:
            int: 最後に挿入したデータのindexを返します。
        """
        cursor = self.execute("select last_insert_id()")
        return cursor.fetchone()[0]
