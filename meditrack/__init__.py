import pymysql

pymysql.install_as_MySQLdb()
# Django 4.2+ requires mysqlclient >= 2.2.1; PyMySQL still exposes 1.4.6 for
# MySQLdb compatibility. Bump the advertised version so the backend loads.
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.__version__ = "2.2.1"