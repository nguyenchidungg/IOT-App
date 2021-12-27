import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="thoi_tiet"
)

mycursor = db.cursor()

now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
# mycursor.execute("INSERT INTO thoi_tiet (Time, Temp, Humi) VALUES (%s, %s, %s)", (formatted_date, "33","72"))
# db.commit()
mycursor.execute("SELECT * FROM thoi_tiet ORDER BY id DESC LIMIT 10")
rows = mycursor.fetchall()
listdata=[]
print(type(rows))
for i in rows:
    print(i[0])
# print(rows)
# for x in range(len(rows)):
#     print(x)
    # dictdata={
    #     "id":x[0][0],
    #     "Time":str(x[0][1]),
    #     "Temp":x[0][2], 
    #     "Humi":x[0][3]
    # }
    # listdata.append(dictdata)
    # print(listdata)

