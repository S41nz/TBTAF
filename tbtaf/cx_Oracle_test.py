import cx_Oracle
import os
import pandas as pd

os.environ['TNS_ADMIN'] = '/Users/david.torres/Documents/MCAP/system-desing/TBTAF/tbtaf/adb_virt_env'
connection = cx_Oracle.connect('admin', 'Miaalejandra2005!', 'db202204021419_medium')
cursor = connection.cursor()
rs = cursor.execute("SELECT * FROM test_suite")
df = pd.DataFrame(rs.fetchall())
print(df.columns)

cursor.execute("INSERT INTO SomeTable VALUES(:now)", {'now': datetime.datetime.now()})
