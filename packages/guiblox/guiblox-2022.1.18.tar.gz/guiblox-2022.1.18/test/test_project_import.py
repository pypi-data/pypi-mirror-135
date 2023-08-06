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
        self.GUI = theme().addColor()                            #Create GUI object
        print("",end="")
        pass

    def tearDown(self):                             #Run after each test
        pass

###############################################################################
### <Test>
###############################################################################
    def test_aaa_guiBlox(self):
        import projects.aaa_guiblox

    def test_aaa_guiBlox_jaVISA_socket(self):
        import projects.aaa_guiblox_jaVISA_socket

    def test_aaa_print(self):
        import projects.aaa_print

    def test_aaa_tkinter(self):
        import projects.aaa_tkinter

    def test_DebugTool(self):
        import projects.DebugTool

    def test_IQConvert(self):
        import projects.IQConvert

    def test_Unity(self):
        import projects.Unity_K144

    def test_VSA_VSG_Sweep(self):
        import projects.VSA_VSG_Sweep


###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
