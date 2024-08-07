from machine import Timer
import time
import PicoOled13
from button import Button
from multiDigitDisplay import MultiDigitDisplay
import random

class PicoD:

    # Constructor
    def __init__(self):
        
        self.diceSize = 32
        
        self.display=PicoOled13.get()
        self.display.clear()
        
        self.key0 = Button(15)
        self.key1 = Button(17)
        
        self.digits = MultiDigitDisplay(self.display,
                          50, 17,
                          digitCount = 2,
                          displayLeadingZeros = False)


    def run(self):
        print("Running")
        
        self.display.clear()
        self.digits.displayNumber(88)
        self.display.show()
        
        self.__setState_RollDice()
        
        while(True):
            self.key0.execute()
            self.key1.execute()
            time.sleep_ms(1)
        
    
    def __setState_RollDice(self):
       
        self.key0.setCallback_buttonDown(None)
        self.key0.setCallback_click(None)
        self.key0.setCallback_longPress(None)
        self.key0.setCallback_buttonUp(None)
        
        self.key1.setCallback_buttonDown(None)
        self.key1.setCallback_click(self.__rollDice)
        self.key1.setCallback_longPress(None)
        self.key1.setCallback_buttonUp(None)

    
    # Clears the display buffer without sending it to the display
    def __clearDisplay(self):
        self.display.fill(0)
        
    def __DisplayShowDice(self):
        self.display.show(6, 17, 11, 47)
        
        
    def __rollDice(self):
        print("rolling dice")
        
        self.__clearDisplay()
        
        number: int = 0
        sleepTime: int = 50
        
        bounces = random.randint(13, 25)
        rollTimeSteps = random.randint(4, 10)
        
        for i in range(bounces):
            
            number = random.randint(0, self.diceSize + 1)
            
            self.digits.displayNumber(number)
            self.__DisplayShowDice()
            time.sleep_ms(sleepTime)
            sleepTime += rollTimeSteps
        
        

# Application runs from here
if __name__ == '__main__':
    runner = PicoD()
    runner.run()

