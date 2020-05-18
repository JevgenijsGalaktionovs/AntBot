#!/usr/bin/env python
# -*- coding: utf-8 -*-

from example import *
import time

if __name__ == '__main__':
    time_main_start = time.time()
    target_info, target_images, times = verify_target()
    print(target_info['fullName'])
    