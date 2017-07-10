# -*- coding: utf-8 -*-
#http://stackoverflow.com/questions/4613465/using-python-to-write-mysql-query-to-csv-need-to-show-field-names
import sys
import csv
import pymysql
import time

db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="goal",
                     db="goal")
cur = db.cursor()
number_rows = 100
number_ID = 0
try:

    while True:
        # Check if there are rows which are not transfered into an CSV
        number_ID=69
        count_ID=0
        print("before SQL")
        print(number_ID)
        cur.execute("SELECT COUNT(ID) FROM xy WHERE upload_status = 0")
        count_ID = cur.fetchall()
        for row in count_ID:
            number_ID=row[0]
        print("after SQL")
        print(number_ID)
        # If there are more rows than number_rows then create a CSV file
        if number_ID > number_rows:
            #Find the lowest ID where x/y is not uploaded and save it in the min_ID variable
            cur.execute("SELECT min(ID) FROM xy WHERE upload_status = 0")
            results2 = cur.fetchall()
            for row in results2:
                min_ID=row[0]

            #Set the max_ID which is included in the csv file
            max_ID=min_ID+number_rows-1

            #set the filename of the CSV with file100-1002.csv
            file_number = "%d" % min_ID+"-"+"%d" % max_ID
            filename = "file%s.csv" % file_number

            #Select all the necessary parameters
            cur.execute("SELECT table_ID,timestamp,x,y FROM xy WHERE upload_status = 0 ORDER BY ID limit %s", (number_rows))
            results = cur.fetchall()

            #Write the results in the csv
            fp = open(filename, 'w')
            myFile = csv.writer(fp, lineterminator='\n')
            myFile.writerows(results)
            fp.close()

            #Update the upload_status to 1
            cur.execute("UPDATE xy SET upload_status=1 WHERE ID<=%s ", (max_ID))
            db.commit()
        #if there are to less rows wait 60sec
        if number_ID < number_rows:

            print("waiting")
            time.sleep(5)
            db.commit()
except KeyboardInterrupt:
    cur.close()
