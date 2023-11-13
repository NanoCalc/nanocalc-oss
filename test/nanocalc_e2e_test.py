import unittest
import requests
from bs4 import BeautifulSoup

HOST = 'http://172.17.0.2'

class NanoCalcE2ETest(unittest.TestCase):
    def validator(self, url, files, webapp, data): 
        """
        Asserts: 
        - response status code is 200 OK 
        - download link is valid 
        - downloaded file is a zip file
        """

        response = requests.post(url, files=files, data=data)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')         
        download_link = soup.find('a', class_='links')['href']

        download_url = f"{HOST}{download_link}" 
        print(f'{webapp} download url: {download_url}') 
        download_response = requests.get(download_url)
        
        self.assertEqual(download_response.status_code, 200)
        self.assertTrue(download_response.content.startswith(b'PK'))


    def test_fret_calc_upload(self):
        url = f'{HOST}/fret/submit' 
        with open('samples/fret/input.xlsx', 'rb') as xif, \
             open('samples/fret/emission.dat', 'rb') as ef, \
             open('samples/fret/refractive.dat', 'rb') as rfi, \
             open('samples/fret/extinction.dat', 'rb') as ecf:

            files = {'xif': xif, 'ef': ef, 'rfi': rfi, 'ecf': ecf}

            self.validator(url, files, 'FRET-Calc', data=None)


    def test_ri_calc_decadic_upload(self):
        pass 


    def test_ri_calc_k_upload(self):
        pass 


    def test_plq_sim_acceptor_upload(self):
        url = f'{HOST}/plqsim/submit'
        with open('samples/plqsim/input.xlsx', 'rb') as xif: 
            files = {'xif': xif}
            data = {'action': 'Calculate Acceptor Excitation'}

            self.validator(url, files, 'PLQ-Sim Acceptor Calculation', data)
    

    def test_plq_sim_donor_upload(self):
        url = f'{HOST}/plqsim/submit' 
        with open('samples/plqsim/input.xlsx', 'rb') as xif: 
            files = {'xif': xif}
            data = {'action': 'Calculate Donor Excitation'}

            self.validator(url, files, 'PLQ-Sim Donor Calculation', data )



if __name__ == '__main__':
    unittest.main()
