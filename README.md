# GreenThumb
A system to automatically tend plants

# BOM
- Water pump https://www.amazon.com/gp/product/B07CZ7XFCF/
- Raspberry Pi Zero W (I set up the SD card image on a full-size Pi so that it was easier to connect to it with internet access)
- ADC: https://www.adafruit.com/product/1083
- Motor driver: https://www.sparkfun.com/products/9479
- Motor driver breakout: https://www.sparkfun.com/products/9540
- Moisture sensor: https://www.sparkfun.com/products/13322
- Conformal coat: https://www.amazon.com/gp/product/B008O9YIV6

# Assembly notes
- Wiring diagram: https://github.com/jwalthour/GreenThumb/blob/master/2018-8-26%20green%20thumb%20wiring%20diagram.pdf
- Used this manual to set up the Pi as an access point: https://learn.sparkfun.com/tutorials/setting-up-a-raspberry-pi-3-as-an-access-point 

# Operation and setup notes
- Cheap fountain pumps tend to have a limited "head" - the height to which they can raise water.  However, you absolutely must maintain a positive head - the outlet must be above the inlet - or else you will start a siphon.  If you have a negative head (reservoir water level is above the outlet), turning on the pump once will drain the whole reservoir into your plant.  The pump I bought was a simple centrifugal impeller, so when you turn it off, it does not impede the flow at all.  Note that, in the assembly photos, the output of the hose is held above the surface of the soil, to prevent this effect.
- Make sure you have an overflow catch tray that is capable of catching the entire contents of the input reservoir.  This way, if something bugs out and the pump just goes forever, it doesn't make a huge mess everywhere.  Note the small mason jar as an input reservoir, and the large output catch tray.
- These sensors work on electrical resistance between two electrodes.  They're measuring the minimum resistance between any two points along the electrodes.  Thus, if you push them all 2" or so into the soil, they're measuring the wettest point along a 2" deep column.  So you can have a bone-dry surface, and still have the sensors report "super damp", if it's super damp 2" down.  So you'll note the sensors in the photos aren't inserted all the way, which is intentional.
