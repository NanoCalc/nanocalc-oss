import unittest
import requests
import zipfile
import io
from bs4 import BeautifulSoup

class NanoCalcE2ETest(unittest.TestCase):
    HOST = "http://localhost:8080"
    
    def validator(self, url, files, webapp, data): 
        """
        Asserts: 
        - response status code is 200 OK 
        - downloaded file is a zip file
        """

        form_data = self.build_form_data(files, data)
        response = requests.post(url, files=form_data['files'], data=form_data['data'])
        # print(f"Server message: {response.text}")
        
        self.assertEqual(response.status_code, 200)
                
        download_response = response.content
        self.assertTrue(download_response.startswith(b'PK'), "Downloaded content is not a valid ZIP file.")

        with zipfile.ZipFile(io.BytesIO(download_response)) as zip_file:
            self.assertTrue(zip_file.testzip() is None, "The ZIP file is corrupted.")
            print(f'{webapp} ZIP file contents:\n{zip_file.namelist()}')

    def error_validator(self, url, files, webapp, data):
        """
        Asserts: 
        - response status code is not 200 OK 
        - error message is shown
        """

        form_data = self.build_form_data(files, data)
        response = requests.post(url, files=form_data['files'], data=form_data['data'])
        
        
        self.assertNotEqual(response.status_code, 200, "Expected an error status code but got 200 OK.")
        print(f"Server error message: {response.text}")
        print(f'{webapp} has successfully shown an error message.')

    def build_form_data(self, files, mode):
        """
        Converts the provided files and mode into the structure expected by the backend.
        """
        MODE_FORM_FIELD = 'NANOCALC_USER_MODE'
        FILE_ID_FORM_FIELD = 'NANOCALC_FILE_ID_FORM_FIELD'
        FILES_FORM_FIELD = 'NANOCALC_USER_UPLOADED_FILES'
        

        form_data = {
            'files': [],    # request.files
            'data': {}      # request.form
        }

        if mode:
            form_data['data'][MODE_FORM_FIELD] = mode
        
        for file_id, file_objs in files.items():
            for file_obj in file_objs:
                form_data['data'].setdefault(FILE_ID_FORM_FIELD, []).append(file_id)
                form_data['files'].append((FILES_FORM_FIELD, file_obj))

        return form_data

    def test_fret_calc_upload_success(self):
        url = f'{self.HOST}/upload/fretcalc' 
        with open('samples/fret/input.xlsx', 'rb') as xif, \
             open('samples/fret/emission.dat', 'rb') as ef, \
             open('samples/fret/refractive.dat', 'rb') as rfi, \
             open('samples/fret/extinction.dat', 'rb') as ecf:

            files = {
                'inputExcel': [xif],
                'emissionCoefficient': [ef],
                'refractiveIndex': [rfi],
                'extinctionCoefficient': [ecf]
            }

            mode = None 
            self.validator(url, files, 'FRET-Calc', data=mode)


    def test_fret_calc_upload_error(self):
        url = f'{self.HOST}/upload/fretcalc' 
        with open('samples/broken/broken_input.xlsx', 'rb') as xif, \
             open('samples/broken/broken_data.dat', 'rb') as ef, \
             open('samples/broken/broken_data.dat', 'rb') as rfi, \
             open('samples/broken/broken_data.dat', 'rb') as ecf:

            files = {
                'inputExcel': [xif],
                'emissionCoefficient': [ef],
                'refractiveIndex': [rfi],
                'extinctionCoefficient': [ecf]
            }

            mode = None 
            self.error_validator(url, files, 'FRET-Calc', data=mode)

    def test_ri_calc_optical_constants_upload_success(self):
        url = f'{self.HOST}/upload/ricalc'

        with open('samples/ri/input.xlsx', 'rb') as inputExcel, \
             open('samples/ri/decadic.dat', 'rb') as decadicCoefficient:

            files = {
                'inputExcel': [inputExcel],
                'decadicCoefficient': [decadicCoefficient],
            }

            mode = 'opticalConstants' 
            self.validator(url, files, 'RI-Calc Optical Constants', data=mode)

    def test_ri_calc_optical_constants_upload_error(self):
        url = f'{self.HOST}/upload/ricalc'

        with open('samples/broken/broken_input.xlsx', 'rb') as inputExcel, \
             open('samples/broken/broken_data.dat', 'rb') as decadicCoefficient:

            files = {
                'inputExcel': [inputExcel],
                'decadicCoefficient': [decadicCoefficient],
            }

            mode = 'opticalConstants' 
            self.error_validator(url, files, 'RI-Calc Optical Constants', data=mode)

    def test_ri_calc_refractive_index_upload_success(self):
        url = f'{self.HOST}/upload/ricalc'
        
        with open('samples/ri/input.xlsx', 'rb') as inputExcel, \
             open('samples/ri/decadic.dat', 'rb') as decadicCoefficient:

            files = {
                'inputExcel': [inputExcel],
                'constantK': [decadicCoefficient],
            }

            mode = 'refractiveIndex' 
            self.validator(url, files, 'RI-Calc Refractive Index', data=mode)

    def test_ri_calc_refractive_index_upload_error(self):
        url = f'{self.HOST}/upload/ricalc'

        with open('samples/broken/broken_input.xlsx', 'rb') as inputExcel, \
             open('samples/broken/broken_data.dat', 'rb') as decadicCoefficient:

            files = {
                'inputExcel': [inputExcel],
                'decadicCoefficient': [decadicCoefficient],
            }

            mode = 'refractiveIndex' 
            self.error_validator(url, files, 'RI-Calc Refractive Index', data=mode)

    def test_plq_sim_acceptor_upload_success(self):
        url = f'{self.HOST}/upload/plqsim'
        with open('samples/plqsim/input.xlsx', 'rb') as xif: 
            files = {'inputExcel': [xif]}
            mode = 'acceptorExcitation'

            self.validator(url, files, 'PLQ-Sim Acceptor Calculation', mode)

    def test_plq_sim_acceptor_upload_error(self):
        url = f'{self.HOST}/upload/plqsim'
        with open('samples/broken/broken_input.xlsx', 'rb') as xif: 
            files = {'inputExcel': [xif]}
            mode = 'acceptorExcitation'

            self.error_validator(url, files, 'PLQ-Sim Acceptor Calculation', mode)


    def test_plq_sim_donor_upload_success(self):
        url = f'{self.HOST}/upload/plqsim' 
        with open('samples/plqsim/input.xlsx', 'rb') as xif: 
            files = {'inputExcel': [xif]}
            mode = 'donorExcitation'

            self.validator(url, files, 'PLQ-Sim Donor Calculation', mode)


    def test_plq_sim_donor_upload_error(self):
        url = f'{self.HOST}/upload/plqsim' 
        with open('samples/broken/broken_input.xlsx', 'rb') as xif: 
            files = {'inputExcel': [xif]}
            mode = 'donorExcitation'

            self.error_validator(url, files, 'PLQ-Sim Donor Calculation', mode)


    def test_tmm_sim_bhj_upload_success(self):
        url = f'{self.HOST}/upload/tmmsim' 
        files = []
        try: 
            with open('samples/tmm/input_bhj.xlsx', 'rb') as xif, \
                 open('samples/tmm/AM15G.csv', 'rb') as am15g, \
                 open('samples/tmm/nk_Air.csv', 'rb') as air, \
                 open('samples/tmm/nk_Al.csv', 'rb') as al, \
                 open('samples/tmm/nk_Ca.csv', 'rb') as ca, \
                 open('samples/tmm/nk_ITO.csv', 'rb') as ito, \
                 open('samples/tmm/nk_P3HT.csv', 'rb') as p3ht, \
                 open('samples/tmm/nk_P3HTPCBM.csv', 'rb') as p3htpcbm, \
                 open('samples/tmm/nk_PCBM.csv', 'rb') as pcbm, \
                 open('samples/tmm/nk_PEDOT.csv', 'rb') as pedot, \
                 open('samples/tmm/nk_SiO2.csv', 'rb') as sio2: 

                files = {
                    'inputExcel': [xif],
                    'layerFiles': [
                        am15g, air, al, ca, ito, p3ht, p3htpcbm, pcbm, pedot, sio2
                    ]
                }

                self.validator(url, files, 'TMM-Sim BHJ', data=None)

        finally:
            for file_list in files.values():
                for file_obj in file_list:
                    file_obj.close()

        
        def test_tmm_sim_bilayer_upload_success(self):
            url = f'{self.HOST}/upload/tmmsim' 
            files = []
            try: 
                with open('samples/tmm/input_bilayer.xlsx', 'rb') as xif, \
                     open('samples/tmm/AM15G.csv', 'rb') as am15g, \
                     open('samples/tmm/nk_Air.csv', 'rb') as air, \
                     open('samples/tmm/nk_Al.csv', 'rb') as al, \
                     open('samples/tmm/nk_Ca.csv', 'rb') as ca, \
                     open('samples/tmm/nk_ITO.csv', 'rb') as ito, \
                     open('samples/tmm/nk_P3HT.csv', 'rb') as p3ht, \
                     open('samples/tmm/nk_P3HTPCBM.csv', 'rb') as p3htpcbm, \
                     open('samples/tmm/nk_PCBM.csv', 'rb') as pcbm, \
                     open('samples/tmm/nk_PEDOT.csv', 'rb') as pedot, \
                     open('samples/tmm/nk_SiO2.csv', 'rb') as sio2: 

                    files = {
                        'inputExcel': [xif],
                        'layerFiles': [
                            am15g, air, al, ca, ito, p3ht, p3htpcbm, pcbm, pedot, sio2
                        ]
                    }

                    self.validator(url, files, 'TMM-Sim Bilayer', data=None)

            finally:
                for file_list in files.values():
                    for file_obj in file_list:
                        file_obj.close()


if __name__ == '__main__':
    unittest.main()
