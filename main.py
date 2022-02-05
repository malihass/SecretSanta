import numpy as np
import smtplib
import imaplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
sys.path.append('utils')
import myparser

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~ Parse input
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

inpt = myparser.parseInputFile()
hostEmail = inpt['hostEmail']
hostPassword = inpt['hostPassword']

def send_email(name, email, nameReceiver):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(hostEmail,hostPassword)
    subject = 'Secret Santa 2021!'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = "The Secret Santa Corporation"
    msg['To'] = email
    
    body = 'Hi ' + name + '!' + '<br>' + \
           "It is that time of the year again: welcome to the 2021 edition of the Tenney family's Secret Santa!<br><br>" + \
           'You have been assigned the following person for Secret Santa : ' +  nameReceiver + '!<br><br>' + \
           'Link to the google doc for gifts: https://XXXXXX <br><br>' + \
           'The Secret Santa Corporation prides itself in satisfying its loyal clients and keeps innovating to make your Christmas experience even more magical.<br>' + \
           'This year, we have ensured that your Secret Santa is different than the past two years.<br>' + \
           'If you are not satisfied with your Secret Santa, message our assistant Malik: XXX@XXX.XXX <br>' + \
           'If you need to sue the Secret Santa Corporation, we may be served at the following address: XXX@XXX.XXX <br><br>' + \
           'Additional instructions: <br>&nbsp;&nbsp;&nbsp;&nbsp;1) On your gift, please indicate the name of the receiver and include the word "Rudolph". Example: Senna sends a gift to James. After wrapping the gift, Senna adresses it to "James Rudolph Tenney".<br>'+ \
           '&nbsp;&nbsp;&nbsp;&nbsp;2) Hannah, Josiah and Isaac do not have Secret Santas. Remember to send them something too!<br><br>' + \
           '<b>Merry Christmas ! <3 Joyeux Noel ! <3 Bark Bark ! <3<b><br><br>'
  
    body += """\
    <html>
      <head></head>
      <body>
        <p align="center"><b><font style="color: red;">The Secret </font><font style="color: green;">Santa Corporation</b></p>
      </body>
    </html>
    """

    part1 = MIMEText(body, 'html')
    
    msg.attach(part1) # text must be the first one

    server.sendmail(hostEmail, email, msg.as_string())
   
    print(' Email has been sent ' )
    server.quit()

def deleteSentEmails():
    box = imaplib.IMAP4_SSL('smtp.gmail.com', 993)
    box.login(hostEmail,hostPassword)
    box.select('"[Gmail]/Sent Mail"')
    typ, data = box.search(None, 'ALL')
    for num in data[0].split():
        box.store(num, '+FLAGS', '\\Deleted')
    box.expunge()
    box.close()
    print(' Send box emptied ' )
    box.logout()

    
# ~~~~ List of attendees
Attendees = []

dummyemail = 'test123@gpail.cop' 

# Name of guest /  email adress / person guest gave to the past years
Attendees.append(['Dad Tenney',   'test123@gpail.cop',     ['Mom Tenney','Jason']])
Attendees.append(['Mom Tenney',   'test123@gpail.cop'    ,     ['Amy','Kristin','Dad Tenney','Malik']])
Attendees.append(['Wendy',        'test123@gpail.cop',       ['Dad Tenney','Amy','Aaron']])
Attendees.append(['Aaron',        'test123@gpail.cop',       ['Beth','Malik','Wendy']])
Attendees.append(['Amy',          'test123@gpail.cop',      ['Jason','Dad Tenney', 'Kristin']])
Attendees.append(['Beth',         'test123@gpail.cop',        ['Malik','Mom Tenney']])
Attendees.append(['Jason',        'test123@gpail.cop',         ['Wendy','Beth','Amy']])
Attendees.append(['Kristin',      'test123@gpail.cop',          ['Aaron','Wendy','Malik']])
Attendees.append(['Malik',        'test123@gpail.cop',  ['Kristin','Aaron','Dad Tenney']])


# ~~~~ List of previous pairs
PreviousGiver =       [ entry[0] for entry in Attendees ]
PreviousReceiver =    [ entry[2] for entry in Attendees ]



# ~~~~ Figure out who gives to who
nGuests = len(Attendees)
Receivers = list(range(nGuests))
listNames = [ entry[0] for entry in Attendees]


def fillGivers (Receivers, nGuests, listNames):
    Givers = []
    for i in range(nGuests):
        # Make a list of potential givers that could give to person i
        PotentialGivers = Receivers.copy()
    
        # Remove the receiver
        PotentialGivers.pop(PotentialGivers.index(i))

        # Did I give to you before ? If yes, remove me from givers list
        nameReceiver = listNames[i]
        for igiver, giver in enumerate(Attendees):
            if nameReceiver in giver[2]:
               PotentialGivers.pop(PotentialGivers.index(igiver)) 
     
        # Remove people who already gave
        for igiver in Givers:
            if igiver in PotentialGivers:
                PotentialGivers.pop(PotentialGivers.index(igiver)) 
       
        # Choose any of the potential givers
        giverID = random.choice(PotentialGivers)
        Givers.append(giverID)
 
    return Givers


# Try until it works
Givers = None
nFailure = 0
while Givers is None:
    try:
        # connect
        Givers = fillGivers (Receivers, nGuests, listNames)
    except:
         nFailure += 1
         

print('Failed ' + str(nFailure) + ' times')




# ~~~~ LOG
for i in range(nGuests): 
    string = Attendees[Givers[i]][0] + ' gives to ' + Attendees[Receivers[i]][0]
    string += ' / ' 
    if len(Attendees[Givers[i]][2])==0:
        string += ' nobody '
    else:
        for ientry in range(len(Attendees[Givers[i]][2])):
            string += Attendees[Givers[i]][2][ientry]
            if not ientry==len(Attendees[Givers[i]][2])-1:
                string += ' and '
    string += ' before '

    print(string)





## ~~~~ Now Send emails
#for i in range(nGuests):
#    send_email(Attendees[Givers[i]][0], Attendees[Givers[i]][1], Attendees[Receivers[i]][0]) 


## Delete Emails sent so I cannot know who gives what
#deleteSentEmails()
