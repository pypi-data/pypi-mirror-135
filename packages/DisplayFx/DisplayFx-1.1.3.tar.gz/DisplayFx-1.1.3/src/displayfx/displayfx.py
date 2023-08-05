'''Inset headline here

Insert description here
'''
import logging
from pathlib import Path
import sys
import beetools

_VERSION = '1.3.3'
_path = Path(sys.argv[0])
_name = _path.stem


class DisplayFx:
    '''Display progress indicator on CRT (Dos) screen'''

    def __init__(
        self, p_parent_logger_name, p_max_val, p_verbose=False, p_msg='', p_bar_len=50
    ):
        '''Initialize the class'''
        self.logger_name = '{}.{}'.format(p_parent_logger_name, _name)
        self.logger = logging.getLogger(self.logger_name)
        self.logger.info('Start')
        self.version = _VERSION
        self.bar_end_pos = 0
        self.bar_start_pos = 0
        self.bar_len = p_bar_len
        self.calibrate = 0
        self.leader_str = ''
        self.marker_len = 0
        self.markers = []
        self.marker_slice = 0
        self.max_val = p_max_val
        self.progress = 0
        self.silent = p_verbose
        self.msg = p_msg
        self.bar_len = max(self.bar_len, 20)
        self.leader_str = '{:.<{leaderLen}}'.format('', leaderLen=self.bar_len)
        if self.max_val <= 1:
            self.markers = ['100%']
        elif self.max_val == 2:
            self.markers = ['50%', '100%']
        elif self.max_val == 3:
            self.markers = ['33%', '67%', '100%']
        elif self.max_val == 4:
            self.markers = ['25%', '50%', '75%', '100%']
        else:
            self.markers = ['20%', '40%', '60%', '80%', '100%']
        self.marker_qty = len(self.markers)
        self.marker_slice = self.bar_len / self.marker_qty
        # self.remInc = ( self.bar_len / self.marker_qty ) - self.marker_slice
        for i in range(self.marker_qty):
            self.marker_len = len(self.markers[i])
            self.bar_end_pos = round(self.marker_slice * (i + 1))
            self.leader_str = (
                self.leader_str[: self.bar_end_pos - self.marker_len]
                + self.markers[i]
                + self.leader_str[self.bar_end_pos :]
            )
        if self.max_val >= self.bar_len:
            self.marker_slice = self.bar_len / self.max_val
        if not self.silent:
            print('{}'.format(self.msg), end='', flush=True)
            if self.max_val == 0:
                print(self.leader_str)

    # end __init__

    def update(self, p_i):
        '''Print the current progress to screen'''
        if not self.silent:
            # self.barCurrPos = 0
            if p_i == 0:
                self.calibrate = 1
            self.progress = (p_i + self.calibrate) / (self.max_val)
            self.bar_end_pos = round(self.progress * self.bar_len)
            if self.bar_end_pos > self.bar_start_pos:
                print(
                    self.leader_str[self.bar_start_pos : self.bar_end_pos],
                    end='',
                    flush=True,
                )
                self.bar_start_pos = self.bar_end_pos
                # self.marker_slice += self.marker_slice
            if p_i + self.calibrate == self.max_val:
                print()

    # end update


# end DisplayFx


def do_tests(p_app_path='', p_cls=True):
    '''Test the class methods.

    Also called by the PackageIt PIP app to
    test the module during PIP installation
    '''

    def basic_test():
        '''Basic and mandatory scenario tests for certification of the class'''
        success = True
        bar_len_list = [10, 30, 50, 100]
        # bar_len_list = [ 100 ]
        max_val_list = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 50000]
        # max_val_list = [ 0 ]
        max_bar_len_list_len = len(str(max(bar_len_list)))
        max_vax_val_list_len = len(str(max(max_val_list)))
        for bar_len in bar_len_list:
            for max_val in max_val_list:
                subject = beetools.msg_display(
                    'Bar {: >{x}}, Max {: >{y}}'.format(
                        bar_len, max_val, x=max_bar_len_list_len, y=max_vax_val_list_len
                    ),
                    p_len=23,
                )
                t_displayfx = DisplayFx(
                    _name, max_val, p_msg=subject, p_bar_len=bar_len
                )
                for x in range(0, max_val):
                    t_displayfx.update(x)
        return success

    # end basic_test

    success = True
    b_tls = beetools.Archiver(__doc__[0], p_app_path, p_cls=p_cls)
    logger = logging.getLogger(_name)
    logger.setLevel(beetools.DEF_LOG_LEV)
    file_handle = logging.FileHandler(beetools.LOG_FILE_NAME, mode='w')
    file_handle.setLevel(beetools.DEF_LOG_LEV_FILE)
    console_handle = logging.StreamHandler()
    console_handle.setLevel(beetools.DEF_LOG_LEV_CON)
    file_format = logging.Formatter(
        beetools.LOG_FILE_FORMAT, datefmt=beetools.LOG_DATE_FORMAT
    )
    console_format = logging.Formatter(beetools.LOG_CONSOLE_FORMAT)
    file_handle.setFormatter(file_format)
    console_handle.setFormatter(console_format)
    logger.addHandler(file_handle)
    logger.addHandler(console_handle)

    b_tls.print_header(p_cls=p_cls)
    success = basic_test()
    beetools.result_rep(success, 'Done')
    b_tls.print_footer()


# end do_tests

if __name__ == '__main__':
    do_tests(p_app_path=_path)
# end __main__
