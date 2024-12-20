from dataclasses import dataclass, field
from tkinter import TRUE
from xmlrpc.client import Boolean
from enum import Enum
from threading import Thread
from typing import Tuple, List # for type hinting
from datetime import *
import re
import winsound
import time

audiofile = "alarm.wav"

@dataclass   
class MedicineTimers: # holds a timer object
    time_obj: datetime
    triggeredFlag: bool = False    

@dataclass 
class MedicineInfo: # holds a medicine object
    rxName: str
    timers: List[MedicineTimers] = field(default_factory= list)
    
@dataclass
class UserInfo:
   firstName: str = None
   lastName: str = None
   email: str = None
   password: str = None 
   phoneNumber: str = None
   SSN: str  = ""
   symptom_list : list  = field(default_factory= list)
   insurance: bool = None
   medicineList : List[MedicineInfo] = field(default_factory= list)


   fieldMap = { #maps input integers to 2-tuple fields. First parameter is the field name, and the second is a lambda function that can validate a potential input
           "1": ("firstName",lambda x, isInDataBase: len(x) <= 50),
           "2": ("lastName", lambda x, isInDataBase: len(x) <= 50),
           "3": ("email", lambda x, isInDataBase: (len(x) <= 50) and "@" in x and not isInDataBase(x, "email")),
           "4": ("password",lambda x, isInDataBase: len(x) <= 50),
           "5": ("phoneNumber",lambda x, isInDataBase: len(x) == 10 and x.isdigit()),
           "6": ("insurance",lambda x, isInDataBase: x.lower() in ["yes","no"]),
           "7": ("SSN",lambda x, isInDataBase: len(x) == 9 and x.isdigit() and not isInDataBase(x,"SSN")),
           "8": ("symptom_list")
              }
   

class UserLogin:
    def __init__(self) -> None:
        self.UserArray: List[UserInfo] = []   # holds UserInfo objects
        self.loggedinUser = None # holds Single UserInfo object
        self.timerThread = None
        self.exitFlag = False
        self.startMonitoringTimers()


    #helper functions

    def isInDataBase(self, x, field) -> Boolean: #checks if x is in field of the UserArray (ex if abc is already in the username field)
      
      for user in self.UserArray:
        if(getattr(user, field) == x): #getattr is built into python and it takes an object and a string that is a field of the object as parameters
          return(True)   
         
      return(False)

    def getValidInput(self, prompt, specification, isInDataBase): #generalizes input validation. specifcation is the specific thing we are validating by (ex email must contain @)
        while(True):
            userIn = input(prompt)
            if(userIn == "cancel"):
                return(None) 
            if(specification(userIn, isInDataBase)):
                return(userIn)

    def login(self) -> bool:
      """
      Returns true if login was successful, else false 
      """
      email = input("Enter the email you have an account with: ")
      password = input("Enter your password: ")
      for user in self.UserArray:
         if (user.email == email):
            if(user.password == password):
               self.loggedinUser = user
               print("Login Successful!")
               return True
      print("No Login found, try again")
      return False


    def create_account(self): # loops through the dictionary fieldMap and validates each input respective to what the field is (ex firstName must be <= 50 characters long)
        newUser = UserInfo()
        # sets all fields to None (I don't know how to rig a default constructor for the code at this point)
        for fieldThing, (field, fieldValidator) in list(UserInfo.fieldMap.items())[:-2]: # does not iterate over the last two elements because they aren't    part of a base account
            if(field == "insurance"):
                print("Please enter 'yes' or 'no' if you have insurance.")
            if(field == "phoneNumber"):
                print("Enter a valid phone number, ex: 1234567890 ")
                
            userIn = self.getValidInput("Please input your " + field + ": ", fieldValidator, self.isInDataBase)

            if(userIn is None):
                # I think python garbage collects the partially completed new user
                return()
            setattr(newUser, field, userIn) #sets the validated attributes to the new user

        if(newUser.insurance == "1"):
            newUser.insurance = True
        else:
            newUser.insurance = False
        
        # newUser.symptom_list = None
        
        self.UserArray.append(newUser)
   

    def main(self):

      while(self.loggedinUser is None): # Login Loop
         print("1: login, 2: create account, 3: quit")
         userIn = input("Select Option: ")

         if(userIn == "1"): # login

            if(self.login()):
              print("welcome, " + self.loggedinUser.firstName + " " + self.loggedinUser.lastName)
              self.userAccount()

         elif(userIn == "2"): # create account
            self.create_account()
         elif(userIn == "3"): # exit
            break
         elif(userIn == "super"):
             newUser = UserInfo("super", "super", "@", "super", "1234567890", "123456789", [], False)
             self.UserArray.append(newUser)
             self.loggedinUser = newUser
             self.userAccount()
             
    def monitorTimers(self):
        # print("hi")
        while(self.exitFlag == False):
            time.sleep(1) # sleep for a second each iteration to not overload cpu
            if(self.UserArray is None): 
                continue
            
            currTime = datetime.now()
            hour, minute = currTime.hour, currTime.minute
            for user in self.UserArray[:]:
                for med in user.medicineList:
                    currentTimers = med.timers
                    if currentTimers is None:
                        continue
                    
                    for timer in currentTimers:
                        timer_obj = timer.time_obj
                        timehour = timer_obj.hour
                        timeminute = timer_obj.minute
                        if ((hour == timehour and minute == timeminute) and timer.triggeredFlag == False): 
                            winsound.PlaySound(audiofile, winsound.SND_FILENAME)
                            timer.triggeredFlag = True
                            

    def startMonitoringTimers(self):
        self.timerThread = Thread(target=self.monitorTimers, daemon= True)
        self.timerThread.start()
                
        
        

    def userAccount(self):
        while(self.loggedinUser is not None):
            print("1: Add medication reminder, 2: view account, 3: edit account info, 4: log out")
            userIn = input("select Option: ")

            if(userIn == "4"): #logs the user out
                self.loggedinUser = None
                print("You have logged out!")
                return()
            if(userIn == "3"):
                self.editInfo()
            if(userIn == "2"):
                self.viewInfo()
            if(userIn == "1"):
                self.modifyMedicine()
                
                

    def modifyMedicine(self):
        """
        Allows User to view, modify(add/remove), and set timers for medicine
        """
        while(True):
            option = input("Would you like to: \n1: Add a medicine\n2: Remove a medicine(will clear timers)\n3: Set a timer for an existing medicine\n4: Remove a timer\n5: View all medicines and timers set\n6: Exit")
            if(option == "1"):
                self.addMedicine()
            elif(option == "2"):
                self.removeMedicine()
            elif(option == "3"):
                self.addMedicineReminderWrapper()
            elif(option == "4"):
                self.removeTimer()
            elif(option == "5"):
                self.viewMedicineWrapper()
            elif(option == "6"):
                break
            else:
                print("please enter a valid option")
        
    
    def validTime(self, reminderTime): # simple string parser
        #num 1-9 if we have 1:00 - 9:00, OR(|) 1, then 0-2, if we have 10:00- 12:00, 
        # ':' char, num 0-5, num 0-9
        if(re.search("([1-9]|1[0-2]):[0-5][0-9](AM|PM)$", reminderTime) is not None):
            return True
        print("Invalid Format, please try again.")
        return False
    
    def addMedicineReminder(self, med : MedicineInfo):
        #prompt user for when. 
        while(True):
            reminderTime = input("What time would you like your reminder to go off?\nEx: 7:30PM, 1:00PM\n")
            if(reminderTime == "exit"):
                break
            if(self.validTime(reminderTime) == True):
                break
        
        format_string = "%I:%M%p" # 12 hour format, minutes, AM/PM
        datetime_obj = datetime.strptime(reminderTime, format_string)
        med.timers.append(MedicineTimers(time_obj=datetime_obj))
        print(f"Timer Set for {datetime_obj.strftime('%I:%M %p')}:") #gets time in our format 7:30PM 
    
    def addMedicineReminderWrapper(self):
        while(True):
            self.viewMedicine()
            query = input("Which Medicine would you like to add a reminder for. Enter ID\n")
            if(query == "exit"):
                break
            elif(self.validateID(query) == True):
                selectedMed = self.loggedinUser.medicineList[int(query)]
                self.addMedicineReminder(selectedMed)
                break
            

        
            
    def validateID(self, medID : str):
        # print(medID)
        try:
            mediD = int(medID)
            # print("test")
            for i, _ in enumerate(self.loggedinUser.medicineList):
                if(i == mediD):
                    return True
            # print(mediD + " " + i)
            print("ID does not exist. enter a valid ID")
        except ValueError:
            print("Please input a valid Medicine ID: ")
        return False
        
        
    def viewMedicineWrapper(self):
        """
        extends viewMedicine functionality by allowing users to stay on screen before exiting
        """    
        self.viewMedicine()
        while(True):
            confirm = input("Press enter to go back.")
            if(confirm == ""):
                break
        

    def viewMedicine(self): # prints medicine list and reminder time if given
        print("Your medicine list:")
        for i, med in enumerate(self.loggedinUser.medicineList):
            timersconcat = ""
            for t in med.timers: 
                currentTimer = t.time_obj.strftime('%I:%M %p')
                timersconcat += currentTimer + " | "
            print(f"ID: {i} | Name {med.rxName} | Timers set: {timersconcat}") 


    def addMedicine(self):
        while(True):
            entry = input("Enter the name of the medicine you are currently taking, Type exit to exit.")
            if(entry.lower() == "exit"):
                break 
            if(self.validMedicine(entry) == False):
                continue
            
            newMedicine = MedicineInfo(entry)
            

            while(True):
                optionalTimer = input("Would you like to add a reminder? This can be done at anytime.\n1 for yes, 2 for no.")

                if(optionalTimer == "1"):
                    self.addMedicineReminder(newMedicine)
                    break
                if(optionalTimer == "2"):
                    break
                
            self.loggedinUser.medicineList.append(newMedicine) 
            return()
    
                
    def validMedicine(self, entry) -> bool:
        """
        simple checks to check input, maybe if length is none, only a number, easy testable things
        print what went wrong before returing
        """
        if(len(entry) < 1 or len(entry) >= 50):
            print("Please enter a medicine with between 1 and 50 characters: ")
            return(False)
        if(entry.isdigit()):
            print("Please enter a medicine name, not number: ")
            return(False)
        
        return(True)
    
    def removeMedicine(self): # easy iterate and remove item from list
        while(True):
            self.viewMedicine()
            choice = input("Enter the ID of the medicine you want to remove: ")
            if(choice == "exit"):
                break
            if(self.validateID(choice)):
                del self.loggedinUser.medicineList[int(choice)]
                break

    def removeTimer(self):
        while(True):
            self.viewMedicine()
            medicinePick = input("Please input the ID for the medicine of the timer that you want to remove: ")
            if(medicinePick == "exit"):
                return()
            if(self.validateID(medicinePick)):
                break
        
        med = self.loggedinUser.medicineList[int(medicinePick)]
        if(len(med.timers) == 0):
            print("There are no timers to remove!")
            return()

        while(True):
            print("here are the timers you can remove: ")
            # timerList = ""
            i = 0
            for timer in med.timers:
                print(f"{i}: {timer.time_obj.strftime('%I:%M %p')}")
                i += 1
            
            timerPick = input("Which timer would you like to remove? ")
            if(timerPick == "exit"):
                return()
            if(not timerPick.isdigit()):
                print("Please enter the number for the timer you want to remove!")
                continue
            intPick = int(timerPick)
            if(intPick < 0 or intPick >= len(med.timers)):
                print("Please enter the number for the timer you want to remove!")
                continue

            del(med.timers[intPick])
            print("Here is your updated medicine reminder list: ")
            self.viewMedicine()
            return()

    def editInfo(self): #edits account info
        # user must input password first
        inputPassword = self.getValidInput("Input your password: ", lambda x, isInDataBase: x == self.loggedinUser.password, self.isInDataBase)
        if(inputPassword is None):
            return()
    
        while(True):
            print("1:first name 2:last name 3:email 4:password 5:phone number 6:insurance 7:SSN 8:Symptoms")
            fieldNum = input("Which info would you like to edit? ")
            if(fieldNum in UserInfo.fieldMap): # checks to make sure the input number is mapped to a UserInfo field
                break # leaves while loop to next input loop
            elif(fieldNum == "cancel"):
                return() # exits the edit info function
        
        if(UserInfo.fieldMap.get(fieldNum) == "symptom_list"):
            self.editSymptoms()
            return()
        if(UserInfo.fieldMap.get(fieldNum)[0] == "phoneNumber"):
            print("Please enter a new valid 10 digit number")
            

        newValue = self.getValidInput("Input what you want to update "+UserInfo.fieldMap.get(fieldNum)[0] +" to: ", UserInfo.fieldMap.get(fieldNum)[1], self.isInDataBase) #update to change specification parameter
        if(newValue is None):
            return()
    
        setattr(self.loggedinUser, UserInfo.fieldMap.get(fieldNum)[0], newValue)
        print("Successfully updated to " +newValue)

    def editSymptoms(self):
        user = self.loggedinUser
        while(True):
            option = self.getValidInput("Do you want to 1: Add a symptom, 2: Remove a symptom? or 3: Exit menu ", lambda x,  isInDataBase: x in ["1", "2", "3"], self.isInDataBase)
            
            if(option == "3" or option is None):
                return()  
            if(option == "1"):
                symptom = self.getValidInput("Input a symptom to add: ", lambda x, isInDataBase: (len(x) > 0 and len(x) <= 50), self.isInDataBase )
                if(symptom is None):
                    return()
                user.symptom_list.append(symptom)
                print("added " + symptom + " to symptom list.")
            else:
                if(len(user.symptom_list) == 0):
                    print("There are currently no symptoms to remove")
                    return()
                print("here's the current symptom list: ")
                print(", ".join(map(str, user.symptom_list))) # prints the list
                symptom = self.getValidInput("Input a symptom to remove: ", lambda x, isInDataBase: x in user.symptom_list, self.isInDataBase)
                if(symptom is None):
                    return()
                user.symptom_list.remove(symptom)
                print("removed " + symptom)

    def viewInfo(self): # prints out accFiount info
        user = self.loggedinUser

        print("name: " + user.firstName +" "+ user.lastName)
        print("email: " + user.email)
        print("phone number: " + user.phoneNumber)
        if(len(user.symptom_list) == 0): 
            print("No recorded symptoms")
        else:
            print("symptoms: ")
            print(", ".join(map(str, user.symptom_list))) # prints the list
        if(user.insurance):
            print("insurance: yes")
        else:
            print("insurance: no")
        # checks if user wants to view password and SSN
        viewMore = self.getValidInput("Do you want to view private info? Yes: 1, No: 2 ", lambda x, isInDataBase: x in ["1", "2"], self.isInDataBase)
        if(viewMore is None or viewMore == "2"):
            return()
    
        inputPassword = self.getValidInput("Input your password: ", lambda x, isInDataBase: x == user.password, self.isInDataBase)
        if(inputPassword is None):
            return()
        if(inputPassword): #input password is correct
            print("SSN: " + user.SSN)
            print("Password: " + user.password)

if __name__=="__main__":
   UserLogin().main() 