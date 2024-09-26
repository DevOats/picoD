from machine import Timer
import time
import PicoOled13
from button import Button
from multiDigitDisplay import MultiDigitDisplay
import random

class PicoD:


    # Constructor
    def __init__(self):
        
        self.diceOptions = [4, 6, 8, 10, 12, 20]
        
        self.selectedDiceIndex = 1
        self.diceListY = 4
        self.number = -1
        self.display=PicoOled13.get()
        self.display.clear()
        
        self.key0 = Button(15)
        self.key1 = Button(17)
        
        self.digits = MultiDigitDisplay(self.display,
                          74, 17,
                          digitCount = 2,
                          displayLeadingZeros = False,
                          autoCenter = True)


    def run(self):
        print("Running")
        self.__showSplash() 
        self.__setState_RollDice()
        
        
        while(True):
            self.key0.execute()
            self.key1.execute()
            time.sleep_ms(1)
        
    def __showSplash(self):
        self.display.clear()
        self.display.rect(0, 0, 128, 64, 1, 0)
        self.display.rect(2, 2, 124, 60, 1, 0)
        self.display.text("Pico D", 50, 15)
        self.display.text("MakeITWork", 35, 32)
        self.display.text("Groningen", 39, 42)
        self.display.show()
        time.sleep_ms(5000)
    
    def __setState_RollDice(self):
        self.__drawRollDiceScreen()
        self.__enableKeys()
        
        
    def __enableKeys(self):
        self.key0.reset()
        self.key1.reset()
        self.key0.setCallback_buttonDown(None)
        self.key0.setCallback_click(self.__selectNextDice)
        self.key0.setCallback_longPress(None)
        self.key0.setCallback_buttonUp(None)
        
        self.key1.setCallback_buttonDown(None)
        self.key1.setCallback_click(self.__rollDice)
        self.key1.setCallback_longPress(None)
        self.key1.setCallback_buttonUp(None)
        
        
    def __disableKeys(self):
        self.key0.setCallback_buttonDown(None)
        self.key0.setCallback_click(None)
        self.key0.setCallback_longPress(None)
        self.key0.setCallback_buttonUp(None)
        
        self.key1.setCallback_buttonDown(None)
        self.key1.setCallback_click(None)
        self.key1.setCallback_longPress(None)
        self.key1.setCallback_buttonUp(None)


    def __drawRollDiceScreen(self):
        self.__clearDisplay()
        self.display.rect(0, 0, 128, 64, 1, 0)
        self.display.rect(64, 7, 57, 50, 1, 1)
        self.display.rect(69, 12, 47, 40, 0, 1)
        
        y = self.diceListY
        for option in self.diceOptions:
            self.display.text("D" + str(option), 24, y);
            y += 10
            
        self.__drawDiceSelector()
        self.display.show()
        
    def __drawDiceSelector(self):
        # Clear
        self.display.rect(16, self.diceListY, 8, self.diceListY + 53, 0, 1)
        y = self.diceListY + (self.selectedDiceIndex * 10)
        self.display.text(">", 16, y)


    def __selectNextDice(self):
        
        if(self.number != -1):
           self.number = -1
           self.display.rect(74, 17, 36, 30, 0, 1)
           self.__DisplayShowDice()
        
        self.selectedDiceIndex += 1
        if(self.selectedDiceIndex >= len(self.diceOptions)):
            self.selectedDiceIndex = 0
        self.__drawDiceSelector()
        self.__displayShowDiceSelector()


    # Clears the display buffer without sending it to the display
    def __clearDisplay(self):
        self.display.fill(0)
        
    def __DisplayShowDice(self):
        self.display.show(9, 17, 14, 47)
        
    def __displayShowDiceSelector(self):
        #self.display.show()
        self.display.show(2, self.diceListY, 3, self.diceListY + 60)

        
    def __rollDice(self):
        self.__disableKeys()
        print("rolling dice")
        
        self.__clearDisplay()
        
        number: int = 0
        sleepTime: int = 50
        
        bounces = random.randint(13, 25)
        rollTimeSteps = random.randint(4, 15)
        diceSize = self.diceOptions[self.selectedDiceIndex]
        for i in range(bounces):
            self.number = random.randint(1, diceSize)          
            self.digits.displayNumber(self.number)
            self.__DisplayShowDice()
            time.sleep_ms(sleepTime)
            sleepTime += rollTimeSteps
            
        self.__enableKeys()
        
        

# Application runs from here
if __name__ == '__main__':
    runner = PicoD()
    runner.run()

