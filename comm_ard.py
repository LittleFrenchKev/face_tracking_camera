import serial

class ard_connect():
    def __init__(self, parent):
        self.parent = parent
        self.startMarker = 60 #utf-8 for '<'
        self.endMarker = 62   #utf-8 for '>'
        #self.ser = serial.Serial('COM3', 9600)
        print("ard created")


    def connect(self, port):
        try:
            self.ser = serial.Serial(port, 115200)
            self.waitForArduino()
            self.parent.is_connected = True
            return True
        except:
            print("Not able to connect on this port")
            return False

    def waitForArduino(self):

        msg = ""
        while msg.find("Hasta la vista baby") == -1:  #string.find() return -1 if value not found

            while self.ser.inWaiting() == 0:  #inWaiting() return number of bytes in buffer, equivalent of Serial.available in arduino
                pass

            msg = self.recvFromArduino()   #return decoded serial data
            print(msg)  # python3 requires parenthesis
            #print()

    def recvFromArduino(self):

        message_received = "" #message received start as an empty string
        x = "z"  #next char read from serial . need to start as any value that is not an end- or startMarker
        byteCount = -1  #to allow for the fact that the last increment will be one too many

        # wait for the start character
        while ord(x) != self.startMarker:  # ord() return utf-8 for a char(1 length string)  ex: return 60 for char <
            x = self.ser.read()  # loop until start marker found

        # save data until the end marker is found
        while ord(x) != self.endMarker:  # loop until end marker found
            if ord(x) != self.startMarker:  # if not start marker
                message_received = message_received + x.decode("utf-8")  # add decoded char to string
                byteCount += 1  # WHY IS BYTECOUNT FOR?
            x = self.ser.read()  # read next char

        return (message_received)

    def sendToArduino(self, sendStr):
        #print("sent to arduino func : ", sendStr)
        self.ser.write(sendStr.encode('utf-8'))  # change for Python3
        #self.ser.write(sendStr)  #send data as it is if only dealing with int

    def runTest(self, message_to_send):

        waitingForReply = False

        if waitingForReply == False:
            self.sendToArduino(message_to_send)  # write message to serial
            waitingForReply = True

        if waitingForReply == True:    #waitfor datafrom arduino
            while self.ser.inWaiting() == 0:   # equivalent of Serial.available in arduino
                pass  # loop until data available

            dataRecvd = self.recvFromArduino() # SPLIT STRING INTO INT TO HAVE USABLE DATA


            split_data = dataRecvd.split(",")
            #self.parent.update_LCD_display(split_data[0], split_data[1])
            try:
                self.parent.current_pan = split_data[0]
                self.parent.current_tilt = split_data[1]
                self.parent.update_LCD_display()
            except:
                print("error split data : ", len(split_data))

            #print("Reply Received  " + dataRecvd)

            waitingForReply = False

            #print("===========")