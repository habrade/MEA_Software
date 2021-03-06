#!/usr/bin/env python3

from lib.dac8568_device import Dac8568Device
import time
import coloredlogs
import logging
from lib.freq_ctr_device import FreqCtr
from lib.global_device import GlobalDevice
from lib.ipbus_link import IPbusLink
from lib.mea_device import MeaDevice

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
coloredlogs.install(level='DEBUG', logger=log)

__author__ = "Sheng Dong"
__email__ = "s.dong@mails.ccnu.edu.cn"


def set_mea(mea_dev, Fout, Precision):
    log.debug("MMCM initial Status:")
    log.debug("MEA clock is locked: {:}!".format(mea_dev.is_locked()))

    mea_dev.set_frq(Fout, Precision)
    time.sleep(1)
    # Set Mea IO
    mea_dev.start_scan()


def fre_counter(freq_ctr_dev):
    N_CLK = 2
    clock_name = ["clk_dac", "clk_mea"]
    for i in range(N_CLK):
        freq = freq_ctr_dev.get_chn_freq(i)
        log.info("Tested {:s} frequency is : {}".format(clock_name[i], freq))


def main(Fout, Precision):
    ## Get ipbus connection
    hw = IPbusLink().get_hw()
    global_dev = GlobalDevice(hw)
    mea_dev = MeaDevice(hw)
    dac_dev = Dac8568Device(hw)
    freq_ctr_dev = FreqCtr(hw)
    ## Soft reset
    # global_dev.set_nuke()
    global_dev.set_soft_rst()
    # Set DAC8568
    dac_dev.reset_dev()
    dac_dev.select_ch(0xFF)
    dac_dev.set_data(0, 0x1F00)
    dac_dev.set_data(1, 0x2410)
    dac_dev.set_data(4, 0x0fff)
    dac_dev.start_conv()
    ## Set MEA
    """ set clock """
    # set_mea(mea_dev, Fout, Precision)
    """ start scan """
    mea_dev.reset_scan()
    mea_dev.start_scan()
    mea_dev.set_div(div=2)
    mea_dev.sel_mea_clk(is_div=True)
    ## Test clock frq
    fre_counter(freq_ctr_dev)


if __name__ == '__main__':
    Fout = 10.0  ## Unit: MHz
    Precision = 0.2  ## Unit: Hundred percent, %
    main(Fout, Precision)
