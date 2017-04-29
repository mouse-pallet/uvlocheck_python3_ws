import wiringpi2 as wp
import dSPIN as hd
import dSPIN_command as com
import dSPIN_support as sup
import webiopi

def setup():

    ans = 0;
    sup.dSPIN_init();


    print("Confug:"+('%x' % hd.dSPIN_CONFIG));
    print("Status:"+('%x' % hd.dSPIN_STATUS));
    print("config register = {0}" .format(hex(com.dSPIN_GetParam(hd.dSPIN_CONFIG))));

    com.dSPIN_SetParam(hd.dSPIN_STEP_MODE, (not hd.dSPIN_SYNC_EN) | hd.dSPIN_STEP_SEL_1_2 | hd.dSPIN_SYNC_SEL_1)

    print("step_mode = {0}" .format(hex(com.dSPIN_GetParam(hd.dSPIN_STEP_MODE))))


    com.dSPIN_SetParam(hd.dSPIN_MAX_SPEED, sup.MaxSpdCalc(2000));
    print("max_speed = {0}" .format(hex(com.dSPIN_GetParam(hd.dSPIN_MAX_SPEED))))

    com.dSPIN_SetParam(hd.dSPIN_FS_SPD, sup.FSCalc(400));
    print("fs_speed = {0}" .format(hex(com.dSPIN_GetParam(hd.dSPIN_FS_SPD))))
    com.dSPIN_SetParam(hd.dSPIN_ACC, 0x05);
    print("acc = {0}" .format(hex(com.dSPIN_GetParam(hd.dSPIN_ACC))))

    com.dSPIN_SetParam(hd.dSPIN_OCD_TH, hd.dSPIN_OCD_TH_3750mA);
    print("OCD_TH = {0}" .format(hex(com.dSPIN_GetParam(hd.dSPIN_OCD_TH))))


    com.dSPIN_SetParam(hd.dSPIN_CONFIG,
                       hd.dSPIN_CONFIG_PWM_DIV_2 | hd.dSPIN_CONFIG_PWM_MUL_1 | hd.dSPIN_CONFIG_SR_290V_us
                     | hd.dSPIN_CONFIG_OC_SD_DISABLE | hd.dSPIN_CONFIG_VS_COMP_ENABLE
                     | hd.dSPIN_CONFIG_SW_USER | hd.dSPIN_CONFIG_INT_16MHZ);

    print("dSPIN_CONFIG = {0}" .format(hex(com.dSPIN_GetParam(hd.dSPIN_CONFIG))))
    com.dSPIN_SetParam(hd.dSPIN_KVAL_RUN, 0xFF);
    print("KVAL_RUN = {0}" .format(hex(com.dSPIN_GetParam(hd.dSPIN_KVAL_RUN))))

    print("Status code is:{0} See datasheet sec.9.1.22 to decode.".format(hex(com.dSPIN_GetStatus())));

    wp.delay(200);

    ans = com.dSPIN_GetStatus() & 0x0200;
    print("ans = {0}".format(hex));
    print(hex(ans))
    while(ans == 0x0000):
        print("Undervoltage lockout is active:")
        print(com.dSPIN_GetStatus());
        ans = com.dSPIN_GetStatus() & 0x0200;
        wp.delay(500);

def loop():
    pass

@webiopi.macro
def mae(radian):
    print("Status code is:{0} See datasheet sec.9.1.22 to decode.".format(hex(com.dSPIN_GetStatus())));

    com.dSPIN_Move(hd.FWD, int(radian));
    print("command completed 'dSPIN_Move(FWD, 200);'\n");

    while (wp.digitalRead(hd.dSPIN_BUSYN) == wp.GPIO.LOW):
        pass

    print("no longer busy; sending next command");
    com.dSPIN_SoftStop();

    while (wp.digitalRead(hd.dSPIN_BUSYN) == wp.GPIO.LOW):
        pass
    wp.delay(500);

@webiopi.macro
def ushiro(radian):
    com.dSPIN_Move(hd.REV, int(radian));

    while (wp.digitalRead(hd.dSPIN_BUSYN) == wp.GPIO.LOW):
        pass
    com.dSPIN_SoftStop();

    while (wp.digitalRead(hd.dSPIN_BUSYN) == wp.GPIO.LOW):
        pass
    wp.delay(500);


#setup()
#ushiro()
#mae()
