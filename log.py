#!/usr/bin/python
# -*- coding: UTF-8 -*-

import httplib,urllib,serial,time,struct sht31
ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, stopbits=1, parity="N", timeout=2)

headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

ser.flushInput()

byte, lastbyte = "\x00", "\x00"

while lastbyte == "\xAA" and byte == "\xC0"::
    lastbyte = byte
    byte = ser.read(size=1)

        sentence = ser.read(size=8) # Read 8 more bytes
        readings = struct.unpack('<hhxxcc',sentence) # Decode the packet - big endian, 2 shorts for pm2.5 and pm10, 2 reserved bytes, checksum, message tail

        pm_25 = readings[0]/10.0
        pm_10 = readings[1]/10.0
        # ignoring the checksum and message tail
        (temp,hum) = sht31.readTempHum()
        temp = round(temp,2)
        hum = round(hum,2)
        print "PM 2.5:",pm_25,"μg/m^3  PM 10:",pm_10,"μg/m^3 Temp (C):",temp," RH: ",hum
        params = urllib.urlencode({'field1': pm_25, 'field2': pm_10,'field3':temp,'field4':hum,'key':'3LJ9WGIX9NGGCS3K'})
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
	           conn.request("POST", "/update", params, headers)
	           conn.close()
               print "upload OK"
        except:
	           print "connection failed"
