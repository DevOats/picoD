from machine import Pin
import time

class Button:
    
    # Constructor
    def __init__(self, gpioPinNumber: int):
        
        self.clickCallback = None
        self.longClickCallback = None
        
        self.longClickTime = 2000
        
        self.buttonState = 1
        
        self.clickedFlag: bool = False;
        self.longClickedFlag: bool = False;
        
        self.buttonDownStartTicks = 0;
        
        self.button = Pin(15,Pin.IN,Pin.PULL_UP)
        self.button.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler = self.__button_interruptHandler)


    def __button_interruptHandler(self, buttonPin):
        print("Button_Interrupt")
        
        # Disable interrupts while handling this one
        self.button.irq(handler = None)
        
        # If we weren't pressed, but we're now Released
        if((self.buttonState == 0) and (self.button.value() == 1)):
            self.buttonState = 1
            
            # ToDo: Determine LongClick
            if(self.buttonDownStartTicks != -1):
                delta = time.ticks_diff(time.ticks_ms(), self.buttonDownStartTicks) # compute time difference
                
            self.buttonDownStartTicks = -1
            self.clickedFlag = True
            
            print("button_Released")
            
        # If we were Released, but we're now pressed
        if((self.buttonState == 1) and (self.button.value() == 0)):
            self.buttonState = 0
            self.buttonDownStartTicks = time.ticks_ms() # get millisecond counter
            print("button_Pressed")
        
        #Re-enable the interrupts
        self.button.irq(handler = self.__button_interruptHandler)


    def setclickCallback(self, callback):
        self.clickCallback = callback
    
    def setLongClickCallback(self, callback):
        self.longClickCallback = callBack


    # Execute this method from your main application loop for the appropriate callbacks to be called
    # This is to prevent lengthy application code to be executed on the interrupt handler routine
    def execute(self):
        #Call the callbacks
        
        if(self.clickedFlag):
            if(self.clickCallback != None):
                self.clickCallback()
                
            self.clickedFlag = False



def clickTestCallback():
    print("Clicked from the callback")

# Only run this to test the library
if __name__ == '__main__':
    
    button = Button(15)
    button.setclickCallback(clickTestCallback);
    
    while(True):
        button.execute()
        time.sleep_ms(1)
        

