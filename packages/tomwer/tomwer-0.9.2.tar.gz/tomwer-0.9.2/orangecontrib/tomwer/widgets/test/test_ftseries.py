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
__date__ = "24/01/2017"


import logging
import os
import shutil
import tempfile
import unittest
import gc
from silx.gui.utils.testutils import TestCaseQt
from silx.gui import qt
from orangecontrib.tomwer.widgets.reconstruction.FtseriesOW import FtseriesOW
from tomwer.core.process.reconstruction.ftseries.params.fastsetupdefineglobals import (
    FastSetupAll,
)
from tomwer.core.process.reconstruction.ftseries.params.paganin import PaganinMode
from tomwer.core.process.reconstruction.ftseries.params.beamgeo import BeamGeoType
from tomwer.core.process.reconstruction.ftseries.params.reconsparams import _ReconsParam
from tomwer.core.process.reconstruction.ftseries.params.ft import (
    VolSelMode,
    FixedSliceMode,
)
from tomwer.gui.qtapplicationmanager import QApplicationManager
from tomwer.synctools.ftseries import QReconsParams
from tomwer.core.utils import ftseriesutils
from tomwer.core.utils.scanutils import MockEDF


logging.disable(logging.INFO)

# Makes sure a QApplication exists
_qapp = QApplicationManager()


class TestFTSerieWidget(TestCaseQt):
    """Simple unit test to test the start/stop observation button action"""

    def setUp(self):
        super(TestFTSerieWidget, self).setUp()
        self.owftseriewidget = FtseriesOW(_connect_handler=False)
        self._reconsParams = self.owftseriewidget.recons_params

        self.ftseriewidget = self.owftseriewidget._ftserie

        self.tempdir = tempfile.mkdtemp()
        MockEDF.mockScan(self.tempdir, nRadio=5, nRecons=1, nPagRecons=0, dim=10)

        self.h5_fname = os.path.join(self.tempdir, "octave.h5")
        ftseriesutils.generateDefaultH5File(self.h5_fname)
        self.savePath = tempfile.mkstemp(suffix=".h5")[1]
        self._reconsParams.copy(FastSetupAll.DEFAULT_VALUES)
        self.owftseriewidget.setAttribute(qt.Qt.WA_DeleteOnClose)

    def tearDown(self):
        os.unlink(self.savePath)
        if os.path.isdir(self.tempdir):
            shutil.rmtree(self.tempdir)
        self.owftseriewidget.close()
        self.owftseriewidget = None
        self.qapp.processEvents()
        gc.collect()
        super(TestFTSerieWidget, self).tearDown()

    def testAngleOffset(self):
        self.ftseriewidget.updatePath(self.tempdir)
        self.assertTrue(
            self.ftseriewidget.getReconsParamSetEditor().isParamH5Managed(
                "FT", "ANGLE_OFFSET"
            )
        )
        _qapp.processEvents()
        ft = self.ftseriewidget.getReconsParamSetEditor().getStructs()
        self.assertTrue(ft["FT"]["FIXEDSLICE"] == "middle")
        self.assertTrue(float(ft["FT"]["ANGLE_OFFSET_VALUE"]) == 0.0)

        self.owftseriewidget.show()

        self.ftseriewidget.save(self.savePath)
        _qapp.processEvents()

        readed = FastSetupAll()
        readed.readAll(self.h5_fname, 3.8)
        self.assertTrue(readed.structures["FT"]["ANGLE_OFFSET"] == 0)

        self._reconsParams.ft["ANGLE_OFFSET_VALUE"] = 1.0
        self.assertTrue(self._reconsParams.ft["ANGLE_OFFSET"] == 1)
        self.ftseriewidget.save(self.savePath)
        _qapp.processEvents()
        readed = FastSetupAll()
        readed.readAll(self.savePath, 3.8)
        self.assertTrue(readed.structures["FT"]["ANGLE_OFFSET_VALUE"] == 1)
        self.assertTrue(readed.structures["FT"]["ANGLE_OFFSET"] == 1)


class TestControlsFTSeriesWidget(TestCaseQt):
    """Simple test of the control button for the FTserieWidget"""

    def setUp(self):
        super(TestControlsFTSeriesWidget, self).setUp()
        # create octave h5 with default
        self.path = tempfile.mkdtemp()
        self.scan = MockEDF.mockScan(
            self.path, nRadio=5, nRecons=1, nPagRecons=0, dim=10
        )
        # one with some modifications
        self.modifySettings = os.path.join(self.path, "modifySettings.h5")
        ft = FastSetupAll()
        assert ft.structures["PAGANIN"]["MODE"] != 2
        ft.structures["PAGANIN"]["MODE"] = 2
        ft.writeAll(self.modifySettings, 3.8)
        # simulate an acquisition (files at least)
        self.widget = FtseriesOW(_connect_handler=False)
        self.widget.setDryRun(True)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        if os.path.isdir(self.path):
            shutil.rmtree(self.path)
        self.qapp.processEvents()
        gc.collect()
        super(TestControlsFTSeriesWidget, self).tearDown()

    def testShow(self):
        """make sure the h5file is created in the scan directory"""
        self.widget.reprocess(self.scan)
        _qapp.processEvents()
        self.assertTrue(self.path == self.widget.scan.path)

    def testSave(self):
        """Make sure that the save action is correct"""
        self.widget.updatePath(self.scan)
        _qapp.processEvents()
        self.assertTrue(self.path == self.widget.scan.path)

        tmpH5File = tempfile.mkstemp(suffix=".h5")[1]
        self.widget.save(tmpH5File, displayInfo=False)

        ftOri = FastSetupAll()
        originalStructures = ftOri.structures

        ftSaved = FastSetupAll()
        ftSaved.readAll(filn=self.modifySettings, targetted_octave_version=3.8)
        self.assertTrue(ftSaved.structures["PAGANIN"]["MODE"].value == 2)
        ftSaved.structures["PAGANIN"]["MODE"] = originalStructures["PAGANIN"]["MODE"]
        self.assertTrue(originalStructures.to_dict() == ftSaved.structures.to_dict())

    def testLoad(self):
        """Make sure the load action is correct"""
        self.widget.updatePath(self.scan)
        _qapp.processEvents()
        self.assertTrue(self.path == self.widget.scan.path)
        self.widget.show()
        self.widget.load_recons_params(self.modifySettings)

        tmpH5File = tempfile.mkstemp(suffix=".h5")[1]
        self.widget.save(tmpH5File)
        self.assertTrue(self.fileContainEqual(self.modifySettings, tmpH5File))
        os.unlink(tmpH5File)

    def fileContainEqual(self, f1, f2):
        ft1 = FastSetupAll()
        ft1.readAll(filn=f1, targetted_octave_version=3.8)

        ft2 = FastSetupAll()
        ft2.readAll(filn=f2, targetted_octave_version=3.8)

        return ft1.structures.to_dict() == ft2.structures.to_dict()


class TestExploreDatasetForH5(TestCaseQt):
    """Make sure that in the case the octave_FT_params.h5 exists in a directory
    this will be the one picked by the editor if the 'explore scan' option
    is activated
    """

    def setUp(self):
        super(TestExploreDatasetForH5, self).setUp()
        self._reconsParams = QReconsParams()

        self.pathWithH5 = tempfile.mkdtemp()
        self.pathWithoutH5 = tempfile.mkdtemp()
        for folder in (self.pathWithH5, self.pathWithoutH5):
            MockEDF.mockScan(folder, nRadio=5, nRecons=1, nPagRecons=0, dim=10)

        self.ft = FastSetupAll()
        assert self.ft.structures["PAGANIN"]["MODE"] != 2
        self.ft.structures["PAGANIN"]["MODE"] = 2

        self.modifySettings = os.path.join(self.pathWithH5, "octave_FT_params.h5")
        self.ft.writeAll(self.modifySettings, 3.8)

        self.owWidget = FtseriesOW(
            _connect_handler=False, recons_params=self._reconsParams
        )
        self.widget = self.owWidget._ftserie

        self._reconsParams.copy(self.ft.DEFAULT_VALUES)

    def tearDown(self):
        if os.path.isfile(self.modifySettings):
            os.remove(self.modifySettings)
        if os.path.isdir(self.pathWithH5):
            shutil.rmtree(self.pathWithH5)
        if os.path.isdir(self.pathWithoutH5):
            shutil.rmtree(self.pathWithoutH5)
        self.owWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.owWidget.close()
        self.owWidget = None
        self.qapp.processEvents()
        gc.collect()
        super(TestExploreDatasetForH5, self).tearDown()

    def testExploreInFolderWithH5(self):
        """Make sure the widget if try to explore the scan dir will load
        the reconstruction parameters from it
        """
        self.widget.setH5Exploration(True)
        self.widget.updatePath(self.pathWithH5)
        self.assertTrue(self.pathWithH5 == self.widget.scan.path)
        self.assertTrue(self._reconsParams.paganin.mode.value == 2)

    def testExploreInFolderWithoutH5(self):
        """Make sure the widget if try to explore the scan dir will load
        the reconstruction parameters from it
        """
        self.widget.setH5Exploration(False)
        self.widget.updatePath(self.pathWithoutH5)
        self.assertTrue(self.pathWithoutH5 == self.widget.scan.path)
        self.assertTrue(self._reconsParams.paganin.mode.value != 2)

    def testNoExploreInFolderWithoutH5(self):
        self.widget.setH5Exploration(False)
        self.widget.updatePath(self.pathWithH5)
        self.assertTrue(self.pathWithH5 == self.widget.scan.path)
        self.assertTrue(self._reconsParams.paganin.mode.value != 2)

    def testNoExploreInFolderWithH5(self):
        self.widget.setH5Exploration(False)
        self.widget.updatePath(self.pathWithoutH5)
        self.assertTrue(self.pathWithoutH5 == self.widget.scan.path)
        self.assertTrue(self._reconsParams.paganin.mode.value != 2)


class TestLoadSaveH5File(TestCaseQt):
    """Simple test that make sure we are able to manage correctly input h5 file
    with the following behavior :
        - if some H5 parameter are missing fron the default set of parameter
        then we are loading the default parameter
        - if the h5 file as some extra H5 parameter or structure then the
        editor should also store them.
    """

    def setUp(self):
        super(TestLoadSaveH5File, self).setUp()
        self.path = tempfile.mkdtemp()
        MockEDF.mockScan(self.path, nRadio=5, nRecons=1, nPagRecons=0, dim=10)
        self.ft = FastSetupAll()
        self.file = os.path.join(self.path, "octave_FT_params.h5")

    def tearFown(self):
        del self.ft
        del self.file
        if os.path.isdir(self.path):
            shutil.rmtree(self.path)
        super(TestLoadSaveH5File, self).tearDown()

    def loadAndSave(self):
        # save actual FastSetup status
        self.ft.writeAll(self.file, 3.8)

        # create FTSerie, load and save dataparamValue = self.getDefaultValue(param)
        owWidgetWithout = FtseriesOW(_connect_handler=False)
        widgetWithout = owWidgetWithout._ftserie
        owWidgetWithout.setAttribute(qt.Qt.WA_DeleteOnClose)

        widgetWithout.setH5Exploration(True)
        widgetWithout.updatePath(self.path)
        widgetWithout.save(self.file)
        owWidgetWithout.close()
        # then get back what FTSerie has saved
        loader = FastSetupAll()
        loader.readAll(self.file, targetted_octave_version=3.8)
        return loader.structures

    def testDefaultFileWithExtraParameters(self):
        self.ft.structures["TEST"] = {"PARAM1": 1, "PARAM2": "dsadsa"}
        self.ft.structures["FT"]["PARAMTATA"] = 56.3

        savedData = self.loadAndSave()
        self.assertTrue("PARAMTATA" in savedData["FT"].all_params)
        self.assertTrue(savedData["FT"]["PARAMTATA"] == 56.3)


class TestSync(TestCaseQt):
    """Make sure all the tab from the editor are correctly sync with
    :class:`ReconsParam` instance"""

    def setUp(self):
        super(TestSync, self).setUp()
        self._reconsParams = QReconsParams()
        self.owWidget = FtseriesOW(_connect_handler=False)
        self.owWidget.setReconsParams(self._reconsParams)
        self.widget = self.owWidget._ftserie
        assert id(self.widget._recons_params) == id(self._reconsParams)
        assert id(self.widget._recons_params.pyhst) == id(self._reconsParams.pyhst)
        assert id(self.widget.getReconsParamSetEditor().reconsparams) == id(
            self._reconsParams
        )
        assert id(self.widget.getReconsParamSetEditor().reconsparams.pyhst) == id(
            self._reconsParams.pyhst
        )

    def tearDown(self):
        self.owWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.owWidget.close()
        self.owWidget = None
        super(TestSync, self).tearDown()

    def testFTRead(self):
        """Make sure modifications from the ReconsParam are take into account"""
        ftWidget = self.widget.getReconsParamSetEditor()._mainWidget
        assert self._reconsParams["FT"]["DO_TEST_SLICE"] == 1
        self._reconsParams["FT"]["DO_TEST_SLICE"] = 0
        self.assertFalse(ftWidget._qcbDoTestSlice.isChecked())

        assert self._reconsParams.to_dict()["FT"]["FIXEDSLICE"] == "middle"
        assert self._reconsParams["FT"]["FIXEDSLICE"] == FixedSliceMode.middle
        self._reconsParams["FT"]["FIXEDSLICE"] = FixedSliceMode.row_n
        self.assertTrue(ftWidget._qcbSelectSlice.currentText() == "row n")

        assert self._reconsParams["FT"]["CORRECT_SPIKES_THRESHOLD"] == 0.04
        self._reconsParams["FT"]["CORRECT_SPIKES_THRESHOLD"] = 1.23
        self.assertTrue(float(ftWidget._qleThresholdSpikesRm.text()) == 1.23)

        assert self._reconsParams["FT"]["RINGSCORRECTION"] == 0
        self._reconsParams["FT"]["RINGSCORRECTION"] = 1
        self.assertTrue(ftWidget._qcbRingsCorrection.isChecked())

        assert self._reconsParams["FT"]["VOLSELECTION_REMEMBER"] == 0
        self._reconsParams["FT"]["VOLSELECTION_REMEMBER"] = 1
        self.assertTrue(ftWidget._qcbVolSelRemenber.isChecked())

        assert self._reconsParams.to_dict()["FT"]["VOLSELECT"] == "total"
        assert self._reconsParams["FT"]["VOLSELECT"] == VolSelMode.total
        self._reconsParams["FT"]["VOLSELECT"] = VolSelMode.graphics
        self.assertTrue(ftWidget._qcbVolumeSelection.currentText() == "graphics")

    def testFTWrite(self):
        """Make sure user modification from the gui are updating the
        :class:`ReconsParam` instance"""
        ftWidget = self.widget.getReconsParamSetEditor()._mainWidget

        assert self._reconsParams["FT"]["DO_TEST_SLICE"] == 1
        ftWidget._qcbDoTestSlice.setChecked(False)
        self.qapp.processEvents()
        self.assertTrue(self._reconsParams["FT"]["DO_TEST_SLICE"] == 0)
        assert self._reconsParams["FT"]["FIXEDSLICE"] == FixedSliceMode.middle
        assert self._reconsParams.to_dict()["FT"]["FIXEDSLICE"] == "middle"

        ftWidget._qleSliceN.setText("4")
        iRowN = ftWidget._qcbSelectSlice.findText("row n")
        assert iRowN >= 0
        ftWidget._qcbSelectSlice.setCurrentIndex(iRowN)
        self.assertEqual(self._reconsParams["FT"]["FIXEDSLICE"], "4")
        self.assertEqual(self._reconsParams.to_dict()["FT"]["FIXEDSLICE"], "4")

        assert self._reconsParams["FT"]["VOLOUTFILE"] == 0
        self._reconsParams["FT"]["VOLOUTFILE"] = 0
        ftWidget._setSingleVolOrStack(1)
        self.assertTrue(self._reconsParams["FT"]["VOLOUTFILE"] == 1)

        assert self._reconsParams["FT"]["CORRECT_SPIKES_THRESHOLD"] == 0.04
        ftWidget._setSpikeThreshold(1.12)
        ftWidget._qleThresholdSpikesRm.editingFinished.emit()
        self.assertTrue(self._reconsParams["FT"]["CORRECT_SPIKES_THRESHOLD"] == 1.12)
        ftWidget._grpThreshold.setChecked(False)
        self.assertTrue(self._reconsParams["FT"]["CORRECT_SPIKES_THRESHOLD"] == "Inf")

        assert self._reconsParams["FT"]["RINGSCORRECTION"] == 0
        ftWidget._qcbRingsCorrection.setChecked(True)
        self.assertTrue(self._reconsParams["FT"]["RINGSCORRECTION"] == 1)

        assert self._reconsParams["FT"]["VOLSELECTION_REMEMBER"] == 0
        ftWidget._qcbVolSelRemenber.setChecked(True)
        self.assertTrue(self._reconsParams["FT"]["VOLSELECTION_REMEMBER"] == 1)

        assert self._reconsParams.to_dict()["FT"]["VOLSELECT"] == "total"
        assert self._reconsParams["FT"]["VOLSELECT"] == VolSelMode.total
        iSel = ftWidget._qcbVolumeSelection.findText("manual")
        assert iSel >= 0
        ftWidget._qcbVolumeSelection.setCurrentIndex(iSel)
        assert self._reconsParams.to_dict()["FT"]["VOLSELECT"] == "manual"
        assert self._reconsParams["FT"]["VOLSELECT"] == VolSelMode.manual

    def testFTAxisRead(self):
        ftAxisWidget = self.widget.getReconsParamSetEditor()._axisWidget

        assert self._reconsParams["FTAXIS"]["DO_AXIS_CORRECTION"] == 1
        self._reconsParams["FTAXIS"]["DO_AXIS_CORRECTION"] = 0
        self.qapp.processEvents()
        self.assertFalse(ftAxisWidget._doAxisCorrection.isChecked())

        assert self._reconsParams["FTAXIS"]["USE_TOMWER_AXIS"] == 1
        self._reconsParams["FTAXIS"]["USE_TOMWER_AXIS"] = 0
        self.assertFalse(ftAxisWidget._useTomwerAxis.isChecked())

        assert self._reconsParams["FTAXIS"]["TRY_USE_OLD_TOMWER_AXIS"] == 1
        self._reconsParams["FTAXIS"]["TRY_USE_OLD_TOMWER_AXIS"] = 0
        self.assertFalse(ftAxisWidget._useOldTomwerAxis.isChecked())

    def testDisplayRead(self):
        ftAxisWidget = self.widget.getReconsParamSetEditor()._displayWidget

        assert self._reconsParams["FT"]["SHOWPROJ"] == 0
        self._reconsParams["FT"]["SHOWPROJ"] = True
        self.qapp.processEvents()
        self.assertTrue(ftAxisWidget._qcbShowProj.isChecked())

        assert self._reconsParams["FT"]["SHOWSLICE"] == 1
        self._reconsParams["FT"]["SHOWSLICE"] = 0
        self.assertFalse(ftAxisWidget._qcbShowSlice.isChecked())

        assert self._reconsParams["FT"]["ANGLE_OFFSET"] == 0
        assert self._reconsParams["FT"]["ANGLE_OFFSET_VALUE"] == 0.0
        self._reconsParams["FT"]["ANGLE_OFFSET_VALUE"] = 2.3
        self.assertTrue(ftAxisWidget._qleAngleOffset.text() == "2.3")

    def testDisplayWrite(self):
        displayWidget = self.widget.getReconsParamSetEditor()._displayWidget
        assert self._reconsParams["FT"]["SHOWPROJ"] is False
        assert self._reconsParams.to_dict()["FT"]["SHOWPROJ"] == 0
        displayWidget._qcbShowProj.setChecked(True)
        self.assertTrue(self._reconsParams.to_dict()["FT"]["SHOWPROJ"] == 1)
        self.assertTrue(self._reconsParams["FT"]["SHOWPROJ"] is True)

        assert self._reconsParams.to_dict()["FT"]["SHOWSLICE"] == 1
        assert self._reconsParams["FT"]["SHOWSLICE"] is True
        displayWidget._qcbShowSlice.setChecked(False)
        self.assertTrue(self._reconsParams.to_dict()["FT"]["SHOWSLICE"] == 0)
        self.assertTrue(self._reconsParams["FT"]["SHOWSLICE"] is False)

        assert self._reconsParams["FT"]["ANGLE_OFFSET"] is False
        assert self._reconsParams["FT"]["ANGLE_OFFSET_VALUE"] == 0.0
        displayWidget._qleAngleOffset.setText("2.3")
        self.qapp.processEvents()
        displayWidget._qleAngleOffset.editingFinished.emit()
        assert self._reconsParams["FT"]["ANGLE_OFFSET_VALUE"] == 2.3
        assert self._reconsParams.to_dict()["FT"]["ANGLE_OFFSET"] == 1.0
        displayWidget._qleAngleOffset.setText("0.0")
        displayWidget._qleAngleOffset.editingFinished.emit()
        assert self._reconsParams.to_dict()["FT"]["ANGLE_OFFSET"] == 0
        assert self._reconsParams.to_dict()["FT"]["ANGLE_OFFSET_VALUE"] == 0.0

    def testPaganinRead(self):
        pagWidget = self.widget.getReconsParamSetEditor()._PaganinWidget

        assert self._reconsParams.to_dict()["PAGANIN"]["MODE"] == 0
        assert self._reconsParams["PAGANIN"]["MODE"] == PaganinMode.off
        self._reconsParams["PAGANIN"]["MODE"] = PaganinMode.multi
        self.assertTrue(pagWidget._qcbpaganin.currentText() == "multi")

        assert self._reconsParams["PAGANIN"]["DB"] == 500.0
        self._reconsParams["PAGANIN"]["DB"] = 2.3
        self.assertTrue(pagWidget._qleSigmaBeta.text() == "2.3")

        assert self._reconsParams["PAGANIN"]["DB2"] == 100.0
        self._reconsParams["PAGANIN"]["DB2"] = 3.6
        self.assertTrue(pagWidget._qleSigmaBeta2.text() == "3.6")

        assert self._reconsParams["PAGANIN"]["UNSHARP_COEFF"] == 3.0
        self._reconsParams["PAGANIN"]["UNSHARP_COEFF"] = 2.6
        self.assertTrue(pagWidget._unsharp_sigma_coeff.text() == "2.6")

        assert self._reconsParams["PAGANIN"]["UNSHARP_SIGMA"] == 0.8
        self._reconsParams["PAGANIN"]["UNSHARP_SIGMA"] = 1.0
        self.assertTrue(pagWidget._unsharp_sigma_mask_value.text() == "1.0")

        assert self._reconsParams["PAGANIN"]["THRESHOLD"] == 500.0
        self._reconsParams["PAGANIN"]["THRESHOLD"] = 1.0
        self.assertTrue(pagWidget._qleThreshold.text() == "1.0")

        assert self._reconsParams["PAGANIN"]["DILATE"] == 2
        self._reconsParams["PAGANIN"]["DILATE"] = 1
        self.assertTrue(pagWidget._qleDilatation.text() == "1")

        assert self._reconsParams["PAGANIN"]["MEDIANR"] == 4
        self._reconsParams["PAGANIN"]["MEDIANR"] = 1
        self.assertTrue(pagWidget._qleMedianFilterSize.text() == "1")

        assert self._reconsParams["PAGANIN"]["MKEEP_BONE"] == 0
        self._reconsParams["PAGANIN"]["MKEEP_BONE"] = 1
        self.assertTrue(pagWidget._qcbKeepBone.isChecked())

        assert self._reconsParams["PAGANIN"]["MKEEP_SOFT"] == 0
        self._reconsParams["PAGANIN"]["MKEEP_SOFT"] = 1
        self.assertTrue(pagWidget._qcbKeepSoft.isChecked())

        assert self._reconsParams["PAGANIN"]["MKEEP_ABS"] == 0
        self._reconsParams["PAGANIN"]["MKEEP_ABS"] = 1
        self.assertTrue(pagWidget._qcbKeepAbs.isChecked())

        assert self._reconsParams["PAGANIN"]["MKEEP_CORR"] == 0
        self._reconsParams["PAGANIN"]["MKEEP_CORR"] = 1
        self.assertTrue(pagWidget._qcbKeepCorr.isChecked())

        assert self._reconsParams["PAGANIN"]["MKEEP_MASK"] == 0
        self._reconsParams["PAGANIN"]["MKEEP_MASK"] = 1
        self.assertTrue(pagWidget._qcbKeepMask.isChecked())

    def testPaganinWrite(self):
        pagWidget = self.widget.getReconsParamSetEditor()._PaganinWidget

        iMulti = pagWidget._qcbpaganin.findText("multi")
        assert iMulti >= 0
        pagWidget._qcbpaganin.setCurrentIndex(iMulti)
        self.qapp.processEvents()
        self.assertTrue(self._reconsParams.to_dict()["PAGANIN"]["MODE"] == 3)
        self.assertTrue(self._reconsParams["PAGANIN"]["MODE"] == PaganinMode.multi)

        assert self._reconsParams["PAGANIN"]["DB"] == 500.0
        pagWidget._qleSigmaBeta.setText("2.3")
        pagWidget._qleSigmaBeta.editingFinished.emit()
        self.assertEqual(self._reconsParams.to_dict()["PAGANIN"]["DB"], "2.3")
        self.assertEqual(self._reconsParams["PAGANIN"]["DB"], 2.3)

        assert self._reconsParams["PAGANIN"]["DB2"] == 100.0
        pagWidget._qleSigmaBeta2.setText("3.6")
        pagWidget._qleSigmaBeta2.editingFinished.emit()
        self.assertEqual(self._reconsParams.to_dict()["PAGANIN"]["DB2"], "3.6")
        self.assertEqual(self._reconsParams["PAGANIN"]["DB2"], 3.6)

        assert self._reconsParams.to_dict()["PAGANIN"]["UNSHARP_COEFF"] == 3.0
        pagWidget._unsharp_sigma_coeff.setText("1.2")
        pagWidget._unsharp_sigma_coeff.editingFinished.emit()
        assert self._reconsParams.to_dict()["PAGANIN"]["UNSHARP_COEFF"] == 1.2

        assert self._reconsParams.to_dict()["PAGANIN"]["UNSHARP_SIGMA"] == 0.8
        pagWidget._unsharp_sigma_mask_value.setText("1.0")
        pagWidget._unsharp_sigma_mask_value.editingFinished.emit()
        assert self._reconsParams.to_dict()["PAGANIN"]["UNSHARP_SIGMA"] == 1.0

        assert self._reconsParams.to_dict()["PAGANIN"]["THRESHOLD"] == 500.0
        pagWidget._qleThreshold.setText("1.0")
        pagWidget._qleThreshold.editingFinished.emit()
        assert self._reconsParams.to_dict()["PAGANIN"]["THRESHOLD"] == 1.0

        assert self._reconsParams["PAGANIN"]["DILATE"] == 2
        pagWidget._qleDilatation.setText("1")
        pagWidget._qleDilatation.editingFinished.emit()
        assert self._reconsParams["PAGANIN"]["DILATE"] == 1

        assert self._reconsParams["PAGANIN"]["MEDIANR"] == 4
        pagWidget._qleMedianFilterSize.setText("1")
        pagWidget._qleMedianFilterSize.editingFinished.emit()
        assert self._reconsParams["PAGANIN"]["MEDIANR"] == 1

        assert self._reconsParams["PAGANIN"]["MKEEP_BONE"] == 0
        pagWidget._qcbKeepBone.setChecked(True)
        assert self._reconsParams["PAGANIN"]["MKEEP_BONE"] == 1

        assert self._reconsParams["PAGANIN"]["MKEEP_SOFT"] == 0
        pagWidget._qcbKeepSoft.setChecked(True)
        assert self._reconsParams["PAGANIN"]["MKEEP_SOFT"] == 1

        assert self._reconsParams["PAGANIN"]["MKEEP_ABS"] == 0
        pagWidget._qcbKeepAbs.setChecked(True)
        assert self._reconsParams["PAGANIN"]["MKEEP_ABS"] == 1

        assert self._reconsParams["PAGANIN"]["MKEEP_CORR"] == 0
        pagWidget._qcbKeepCorr.setChecked(True)
        assert self._reconsParams["PAGANIN"]["MKEEP_CORR"] == 1

        assert self._reconsParams["PAGANIN"]["MKEEP_MASK"] == 0
        pagWidget._qcbKeepMask.setChecked(True)
        assert self._reconsParams["PAGANIN"]["MKEEP_MASK"] == 1

    def testPyHSTRead(self):
        pyHSTWidget = self.widget.getReconsParamSetEditor()._PyHSTWidget
        self.assertEqual(
            type(self._reconsParams.pyhst), type(pyHSTWidget._recons_params)
        )
        self.assertTrue(id(self._reconsParams.pyhst) == id(pyHSTWidget._recons_params))

        assert self._reconsParams["PYHSTEXE"]["VERBOSE"] == 0
        self.assertFalse(pyHSTWidget._qcbverbose.isChecked())
        self.assertTrue(id(self._reconsParams.pyhst) == id(pyHSTWidget._recons_params))
        self._reconsParams["PYHSTEXE"]["VERBOSE"] = True
        self.assertTrue(id(self._reconsParams.pyhst) == id(pyHSTWidget._recons_params))

        self.qapp.processEvents()
        self.assertTrue(pyHSTWidget._qcbverbose.isChecked())

        assert self._reconsParams["PYHSTEXE"]["EXE"] == "pyhst2"
        self._reconsParams["PYHSTEXE"]["EXE"] = "pyhst3"
        self.assertTrue(pyHSTWidget._qcbPyHSTVersion.currentText() == "pyhst3")

        assert self._reconsParams["PYHSTEXE"]["OFFV"] == "pyhst2"
        self._reconsParams["PYHSTEXE"]["OFFV"] = "pyhst3"
        self.assertTrue(pyHSTWidget._qlOfficalVersion.text() == "pyhst3")

        assert self._reconsParams["PYHSTEXE"]["VERBOSE_FILE"] == "pyhst_out.txt"
        self._reconsParams["PYHSTEXE"]["VERBOSE_FILE"] = "outToto.dsad"
        self.assertTrue(pyHSTWidget._qleVerboseFile.text() == "outToto.dsad")

    def testPyHSTWrite(self):
        pyHSTWidget = self.widget.getReconsParamSetEditor()._PyHSTWidget
        assert self._reconsParams["PYHSTEXE"]["VERBOSE"] is False
        pyHSTWidget._qcbverbose.setChecked(True)
        self.qapp.processEvents()
        assert self._reconsParams["PYHSTEXE"]["VERBOSE"] is True

        assert self._reconsParams["PYHSTEXE"]["EXE"] == "pyhst2"
        pyHSTWidget._qcbPyHSTVersion.addItem("pyhst3Toto")
        pyHSTWidget._qcbPyHSTVersion.setCurrentIndex(
            pyHSTWidget._qcbPyHSTVersion.count() - 1
        )
        assert self._reconsParams["PYHSTEXE"]["EXE"] == "pyhst3Toto"

        assert self._reconsParams["PYHSTEXE"]["VERBOSE_FILE"] == "pyhst_out.txt"
        pyHSTWidget._qleVerboseFile.setText("outFile.dsad")
        pyHSTWidget._qleVerboseFile.editingFinished.emit()
        assert self._reconsParams["PYHSTEXE"]["VERBOSE_FILE"] == "outFile.dsad"

    def testBeamGeoRead(self):
        beamGeoWidget = self.widget.getReconsParamSetEditor()._beamGeoWidget

        assert self._reconsParams.to_dict()["BEAMGEO"]["TYPE"] == "p"
        assert self._reconsParams["BEAMGEO"]["TYPE"] == BeamGeoType.parallel
        self._reconsParams["BEAMGEO"]["TYPE"] = "f"
        self.assertTrue(beamGeoWidget._qcbType.currentText() == "fan beam")

        assert self._reconsParams["BEAMGEO"]["SX"] == 0.0
        self._reconsParams["BEAMGEO"]["SX"] = 10.2
        assert self._reconsParams["BEAMGEO"]["SX"] == 10.2
        self.assertTrue(beamGeoWidget._qleSX.text() == "10.2")

        assert self._reconsParams["BEAMGEO"]["SY"] == 0.0
        self._reconsParams["BEAMGEO"]["SY"] = 20.2
        self.assertTrue(beamGeoWidget._qleSY.text() == "20.2")

        assert self._reconsParams["BEAMGEO"]["DIST"] == 55.0
        self._reconsParams["BEAMGEO"]["DIST"] = 1.0
        self.assertTrue(beamGeoWidget._qleDIST.text() == "1.0")

    def testBeamGeoWrite(self):
        beamGeoWidget = self.widget.getReconsParamSetEditor()._beamGeoWidget

        assert self._reconsParams["BEAMGEO"]["TYPE"] == BeamGeoType.parallel
        assert self._reconsParams.to_dict()["BEAMGEO"]["TYPE"] == "p"
        iType = beamGeoWidget._qcbType.findText("fan beam")
        assert iType >= 0
        beamGeoWidget._qcbType.setCurrentIndex(iType)
        assert self._reconsParams["BEAMGEO"]["TYPE"] == BeamGeoType.fan
        assert self._reconsParams.to_dict()["BEAMGEO"]["TYPE"] == "f"

        assert self._reconsParams["BEAMGEO"]["SX"] == 0.0
        beamGeoWidget._qleSX.setText("10.2")
        beamGeoWidget._qleSX.editingFinished.emit()
        assert self._reconsParams["BEAMGEO"]["SX"] == 10.2

        assert self._reconsParams["BEAMGEO"]["SY"] == 0.0
        beamGeoWidget._qleSY.setText("11.2")
        beamGeoWidget._qleSY.editingFinished.emit()
        assert self._reconsParams["BEAMGEO"]["SY"] == 11.2

        assert self._reconsParams["BEAMGEO"]["DIST"] == 55.0
        beamGeoWidget._qleDIST.setText("0.2")
        beamGeoWidget._qleDIST.editingFinished.emit()
        assert self._reconsParams["BEAMGEO"]["DIST"] == 0.2

    def testExpertRead(self):
        expertWidget = self.widget.getReconsParamSetEditor()._expertWidget

        assert self._reconsParams["FT"]["NUM_PART"] == 4
        self._reconsParams["FT"]["NUM_PART"] = 2
        self.assertTrue(expertWidget._qsbNumPart.value() == 2)

        assert self._reconsParams["FT"]["VERSION"] == "fastomo3 3.2"
        self._reconsParams["FT"]["VERSION"] = "toto"
        self.assertTrue(expertWidget._qleVersion.text() == "toto")

        assert self._reconsParams["FT"]["DATABASE"] == 0
        self._reconsParams["FT"]["DATABASE"] = 1
        self.assertTrue(expertWidget._qcbDataBase.isChecked())

        assert self._reconsParams["FT"]["NO_CHECK"] == 0
        self.assertFalse(expertWidget._qcbNocheck.isChecked())
        self._reconsParams["FT"]["NO_CHECK"] = 1
        self.assertTrue(expertWidget._qcbNocheck.isChecked())

        assert self._reconsParams["FT"]["ZEROOFFMASK"] == 1
        self._reconsParams["FT"]["ZEROOFFMASK"] = 0
        self.assertFalse(expertWidget._qcbZeroRegionMask.isChecked())

        assert self._reconsParams["FT"]["FIXHD"] == 0
        self._reconsParams["FT"]["FIXHD"] = 1
        self.assertTrue(expertWidget._qcbFixHD.isChecked())

    def testExpertWrite(self):
        expertWidget = self.widget.getReconsParamSetEditor()._expertWidget

        assert self._reconsParams["FT"]["NUM_PART"] == 4
        expertWidget._qsbNumPart.setValue(2)
        self.qapp.processEvents()
        assert self._reconsParams["FT"]["NUM_PART"] == 2

        assert self._reconsParams["FT"]["DATABASE"] == 0
        expertWidget._qcbDataBase.setChecked(True)
        assert self._reconsParams["FT"]["DATABASE"] == 1

        assert self._reconsParams["FT"]["NO_CHECK"] == 0
        expertWidget._qcbNocheck.setChecked(True)
        assert self._reconsParams["FT"]["NO_CHECK"] == 1

        assert self._reconsParams["FT"]["ZEROOFFMASK"] == 1
        expertWidget._qcbZeroRegionMask.setChecked(False)
        assert self._reconsParams["FT"]["ZEROOFFMASK"] == 0

        assert self._reconsParams["FT"]["FIXHD"] == 0
        expertWidget._qcbFixHD.setChecked(True)
        assert self._reconsParams["FT"]["FIXHD"] == 1

    def testOtherRead(self):
        assert isinstance(self._reconsParams["FT"], _ReconsParam)
        self._reconsParams["FT"]["MYPARAM"] = "tata"
        assert isinstance(self._reconsParams["FT"], _ReconsParam)
        otherWidget = self.widget.getReconsParamSetEditor()._otherWidget
        widgetTata = otherWidget.paramToWidget["FT"]["MYPARAM"]
        assert widgetTata.text() == "tata"
        p = self._reconsParams["FT"]
        p._set_parameter_value("MYPARAM", "toto")
        self._reconsParams["FT"]._set_parameter_value("MYPARAM", "toto")
        self.qapp.processEvents()
        otherWidget = self.widget.getReconsParamSetEditor()._otherWidget
        widgetTata = otherWidget.paramToWidget["FT"]["MYPARAM"]
        self.assertTrue(widgetTata.text() == "toto")

    def testOtherWrite(self):
        self._reconsParams["FT"]["MYPARAM"] = "tata"
        otherWidget = self.widget.getReconsParamSetEditor()._otherWidget
        widgetTata = otherWidget.paramToWidget["FT"]["MYPARAM"]
        widgetTata.setText("toto")
        self._reconsParams["FT"]["MYPARAM"] = "toto"


def suite():
    test_suite = unittest.TestSuite()
    for ui in (
        TestControlsFTSeriesWidget,
        TestFTSerieWidget,
        TestExploreDatasetForH5,
        TestLoadSaveH5File,
        TestSync,
    ):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
