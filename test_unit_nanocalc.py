from helper_functions import *
from flask import Flask
from config import TestConfig
import unittest
import unittest.mock as mock
import tempfile 

class TestHelperFunctions(unittest.TestCase):
    def test_allowed_file(self):
        self.assertTrue(allowed_file("test.jpg", ["jpg", "jpeg"]))
        self.assertFalse(allowed_file("test.txt", ["jpg", "jpeg"])) 
        self.assertFalse(allowed_file("test.txt", [])) 


    @mock.patch('uuid.uuid4')
    def test_save_file_with_uuid(self, mock_uuid4):
        mock_uuid4.return_value = uuid.UUID('d'*32)  

        with tempfile.TemporaryDirectory() as tmpdirname:
            file_mock = mock.MagicMock()
            filepath = save_file_with_uuid(tmpdirname, file_mock, 'txt')

            expected_path = os.path.join(tmpdirname, "dddddddd-dddd-dddd-dddd-dddddddddddd.txt")
            self.assertEqual(filepath, expected_path)

            file_mock.save.assert_called_once_with(expected_path)
             

    @mock.patch('uuid.uuid4')
    def test_generate_zip(self, mock_uuid4):
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(os.path.join(tmpdirname, "dummy.txt"), 'w') as f:
                f.write("Hello World")

            zip_filename = generate_zip(tmpdirname, 'fret', TestConfig.UPLOAD_FOLDER)
            zip_path = os.path.join(TestConfig.UPLOAD_FOLDER, 'fret', zip_filename)
            self.assertTrue(os.path.exists(zip_path))
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                self.assertIn("dummy.txt", zip_ref.namelist()) 



if __name__ == '__main__':
    unittest.main()