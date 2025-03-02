from helper_functions import generate_zip
import unittest
import unittest.mock as mock
import os
import tempfile
import zipfile

class TestHelperFunctions(unittest.TestCase):
    
    def test_generate_zip(self):

        with tempfile.TemporaryDirectory() as sourceDir, tempfile.TemporaryDirectory() as targetDir:
            file_mock1 = mock.MagicMock()
            file_mock2 = mock.MagicMock()   
            file_mock1.filename = "myPicture.png"
            file_mock2.filename = "myData.dat"

            with open(os.path.join(sourceDir, "myPicture.png"), 'w') as f:
                f.write("0xFF")
            with open(os.path.join(sourceDir, "myData.dat"), 'w') as f:
                f.write("Data | in | columns")

            finalZipFilePath = generate_zip(sourceDir, targetDir)
            finalZipFileName = finalZipFilePath.split("/").pop()

            self.assertEqual(finalZipFileName, "generated-data.zip")

            with zipfile.ZipFile(finalZipFilePath, 'r') as zip_ref:
                self.assertIn("myPicture.png", zip_ref.namelist()) 
                self.assertIn("myData.dat", zip_ref.namelist())

                with zip_ref.open("myPicture.png") as file:
                    content = file.read().decode('utf-8')
                    self.assertEqual(content, "0xFF")

                with zip_ref.open("myData.dat") as file:
                    content = file.read().decode('utf-8')
                    self.assertEqual(content, "Data | in | columns")


if __name__ == '__main__':
    unittest.main()
