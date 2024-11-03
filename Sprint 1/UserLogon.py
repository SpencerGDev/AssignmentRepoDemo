from dataclasses import dataclass
from xmlrpc.client import Boolean

@dataclass
class UserInfo:
   firstName: str
   lastName: str
   email: str
   password: str
   phoneNumber: str
   symptom_list: list
   insurance: bool 


   # add fields for the other info listed in activity 2. add input for create_account
   
   
class UserLogin:
   def __init__(self) -> None:
      self.UserArray = []  # holds UserInfo objects
      self.loggedinUser = None # holds Single UserInfo object
   

   def isInDataBase(self, x, field) -> Boolean: #checks if x is in field of the UserArray (ex if abc is already in the username field)
      
      for user in self.UserArray:
        if(getattr(user, field) == x): #getattr is built in to python and it takes an object and a string that is a field of the object as parameters
          return(True)   
         
      return(False)
   

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


   def create_account(self): # max entry length needs to be added, ex max 9 chars for ssn. should be in the second activity
      
      while(True):
        firstName = input("Enter your first name: ")
        
        if(firstName == "cancel"):
           return()
        if(len(firstName) <= 50):
           break
        print("Please enter a name with less than 50 characters") 
        

      while(True):
        lastName = input("Enter your last name: ")
        
        if(lastName == "cancel"):
           return()
        if(len(lastName) <= 50):
           break
        print("Please enter a name with less than 50 characters") 


      while(True): #makes sure a valid email is entered
        email = input("Enter your email address: ")
        
        if(email == "cancel"):
           return()
        if(len(email) > 50):
           print("Please enter an email address with less than 50 characters")
           continue
        if(not ("@" in email)): #if @ is not in the input, do not allow the input
           print("Please enter a valid email! (Must include @) \n")
           continue
        if(self.isInDataBase(email, "email")): #if input is already a registered email, do not allow the input
           print("There is already an account with this email!")
           continue 
        break 
   
    
      while(True):
        password = input("Enter your password: ")

        if(password == "cancel"):
           return()        
        if(len(password) <= 50):
           break
        print("Please enter a password with less than 50 characters")
        

      while(True):
         phoneNumber = input("Enter your phone number: ")
         
         if(phoneNumber == "cancel"):
            return()
         if(self.isInDataBase(phoneNumber, "phoneNumber")):
            print("There is already an account with this phone number!")
         elif(len(phoneNumber) == 10 and phoneNumber.isdigit()): #input must have 10 digits, which must all be numbers
            break
         print("Please input a valid phone number") 
         

      while(True):
         insuranceInput = input("Do you currently have insurance? Yes or No").lower()
         if(insuranceInput == "no"):
            insurance = False
            break
         elif(insuranceInput == "yes"):
            insurance = True
            break
         else:
            print("Please input a valid input: Yes or No") 

      
      # add additional fields. For now, I am only doing First/Last name, email, password, phone number, and SSN

      #add confirm action conditional. 
      
      while(True):
          print("Create account with this information?")
          print(">Name: " + firstName + " " + lastName + "\n>Email: " + email + "\n>Password: " + password + "\n>Phone number: " + phoneNumber + "\nInsurance " + str(insurance) )
          isCorrect = input("1: Confirm, 2: Cancel ")

          if(isCorrect == "1"):
              break
          if(isCorrect == "2"):
              return()
          print("Please enter 1 or 2")
      newUser = UserInfo(firstName, lastName, email, password, phoneNumber, {}, insurance)
      self.UserArray.append(newUser)
   

   def main(self): # do we want to bring the user to another loop once theyre logged in?

      while(self.loggedinUser is None): # Login Loop
         print("1: login, 2: create account, 3: quit")
         userIn = input("Select Option: ")

         if(userIn == "1"): # menu: login

            if(self.login()):
              user = self.loggedinUser #sets the user to the currently logged in user so we don't have to type self.loggedInUser... every time
              print("welcome, " + user.firstName + user.lastName)

            while(self.loggedinUser is not None):
               print("1: view account, 2: edit account info, 3: log out")
               userIn = input("select Option:")

               if(userIn == "3"): #logs the user out
                   user = None
                   self.loggedinUser = None
                   print("You have logged out!")
                   break
               break # placeholder code. Add account functionality later   

         elif(userIn == "2"): # menu: create account
            self.create_account()
         elif(userIn == "3"): # menu: exit
            break
      
      


if __name__=="__main__":
   UserLogin().main()       
