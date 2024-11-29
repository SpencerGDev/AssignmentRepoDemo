import re
from datetime import *
from dataclasses import dataclass, field
from typing import Tuple # for type hinting
import os
import winsound

@dataclass 
class MedicineInfo:
    rxName: str
    time: Tuple[int, int] = None

   
def validTime(reminderTime): # simple string parser
      #num 1-9 if we have 1:00 - 9:00, OR(|) 1, then 0-2, if we have 10:00- 12:00, 
      # ':' char, num 0-5, num 0-9
      reminderTime = reminderTime.upper()
      if(re.search("^([1-9]|1[0-2]):[0-5][0-9](AM|PM)$", reminderTime) is not None):
         return True
      return False

def testFunc(med : MedicineInfo):
   med.time = (3,3)
   
   
def main():
   time1 = "10:45"
   time2 = "13:30"
   time3 = "9:30"
   time4 = "1:60"
   print(validTime(time1))
   print(validTime(time2))
   print(validTime(time3))
   print(validTime(time4))
   
   timestamp_string = "2:13PM"
   format_string = "%I:%M%p" # 12 hour format, minutes, AM/PM
   
   datetime_obj = datetime.strptime(timestamp_string, format_string)
   hour = datetime_obj.hour
   minute = datetime_obj.minute
   print(f"Hour: {hour} Minute: {minute}")
   
   now = datetime.now()
   print(now.hour, now.minute)
   
   print(True if (now.hour == hour) and (now.minute == minute) else False)
   
   #testing changing timer.
   joe = MedicineInfo("cool")
   testFunc(joe)
   print(joe)
   
   audiofile = "alarm.wav"

   winsound.PlaySound(audiofile, winsound.SND_FILENAME)

   
   
   
   
if(__name__ == "__main__"):
   main()


   