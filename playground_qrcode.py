#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-10-25 13:06:05
# @Last Modified 2015-10-25 Jeremiah@JLMarks.org
# @Last Modified time: 2015-10-25 13:06:38

import qrcode
qr=qrcode.QRCode(version=1, box_size=100, border=0)
qr.add_data("Hello World!")
qr.make()
l.save(open('qrimage.png', 'wb'))

