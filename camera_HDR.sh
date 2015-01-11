#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")
DATE_m10=$(date +"%Y-%m-%d_%H%M")_m10
DATE_m5=$(date +"%Y-%m-%d_%H%M")_m5
DATE_0=$(date +"%Y-%m-%d_%H%M")_0
DATE_p5=$(date +"%Y-%m-%d_%H%M")_p5
DATE_p10=$(date +"%Y-%m-%d_%H%M")_p10

OPT="-ISO 100 -awb none -ifx none -drc off"

raspistill $OPT -v -t 1 -vf -hf -w 1024 -h 768 -ss 600 -o /home/pi/camera/$DATE_m10.jpg
raspistill $OPT -v -t 1 -vf -hf -w 1024 -h 768 -ss 6000 -o /home/pi/camera/$DATE_m5.jpg
raspistill $OPT -v -t 1 -vf -hf -w 1024 -h 768 -ss 60000 -o /home/pi/camera/$DATE_0.jpg
raspistill $OPT -v -t 1 -vf -hf -w 1024 -h 768 -ss 600000 -o /home/pi/camera/$DATE_p5.jpg
raspistill $OPT -v -t 1 -vf -hf -w 1024 -h 768 -ss 6000000 -o /home/pi/camera/$DATE_p10.jpg


enfuse -o /home/pi/camera/$DATE.jpg \
          /home/pi/camera/$DATE_m10.jpg \
          /home/pi/camera/$DATE_m5.jpg \
          /home/pi/camera/$DATE_0.jpg \
          /home/pi/camera/$DATE_p5.jpg \
          /home/pi/camera/$DATE_p10.jpg 

#raspistill Camera App v1.3.8

#Runs camera for specific time, and take JPG capture at end if requested

#usage: raspistill [options]

#Image parameter commands

#-?, --help	: This help information
#-w, --width	: Set image width <size>
#-h, --height	: Set image height <size>
#-q, --quality	: Set jpeg quality <0 to 100>
#-r, --raw	: Add raw bayer data to jpeg metadata
#-o, --output	: Output filename <filename> (to write to stdout, use '-o -'). If not specified, no file is saved
#-l, --latest	: Link latest complete image to filename <filename>
#-v, --verbose	: Output verbose information during run
#-t, --timeout	: Time (in ms) before takes picture and shuts down (if not specified, set to 5s)
#-th, --thumb	: Set thumbnail parameters (x:y:quality) or none
#-d, --demo	: Run a demo mode (cycle through range of camera options, no capture)
#-e, --encoding	: Encoding to use for output file (jpg, bmp, gif, png)
#-x, --exif	: EXIF tag to apply to captures (format as 'key=value') or none
#-tl, --timelapse	: Timelapse mode. Takes a picture every <t>ms
#-fp, --fullpreview	: Run the preview using the still capture resolution (may reduce preview fps)
#-k, --keypress	: Wait between captures for a ENTER, X then ENTER to exit
#-s, --signal	: Wait between captures for a SIGUSR1 from another process
#-g, --gl	: Draw preview to texture instead of using video render component
#-gc, --glcapture	: Capture the GL frame-buffer instead of the camera image
#-set, --settings	: Retrieve camera settings and write to stdout
#-cs, --camselect	: Select camera <number>. Default 0
#-bm, --burst	: Enable 'burst capture mode'
#-md, --mode	: Force sensor mode. 0=auto. See docs for other modes available

#Preview parameter commands

#-p, --preview	: Preview window settings <'x,y,w,h'>
#-f, --fullscreen	: Fullscreen preview mode
#-op, --opacity	: Preview window opacity (0-255)
#-n, --nopreview	: Do not display a preview window

#Image parameter commands

#-sh, --sharpness	: Set image sharpness (-100 to 100)
#-co, --contrast	: Set image contrast (-100 to 100)
#-br, --brightness	: Set image brightness (0 to 100)
#-sa, --saturation	: Set image saturation (-100 to 100)
#-ISO, --ISO	: Set capture ISO
#-vs, --vstab	: Turn on video stabilisation
#-ev, --ev	: Set EV compensation
#-ex, --exposure	: Set exposure mode (see Notes)
#-awb, --awb	: Set AWB mode (see Notes)
#-ifx, --imxfx	: Set image effect (see Notes)
#-cfx, --colfx	: Set colour effect (U:V)
#-mm, --metering	: Set metering mode (see Notes)
#-rot, --rotation	: Set image rotation (0-359)
#-hf, --hflip	: Set horizontal flip
#-vf, --vflip	: Set vertical flip
#-roi, --roi	: Set region of interest (x,y,w,d as normalised coordinates [0.0-1.0])
#-ss, --shutter	: Set shutter speed in microseconds
#-awbg, --awbgains	: Set AWB gains - AWB mode must be off
#-drc, --drc	: Set DRC Level
#-st, --stats	: Force recomputation of statistics on stills capture pass

#Notes

#Exposure mode options :
#auto,night,nightpreview,backlight,spotlight,sports,snow,beach,verylong,fixedfps,antishake,fireworks

#AWB mode options :
#off,auto,sun,cloud,shade,tungsten,fluorescent,incandescent,flash,horizon

#Image Effect mode options :
#none,negative,solarise,sketch,denoise,emboss,oilpaint,hatch,gpen,pastel,watercolour,film,blur,saturation,colourswap,washedout,posterise,colourpoint,colourbalance,cartoon

#Metering Mode options :
#average,spot,backlit,matrix

#Dynamic Range Compression (DRC) options :
#off,low,med,high

#Preview parameter commands

#-gs, --glscene	: GL scene square,teapot,mirror,yuv,sobel
#-gw, --glwin	: GL window settings <'x,y,w,h'>

