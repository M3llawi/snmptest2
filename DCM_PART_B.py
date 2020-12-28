import numpy as np
import matplotlib.pyplot as plt
import time
import schedule
import sys
from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen
import csv
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import matplotlib.pyplot as plt;plt.rcdefaults()






 # Email

def sentmail():
    smtpHost = 'smtp.gmail.com'
    smtpPort = 465
    username = 'test.test.dcm123@gmail.com'
    password = '201501579*'
    sender = 'test.test.dcm123@gmail.com'
    targets = [Semail]

    Subject = 'SNMP report'

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(targets)
    msg['Subject'] = Subject
    fileName = 'output.csv'
    attachment = open(fileName, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + fileName)
    msg.attach(part)
    fileName2 = 'graph.png'
    attachment2 = open(fileName2, 'rb')
    part2 = MIMEBase('application', 'octet-stream')
    part2.set_payload(attachment2.read())
    encoders.encode_base64(part2)
    part2.add_header('Content-Disposition', "attachment; filename= " + fileName2)
    msg.attach(part2)
    server = smtplib.SMTP_SSL(smtpHost, smtpPort)
    server.login(username, password)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()
    print("The report has been sent to ",Semail)
    sys.exit()
    
    #Plotting the graph into png file

def plot (ram, cpu):
    objects = ('RAM','CPU')
    y_pos = np.arange(len(objects))
    t = [ram, cpu]
    plt.clf()
    plt.bar(y_pos, t, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('RAM usage')
    plt.savefig("graph.png")
    plt.show()

def getinfo ():
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               UsmUserData('privUser', 'AuthPasswor', 'CryptoPassword'),
               UdpTransportTarget(('172.16.1.80', 161)),
               ContextData(),
               #Total RAM OID
               ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.4.5.0')),
               #RAM 
               ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.4.6.0')),
               #CPU Usage
               ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.11.9.0')),
               #System info
               ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.10.1.3.3')),
               #CPU load 15 
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
    )


    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1] or '?'))

    else:
        percentage = []
        print("Getting Information from the server")
        for system, percent in varBinds:
            percentage.append(str(percent))
        with open('output.csv', 'a') as File:
            # Create CSV file and Write to file
            writer = csv.writer(File, delimiter=',')
            write = ['Total RAM', 'RAM', 'CPU','CUP 15 min' ,'System information','Time']
            writer.writerow(write)
            writer.writerow(percentage)
            File.close()
            y = int(percentage[0])
            p = int(percentage[1])
            x = y / 100
            ram = p / x
            cpu = int(percentage[2])
            tim11e=now.strftime
            plot(ram, cpu)

            if int(ram) >= 70 or int(cpu) >= 70:
                sentmail()
            time.sleep(10)



schedule.every().day.at("14:00").do(sentmail)



################################################


print('************************************************************************')
print('Please Enter the username and the password to start \n*Note* Password and Username are hardcoded \n*The Schedule email will be sent at 14:00 everyday ')
x=0
now = datetime.datetime.now()
while x < 3:
    username = input('Enter username: ')
    password = input('Enter password: ')
    if password=='1' and username=='allawi':
        print('Welcome', username)
        print("Scanning .....")
        Semail = input('Which email you want to send the report to: ')
        print (" The reported generated at:  ")
        print (now.strftime("%Y-%m-%d %H:%M:%S"))
        getinfo()
        schedule()
        sentmail()
        print('************************************************************************')
        break
    else:
        print('Access denied. Try again.')
        x += 1

