import dSPIN_support as sup
import dSPIN as hd


def dSPIN_ParamHandler(param, value):
    ret_val=0

    if param == hd.dSPIN_ABS_POS:
        ret_val = sup.dSPIN_Param(value, 22);

    if param == hd.dSPIN_EL_POS:
        ret_val = sup.dSPIN_Param(value, 9);

    if param == hd.dSPIN_MARK:
        ret_val = sup.dSPIN_Param(value, 22);

    if param == hd.dSPIN_SPEED:
        ret_val = sup.dSPIN_Param(0, 20);

    if param == hd.dSPIN_ACC:
        ret_val = sup.dSPIN_Param(value, 12);

    if param == hd.dSPIN_DEC:
        ret_val = sup.dSPIN_Param(value, 12);

    if param == hd.dSPIN_MAX_SPEED:
        ret_val = sup.dSPIN_Param(value, 10);

    if param == hd.dSPIN_MIN_SPEED:
        ret_val = sup.dSPIN_Param(value, 12);

    if param == hd.dSPIN_FS_SPD:
        ret_val = sup.dSPIN_Param(value, 10);

    if param == hd.dSPIN_KVAL_HOLD:
        ret_val = sup.dSPIN_Xfer(value);

    if param == hd.dSPIN_KVAL_RUN:
        ret_val = sup.dSPIN_Xfer(value);

    if param == hd.dSPIN_KVAL_ACC:
        ret_val = sup.dSPIN_Xfer(value);

    if param == hd.dSPIN_KVAL_DEC:
        ret_val = sup.dSPIN_Xfer(value);

    if param == hd.dSPIN_INT_SPD:
        ret_val = sup.dSPIN_Param(value, 14);

    if param == hd.dSPIN_ST_SLP:
        ret_val = sup.dSPIN_Xfer(value);

    if param == hd.dSPIN_FN_SLP_ACC:
        ret_val = sup.dSPIN_Xfer(value);

    if param == hd.dSPIN_FN_SLP_DEC:
        ret_val = sup.dSPIN_Xfer(value);

    if param == hd.dSPIN_K_THERM:
        ret_val = sup.dSPIN_Xfer(value & 0x0F);

    if param == hd.dSPIN_ADC_OUT:
        ret_val = sup.dSPIN_Xfer(0);

    if param == hd.dSPIN_OCD_TH:
        ret_val = sup.dSPIN_Xfer(value & 0x0F);

    if param == hd.dSPIN_STALL_TH:
        ret_val = sup.dSPIN_Xfer(value & 0x7F);

    if param == hd.dSPIN_STEP_MODE:
       ret_val = sup.dSPIN_Xfer(value)

    if param == hd.dSPIN_CONFIG:
        ret_val = sup.dSPIN_Param(value, 16)

    return ret_val


def dSPIN_SetParam(param,value):
    sup.dSPIN_Xfer(hd.dSPIN_SET_PARAM | param);
    dSPIN_ParamHandler(param, value);

def dSPIN_GetParam(param):
    sup.dSPIN_Xfer(hd.dSPIN_GET_PARAM | param);
    return dSPIN_ParamHandler(param, 0);

def dSPIN_SoftStop():
    sup.dSPIN_Xfer(hd.dSPIN_SOFT_STOP)

def dSPIN_Move(dir,n_step):
    sup.dSPIN_Xfer(hd.dSPIN_MOVE | dir)
    if (n_step > 0x3FFFFF):
    	n_step = 0x3FFFFF;
    print("n_step >> 16:{0}".format(hex(n_step >> 16)))
    print("n_step >> 8:{0}".format(hex(n_step >> 8)))
    print("n_step:{0}".format(hex(n_step)))
    sup.dSPIN_Xfer(n_step >> 16);
    sup.dSPIN_Xfer(n_step >> 8);
    sup.dSPIN_Xfer(n_step);

def dSPIN_GetStatus():
    temp = 0;
    sup.dSPIN_Xfer(hd.dSPIN_GET_STATUS);
    temp = sup.dSPIN_Xfer(0)<<8;
    temp |= sup.dSPIN_Xfer(0);
    return temp;
