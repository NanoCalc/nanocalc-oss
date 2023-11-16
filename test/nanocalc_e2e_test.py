import unittest
import requests
from bs4 import BeautifulSoup
# import argparse
# import sys


# def parse_custom_args():
#     parser = argparse.ArgumentParser(add_help=False)
#     parser.add_argument('--HOST', default='http://172.17.0.2', help='Host to run tests against')
#     args, unknown = parser.parse_known_args()
#     return args, unknown

# args, unknown = parse_custom_args()
# sys.argv = [sys.argv[0]] + unknown

class NanoCalcE2ETest(unittest.TestCase):
    HOST = "http://localhost:8080"
    
    def validator(self, url, files, webapp, data): 
        """
        Asserts: 
        - response status code is 200 OK 
        - download link is valid 
        - downloaded file is a zip file
        """

        response = requests.post(url, files=files, data=data)
        self.assertEqual(response.status_code, 200)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Content (Snippet): {response.content}")

        soup = BeautifulSoup(response.content, 'html.parser')         
        download_link = soup.find('a', class_='links')['href']

        download_url = f"{self.HOST}{download_link}" 
        print(f'{webapp} download url: {download_url}') 
        download_response = requests.get(download_url)

        print(f"Download Response Status Code: {download_response.status_code}")
        print(f"Download Response Headers: {download_response.headers}")
        #print(f"Download Response Content (Snippet): {download_response.content}")
        
        self.assertEqual(download_response.status_code, 200)
        self.assertTrue(download_response.content.startswith(b'PK'))


    def error_validator(self, url, files, webapp, data):
        """
        Asserts: 
        - response status code is 200 OK 
        - error message is shown
        """

        response = requests.post(url, files=files, data=data)
        self.assertEqual(response.status_code, 200)

        print(f"Error Response Status Code: {response.status_code}")
        print(f"Error Response Headers: {response.headers}")
        print(f"Error Response Content: {response.text}")


        soup = BeautifulSoup(response.content, 'html.parser')         
        error_header = soup.find('h1')
        self.assertIsNotNone(error_header)
        self.assertEqual(error_header.text.strip(), "That's an input error!")
        print(f'{webapp} has successfully shown an error message.')
        

    def test_fret_calc_upload_success(self):
        url = f'{self.HOST}/fret/submit' 
        with open('test/samples/fret/input.xlsx', 'rb') as xif, \
             open('test/samples/fret/emission.dat', 'rb') as ef, \
             open('test/samples/fret/refractive.dat', 'rb') as rfi, \
             open('test/samples/fret/extinction.dat', 'rb') as ecf:

            files = {'xif': xif, 'ef': ef, 'rfi': rfi, 'ecf': ecf}

            self.validator(url, files, 'FRET-Calc', data=None)

    @unittest.skip
    def test_fret_calc_upload_error(self):
        url = f'{self.HOST}/fret/submit' 
        with open('test/samples/broken/broken_input.xlsx', 'rb') as xif, \
             open('test/samples/broken/broken_data.dat', 'rb') as ef, \
             open('test/samples/broken/broken_data.dat', 'rb') as rfi, \
             open('test/samples/broken/broken_data.dat', 'rb') as ecf:

            files = {'xif': xif, 'ef': ef, 'rfi': rfi, 'ecf': ecf}

            self.error_validator(url, files, 'FRET-Calc', data=None)

    @unittest.skip
    def test_ri_calc_decadic_upload_success(self):
        pass 

    @unittest.skip
    def test_ri_calc_k_upload_success(self):
        pass 

    @unittest.skip
    def test_plq_sim_acceptor_upload_success(self):
        url = f'{self.HOST}/plqsim/submit'
        with open('test/samples/plqsim/input.xlsx', 'rb') as xif: 
            files = {'xif': xif}
            data = {'action': 'Calculate Acceptor Excitation'}

            self.validator(url, files, 'PLQ-Sim Acceptor Calculation', data)
    
    @unittest.skip
    def test_plq_sim_acceptor_upload_error(self):
        url = f'{self.HOST}/plqsim/submit'
        with open('test/samples/broken/broken_input.xlsx', 'rb') as xif: 
            files = {'xif': xif}
            data = {'action': 'Calculate Acceptor Excitation'}

            self.error_validator(url, files, 'PLQ-Sim Acceptor Calculation', data)

    @unittest.skip
    def test_plq_sim_donor_upload_success(self):
        url = f'{self.HOST}/plqsim/submit' 
        with open('test/samples/plqsim/input.xlsx', 'rb') as xif: 
            files = {'xif': xif}
            data = {'action': 'Calculate Donor Excitation'}

            self.validator(url, files, 'PLQ-Sim Donor Calculation', data)


    @unittest.skip
    def test_plq_sim_donor_upload_error(self):
        url = f'{self.HOST}/plqsim/submit' 
        with open('test/samples/broken/broken_input.xlsx', 'rb') as xif: 
            files = {'xif': xif}
            data = {'action': 'Calculate Donor Excitation'}

            self.error_validator(url, files, 'PLQ-Sim Donor Calculation', data)

    
    @unittest.skip
    def test_tmm_sim_bhj_upload_success(self):
        url = f'{self.HOST}/tmmsim/submit' 
        files = []
        try: 
            with open('test/samples/tmm/input_bhj.xlsx', 'rb') as xif, \
                 open('test/samples/tmm/AM15G.csv', 'rb') as am15g, \
                 open('test/samples/tmm/nk_Air.csv', 'rb') as air, \
                 open('test/samples/tmm/nk_Al.csv', 'rb') as al, \
                 open('test/samples/tmm/nk_Ca.csv', 'rb') as ca, \
                 open('test/samples/tmm/nk_ITO.csv', 'rb') as ito, \
                 open('test/samples/tmm/nk_P3HT.csv', 'rb') as p3ht, \
                 open('test/samples/tmm/nk_P3HTPCBM.csv', 'rb') as p3htpcbm, \
                 open('test/samples/tmm/nk_PCBM.csv', 'rb') as pcbm, \
                 open('test/samples/tmm/nk_PEDOT.csv', 'rb') as pedot, \
                 open('test/samples/tmm/nk_SiO2.csv', 'rb') as sio2: 

                files = [
                    ('xif', ('input_bhj.xlsx', open('test/samples/tmm/input_bhj.xlsx', 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
                    ('layer_files', ('AM15G.csv', open('test/samples/tmm/AM15G.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_Air.csv', open('test/samples/tmm/nk_Air.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_Al.csv', open('test/samples/tmm/nk_Al.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_Ca.csv', open('test/samples/tmm/nk_Ca.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_ITO.csv', open('test/samples/tmm/nk_ITO.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_P3HT.csv', open('test/samples/tmm/nk_P3HT.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_P3HTPCBM.csv', open('test/samples/tmm/nk_P3HTPCBM.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_PCBM.csv', open('test/samples/tmm/nk_PCBM.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_PEDOT.csv', open('test/samples/tmm/nk_PEDOT.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_SiO2.csv', open('test/samples/tmm/nk_SiO2.csv', 'rb'), 'text/csv')),
                ]

                self.validator(url, files, 'TMM-Sim BHJ', data=None)

        finally:
            for _, file_tuple in files:
                if isinstance(file_tuple, tuple):
                    file_tuple[1].close()

    @unittest.skip
    def test_tmm_sim_bhj_upload_error(self):
        pass

    @unittest.skip
    def test_tmm_sim_bilayer_upload_success(self):
        url = f'{self.HOST}/tmmsim/submit' 
        files = []
        try: 
            with open('test/samples/tmm/input_bilayer.xlsx', 'rb') as xif, \
                 open('test/samples/tmm/AM15G.csv', 'rb') as am15g, \
                 open('test/samples/tmm/nk_Air.csv', 'rb') as air, \
                 open('test/samples/tmm/nk_Al.csv', 'rb') as al, \
                 open('test/samples/tmm/nk_Ca.csv', 'rb') as ca, \
                 open('test/samples/tmm/nk_ITO.csv', 'rb') as ito, \
                 open('test/samples/tmm/nk_P3HT.csv', 'rb') as p3ht, \
                 open('test/samples/tmm/nk_P3HTPCBM.csv', 'rb') as p3htpcbm, \
                 open('test/samples/tmm/nk_PCBM.csv', 'rb') as pcbm, \
                 open('test/samples/tmm/nk_PEDOT.csv', 'rb') as pedot, \
                 open('test/samples/tmm/nk_SiO2.csv', 'rb') as sio2: 

                files = [
                    ('xif', ('input_bilayer.xlsx', open('test/samples/tmm/input_bilayer.xlsx', 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
                    ('layer_files', ('AM15G.csv', open('test/samples/tmm/AM15G.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_Air.csv', open('test/samples/tmm/nk_Air.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_Al.csv', open('test/samples/tmm/nk_Al.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_Ca.csv', open('test/samples/tmm/nk_Ca.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_ITO.csv', open('test/samples/tmm/nk_ITO.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_P3HT.csv', open('test/samples/tmm/nk_P3HT.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_P3HTPCBM.csv', open('test/samples/tmm/nk_P3HTPCBM.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_PCBM.csv', open('test/samples/tmm/nk_PCBM.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_PEDOT.csv', open('test/samples/tmm/nk_PEDOT.csv', 'rb'), 'text/csv')),
                    ('layer_files', ('nk_SiO2.csv', open('test/samples/tmm/nk_SiO2.csv', 'rb'), 'text/csv')),
                ]

                self.validator(url, files, 'TMM-Sim Bilayer', data=None)

        finally:
            for _, file_tuple in files:
                if isinstance(file_tuple, tuple):
                    file_tuple[1].close()

    @unittest.skip
    def test_tmm_sim_bilayer_upload_error(self):
        pass



if __name__ == '__main__':
    unittest.main()
