from sevenSegmentDraw import SevenSegmentDigit

#Represents a multi Digit Seven Segment Display
class MultiDigitDisplay:

    def __init__(self,
                 frameBuf: framebuf.FrameBuffer,
                 x: int,
                 y: int,
                 digitCount: int = 2,
                 digitWidth:int = 15,
                 digitHeight: int = 30,
                 digitSpacing: int = 6,
                 segmentThickness: int = 4,
                 displayLeadingZeros: bool = True,
                 ):
    
        self.display = frameBuf
        self.x = x
        self.y = y
        self.digitWidth = digitWidth
        self.digitSpacing = digitSpacing
        self.segmentThickness = segmentThickness
        self.digitCount = digitCount
        self.digits = []
        self.number = 0
        self.displayLeadingZeros = displayLeadingZeros
        self.decimalSeperatorIndex = -1
        self.Height = digitHeight
        self.Width = (digitWidth * digitCount) + (digitSpacing * (digitCount - 1))
        
        # Instatiate the individual digits and calculate their x positions
        xPos = x
        for i in range(digitCount):
            digit = SevenSegmentDigit(self.display, xPos, y, digitWidth, digitHeight, segmentThickness)
            self.digits.append(digit)
            xPos += digitWidth + digitSpacing
            
    
    # draws the specified number to the frame buffer.
    # Optionally a decimal separator index can be specified. Set to -1 to disable
    def displayNumber(self,
                      number: int,
                      decimalSeparatorIndex: int = -1):
        
        self.number = number
        self.decimalSeperatorIndex = decimalSeparatorIndex
        
        self.__drawNumber()
        self.__drawDecimalSeparator()
        
        
    def __drawNumber(self):
        
        num:int = self.number
        digitIndex = 1
              
        # Mathematically get the individual number that needs the be drawn at the specific digit
        for i in range(self.digitCount -1, -1, -1):
            
            modulus = digitIndex * 10
            drawDigit = (num > 0
                         or self.displayLeadingZeros
                         or i == self.digitCount -1)
 
            if(drawDigit):
                digitVal : int = num % modulus
            else:
                digitVal = -1
            
            self.digits[i].displayNumber(digitVal)
            num = int(num / 10)
            digitIndex + 1
        
        
    def __drawDecimalSeparator(self):
        
        if((self.decimalSeperatorIndex >= 0) and (self.decimalSeperatorIndex <= self.digitCount)):
            xPos = self.x + self.Width - (self.decimalSeperatorIndex * (self.digitWidth + self.digitSpacing))
            xCenterAdjust = int((self.digitSpacing - self.segmentThickness) / 2)
            xPos += xCenterAdjust
            yPos = self.y + self.Height - self.segmentThickness
            self.display.rect(xPos, yPos, self.segmentThickness, self.segmentThickness, 1, 1)
        
    
    
if __name__=='__main__':
    print("This library is not intended to be executed directly")
    
