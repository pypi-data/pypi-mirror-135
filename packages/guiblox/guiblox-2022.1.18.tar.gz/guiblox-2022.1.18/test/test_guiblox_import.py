###############################################################################
### Rohde & Schwarz SCPI Driver Software Test
###
### Purpose: Import Library-->Create Object-->Catch obvious typos.
###          Tests do not require instrument.
### Author:  mclim
### Date:    2018.06.13
###############################################################################
### Code Start
###############################################################################
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #Run before each test
        from guiblox import theme
        self.GUI = theme().addColor()               #Create GUI object
        print("",end="")

    def tearDown(self):                             #Run after each test
        pass

###############################################################################
### <Test>
###############################################################################
    def test_buttonCol(self):
        from guiblox import buttonCol
        self.testObj = buttonCol(self.GUI, 3)

    def test_buttonrow(self):
        from guiblox import buttonRow
        self.testObj = buttonRow(self.GUI, 3)

    def test_common(self):
        pass

    def test_entryCol(self):
        from guiblox import entryCol
        entryDict = {}
        entryDict['Label1'] = 'Value1'
        entryDict['Label2'] = 'Value2'
        self.testObj = entryCol(self.GUI, entryDict)

    def test_listWindow(self):
        from guiblox import listWindow
        self.testObj = listWindow(self.GUI)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
