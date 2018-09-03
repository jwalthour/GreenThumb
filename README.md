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
- Cheap fountain pumps tend to have a limited "head" - the height to which they can raise water.  However, you absolutely must maintain a positive head - the outlet must be above the inlet - or else you will start a siphon.  If you have a negative head (reservoir water level is above the outlet), turning on the pump once will drain the whole reservoir into your plant.  The pump I bought was a simple centrifugal impeller, so when you turn it off, it does not impede the flow at all.
- Wiring diagram: https://github.com/jwalthour/GreenThumb/blob/master/2018-8-26%20green%20thumb%20wiring%20diagram.pdf
