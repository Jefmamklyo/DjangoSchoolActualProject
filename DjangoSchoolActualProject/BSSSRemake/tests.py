"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from typing import override
from warnings import simplefilter
import django
from django.conf import settings

import os
import shutil

from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from .service import saveFile

from functools import wraps




#________________________________________________________ VALIDATION TESTING_____________________________________________________________________________#

#____________________________________________#
#__________HigherOrder decorators____________#
#____________________________________________#
def testLogger(func):
    @wraps(func)
    def wrapper (*args, **kwargs):

        print(f"Running function {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished Running {func.__name__} || RESULTS ARE {result}")
        return result
    return wrapper







#Create new media root 
@override_settings(MEDIA_ROOT = "test_media")
class userTests(TestCase):
    

    #setupclass method move to setup
    

    def setUp(self):
        #create upload directory
        self.upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(self.upload_dir, exist_ok=True)

        pass

    def tearDown(self):
        #cleanup upload directoy
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)


    
    #Utlitiy
    def fileSize(self, x):
        return x * 1024 * 1024 #in megabytes
    ####

            
    #test invalid mimetype
    @testLogger
    def testMimeType(self):
        testFile = SimpleUploadedFile(name = "virus.exe", content = b"mal content", content_type = 'application/octet-stream')

        errors = []

        with self.assertRaises(ValidationError):
            saveFile(testFile, errors)





    #test File boundry
    @testLogger
    def testFileBoundry(self):
         testFile = SimpleUploadedFile(name = "test.png", content = b"x" * self.fileSize(11), content_type = 'image/png')

         errors= []

         with self.assertRaises(ValidationError):
            saveFile(testFile, errors)


    #test filename sanitatsion

    @testLogger
    def testFilename(self):

        original = "safe_name.png"

        testFile = SimpleUploadedFile(
        name=original,
        content=b"x" * (1024),  # small valid file
        content_type="image/png"
        )

        errors = []

        filename = saveFile(testFile, errors)

        self.assertTrue(filename)
        self.assertNotEqual(filename, original)