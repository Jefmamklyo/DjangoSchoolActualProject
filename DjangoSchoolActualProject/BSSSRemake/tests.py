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


    
#Utlitiy
def fileSize(x):
    return x * 1024 * 1024 #in megabytes

PNG_HEADER = b"\x89PNG\r\n\x1a\n"






@override_settings(MEDIA_ROOT="test_media")
class userTests(TestCase):

    def setUp(self):
        self.upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(self.upload_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def fileSize(self, mb):
        return mb * 1024 * 1024
    
    @testLogger  #test all valid files
    def testValidFile(self):

        testFile = SimpleUploadedFile(
            name="safe.png",
            content=PNG_HEADER + b"\x00" * 200,
            content_type="image/png"
        )

        errors = []

        filename = saveFile(testFile, errors)

        self.assertTrue(filename)


            
    @testLogger
    def testMimeType(self):

        testFile = SimpleUploadedFile(
            name="virus.exe",
            content=b"random bad data",
            content_type="application/octet-stream"
        )

        errors = []

        with self.assertRaises(ValidationError):
            saveFile(testFile, errors)




    #@testLogger
    def testFileBoundry(self):

        testFile = SimpleUploadedFile(
            name="big.png",
            content=PNG_HEADER + b"\x00" * self.fileSize(11),
            content_type="image/png"
        )

        errors = []

        with self.assertRaises(ValidationError):
            saveFile(testFile, errors)



    @testLogger
    def testFilenameSanitisation(self):

        original = "../unsafe<>name.png"

        testFile = SimpleUploadedFile(
            name=original,
            content=PNG_HEADER + b"\x00" * 200,
            content_type="image/png"
        )

        errors = []

        filename = saveFile(testFile, errors)

        self.assertTrue(filename)
        self.assertNotEqual(filename, original)
        self.assertNotIn("<", filename)
        self.assertNotIn(">", filename)
        self.assertNotIn("..", filename)



    @testLogger #final test
    def testFullPipelineSuccess(self):

        testFile = SimpleUploadedFile(
            name="final.png",
            content=PNG_HEADER + b"\x00" * 300,
            content_type="image/png"
        )

        errors = []

        filename = saveFile(testFile, errors)

        self.assertTrue(filename)