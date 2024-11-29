from dataclasses import dataclass, field
from tkinter import TRUE
from xmlrpc.client import Boolean
from enum import Enum
from threading import Thread
from typing import List # for type hinting


@dataclass 
class MedicineInfo:
    rxName: str
    time: float = None
    timer: Thread = None
    stopFlag : bool = False # used to terminate thread early

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
   medicineList : List[MedicineInfo]

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
        self.UserArray = []  # holds UserInfo objects
        self.loggedinUser = None # holds Single UserInfo object

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
             newUser = UserInfo("big", "wow", "@a", "a", "1234567890", "123456789", [], False)
             self.UserArray.append(newUser)
             self.loggedinUser = newUser
             self.userAccount()
      
      
    def userAccount(self):
        while(self.loggedinUser is not None):   #these lines are commented out because they will be repeated in a seperate method for account menu
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
        pass
    
    def addMedicineReminder(self):
        #prompt user for when. 
        pass
    
    def viewMedicine(self): # prints medicine list and reminder time if given
        pass    

    def addMedicine(self):
        while(True):
            entry = input("Enter the name of the medicine you are currently taking, Type exit to exit.")
            if(entry.lower() == "exit"):
                break 
            if(validMedicine(entry) == False):
                continue
            
            newMedicine = MedicineInfo(entry)
            

            while(True):
                optionalTimer = input("Would you like to add a reminder? This can be done at anytime. 1 for yes, 2 for no.")

                if(optionalTimer == "1"):
                    self.addMedicineReminder(newMedicine)
                if(optionalTimer == "2"):
                    break
                
            self.loggedinUser.medicineList.append(newMedicine) 
            return()
    
                    
            
    
    def validMedicine() -> bool:
        """
        simple checks to check input, maybe if length is none, only a number, easy testable things
        print what went wrong before returing
        """
        pass
    
    def removeMedicine(): # easy iterate and remove from list
        pass
        

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