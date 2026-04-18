# Подмена MySQLdb для Django на хостингах без mysqlclient (Beget: PyMySQL).
try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass
