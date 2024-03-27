from inc_noesis import *


def registerNoesisTypes():
    handle = noesis.register("Battle Mages (2003) mark images", ".mrk")
    noesis.setHandlerTypeCheck(handle, bmsCheckType)
    noesis.setHandlerLoadRGBA(handle, bmsLoadRGBA)

    return 1
         
  
class BMsMarkImage:
    def __init__(self, reader):
        self.filereader = reader
        self.width = 0
        self.height = 0
        self.size = 0
 
    def parseHeader(self): 
        self.filereader.seek(12, NOESEEK_ABS)    
        self.width = self.filereader.readUShort()
        self.height = self.filereader.readUShort()
        self.bytesPerPixel = (self.filereader.readUShort() & 0xFF) >> 3
   
        return 0

    def readImage(self):
        data = self.filereader.readBytes(self.width * self.height * self.bytesPerPixel)
        format = {3:"r8g8b8", 4:"r8g8b8a8"}        
        self.data = rapi.imageDecodeRaw(data, self.width, self.height, format[self.bytesPerPixel])       
         
    def read(self):
        self.parseHeader()
        self.readImage()
    
    
def bmsCheckType(data):
    img = BMsMarkImage(NoeBitStream(data))
    if img.parseHeader() != 0:
        return 0
        
    return 1  


def bmsLoadRGBA(data, texList):
    #noesis.logPopup() 
    image = BMsMarkImage(NoeBitStream(data))       
    image.read() 
    
    texList.append(NoeTexture("tex", image.width, image.height, image.data, noesis.NOESISTEX_RGBA32))
            
    return 1
