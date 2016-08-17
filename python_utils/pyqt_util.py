# coding=utf-8
""" Convenience functions for common pyqt operations.

Author: Ian Davis
"""

from PyQt4.QtCore import QPropertyAnimation
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest

import os_util


def animated_resize(widget, width=0, height=0):
    """ Perform an animated resize on the given widget to the given width and height.

        :param widget: The widget to resize.
        :param width: The width to resize too.
        :param height: The height to resize too.
        :return: The QPropertyAnimation object that was created and started.
    """
    animation = QPropertyAnimation(widget, 'size')
    animation.setEndValue(QSize(width, height))
    animation.start()

    return animation


def left_click(widget):
    """ Simulate a left click on the given QWidget instance.

        :param widget: The QWidget to click.
    """
    QTest.mouseClick(widget, Qt.LeftButton)


def right_click(widget):
    """ Simulate a right click on the given QWidget instance.1

    :param widget: The QWidget to click.
    """
    QTest.mouseClick(widget, Qt.RightButton)


def qt_application():
    """ Shorthand to create a QApplication instance with the command line arguments.

    :return: The new QApplication instance.
    """
    return QApplication(os_util.command_line_arguments())
