######################################
# Purpose:    Analyze log files from ALBOT, write result of errors into Result_(ProcessNumber).csv
#	      Since version 0.4.1 write also production counter information such as input,output and failure
#             Since version 0.5.0 separete what kind of NG was send as NG and what pass on retry action.
# Created by: David ALCZ 
# Date:       2018/1/6
# Ver.:       0.5.3
######################################
#
#Read files from folder C:/ProdLog/Px
import os,csv,time
#Decalaration
#
def onlyMess(mess,number):
    '''
    :param mess:
    :param number:
    :return:
    '''
    out = mess.split(',')
    return out[number]
#
error = {"Error Name":"Occurence rate"} 		    #Declare dict and head of table 
counter = {"Failure":0,"Output":0,"Input":0}
NG = {"End as NG":"Messeage"}
buffer = [""]                                               #Clear the buffer value
a = 1
DownTime = 0                                                #Variable for calculating downtime as if cycle time is over 35 sec then, cycle time - 35 sec.
Waiting = 0                                                 #Variable for calculating waiting time as End time - Start time
#
#Load all files
#
process = input("Select process:(1,2,3,..):")               #Open input window for user, to select process number 
for i in os.listdir("C:/ProdLog/P"+process+"/"):
    path = "C:/ProdLog/P"+process+"/"+i                     #Path to file
    file = open(path,"r",encoding="utf-16")                 #Open and decode fil
#
#Processing all files
#
    for i in file:                                   
        buffer.append(i)                                    #Copy actual line into buffer
        row = i.split(',')				    #Split each line of file, based on comma
        if row[1] == "E03":				    #Check if first element is "E03"(Error code)
            if row[3] in error.keys():			    #Check if error is already in dictionary.index
                error[row[3]] += 1			    #Increment value of index 	
            else:
                error[row[3]] = 1			    #Create new index
        elif row[1] == "E2":
            counter["Failure"] +=1			    #Increment Failure counter
            NG["End as NG"+str(a)] = onlyMess(buffer[-3],3)
            a += 1
        elif row[1] == "E0":
            counter["Input"] +=1			    #Increment Input counter
        elif row[1] == "E1":
            counter["Output"] +=1			    #Increment Output counter
        elif row[1] == "D06":
            if float(row[3]) > 35.0:
                DownTime += float(row[3]) - 35.0
    file.close()
#
#Show result to console
#
temp1 = (counter["Output"])
print ("Effectivnes:"+str(len(NG)/temp1*100))
print ("DownTime was: ",DownTime/60)
#print ("Waiting for parts: ",Waiting/60)
#
#Write result into file, C:/ProdLog/Result_(ProcessNumber).csv
#
with open('C:/ProdLog/Result_'+process+'.csv', 'w', newline='') as csvfile:		#Create new file for write all result
    writer = csv.writer(csvfile)
#
    for k,v in error.items():
        writer.writerow([k,v])
    writer.writerow("")									#Write plain row to separete error and counter information
#
    for k,v in counter.items():
    	writer.writerow([k,v])
    writer.writerow("")
#    
    for v in NG.items():
        writer.writerow([v])
    writer.writerow("")
    print ("Downtime was: "+str(DownTime/60), file=csvfile)
csvfile.close()
#    writer.write("Downtime was: "+str(DownTime/60))
#    writer.writerow("")
#    writer.writerow("Waiting for parts: "+str(Waiting/60))
#    writer.writerow("")										#Close file after result has writte
