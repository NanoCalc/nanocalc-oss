import unittest
import requests
import zipfile
import io
import time

class NanoCalcE2ETest(unittest.TestCase):
    HOST = "http://localhost:8080"
    
    def poll_job_status(self, job_id, timeout=60, interval=2):
        """
        Polls the job status until it is finished or fails.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = requests.get(f"{self.HOST}/status/{job_id}")
            self.assertEqual(response.status_code, 200)
            status = response.json().get("status")
            
            if status == "finished":
                return True
            elif status == "failed":
                self.fail(f"Job {job_id} failed.")
            elif status == "not_found":
                self.fail(f"Job {job_id} not found.")
            
            time.sleep(interval)
        
        self.fail(f"Job {job_id} did not complete within {timeout} seconds.")

    def download_result(self, job_id):
        """
        Downloads the result of a finished job.
        """
        response = requests.get(f"{self.HOST}/download/{job_id}")
        self.assertEqual(response.status_code, 200)
        return response.content

    def validator(self, url, files, webapp, data): 
        """
        Asserts: 
        - response status code is 202 Accepted 
        - job completes successfully
        - downloaded file is a valid ZIP file
        """
        form_data = self.build_form_data(files, data)
        response = requests.post(url, files=form_data['files'], data=form_data['data'])
        
        self.assertEqual(response.status_code, 202)
        job_id = response.json().get("job_id")
        self.assertIsNotNone(job_id, "Job ID not returned in response.")
        
        # Poll job status
        self.poll_job_status(job_id)
        
        # Download result
        download_response = self.download_result(job_id)
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
        print("Testing FRET-Calc successful upload.")
        url = f'{self.HOST}/upload/fretcalc' 
        with open('samples/fretcalc/input.xlsx', 'rb') as xif, \
             open('samples/fretcalc/emission.dat', 'rb') as ef, \
             open('samples/fretcalc/refractive.dat', 'rb') as rfi, \
             open('samples/fretcalc/extinction.dat', 'rb') as ecf:

            files = {
                'inputExcel': [xif],
                'emissionCoefficient': [ef],
                'refractiveIndex': [rfi],
                'extinctionCoefficient': [ecf]
            }

            mode = None 
            self.validator(url, files, 'FRET-Calc', data=mode)


    def test_fret_calc_upload_error(self):
        print("Testing FRET-Calc error upload.")
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
        print("Testing RI-Calc Optical Constants successful upload.")
        url = f'{self.HOST}/upload/ricalc'

        with open('samples/ricalc/input.xlsx', 'rb') as inputExcel, \
             open('samples/ricalc/decadic.dat', 'rb') as decadicCoefficient:

            files = {
                'inputExcel': [inputExcel],
                'decadicCoefficient': [decadicCoefficient],
            }

            mode = 'opticalConstants' 
            self.validator(url, files, 'RI-Calc Optical Constants', data=mode)

    def test_ri_calc_optical_constants_upload_error(self):
        print("Testing RI-Calc Optical Constants error upload.")
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
        print("Testing RI-Calc Refractive Index successful upload.")
        url = f'{self.HOST}/upload/ricalc'
        
        with open('samples/ricalc/input.xlsx', 'rb') as inputExcel, \
             open('samples/ricalc/k.dat', 'rb') as kFile:

            files = {
                'inputExcel': [inputExcel],
                'constantK': [kFile],
            }

            mode = 'refractiveIndex' 
            self.validator(url, files, 'RI-Calc Refractive Index', data=mode)

    def test_ri_calc_refractive_index_upload_error(self):
        print("Testing RI-Calc Refractive Index error upload.")
        url = f'{self.HOST}/upload/ricalc'

        with open('samples/broken/broken_input.xlsx', 'rb') as inputExcel, \
             open('samples/broken/broken_data.dat', 'rb') as kFile:

            files = {
                'inputExcel': [inputExcel],
                'constantK': [kFile],
            }

            mode = 'refractiveIndex' 
            self.error_validator(url, files, 'RI-Calc Refractive Index', data=mode)

    def test_plq_sim_acceptor_upload_success(self):
        print("Testing PLQ-Sim Acceptor successful upload.")
        url = f'{self.HOST}/upload/plqsim'
        with open('samples/plqsim/input.xlsx', 'rb') as xif: 
            files = {'inputExcel': [xif]}
            mode = 'acceptorExcitation'

            self.validator(url, files, 'PLQ-Sim Acceptor Calculation', mode)

    def test_plq_sim_acceptor_upload_error(self):
        print("Testing PLQ-Sim Acceptor error upload.")
        url = f'{self.HOST}/upload/plqsim'
        with open('samples/broken/broken_input.xlsx', 'rb') as xif: 
            files = {'inputExcel': [xif]}
            mode = 'acceptorExcitation'

            self.error_validator(url, files, 'PLQ-Sim Acceptor Calculation', mode)


    def test_plq_sim_donor_upload_success(self):
        print("Testing PLQ-Sim Donor successful upload.")
        url = f'{self.HOST}/upload/plqsim' 
        with open('samples/plqsim/input.xlsx', 'rb') as xif: 
            files = {'inputExcel': [xif]}
            mode = 'donorExcitation'

            self.validator(url, files, 'PLQ-Sim Donor Calculation', mode)


    def test_plq_sim_donor_upload_error(self):
        print("Testing PLQ-Sim Donor error upload.")
        url = f'{self.HOST}/upload/plqsim' 
        with open('samples/broken/broken_input.xlsx', 'rb') as xif: 
            files = {'inputExcel': [xif]}
            mode = 'donorExcitation'

            self.error_validator(url, files, 'PLQ-Sim Donor Calculation', mode)


    def test_tmm_sim_bhj_upload_success(self):
        print("Testing TMM-Sim BHJ successful upload.")
        url = f'{self.HOST}/upload/tmmsim' 
        files = []
        try: 
            with open('samples/tmmsim/input_bhj.xlsx', 'rb') as xif, \
                 open('samples/tmmsim/AM15G.csv', 'rb') as am15g, \
                 open('samples/tmmsim/nk_Air.csv', 'rb') as air, \
                 open('samples/tmmsim/nk_Al.csv', 'rb') as al, \
                 open('samples/tmmsim/nk_Ca.csv', 'rb') as ca, \
                 open('samples/tmmsim/nk_ITO.csv', 'rb') as ito, \
                 open('samples/tmmsim/nk_P3HT.csv', 'rb') as p3ht, \
                 open('samples/tmmsim/nk_P3HTPCBM.csv', 'rb') as p3htpcbm, \
                 open('samples/tmmsim/nk_PCBM.csv', 'rb') as pcbm, \
                 open('samples/tmmsim/nk_PEDOT.csv', 'rb') as pedot, \
                 open('samples/tmmsim/nk_SiO2.csv', 'rb') as sio2: 

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
        print("Testing TMM-Sim Bilayer successful upload.")
        url = f'{self.HOST}/upload/tmmsim' 
        files = []
        try: 
            with open('samples/tmmsim/input_bilayer.xlsx', 'rb') as xif, \
                 open('samples/tmmsim/AM15G.csv', 'rb') as am15g, \
                 open('samples/tmmsim/nk_Air.csv', 'rb') as air, \
                 open('samples/tmmsim/nk_Al.csv', 'rb') as al, \
                 open('samples/tmmsim/nk_Ca.csv', 'rb') as ca, \
                 open('samples/tmmsim/nk_ITO.csv', 'rb') as ito, \
                 open('samples/tmmsim/nk_P3HT.csv', 'rb') as p3ht, \
                 open('samples/tmmsim/nk_P3HTPCBM.csv', 'rb') as p3htpcbm, \
                 open('samples/tmmsim/nk_PCBM.csv', 'rb') as pcbm, \
                 open('samples/tmmsim/nk_PEDOT.csv', 'rb') as pedot, \
                 open('samples/tmmsim/nk_SiO2.csv', 'rb') as sio2: 

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


if __name__ == '__main__':
    unittest.main()
