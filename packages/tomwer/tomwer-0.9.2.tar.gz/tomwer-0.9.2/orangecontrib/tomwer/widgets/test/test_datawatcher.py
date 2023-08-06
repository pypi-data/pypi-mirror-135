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
__date__ = "17/01/2017"

import logging
import os
import shutil
import tempfile
import time
import unittest

from silx.gui import qt

from orangecontrib.tomwer.test.TestAcquisition import Simulation
from orangecontrib.tomwer.widgets.control.DataWatcherOW import DataWatcherOW
from tomwer.core.process.control.datawatcher import status as datawatcherstatus
from tomwer.gui.qtapplicationmanager import QApplicationManager

logging.disable(logging.INFO)

# Makes sure a QApplication exists
_qapp = QApplicationManager()


class DataWatcherWaiter(object):
    """Define a simple objecy able to wait for some state of the DataWatcher
    arrive"""

    def __init__(self):
        self.reset()
        self.lastStatus = []

    def reset(self):
        self.lastStatus = []

    def stateHasChanged(self, val):
        """Register all status"""
        if val not in self.lastStatus:
            self.lastStatus.append(val)

    def waitForState(self, state, maxWaiting):
        """simple function wich wait until the DataWatcherWidget reach the given
        state.
        If the widget doesn't reach this state after maxWaiting second. Then fail.

        :param str state: the state we are waiting for
        :param int maxWaiting: the maximal number of second to wait until failling.
        """
        while state not in self.lastStatus:
            time.sleep(1.0)
            _qapp.processEvents()
            maxWaiting -= 1
            if maxWaiting <= 0:
                return False
        return state in self.lastStatus


class TestDataWatcherAcquisition(unittest.TestCase, DataWatcherWaiter):
    """Functions testing the classical behavior of data watcher
    - signal acquisition is over only when all files are copied
    """

    def tearDown(self):
        while _qapp.hasPendingEvents():
            _qapp.processEvents()
        self.dataWatcherWidget.setObservation(False)
        self.dataWatcherWidget.close()
        del self.dataWatcherWidget
        self.dataWatcherWidget = None
        self.s.wait()
        del self.s
        super(TestDataWatcherAcquisition, self).tearDown()
        if os.path.isdir(self.inputdir):
            shutil.rmtree(self.inputdir)

    def setUp(self):
        self.manipulationId = "test10"

        super(TestDataWatcherAcquisition, self).setUp()
        self.inputdir = tempfile.mkdtemp()
        DataWatcherWaiter.reset(self)
        self.dataWatcherWidget = DataWatcherOW(displayAdvancement=False)
        self.dataWatcherWidget.srcPattern = ""
        self.dataWatcherWidget.sigTMStatusChanged.connect(self.stateHasChanged)
        self.dataWatcherWidget.setAttribute(qt.Qt.WA_DeleteOnClose)

        self.s = Simulation(
            self.inputdir,
            self.manipulationId,
            finalState=Simulation.advancement["acquisitionRunning"],
        )

    def testStartAcquisition(self):
        """Make sure the data watch detect the acquisition of started"""
        observeDir = os.path.join(self.inputdir, self.manipulationId)
        for folder in (self.inputdir, observeDir):
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.assertTrue(os.path.isdir(observeDir))

        self.s.createFinalXML(True)
        self.dataWatcherWidget.setFolderObserved(observeDir)

        self.assertTrue(self.dataWatcherWidget.currentStatus == "not processing")
        self.s.start()
        self.s.advanceTo("acquisitionDone")
        self.s.start()
        self.s.wait()
        self.dataWatcherWidget.startObservation()
        self.dataWatcherWidget._widget.observationThread.wait()
        self.dataWatcherWidget._widget.observationThread.observations.dict[
            observeDir
        ].wait()
        finishedAcqui = (
            self.dataWatcherWidget._widget.observationThread.observations.ignoredFolders
        )
        _qapp.processEvents()
        self.assertTrue(observeDir in finishedAcqui)


class TestDataWatcherInteraction(unittest.TestCase):
    """Simple unit test to test the start/stop observation button action"""

    def setUp(self):
        super(TestDataWatcherInteraction, self).setUp()
        self.inputdir = tempfile.mkdtemp()
        self.dataWatcherWidget = DataWatcherOW(displayAdvancement=False)
        self.dataWatcherWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.dataWatcherWidget.srcPattern = ""

    def tearDown(self):
        while _qapp.hasPendingEvents():
            _qapp.processEvents()
        self.dataWatcherWidget.close()
        del self.dataWatcherWidget
        super(TestDataWatcherInteraction, self).tearDown()
        if os.path.isdir(self.inputdir):
            shutil.rmtree(self.inputdir)

        def tearDown(self):
            while _qapp.hasPendingEvents():
                _qapp.processEvents()

    def testStartAndStopAcquisition(self):
        """test multiple start and stop action on the start observation to
        make sure no crash are appearing
        """
        try:
            self.dataWatcherWidget.setFolderObserved(self.inputdir)
            self.dataWatcherWidget.show()
            self.dataWatcherWidget.setObservation(True)
            for iTest in range(5):

                def tearDown(self):
                    while _qapp.hasPendingEvents():
                        _qapp.processEvents()

                self.dataWatcherWidget._widget._qpbstartstop.pressed.emit()
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)


class WaitForXMLOption(unittest.TestCase, DataWatcherWaiter):
    """test the behavior of datawatcher when the option 'wait for xml copy'
    Basically in this case DataWatcherDirObserver will wait until an .xml
    arrived
    """

    @classmethod
    def setUpClass(cls):
        cls.dataWatcherWidget = DataWatcherOW(displayAdvancement=False)
        cls.dataWatcherWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        cls.dataWatcherWidget.obsMethod = datawatcherstatus.DET_END_XML
        cls.dataWatcherWidget.srcPattern = ""
        cls.manipulationId = "test10"
        super(WaitForXMLOption, cls).setUpClass()

    def setUp(self):
        self.inputdir = tempfile.mkdtemp()
        self.reset()
        self.dataWatcherWidget.setObservation(False)
        self.dataWatcherWidget.resetStatus()
        super(WaitForXMLOption, self).setUp()

    def tearDown(self):
        while _qapp.hasPendingEvents():
            _qapp.processEvents()
        super(WaitForXMLOption, self).tearDown()
        if os.path.isdir(self.inputdir):
            shutil.rmtree(self.inputdir)

    @classmethod
    def tearDownClass(cls):
        cls.dataWatcherWidget.close()
        del cls.dataWatcherWidget
        if hasattr(cls, "s"):
            cls.s.quit()
            del cls.s
        super(WaitForXMLOption, cls).tearDownClass()

    def testAcquistionNotEnding(self):
        """Check behavior if an acquisition never end"""
        observeDir = os.path.join(self.inputdir, self.manipulationId)
        for folder in (self.inputdir, observeDir):
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.assertTrue(os.path.isdir(observeDir))

        self.s = Simulation(
            self.inputdir,
            self.manipulationId,
            finalState=Simulation.advancement["acquisitionRunning"],
        )
        self.dataWatcherWidget.setFolderObserved(observeDir)
        self.dataWatcherWidget.show()
        self.dataWatcherWidget.sigTMStatusChanged.connect(self.stateHasChanged)

        self.assertTrue(self.dataWatcherWidget.currentStatus == "not processing")
        self.s.start()
        self.s.wait()
        self.dataWatcherWidget.setObservation(True)
        self.dataWatcherWidget._widget.observationThread.wait()
        self.dataWatcherWidget._widget.observationThread.observations.dict[
            observeDir
        ].wait()
        finishedAcqui = (
            self.dataWatcherWidget._widget.observationThread.observations.ignoredFolders
        )
        _qapp.processEvents()
        self.assertFalse(observeDir in finishedAcqui)

    def testAcquistionEnded(self):
        """Check behavior if an acquisition is ending"""
        manipulationId = "test10"
        observeDir = os.path.join(self.inputdir, self.manipulationId)
        for folder in (self.inputdir, observeDir):
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.assertTrue(os.path.isdir(observeDir))

        self.s = Simulation(
            self.inputdir,
            manipulationId,
            finalState=Simulation.advancement["acquisitionDone"],
        )
        self.s.createFinalXML(True)
        self.dataWatcherWidget.setFolderObserved(observeDir)
        self.dataWatcherWidget.show()
        self.dataWatcherWidget.sigTMStatusChanged.connect(self.stateHasChanged)

        self.assertTrue(self.dataWatcherWidget.currentStatus == "not processing")
        self.s.start()
        self.s.wait()
        self.dataWatcherWidget.setObservation(True)
        self.dataWatcherWidget._widget.observationThread.wait()
        self.dataWatcherWidget._widget.observationThread.observations.dict[
            observeDir
        ].wait()
        finishedAcqui = (
            self.dataWatcherWidget._widget.observationThread.observations.ignoredFolders
        )
        _qapp.processEvents()
        self.assertTrue(observeDir in finishedAcqui)


class TestRSync(unittest.TestCase, DataWatcherWaiter):
    """test that the synchronization using RSyncManager is working"""

    def setUp(self):
        super(TestRSync, self).setUp()
        self.inputdir = tempfile.mkdtemp()
        self.outputdir = tempfile.mkdtemp()
        DataWatcherWaiter.reset(self)
        self.dataWatcherWidget = DataWatcherOW(displayAdvancement=False)
        self.dataWatcherWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.dataWatcherWidget._widget.setSrcAndDestPattern(
            self.inputdir, self.outputdir
        )

    def tearDown(self):
        while _qapp.hasPendingEvents():
            _qapp.processEvents()
        self.dataWatcherWidget.close()
        del self.dataWatcherWidget
        if hasattr(self, "s"):
            self.s.quit()
            del self.s
        super(TestRSync, self).tearDown()
        for d in (self.inputdir, self.outputdir):
            if os.path.isdir(d):
                shutil.rmtree(d, ignore_errors=True)

    def testStartAcquisition(self):
        """Test that rsync is launched when an acquisition is discovered"""
        manipulationId = "test10"
        observeDir = os.path.join(self.inputdir, manipulationId)
        for folder in (self.inputdir, observeDir):
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.assertTrue(os.path.isdir(observeDir))

        self.s = Simulation(
            self.inputdir,
            manipulationId,
            finalState=Simulation.advancement["acquisitionRunning"],
        )

        self.s.setSrcDestPatterns(self.inputdir, self.outputdir)
        self.s.createFinalXML(True)
        self.dataWatcherWidget.setFolderObserved(self.inputdir)
        self.dataWatcherWidget.show()
        self.dataWatcherWidget.sigTMStatusChanged.connect(self.stateHasChanged)
        self.assertTrue(self.dataWatcherWidget.currentStatus == "not processing")
        self.dataWatcherWidget.setObservation(True)
        self.s.start()
        # check state scanning
        time.sleep(0.5)

        self.dataWatcherWidget.stopObservation()

        # in this case the .info should be in the output dir also
        test10_output = os.path.join(self.outputdir, "test10")
        test10_input = os.path.join(self.inputdir, "test10")
        self.assertTrue(os.path.isfile(os.path.join(test10_output, "test10.info")))

        # make sure file transfert have been started (using rsync)
        # all file in outputdir should be in input dir
        time.sleep(2)
        # check that some .edf file have already been copied
        self.assertTrue(len(test10_output) > 5)

        # xml shouldn't be there because we are righting it at the end
        self.assertFalse(os.path.isfile(os.path.join(test10_output, "test10.xml")))
        self.assertFalse(os.path.isfile(os.path.join(test10_input, "test10.xml")))
