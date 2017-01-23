import picamera.array
import picamera
import time, sys

class main:
    def __init__(self):
        #Camera setup
        self.camera = picamera.PiCamera()
        self.camera.resolution = (480, 640)
        self.rawCapture = picamera.array.PiRGBArray(self.camera)
        print "Camera initialised"
        
        #Other variable declerations
        self.currentFrame = None
        self.oldFrame = None
        self.segmentCount = 5
        self.segmentAccuracy = 16
        self.detectionTollerance = 100
        
        print "Initiation completed..."
        print "Letting camera settle..."
        time.sleep(1)
        print "Done"
        
        
        
    def setSegmentCount(self, newSegmentCount):
        """The number of segments wanted in both the x and y axis per frame"""
        self.segmentCount = newSegmentCount
    def setSegmentAccuracy(self, newSegmentAccuracy):
        """The reciprocal coefficient of the amount of pixels to be analysed per segment"""
        self.segmentAccuracy = newSegmentAccuracy
    def setDetectionTollerance(self, newTollerance):
        """How different a new generation of a segment has to be to trigger movement"""
        self.detectionTollerance = newTollerance
        
    def getSegmentCount(self):
		"""Returns the number of segments per frame"""
		return self.segmentCount
	def getSegmentAccuracy(self):
		"""Returns the reciprocal coefficient of the amount of pixels to be analysed per segment"""
		return self.segmentAccuracy
	def getDetectionTollerance(self):
		"""Returns the difference of the RGB average between segments in frames that has to be surpassed to trigger movement"""
		return self.detectionTollerance
        
    def startRecord(self):
        #current and old frame start as the same - now called frame
        self.currentFrame = self.getImageAverage()
        self.oldFrame = self.currentFrame
        
    def endRecord(self):
        io.cleanup()
        self.rawCapture.truncate(0)
        print "systems cleaned and ready for shutdown. Goodbye."
        
    def detectMovement(self):
        detection = False
        self.oldFrame = self.currentFrame
        self.currentFrame = self.getImageAverage()
        for y in range(self.segmentCount):
            for x in range(self.segmentCount):
                for n in range(3):
                    if abs(self.oldFrame[y][x][n] - self.currentFrame[y][x][n] > self.detectionTollerance):
                        detection = True
                        break
        return detection

    def getImageAverage(self):
        processedFrame = []
        for n in range(self.segmentCount):
            processedFrame.append([])
        
        self.camera.capture(self.rawCapture, "rgb", use_video_port=True)###FORMAT WAS BGR IF DOESN'T WORK, REVERSE IT BACK
        frame = self.rawCapture
        frame = frame.array
        
        segmentWidth = (640/self.segmentCount)
        segmentHeight = (480/self.segmentCount)
        
        for y in range(self.segmentCount):
            for x in range(self.segmentCount):
                minx = x*segmentWidth
                miny = y*segmentHeight
                
                segmentAverage = [0, 0, 0]
                segmentAverage[0] = frame[minx, miny, 0]
                segmentAverage[1] = frame[minx, miny, 1]
                segmentAverage[2] = frame[minx, miny, 2]
                #print "Segment ", x, y                         
                for segmentY in range(segmentHeight/self.segmentAccuracy):
                    for segmentX in range(segmentWidth/self.segmentAccuracy):
                
                        segmentAverage[0] = segmentAverage[0]+frame[segmentX*self.segmentAccuracy+minx, segmentY*self.segmentAccuracy+miny, 0]/2
                        segmentAverage[1] = segmentAverage[1]+frame[segmentX*self.segmentAccuracy+minx, segmentY*self.segmentAccuracy+miny, 1]/2
                        segmentAverage[2] = segmentAverage[2]+frame[segmentX*self.segmentAccuracy+minx, segmentY*self.segmentAccuracy+miny, 2]/2
                processedFrame[y].append(segmentAverage)
        self.rawCapture.truncate(0)#Removes previous frames
        return processedFrame