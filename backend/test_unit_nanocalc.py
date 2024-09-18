from helper_functions import save_file_with_uuid, generate_zip
from flask import Flask
import unittest
import unittest.mock as mock
import os
import tempfile
import zipfile
import uuid

class TestHelperFunctions(unittest.TestCase):

    @mock.patch('uuid.uuid4')
    def test_save_file_with_uuid(self, mock_uuid4):
        mock_uuid4.return_value = "mockUUID"
        filename_mock = "testfile.csv"

        with tempfile.TemporaryDirectory() as tmpdir:
            file_mock = mock.MagicMock()
            file_mock.filename = filename_mock

            finalPath = save_file_with_uuid(tmpdir, file_mock)
            finalFileName = finalPath.split("/").pop()
            
            self.assertEqual(finalFileName, "mockUUID.csv")
            mock_uuid4.assert_called_once()
            self.assertTrue(finalPath.startswith(tmpdir))
            self.assertTrue(finalPath.endswith(".csv"))

            

    @mock.patch('uuid.uuid4')
    def test_generate_zip(self, mock_uuid4):
        mock_uuid4.return_value = "mockUUID"
        webAppName_mock = "randomNanocalcApp"

        with tempfile.TemporaryDirectory() as sourceDir, tempfile.TemporaryDirectory() as targetDir:
            file_mock1 = mock.MagicMock()
            file_mock2 = mock.MagicMock()   
            file_mock1.filename = "myPicture.png"
            file_mock2.filename = "myData.dat"

            with open(os.path.join(sourceDir, "myPicture.png"), 'w') as f:
                f.write("0xFF")
            with open(os.path.join(sourceDir, "myData.dat"), 'w') as f:
                f.write("Data | in | columns")

            finalZipFilePath = generate_zip(sourceDir, webAppName_mock, targetDir)
            finalZipFileName = finalZipFilePath.split("/").pop()

            self.assertEqual(finalZipFileName, "mockUUID" + "-generated-data.zip")

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
