#-------------------------------------------------------------------------------
# Name:        Wii Remote - connect to Bluetooth cwiid
# Purpose:
#
# Author:      Brian Hensley
#
# Created:     21/07/2012
# Copyright:   (c) Brian 2012
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import cwiid
import time


def main():

        print 'Press button 1 + 2 on your Wii Remote...'
        time.sleep(1)

        wm=cwiid.Wiimote()
	print 'Wii Remote connected...'
	print '\nPress the PLUS button to disconnect the Wii and end the application'
        time.sleep(1)
	
	Rumble = False
        wm.rpt_mode = cwiid.RPT_BTN
	
	position = 50
	print 'starting position: ', position

        while True:
            if wm.state['buttons'] == 2048:
               	print 'Left button pressed \n'
                time.sleep(.1)

            if wm.state['buttons'] == 1024:
                print 'Right button pressed \n'
                time.sleep(.1)

	    if wm.state['buttons'] == 1025:
		print 'Moving Forward, Wheel position: ', position
		time.sleep(.1)

	    if wm.state['buttons'] == 1026:
		print 'Moving Reverse, Wheel position: ', position
		time.sleep(.1) 

	    if wm.state['buttons'] == 2049:
		print 'Moving Forward, Wheel position: ', position
		time.sleep(.1) 

	    if wm.state['buttons'] == 2050:
		print 'Moving Reverse, Wheel position: ', position
		time.sleep(.1) 

	    if wm.state['buttons'] == 512:
		print 'Position: ', position
		time.sleep(.1)

            if wm.state['buttons'] == 2:
                print 'Button 1 pressed'
                time.sleep(.1)

            if wm.state['buttons'] == 1:
                print 'Button 2 pressed'
                time.sleep(.1)
	    if wm.state['buttons'] == 16:
		if Rumble == False:		
			wm.rumble = True
			Rumble = True
			time.sleep(1)
		elif Rumble == True:
			wm.rumble = False
			Rumble = False
			time.sleep(1)
	    if wm.state['buttons'] == 4096:
		print 'closing Bluetooth connection. Good Bye!'
		time.sleep(1)
		exit(wm)


if __name__ == '__main__':
    main()

