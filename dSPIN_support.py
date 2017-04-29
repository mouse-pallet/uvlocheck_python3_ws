import dSPIN as hd
import wiringpi2 as wp


def dSPIN_Xfer(data):
    wp.digitalWrite(hd.dSPIN_CS, wp.GPIO.LOW);

    for i in range(8):
        wp.digitalWrite(hd.dSPIN_CLK, wp.GPIO.LOW);

        if(data & 0x80):
            wp.digitalWrite(hd.dSPIN_MOSI, wp.GPIO.HIGH);
        else:
            wp.digitalWrite(hd.dSPIN_MOSI, wp.GPIO.LOW);
        wp.delayMicroseconds( hd.dSPIN_SPI_CLOCK_DELAY);

        data <<= 1;

        if(wp.digitalRead(hd.dSPIN_MISO)):
            data |= 1;

        wp.digitalWrite(hd.dSPIN_CLK, wp.GPIO.HIGH);

        wp.delayMicroseconds( hd.dSPIN_SPI_CLOCK_DELAY);

    wp.digitalWrite(hd.dSPIN_CS, wp.GPIO.HIGH);
    wp.delayMicroseconds( hd.dSPIN_SPI_CLOCK_DELAY );

    return data


def dSPIN_Param(value, bit_len):
    ret_val=0;        # We'll return this to generalize this function
                                  #  for both read and write of registers.
    byte_len = (bit_len*1.0)/8;      # How many BYTES do we have?
    if (bit_len%8 > 0):
        byte_len=bit_len+1  # Make sure not to lose any partial byte values.
    # // Let's make sure our value has no spurious bits set, and if the value was too
    # //  high, max it out.
    mask = 0xffffffff >> (32-bit_len);

    if (value > mask):
        value = mask;
    # // The following three if statements handle the various possible byte length
    # //  transfers- it'll be no less than 1 but no more than 3 bytes of data.
    # // dSPIN_Xfer() sends a byte out through SPI and returns a byte received
    # //  over SPI- when calling it, we typecast a shifted version of the masked
    # //  value, then we shift the received value back by the same amount and
    # //  store it until return time.
    if (byte_len == 3) :
        ret_val |= dSPIN_Xfer(value>>16) << 16;
        # //Serial.println(ret_val, HEX);

    if (byte_len >= 2) :
        ret_val |= dSPIN_Xfer(value>>8) << 8;
    # //Serial.println(ret_val, HEX);

    if (byte_len >= 1):
        ret_val |= dSPIN_Xfer(value);
    # //Serial.println(ret_val, HEX);

    # // Return the received values. Mask off any unnecessary bits, just for
    # //  the sake of thoroughness- we don't EXPECT to see anything outside
    # //  the bit length range but better to be safe than sorry.
    #    print("ret_val")
    #    print(bin(ret_val))
    #    print("mask")
    #    print(bin(mask))

    #    print("ret_val & mask")
    #    print(ret_val & mask)

    return (ret_val & mask)


def MaxSpdCalc(stepsPerSec):
    temp = stepsPerSec * 0.065536;
    if( temp > 0x000003FF):
        return 0x000003FF;
    else:
        return int(temp);


def MinSpdCalc(stepsPerSec):
    temp = stepsPerSec * 4.1943;
    if( temp > 0x00000FFF):
        return 0x00000FFF;
    else:
        return int(temp);

def FSCalc(stepsPerSec):
    temp = (stepsPerSec * .065536)-.5;
    if( temp > 0x000003FF):
        return 0x000003FF;
    else:
        return int(temp);


def dSPIN_init():
    err = 0;
    err = wp.wiringPiSetupGpio();
    wp.pinMode(hd.dSPIN_BUSYN, wp.GPIO.INPUT);
    wp.pinMode(hd.dSPIN_RESET, wp.GPIO.OUTPUT);
    wp.pinMode(hd.dSPIN_CS, wp.GPIO.OUTPUT);
    wp.digitalWrite(hd.dSPIN_CS, wp.GPIO.HIGH);

    if( err !=0):
        print("wiringPi Setup failed with Error"+err);
        return hd.dSPIN_STATUS_FATAL;
    wp.pinMode(hd.dSPIN_MOSI, wp.GPIO.OUTPUT);
    wp.pinMode(hd.dSPIN_MISO, wp.GPIO.INPUT);
    wp.pinMode(hd.dSPIN_CLK,  wp.GPIO.OUTPUT);

    # //SPI_MODE3 (clock idle high, latch data on rising edge of clock)
    wp.digitalWrite(hd.dSPIN_CLK, wp.GPIO.HIGH);

    # // reset the dSPIN chip. This could also be accomplished by
    # //  calling the "dSPIN_ResetDev()" function after SPI is initialized.
    wp.digitalWrite(hd.dSPIN_RESET, wp.GPIO.HIGH);
    wp.delay(2);
    wp.digitalWrite(hd.dSPIN_RESET, wp.GPIO.LOW);
    wp.delay(2);
    wp.digitalWrite(hd.dSPIN_RESET, wp.GPIO.HIGH);
    wp.delay(2);


    return 0;


