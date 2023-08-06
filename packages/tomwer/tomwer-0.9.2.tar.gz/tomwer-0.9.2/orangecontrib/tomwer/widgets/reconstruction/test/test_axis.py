# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017-2019 European Synchrotron Radiation Facility
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
__date__ = "16/06/2021"


from orangecontrib.tomwer.widgets.reconstruction.AxisOW import AxisOW
from tomwer.test.utils import skip_gui_test
from tomwer.test.utils import UtilsTest
from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.core.settings import mock_lsbram
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core import utils
from tomwer.core.utils.scanutils import MockEDF
from silx.gui.utils.testutils import TestCaseQt
from silx.gui import qt
import shutil
import tempfile
import pytest
import time


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestOWAxis(TestCaseQt):
    """Test that the axis widget work correctly"""

    def setUp(self):
        self._window = AxisOW()
        self.recons_params = self._window.recons_params
        self.scan_path = UtilsTest.getEDFDataset("D2_H2_T2_h_")
        self._window.getAxis().mode = AxisMode.centered
        self._window.show()
        self.qWaitForWindowExposed(self._window)

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()

    def testAxisLock(self):
        """Test behavior when locking the axis position. Could not be included
        in the tomwer/gui because the lock action is only available for the OW
        """
        assert self._window.getAxis().mode in (AxisMode.centered, AxisMode.global_)
        radio_axis = self._window._widget._axisWidget._radioAxis
        main_widget = self._window._widget._axisWidget
        self.assertFalse(main_widget._controlWidget._lockBut.isLocked())
        self.assertTrue(radio_axis._controlWidget._mainWidget.isEnabled())
        self.mouseClick(main_widget._controlWidget._lockBut, qt.Qt.LeftButton)
        self.qapp.processEvents()
        self.assertTrue(main_widget._controlWidget._lockBut.isLocked())
        # when the lock button is activated we should automatically switch to
        # the manual mode
        self.assertTrue(self._window.getAxis().mode is AxisMode.manual)
        self.assertFalse(radio_axis._controlWidget._mainWidget.isEnabled())


class TestWindowAxisComputation(TestCaseQt):
    @staticmethod
    def _long_computation(scan):
        time.sleep(5)
        return -1

    """Test that the axis widget work correctly"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._mainWindow = AxisOW()
        self.recons_params = self._mainWindow.recons_params
        self._window = self._mainWindow._widget
        self.scan_path = ScanFactory.create_scan_object(
            UtilsTest.getEDFDataset("D2_H2_T2_h_")
        )
        self._mainWindow.show()
        self.qWaitForWindowExposed(self._mainWindow)
        self._mainWindow.setMode("manual")

    def tearDown(self):
        self._mainWindow.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._mainWindow.close()
        self._mainWindow = None
        self._window = None
        TestCaseQt.tearDown(self)

    def testFailedComputation(self):
        """Test gui if the axis position fails"""
        self.qapp.processEvents()
        self.recons_params.set_position_frm_par_file("not existing", force=True)
        radio_axis = self._window._axisWidget._radioAxis
        radio_axis.setMode("read")
        self.assertEqual(radio_axis.getMode(), AxisMode.read)
        self._mainWindow.process(self.scan_path)
        self.assertEqual(radio_axis.getMode(), AxisMode.read)
        self.assertEqual(self.recons_params.value_ref_tomwer, None)
        self.assertEqual(self.recons_params.mode, AxisMode.read)

    def testComputationSucceed(self):
        """Test gui if the axis position is correctly computed"""
        self.recons_params.mode = AxisMode.manual
        radio_axis = self._window._axisWidget._radioAxis
        self.assertEqual(radio_axis.getMode(), AxisMode.manual)
        radio_axis.setXShift(2.345)
        self._mainWindow.process(self.scan_path)
        self.qapp.processEvents()
        self.assertEqual(radio_axis.getMode(), AxisMode.manual)
        self.assertEqual(self.recons_params.value_ref_tomwer, 2.345)
        position_info_widget = self._window._axisWidget._controlWidget._positionInfo
        self.assertEqual(position_info_widget._tomwerPositionLabel.text(), "2.345")


global _computation_res
_computation_res = 0


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestAxisStack(TestCaseQt):
    """Test axis computation of a stack of scan"""

    @staticmethod
    def _test_computation(scan):
        global _computation_res
        _computation_res += 1
        return _computation_res

    def setUp(self):
        # not working due to OW
        TestCaseQt.setUp(self)
        self._scan1 = MockEDF.mockScan(scanID=tempfile.mkdtemp())
        self._scan2 = MockEDF.mockScan(scanID=tempfile.mkdtemp())
        self._scan3 = MockEDF.mockScan(scanID=tempfile.mkdtemp())
        self._mainWindow = AxisOW()
        self.recons_params = self._mainWindow._axis_params
        self._mainWindow._skip_exec(True)

        global _computation_res
        _computation_res = 0

        self._mainWindow.patch_calc_method(
            AxisMode.centered, TestAxisStack._test_computation
        )
        self.recons_params.mode = AxisMode.centered

        self._mainWindow.show()
        self.qWaitForWindowExposed(self._mainWindow)

    def tearDown(self):
        utils.mockLowMemory(False)
        mock_lsbram(False)
        self._mainWindow.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._mainWindow.close()
        self._mainWindow = None
        self._recons_params = None
        self.qapp.processEvents()
        for scan in (self._scan1, self._scan2, self._scan3):
            shutil.rmtree(scan.path)
        # not working due to OW
        TestCaseQt.tearDown(self)

    def testLowMemory(self):
        """Make sure the axis computation will be skip if we are in low memory"""
        utils.mockLowMemory(True)
        mock_lsbram(True)
        for scan in (self._scan1, self._scan2, self._scan3):
            self.qapp.processEvents()
            self._mainWindow.new_data_in(scan)

        self.assertEqual(self._scan1.axis_params, None)
        self.assertEqual(self._scan2.axis_params, None)
        self.assertEqual(self._scan3.axis_params, None)

    def testUnlockStack(self):
        """Check that all axis position will be computed properly if we set a
        stack of scan"""
        self._mainWindow.recons_params.set_relative_value(1.0)
        for scan in (self._scan1, self._scan2, self._scan3):
            self._mainWindow.process(scan)

        for i in range(5):
            self.qapp.processEvents()
            time.sleep(0.2)
            self.qapp.processEvents()

        self.assertNotEqual(self._scan1.axis_params, None)
        self.assertNotEqual(self._scan2.axis_params, None)
        self.assertNotEqual(self._scan3.axis_params, None)

    def testLockStack(self):
        """Check that axis position will be simply copy if we are in a lock
        stack"""
        self.recons_params.mode = AxisMode.manual
        position_value = 0.36
        self.recons_params.set_relative_value(position_value)

        for scan in (self._scan1, self._scan2, self._scan3):
            self._mainWindow.process(scan)

        for i in range(5):
            self.qapp.processEvents()
            time.sleep(0.2)
            self.qapp.processEvents()

        self.assertEqual(self._scan1.axis_params.value_ref_tomwer, position_value)
        self.assertEqual(self._scan2.axis_params.value_ref_tomwer, position_value)
        self.assertEqual(self._scan3.axis_params.value_ref_tomwer, position_value)
