#Capture User Name for Account creation, Empty string not allowed
def ENTER_USER_NAME():
    U=input("Enter Username: ")           #User name
    if U=='':
        print("User name can not be empty...Retry")
        U=input("\nEnter Username: ")     #User name
        if U=='':
            print("Number of retry exceeded...")
            exit()
    return(U)

#Create User Account, Store Name & Password in table
#User Name already existing is Not allowed
def CREATE_ACCOUNT():
    cur.execute("create table if not exists LoginDetails(UserName char(25),Account_password char(20))")
    U=ENTER_USER_NAME()
    cur.execute("select Account_password from LoginDetails where UserName like '%s'"%(U))
    data=cur.fetchall()      #Fetch data from table to check if User exits
    if any(data):
        print("Username already exist... Try another name !!!\n")
        U=ENTER_USER_NAME()
        cur.execute("select Account_password from LoginDetails where UserName like '%s'"%(U))
        data=cur.fetchall()  #Fetch data from table to check if User exits
        if any(data):
            print("Username already exist... Try another name !!!")
            exit()
  
    Pa=input("Enter Password: ")          #Password
    if Pa=='':
        print("Password can not be empty...Retry")
        Pa=input("\nEnter Password: ")      #Password
        if Pa=='':
            print("Number of retry exceeded...")
            exit()
    E=input("Enter Email ID: ")     #Email
    print("Congratulations!!! Your Account has been successfully created.\n")
    cur.execute("insert ignore into LoginDetails values(%s,%s)",(U,Pa))
    con.commit()
        
#Login to User Account using Name & Password
def LOGIN_ACCOUNT():
    print("\nEnter Login details...")
    L=ENTER_USER_NAME()
    P=input("Enter Password: ")
    cur.execute("select Account_password from LoginDetails where UserName like '%s'"%(L))
    data=cur.fetchall()  #Fetch data from table to check if User exits
    if any(data):
        cur.execute("select Account_password from LoginDetails where UserName like '%s'"%(L))
        data1=cur.fetchone()   #Fetch password from table & compare
        if data1[0]==P:
            print("\t!!! Logged in successfully !!!")
        else:
            print("\n\t!!! Wrong Password !!!")
            exit()
    else:
        print("\n\t!!! User doesnot exist !!!\n\t!!! Create Account!!!")
        exit()
        
#Capture Traveller details..No of Adults, Kids, Gender...
def TRAVELLER_DETAILS():
    print("\nTRAVELLER DETAILS")
    Adult=int(input("NO. OF ADULTS (12+yrs): "))
    if No_passenger>=Adult:
        Kid=No_passenger-Adult
        print("NO. OF CHILD (2-12yrs): ",Kid)
       
        for i in range(Adult):
            print("\nENTER ADULT",i+1,"DETAILS")
            Fname=input("FIRST NAME: ")
            Lname=input("LAST NAME : ")
            NAME=Fname+' '+Lname
            print("GENDER - PRESS: 1.MALE  2.FEMALE")
            Gender=int(input("ENTER GENDER: "))
            if Gender==1:
                GENDER='MALE'
            elif Gender==2:
                GENDER='FEMALE'
            else:
                GENDER='MALE-default'
            cur.execute("insert ignore into PassengerDetails values(%s,%s)",(NAME,GENDER))
            con.commit()
        
        for i in range(Kid):
            print("\nENTER KID",i+1,"DETAILS")
            Fname=input("FIRST NAME: ")
            Lname=input("LAST NAME : ")
            NAME=Fname+' '+Lname
            print("GENDER - PRESS: 1.MALE  2.FEMALE")
            Gender=int(input("ENTER GENDER: "))
            if Gender==1:
                GENDER='MALE'
            elif Gender==2:
                GENDER='FEMALE'
            else:
                GENDER='MALE-default'
            cur.execute("insert ignore into PassengerDetails values(%s,%s)",(NAME,GENDER))
            con.commit()
        return 1
    else:
         return 0

#Display Traveller details from Table
def SHOW_TRAVELLER_DETAILS():
    print("Name\tGender")
    cur.execute("select * from PassengerDetails")
    for info in cur:
        print(info)
    
#Capture Traveller details to send booking details
def TRAVELLER_DETAILS2():
    global no        #global variable protecting Mobile no
    global Email     #global variable protecting Email Isd
    no=int(input("ENTER MOBILE NUMBER: "))
    Email=input("ENTER EMAIL ID: ")

#Capture Travel details - From, To, Date, Class, Category.....
def TRAVEL_FROM_TO():
    global Ticket_fare
    global No_passenger
    global TClass
    global Date
    f=open('Booking','w')
    Departure=input("Enter From : ")
    if Departure=='':
        Departure='Chennai-default'
    Destination=input("Enter To   : ")
    if Destination=='':
        Destination='Delhi-default'

    Date=input("Departure Date(DD/MM/YYYY): ")
    No_passenger=input("\nEnter no. of Passengers Travelling (max 4 booking at a Time): ")
    if No_passenger=='':
        print("Wrong entry!!! default selection - 1")
        No_passenger=1            #default
    No_passenger=int(No_passenger)
    
    if No_passenger<=4:
        pass
    elif No_passenger>4:
        print("\n!!! Max number of passanger allowed in single booking is 4 !!! Try again !!!") 
        No_passenger=int(input("\nEnter no. of Passengers Travelling: "))
        if No_passenger>4:
            print("\n!!! Exceed nummber of re-tries !!!")
            exit()
#Choose Travel class - Economy, Pre. economy, Business
    print("\nChoose Travel Class")
    print("Press:\t1.Economy\t2.Premium Economy\t3.Business")
    Travel_class=input("Enter Class: ")
    if Travel_class=='':
        print("Wrong entry!!! default selection - 1")
        Travel_class=1            #default
    Travel_class=int(Travel_class)
    if Travel_class==1:
        TClass='Economy'
    elif Travel_class==2:
        TClass='Premium Economy'
    elif Travel_class==3:
        TClass='Business'
    else:
        Travel_class==1
        TClass='Economy'
        
#Choose Category - Regular,Armed forces,Sr citizen, Infant
    print("\nChoose Fare Category")
    print("Press: 1.Regular   2.Armed forces  3.Senior citizen  4.Infant")
    Travel_category=input("Enter category: ")
    if Travel_category=='':
        print("Wrong entry!!! default selection - 1")
        Travel_category=1            #default
    Travel_category=int(Travel_category)
    if Travel_category==1:
        TCategory='Regular'
    elif Travel_category==2:
        TCategory='Armed Forces'
    elif Travel_category==3:
        TCategory='Sr Citizen'
    elif Travel_category==4:
        TCategory='Infant'
    else:
        Travel_category=1            #default
        TCategory='Regular-default'
    Ticket_fare=CALCULATE_FARE(Travel_class,Travel_category)
    rec=Departure+','+Destination+','+Date+','+str(No_passenger)+','+TClass+','+TCategory+','+'\n'
    f.write(rec)
    f.close()

#Read contents of file - Booking
def read():
    f=open('Booking')
    for i in f:
        l=i.split(',')
        print('Departure       : ',l[0])
        print('Destination     : ',l[1])
        print('Date            : ',l[2])
        print('No. of passenger: ',l[3])
        print('Travel Class    : ',l[4])
        print('Category        : ',l[5])
    f.close()

#Calculate fare based on Travel class & Category
def CALCULATE_FARE(Travel_class,Travel_category):
    Final_fare=0
    if Travel_class==1:      #Economy
        Base_fare=6000
    elif Travel_class==2:    #Premium
        Base_fare=8000
    elif Travel_class==3:    #Business
        Base_fare=10000
    else:
        Base_fare=6000    #default-Economy

    if Travel_category ==1:     #Regular
        Final_fare=Base_fare
    elif Travel_category ==2:   #Armed forces, 20%
        Final_fare=Base_fare-Base_fare/5
    elif Travel_category ==3:   #Sr citizen, 10%
        Final_fare=Base_fare-Base_fare/10
    elif Travel_category ==4:   #Infant, 50%
        Final_fare=Base_fare/2
    else:
        Final_fare=Base_fare    #default-Regular
    return Final_fare      
       
#Capture flight details
def FLIGHT_SELECTION():
    global FlightName
    global FlightNo
    global DeptTime
    Fs=input("Enter SNo for Flight selection: ")
    if Fs=="":
        Fs="1"   #default
        print("\nWrong Selection...default - 1")
    Fs=int(Fs)   
    if Fs>=10:
        Fs=1     #default
        print("\nWrong Selection...default - 1")
    cur.execute("select Flight_Name from Availability where S_No like '%s'"%(Fs))
    FlightName=cur.fetchone()
    cur.execute("select Flight_No from Availability where S_No like '%s'"%(Fs))
    FlightNo=cur.fetchone()
    cur.execute("select Departure_Time from Availability where S_No like '%s'"%(Fs))
    DeptTime=cur.fetchone()
    
    cur.execute("select * from Availability where S_No like '%s'"%(Fs))
    data2=cur.fetchall()
    if any(data2):
        print("\nYou have selected: ")
        print(data2,"\n")
        return 1
    else:
        return 0

#Print E-Ticket
def Eticket(BookingStatus):
    print("E-TICKET")
    print("Booking ID: MMAT34578")
    print("\nBooking Status: ",BookingStatus)
    cur.execute("select Name from PassengerDetails")
    PasName=cur.fetchall()
    l=list(PasName)
    for i in range(No_passenger):
        print("Passenger",i+1,": ",l[i],"Seat No: ",seat_list[i])
    print("\n-----------------------------------")
    print("Flight Name     : ",FlightName[0])
    print("Flight Number   : ",FlightNo[0])
    read()
    print("Departure Time  : ",DeptTime[0])
    print("------------------------------------")    

#Choose - food options
def FOOD():
    FoodTotal=0
    print("\nPre Book snacks now before you fly....")
    flag=1
    while flag!=0:
        print("\nPRESS 1.Veg   2.Non veg  3.Beverages")
        food=int(input("Choice: "))
        if food==1:
            ch=int(input("\nMenu:\nPress1: Sandwich\nPress2: Ready to Eat\n\nSelect the opton you prefer: "))
            if ch==1:
               print("Press 1 for Tomato, Cucmber lettuce Sandwich")
               print("Press 2 for Panner Tikka Sandwich")
               n=int(input("Choice: "))
               if n==1:
                   print("Tomato, Cucmber lettuce Sandwich")
                   FoodTotal+=350
                   print("Price=350")
               elif n==2:
                  print("Panner Tikka Sandwich")
                  FoodTotal+=300
                  print("Price=300")
               print("\nDo you want to continue food selection ....")
               print("Press0: No\nPress1: Yes")
               flag=int(input("Choice: "))
            elif ch==2:
                print("Press1: Vada Pao")
                print("Press2: Veg Biryani")
                print("Press3: Poha")
                print("Press4: Cup noodles")
                n=int(input("Choice: "))
                if n==1:
                    print("Vada Pao")
                    FoodTotal+=100
                    print("Price=100")
                elif n==2:
                    print("Veg Biryani")
                    FoodTotal+=350
                    print("Price=350")
                elif n==3:
                    print("Poha")
                    FoodTotal+=250
                    print("Price=250")
                elif n==4:
                    print("Cup noodles")
                    FoodTotal+=200
                    print("Price=200")
                print("\nDo you want to continue food selection ....")
                print("Press0: No\nPress1: Yes")
                flag=int(input("Choice: "))
        elif food==2:
            ch=int(input("\nPress: 1.For Meals 2.For Cup Noodles\n\nEnter your choice:"))
            if ch==1:
                print("Press1 Chicken Tikka Sandwich")
                print("Press2 Chicken Nuggets")
                print("Press3 Tikka Chilli Chicken")
                print("Press4 Chapati with Fish currry")
                n=int(input("Choice: "))
                if n==1:
                   print("Chicken Tikka Sandwich")
                   FoodTotal+=150
                   print("Price=150")
                elif n==2:
                   print("Chicken Nuggets")
                   FoodTotal+=350
                   print("Price=350")
                elif n==3:
                    print("Tikka Chilli Chicken")
                    FoodTotal+=250
                    print("Price=250")
                elif n==4:
                    print("Chapati with Fish curry")
                    FoodTotal+=200
                    print("Price=200")

                print("\nDo you want to continue food selection ....")
                print("Press0: No\nPress1: Yes")
                flag=int(input("Choice: "))
            elif ch==2:
                print("Press 1:Chicken noodles")
                print("Press 2:Fish and meat noodles")
                n=int(input("Choice: "))
                if n==1:
                    print("Chicken noodles")
                    FoodTotal+=150
                    print("Price=150")
                elif n==2:
                    print("Fish and meat noodles")
                    FoodTotal+=200
                    print("Price=200")
                print("\nDo you want to continue food selection ....")
                print("Press0: No\nPress1: Yes")
                flag=int(input("Choice: "))
        elif food==3:
            print("Press1 for Tea")
            print("Press2 for Coffee")
            print("Press3 for Paper boat mango")
            n=int(input("Choice: "))
            if n==1:
                print("Tea")
                FoodTotal+=100
                print("Price=100")
            elif n==2:
                print("Coffee")
                FoodTotal+=100
                print("Price=100")
            elif n==3:
                print("Paper boat mango")
                FoodTotal+=150
                print("Price=150")
            print("\nDo you want to continue food selection ....")
            print("Press0: No\nPress1: Yes")
            flag=int(input("Choice: "))
        else:
            print("\nDo you want to continue food selection ....")
            print("Press0: No\nPress1: Yes")
            flag=int(input("Choice: "))
    return FoodTotal

#Load text file (about_us.txt) & read back with information about website
def about_us():
    text_file=open("about_us.txt","w+")
    text_file.write("It's all about easy booking to fly in India....\n")
    text_file.write("MakeMyAirTrip is a pioneer in India’s online travel services.\n\n")
    text_file.write("We started in 2000, with the target to offer easy, at your fingertips booking\n")
    text_file.write("services to the flyers in Indian continent.\n")
    text_file.write("We have completed 10 years and become the most recognizable mascot all over.\n")
    text_file.write("Our air service has won numerous awards for humour, originality & reliability. \n")
    text_file.write("Our  service is more like a friend who reaches out with warmth and hospitality,\n")
    text_file.write("even to the farthest corners of the country.\n\n")
    text_file.write("Some Innovation in our flights to redefine the total passenger experience - \n")
    text_file.write("\t 1.Wider seats and aisles\n")
    text_file.write("\t 2.Bigger windows, 65% larger than other aircraft in the same category\n")
    text_file.write("\t 3.Improved cabin environment (lower altitude, cleaner air, higher humidity)\n")
    text_file.write("\t 4.Versatile range – from efficient short, medium and long-range routes \n")
    text_file.write("\t 5.15% lower fuel consumption compared other same-sized airplanes\n")
    text_file.write("\t 6.Lower maintenance costs than peer airplanes \n")
    text_file.write("\t 7.Cleaner throughout its lifecycle (designed for the environment) \n")
    text_file.write("\t 8.Versatile family – big jet ranges, small jet trip costs \n")
    text_file.write("\t 9. 85 dbA noise stays within airport property\n")
    text_file.write("\t 10.Less hazardous waste and overall waste in production\n\n")
    text_file.write("To know more about us, refer the following details -\n")
    text_file.write("\tContact us on: 93xxxxxx36\n")
    text_file.write("\tEmail us at: makemyairtrip@gmail.com\n")
    text_file.write("\tTweet at: www.makemyairtriptwitter.com \n ")
    text_file.write("\tTo know more log on to: www.makemyairtrip.org.in \n")
    text_file.write("\tGeneral Queries: makemyairtrip.base@trip.in \n")
    text_file.write("\tMissing Miles/Retro Credit on AI: makemytrip.retros@trip.in\n\n")
    text_file.write("\t\tHope you enjoyed with us.. \n")
    text_file.write("\t\tKeep enjoying your jouney with us.. \n")
    text_file.write("\t\tStay safe and stay healthy!!! \n")
    text_file.seek(0)
    for Lines in text_file.readlines():     #readline return line with \n
        print(Lines.rstrip())               #rstrip() remove \n 

#Load text file (travel_rules.txt) & read back - Rules & Regulatiions
def travel_rules():
     travel_rules=open("travel_rules.txt","w+")
     travel_rules.write("We seek your kind assistance and cooperation for your own safety as well as safety\n")
     travel_rules.write("of fellow passengers………Please follow below guidelines: \n\n")
     travel_rules.write("1) All flights shall provide a complimentary safety kit(three layered surgical masks,\n")
     travel_rules.write("a face shield, a sanitizer, a pair of gloves) to all passengers at the boarding gate.\n\n")
     travel_rules.write("2) Passengers seated in middle seats will also be provided with wrap-around gown.\n\n")
     travel_rules.write("3) Passengers must wear a face mask covering their nose and mouth, throughout the\n")
     travel_rules.write("journey. The mask may be removed only while eating and drinking. \n\n")
     travel_rules.write("4) Please maintain appropriate social distancing while boarding and de-boarding the\n")
     travel_rules.write("aircraft.\n\n")
     travel_rules.write("5) Passengers are requested to familiarise themselves with the guidelines published\n")
     travel_rules.write("by the Indian Ministry of Civil Aviation for air passengers.\n\n")
     travel_rules.write("6) Caution: Passengers are advised to strictly follow COVID-19 protocols. Failure\n")
     travel_rules.write("to comply with protocols may attract penal action against the concerned individual.\n\n")
     travel_rules.write("7) As per the current government guidelines, it is mandatory to do web check-in for\n")
     travel_rules.write("all domestic flight. Complete it for free 48 hrs - 60 min before flight.")
     travel_rules.seek(0)
     print(travel_rules.read())
     travel_rules.close()

#Load text file (refund_text.txt) & read back - Refund policies
def refund_policy():
    refund_text=open("refund.txt",'w+')
    read=["1) Cancellation within 24 hours of booking will subject to zero cancellation\n   charges and a full Refund will be provided.\n\n2) Cancellation can be done online and refund will be given after deducting\n   cancellation charges as applicable.\n\n3) Cancellation or changes must be done at least 2 hrs prior to departure.\n\n4) Processing of Refund may take upto 7 working days.\n\n5) Refund will be credited to the same account from which the payment was made.\n\n6) In the case of refund, upfront discount and promo code discount availed at\n   the time of booking would be deducted from the refund amount.\n\n7) Passengers can also claim refund for an unused tickets, however for such\n   tickets only a small amount depending on the flight and fare rules will \n   be refunded, along with the additional fee for cancellation.\n\n8) Please contact our executives for any query from our contact details."]
    refund_text.writelines(read)
    refund_text.seek(0)
    ref=refund_text.readlines()
    for lines in read:
        print(lines.rstrip('\n'))
        
#Load Availability table statically
def INPUTING_FLIGHT_DETAILS():
    cur.execute("delete from Availability")
    cur.execute("insert into Availability values(1,'INDIGO','IDI678A','04:00:00','TICKETS AVAILABLE')")
    cur.execute("insert into Availability values(2,'INDIGO','IDI676B','07:00:00','TICKETS AVAILABLE')")
    cur.execute("insert into Availability values(3,'INDIGO','IDI650C','11:00:00','TICKETS AVAILABLE')")
    cur.execute("insert into Availability values(4,'GO AIR','AIR221C','14:00:00','TICKETS AVAILABLE')")
    cur.execute("insert into Availability values(5,'GO AIR','AIR221B','17:00:00','TICKETS AVAILABLE')")
    cur.execute("insert into Availability values(6,'GO AIR','AIR123A','18:00:00','TICKETS AVAILABLE')")
    cur.execute("insert into Availability values(7,'SPIJET','SPI878C','20:00:00','TICKETS AVAILABLE')")
    cur.execute("insert into Availability values(8,'SPIJET','SPI999B','22:00:00','TICKETS AVAILABLE')")
    cur.execute("insert into Availability values(9,'SPIJET','SPI987A','00:00:00','TICKETS AVAILABLE')")
  
def SHOW_AVAILABLE_FLIGHT():
    cur.execute("select * from Availability")
    for info in cur:
        print(info)

#Paymets selection - Credit card, Debit card, Google Pay, PayTM
#Capture Payment details
def PAYMENT(Total_amt):
    Pay=Total_amt
    print("\nPayment Mode - 1.Credit card   2.Debit card   3.Google Pay   4.PayTM")
       
    n=int(input("Choose mode of payment from the above choices: "))
    fl=1
    while fl!=0:
        if n==1:
            cn=int(input("\nCard number: "))
            nc=input("Name on card: ")
            cv=int(input("CVV: "))
            ed=input("Expiry date on card (MM/YYYY): ")
            fl=0
        elif n==2:
            cn=int(input("Card number: "))
            nc=input("Name on card: ")
            cv=int(input("CVV: "))
            ed=input("Expiry date on card (MM/YYYY): ")
            fl=0
        elif n==3:
            print("\nKindly Google Pay on 96xxxxxx74 ")
            nu=int(input("Enter Gpay Number, in case of Refund: "))
            fl=0
        elif n==4:
            print("\nKindly PayTM on 96xxxxxx84 ")
            nu=int(input("Enter Paytm Number, in case of Refund: "))
            fl=0
        else:
            print("INVALID MODE OF PAYMENT")
            fl=0
            exit()
        print("\nBOOKINGS CONFIRMED\nThank You for Booking with us!! We would like to Help You Again!!")
        print("E-tickets will be sent to registered number")
        
#Web check-in seats display & selection for differnt travel classes
def WEBCHK():
   global seat_list
   seat_list=[]
   if TClass.lower()=="business":#Seat selection Business class
       print ("Available seats are")
       l=['1','2','3','4','5']
       print(l)
       for i in range(No_passenger):
           n=input("\nChoose the seat number: ")
           if n not in l:
               n='1'    #default wrong entry by user
           seat_list.insert(i,n)
           m=l.index(n)
           l.pop(m)
           if No_passenger==1:
               break
           if No_passenger!=i+1:
               print("Remaining seats",l)
       
   elif TClass.lower()=="premium economy":    #Seat selection Premium class
       print ("Available seats are")
       l=['6a','6b','7a','7b','8a','8b','9a','9b','10a','10b']
       print(l)
       for i in range(No_passenger):
           n=input("Choose the seat number: ")
           if n not in l:
               n='6a'   #default wrong entry by user
           seat_list.insert(i,n)
           m=l.index(n)
           l.pop(m)
           if No_passenger==1:
               break
           if No_passenger!=i+1:
               print("Remaining seats ",l)
       
   elif TClass.lower()=="economy":             #Seat selection Economy class
       la=['11a','12a','13a','14a','15a']
       lm=['11b','12b','13b','14b','15b']
       lw=['11c','12c','13c','14c','15c']
       for i in range(No_passenger):
           s=int(input("Choose the kind of seat you prefer\n1.Aisle  2.Middle  3.Window\nChoose the option: "))
           if s==1:
               print ("Available Aisle seats are")
               print(la)
               n=input("\nType the seat number: ")
               if n not in la:
                   n='11a' #default wrong entry by user
               seat_list.insert(i,n)
               m=la.index(n)
               la.pop(m)
           elif s==2:
               print ("Available Middle seats are")
               print(lm)
               n=input("\nType the seat number: ")
               if n not in lm:
                   n='11b' #default wrong entry by user
               seat_list.insert(i,n)
               m=lm.index(n)
               lm.pop(m)
           elif s==3:
               print ("Available Window seats are")
               print(lw)
               n=input("\nType the seat number: ")
               if n not in lw:
                    n='11c' #default wrong entry by user
               seat_list.insert(i,n)
               m=lw.index(n)
               lw.pop(m)
       
def CANCELATION():
    print("Do you want to cancel booking (Y(yes) or N(no))")
    Del=input("Choice: ")
    if Del in'Yy':
        bookingid=input("Enter Booking ID: ")
        if bookingid=='MMAT34578':
            Eticket(BookingStatus)
        else:
            print("Invalid Booking ID")
    else:
        print("Booking Not Cancelled")
    
  
################################################################
                #Main program
################################################################

import mysql.connector
import datetime
con=mysql.connector.connect(host='localhost',user='root',password='root',charset='utf8')
cur=con.cursor()

#Introduction text display
print("\t\t\t\tWELCOME TO MakeMyAirTrip")
print("\t\t\t\t-------------------------")
file=open("Intro.txt","w+")
file.write("MakeMyAirTrip is an online air ticket booking website that provides services like\nflight schedules, ticket reservations, cancellations, web check-in, pre book food.\n\nWhy choose  MakeMyAirTrip?\nOffers : Lowest fares, Multiple mode of payments, Safe refunds.")
file.seek(0)
print(file.read())
file.close()
print()

#Create Database
cur.execute("create database if not exists Reservation")
cur.execute("use Reservation")

print("---------------------------------------------------------------------------------------------------------------------\n")
print("Kindly proceed with the account creation...")

cur.execute("delete from PassengerDetails")
cur.execute("create table if not exists PassengerDetails(Name char(20),Gender char(10))")
cur.execute("create table if not exists  Availability(S_No int primary key,Flight_Name char(20),Flight_No char(20),Departure_Time char(20),Tickect_Booking char(20))")
INPUTING_FLIGHT_DETAILS()           #Load Availabilty table statically

#Clear all records from LoginDetails table
#cur.execute("delete from LoginDetails")
#cur.execute("drop table LoginDetails")

choice=input("1.Create account\t2.Login\nEnter your Choice: ")
if choice=='':
    print("\nWrong entry!!! default selection - 1")
    print("Proceed to Create account...\n")
    choice=1            #default
choice=int(choice)

if choice==1:
    CREATE_ACCOUNT()  #Account creation by user
    LOGIN_ACCOUNT()   #Login by user
elif choice==2:
    LOGIN_ACCOUNT()   #Login by user
else:
    print("\nWrong entry!!! default selection - 1")
    print("Proceed to Create account...\n")
    CREATE_ACCOUNT()  #Account creation by user
    LOGIN_ACCOUNT()   #Login by user
     
start=input("\nEnter any key to start booking...")
if len(start)!=0:
    pass
       
while True:
    print("\nSelect Service -\n\t1.Book Tickects \n\t2.Display Booking \n\t3.Search Booking \n\t4.Update Ticket \n\t5.Cancellation \n\t6.Sort Booking\n\t7.About us\n\t8.Rules and Regulations\n\t9.Refund Policy\n\t10.Exit")
    choice=input("\nEnter Your Choice: ")
    if choice=='':
        print("Wrong entry!!! default selection - 1.Book Tickets\n")
        choice=1            #default
    choice=int(choice)
    
    if choice==1:           #Booking ticket
        TRAVEL_FROM_TO()
        print("\nDetails Entered ")
        read()
        print("\nFlights Availability")
        print("_________________________________________________________")
        print("SNo  Airline   Number     Timing      Availability")
        print("_________________________________________________________")
        SHOW_AVAILABLE_FLIGHT()     #display Availability table
        print("\nFare of each flight per head: Rs",Ticket_fare)
        print("_________________________________________________________")
        print()
        fselect=FLIGHT_SELECTION()  #Flight selection by user
        if fselect==1:
            pass
        elif fselect==0:
            print("\nWrong Flight selection........Retry")
            fselect=FLIGHT_SELECTION()
            if fselect==1:
                pass
            else:
                print("\nCrossed Max attempts\n")
                exit()
        Tdetails=TRAVELLER_DETAILS()
        if Tdetails==1:
            pass
        elif Tdetails==0:
            print("Invalid Passenger Count...Pls Retry\n")
            a=TRAVELLER_DETAILS()
            if a==1:
                pass
            else:
                print("Invalid")
                exit()
        print("\nBooking Details will be sent to...\n")
        TRAVELLER_DETAILS2()
    
        print("\nFetching Details for Available Seat .....")
        print("____________________________________________________________________________________________________________________")
        print("\nWEB CHECK-IN")
        WEBCHK()                   #Web check-in
        print("\nTOTAL AMOUNT:Rs.",Ticket_fare*No_passenger+Ticket_fare*No_passenger*0.18+500,"(inclusive of GST and sub charges)")
        print("____________________________________________________________________________________________________________________")
        Food=input("\nPre-book your Foods now (Y:yes or N:no): ")
        if Food.lower() in 'yY':
                    print("___________________________________________________________________________________________________________________")
                    Food_Tot=FOOD()
                    print("\nFood Total= Rs",Food_Tot)
                    print("___________________________________________________________________________________________________________________")
        else:
                    Food_Tot=0
                    
        print("\nTo confirm the Booking, Kindly Proceed with the Payment \n ")
        print("PAYMENT ")
        Total_amt=((Ticket_fare*No_passenger)+(Ticket_fare*No_passenger*0.18)+500)+Food_Tot
        print("GRAND TOTAL: ",Total_amt)
        PAYMENT(Total_amt)
        BookingStatus='CONFIRMED'
        print("____________________________________________________________________________________________________________________")
        Eticket(BookingStatus)
        print("____________________________________________________________________________________________________________________")
       
    elif choice==2:         #Display Booking & Passenger details
        print("Press 1:To display Booking Details\t2:To display Passenger Details")
        Display_Ticket=int(input("Enter Choice: "))
        if Display_Ticket==1:
            print("\n-----------------------------------------------------------------------------------")
            print("TRAVEL DETAILS: ")
            read()
            print("-----------------------------------------------------------------------------------")
            
        elif Display_Ticket==2:
            print("\n-----------------------------------------------------------------------------------")
            print("PASSENGER DETAILS: ")
            SHOW_TRAVELLER_DETAILS()
            print("Mobile no.: ",no)
            print("Email Id: ",Email)
            print("-----------------------------------------------------------------------------------")
        
    elif choice==3:         #Search
        sn=input("\nEnter Full Name: ")
        cur.execute("select * from PassengerDetails where NAME like '%s'"%(sn))
        data3=cur.fetchall()
        if any(data3):
              print("BOOKING FOUND")
              print(data3)
        else:
              print("BOOKING NOT FOUND")
          
    elif choice==4:         #Update ticket details
        print("Press: 1.Update by Name\t 2.Update Mobile number\t3.Update Email id")
        n=int(input("Choose: "))
        if n==1:
            oldname=input("Enter Old Name to be updated: ")
            cur.execute("select * from PassengerDetails")
            row=cur.fetchall()
            for i in range(0,cur.rowcount):
                if (row[i][0]==oldname):
                    newname=input("Enter New Name : ")
                    gender=input("Enter New Gender: ")
                    cur.execute("update PassengerDetails set Name=%s,Gender=%s where Name=%s",(newname,gender,oldname))
                    con.commit()
                    print("\t!!!Updated Successsfully!!! ")
                    SHOW_TRAVELLER_DETAILS()
                    break
                else:
                    print("Name to be updated not found")
        elif n==2:
            newno=int(input("ENTER MOBILE NUMBER: "))
            no=newno
            print("\t!!!Updated Successsfully!!! ")
            print("Updated Mobile Number: ",no)
        else:
            email_id=input("ENTER NEW EMAIL ID: ")
            Email=email_id
            print("\t!!!Updated Successsfully!!! ")     
            print("Updated Email Id: ",Email)

    elif choice==5:     #Cancel Booking
                BookingStatus='Cancelled'
                CANCELATION()
                break
              
    elif choice==6:     #Sorting
                cur.execute("select * from PassengerDetailS order by NAME asc")
                data4=cur.fetchall()
                for x in data4:
                      print(x)

    elif choice==7:     #Display about Website
                print("\n\t\t\t\tABOUT US\n\t\t\t\t--------")
                about_us()
                print("-----------------------------------------------------------------------------------")


    elif choice==8:     #Display Rules and regulations
                print("\nRules and regulations")
                print("---------------------")
                travel_rules()
                print("-----------------------------------------------------------------------------------")
            
    elif choice==9:     #Display Refund Policy
                print("\nMakeMyAirTrip Refund Policy")
                print("---------------------------")
                refund_policy()
                print("-------------------------------------------------------------------------------")
                
    else:               #Exit
                print("Exit\n")
                break
                con.close()
                cur.close()
            

