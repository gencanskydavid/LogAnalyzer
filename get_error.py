#Read files from folder C:/ProdInfo
import os,csv
#Decalaration
#
error = {}
list = []
for i in os.listdir("C:/ProdLog/P1/"):
    path = "C:/ProdLog/P1/"+i                                 #Path to file
    file = open(path,"r",encoding="utf-16")                 #Open and decode fil
#
    for i in file:
        row = i.split(',')
        if row[1] == "E03":
            if row[3] in error.keys():
                error[row[3]] = 
            error[row[0]] = row[3]
    file.close()
#
#Write result into file, C:/ProdInfo/Tact_Result.csv
#
for val in error.values():
    if val in list:
        continue
    else:
        list.append(val)
#
print (list)
#
with open('C:/ProdInfo/Tact_Result.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for k,v in error.items():
        writer.writerow([k,v])
csvfile.close()

