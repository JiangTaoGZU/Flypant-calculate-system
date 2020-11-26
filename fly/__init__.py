import  pymysql
pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()  #将pymsql伪装成mysql驱动,因为另外两个驱动，（1）mysqlient的兼容要求高，（2）mysql-python只支持python2