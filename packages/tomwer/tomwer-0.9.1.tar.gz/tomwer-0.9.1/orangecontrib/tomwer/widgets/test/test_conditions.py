# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "12/08/2021"

import logging
import os
import shutil
import tempfile
from silx.gui import qt
from orangecontrib.tomwer.widgets.control.FilterOW import NameFilterOW
from silx.gui.utils.testutils import TestCaseQt
from tomwer.core.utils.scanutils import MockHDF5, MockEDF
from tomwer.core.scan.edfscan import EDFTomoScan
from silx.gui.utils.testutils import SignalListener


logging.disable(logging.INFO)


class NameFilterOWCI(NameFilterOW):
    sigScanReady = qt.Signal(str)
    """signal emitted when a scan is ready; Parameter is folder path of the
    scan"""

    def _signalScanReady(self, scan):
        self.sigScanReady.emit(scan.path)


class TestFilterWidget(TestCaseQt):
    """class testing the DarkRefWidget"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self.widget = NameFilterOWCI(parent=None)

        self.tmpdir = tempfile.mkdtemp()
        # create hdf5 dataset
        self._hdf5with_mytotodir = MockHDF5(
            scan_path=os.path.join(self.tmpdir, "mytotodir120"), n_proj=10
        ).scan
        self._hdf5without_mytotodir = MockHDF5(
            scan_path=os.path.join(self.tmpdir, "totodir120"), n_proj=10
        ).scan
        # create edf dataset
        mockEDF1 = MockEDF(
            scan_path=os.path.join(self.tmpdir, "mytotodir20"), n_radio=10
        )
        self.edfwith_mytotodir = EDFTomoScan(scan=mockEDF1.scan_path)

        mockEDF2 = MockEDF(scan_path=os.path.join(self.tmpdir, "dir120"), n_radio=10)
        self.edfwithout_mytotodir = EDFTomoScan(scan=mockEDF2.scan_path)

        # add a signal listener
        self.signalListener = SignalListener()
        self.widget.sigScanReady.connect(self.signalListener)

        # define the unix file pattern
        self.widget.setPattern("*mytotodir*")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        TestCaseQt.tearDown(self)

    def testEDF(self):
        """Make sure filtering works with EDF"""
        self.assertEqual(self.signalListener.callCount(), 0)
        self.widget.applyfilter(self.edfwith_mytotodir)
        self.qapp.processEvents()
        self.assertEqual(self.signalListener.callCount(), 1)
        self.widget.applyfilter(self.edfwithout_mytotodir)
        self.qapp.processEvents()
        self.assertEqual(self.signalListener.callCount(), 1)

    def testHDF5(self):
        """Make sure filtering works with HDF5"""
        self.assertEqual(self.signalListener.callCount(), 0)
        self.widget.applyfilter(self._hdf5without_mytotodir)
        self.qapp.processEvents()
        self.assertEqual(self.signalListener.callCount(), 0)
        self.widget.applyfilter(self._hdf5with_mytotodir)
        self.qapp.processEvents()
        self.assertEqual(self.signalListener.callCount(), 1)
