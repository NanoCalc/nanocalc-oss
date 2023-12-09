from helper_functions import *
from flask import Flask
from visitor import db, Visitor
from config import TestConfig
import unittest
import hashlib

class TestHelperFunctions(unittest.TestCase):
    def test_allowed_file(self):
        pass 
    def test_save_file_with_uuid(self):
        pass 
    def test_generate_zip(self):
        pass 
    def test_log_vistor(self):
        pass 
    def test_get_ip_count(self):
        pass
    

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.init_app(self.app)
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    
    def test_visitor_creation(self):
        visitor = Visitor(ip_address='192.168.1.1', user_agent='Mozilla/5.0', operating_system='Linux', country='USA')
        db.session.add(visitor)
        db.session.commit()

        saved_visitor = Visitor.query.filter_by(ip_address=visitor.ip_address).first()
        self.assertIsNotNone(saved_visitor)
        self.assertNotEqual(saved_visitor.ip_address, '192.168.1.1')
        self.assertEqual(saved_visitor.ip_address, hashlib.sha256('192.168.1.1'.encode()).hexdigest())
        self.assertEqual(saved_visitor.user_agent, 'Mozilla/5.0')
        self.assertEqual(saved_visitor.operating_system, 'Linux')
        self.assertEqual(saved_visitor.country, 'USA')



if __name__ == '__main__':
    unittest.main()