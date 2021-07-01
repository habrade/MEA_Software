import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

__author__ = "Sheng Dong"
__email__ = "s.dong@mails.ccnu.edu.cn"


class Dac8568Device:
    def __init__(self, hw):
        self.hw = hw
        self.reg_name_base = "dac8568_dev."
        log.info("DAC8568 device")

    def is_busy(self):
        reg_name = self.reg_name_base + "busy"
        node = self.hw.getNode(reg_name)
        busy_raw = node.read()
        return busy_raw.value() == 1

    def reset_dev(self):
        reg_name = self.reg_name_base + "rst"
        node = self.hw.getNode(reg_name)
        node.write(0)
        node.write(1)
        node.write(0)
        self.hw.dispatch()

    def start_conv(self):
        reg_name = self.reg_name_base + "start"
        node = self.hw.getNode(reg_name)
        node.write(0)
        node.write(1)
        node.write(0)
        self.hw.dispatch()

    def select_ch(self, ch):
        """ 8bit channel map """
        reg_name = self.reg_name_base + "sel_ch"
        node = self.hw.getNode(reg_name)
        node.write(ch)
        self.hw.dispatch()

    def set_data(self, data_ch, data):
        """
        data_ch: num in range(8) data_0, data_1, ... , data_7
        data: 16 bits
        """
        reg_name = self.reg_name_base + "data_" + str(data_ch)
        node = self.hw.getNode(reg_name)
        node.write(data)
        self.hw.dispatch()
