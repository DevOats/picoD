from machine import Pin
import time



# Implements an abstraction for a button, supporting normal and long presses.
# The button used GPIO interrupts, however the callbacks are executed on the main application thread.
class Button:
    
    # Constructor
    def __init__(self,
                 gpioPinNumber: int,
                 clickCallback: Callable = None,
                 longClickCallback: Callable = None,
                 longClickTimeMs: int = 1500):
        
        self.clickCallback = clickCallback
        self.longClickCallback = longClickCallback
        self.longClickTimeMs = longClickTimeMs
        
        self.buttonState = 1
        self.clickedFlag: bool = False
        self.buttonDownStartTicks = -1;
        
        self.button = Pin(gpioPinNumber,Pin.IN,Pin.PULL_UP)
        self.button.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler = self.__button_interruptHandler)


    def __button_interruptHandler(self, buttonPin):
        
        # Disable interrupts while handling this one
        self.button.irq(handler = None)
        
        # If we weren't pressed, but we're now Released
        if((self.buttonState == 0) and (self.button.value() == 1)):
            self.buttonState = 1
            self.buttonDownStartTicks = -1
            self.clickedFlag = True
            
        # If we were Released, but we're now pressed
        if((self.buttonState == 1) and (self.button.value() == 0)):
            self.buttonState = 0
            self.buttonDownStartTicks = time.ticks_ms() # get millisecond counter
        
        #Re-enable the interrupts
        self.button.irq(handler = self.__button_interruptHandler)


    # Sets the callback for handling standard button clicks
    def setclickCallback(self, callback: Callable):
        self.clickCallback = callback
    
    
    # sets the callback for handling long presses
    def setLongClickCallback(self, callback: Callable):
        self.longClickCallback = callback


    # Clears the state of the button and resets any pending callbacks
    # Note that this will not remove the assigenedd callback methods
    def reset(self):
        self.buttonState = 1
        self.clickedFlag = False
        self.buttonDownStartTicks = -1


    # Execute this method from your main application loop for the appropriate callbacks to be called
    # This is to prevent lengthy application code to be executed on the interrupt handler routine
    def execute(self):
        
        # Determine if the button has been clicked
        if(self.clickedFlag):
            if(self.clickCallback != None):
                self.clickCallback()
                
            self.clickedFlag = False
            
        
        # Determine if we waited long enough for a long click if the button is still down
        if(self.buttonState == 0 and (self.longClickCallback != None)):
            if(self.buttonDownStartTicks != -1):
                deltaMs = time.ticks_diff(time.ticks_ms(), self.buttonDownStartTicks) # compute time difference
                
                if(deltaMs > self.longClickTimeMs):
                    self.longClickCallback()
                    self.buttonState = 1
                    self.buttonDownStartTicks = -1



#
# Manual test code from here
#

def clickTestCallback():
    print("Clicked from the callback")
    
    
def longClickTestCallback():
    print("Long click from the callback")


# Only run this to test the library
if __name__ == '__main__':
    
    print("Running the button module is only for testing it")
    
    # Create a button and assign the click and longClick event callbacks
    button = Button(15,
                    clickTestCallback,
                    longClickTestCallback)
    
    # Reset the button state (only here for reference purposes. Not actually needed after instantiating)
    button.reset()
    
    # Alternatively the click and longLick callbacks can be set by calling these two methods:
    #button.setclickCallback(clickTestCallback)
    #button.setLongClickCallback(longClickTestCallback)
    
    
    # In your application logic, periodically call the execute function.
    # This will in turn call the callback methods whe applicable
    while(True):
        button.execute()
        time.sleep_ms(1)
        

