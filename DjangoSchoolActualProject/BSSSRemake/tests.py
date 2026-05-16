import os
import shutil
from functools import wraps

from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.conf import settings

from .service import saveFile


#LOGGING DECOIRATIR
def testLogger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n Executing {func.__name__}")
        result = func(*args, **kwargs)
        print(f" Finished executing {func.__name__}")
        print(result)
    return wrapper


#PNG Binary name
pngBinary = (
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00c\x00\x00\x00c\x01\x03\x00\x00\x00\xb5\xf5,\xd6\x00\x00\x00\x06PLTE\x00\x00\x00\xff\xff\xff\xa5\xd9\x9f\xdd\x00\x00\x00\x02tRNS\xff\xff\xc8\xb5\xdf\xc7\x00\x00\x00\tpHYs\x00\x00\x0b\x12\x00\x00\x0b\x12\x01\xd2\xdd~\xfc\x00\x00\x00\xf1IDAT8\x8d\xcd\xd41\x8e\xc4 \x0c\x05PG\x14\x94s\x01$\xae\x91.W\x82\x0b\x84\xe1\x02\x93+\xd1q\x8dH\\ \xee(P<\x1e\xcd\xeef\x1b\xe2h\x8b\xd5\xb8\xe2u\xfe6\x00\xf4\xbb\xe0\x83\xb5\x01\xcc\x93\t\t\x06IH-$\xb5d>HJ\xc6is\xcb\xe0/h\x86\x82\xd7\x14\xf2z\xbb"j\xf3D\xf1\xe8\xac+\xce\xe7\xb3\xf1G\xda\xae\xb86\xad\xe21\xc1\xae6\rCj\xa0[\x90\x84\xb9\xc4DwX\xbd\xa4\x1d\xb8k\x9eDAID\n+-\xd5FQ\x95\x93\xd9\x07\xd0"i\x9f\xcacTD_\xbd\x9c\x08+\xcc\xa3q\xd0\x06I\xbb.<\x8c\xc0)%aZal\x0e\x14I\xe2\xc2\xd4<YQ\xbc[7\x95\x98\x7f6\xdd\x15\xdf\x177R$\x8b\xa2\x92\xf1\xd9npI\xa1\xf2*\xbe3\x9c\xca\xd7\xd7\x1d\xf4\xa2\x88\xc3\xf1c}o\xecL\xaf|\xbc\x84z\xa4\xed\xe9\xbf\x7f\xa2\xbf\xe9\t\xb2\xe0\xbc\x1a\xa1l|\xbb\x00\x00\x00\x00IEND\xaeB`\x82'
)


@override_settings(MEDIA_ROOT="test_media")
class userTests(TestCase):

    def setUp(self):
        self.upload_dir = os.path.join(settings.MEDIA_ROOT, "test_media")
        os.makedirs(self.upload_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def fileSize(self, mb):
        return mb * 1024 * 1024


    @testLogger
    def testValidFile(self):

        testFile = SimpleUploadedFile(name="test.png",content=pngBinary)

        errors = []

        filename = saveFile(testFile, errors)

        self.assertTrue(filename)



    @testLogger
    def testMimeType(self):

        testFile = SimpleUploadedFile(name="virus.exe",content=b"scary virus")

        errors = []

        with self.assertRaises(ValidationError):
            saveFile(testFile, errors)


    @testLogger
    def testFileBoundary(self):

        testFile = SimpleUploadedFile(name="big.png", content=pngBinary + b"x" * self.fileSize(11))

        errors = []

        with self.assertRaises(ValidationError):
            saveFile(testFile, errors)


    @testLogger
    def testFilenameSanitisation(self):

        original = "../unsafe<>name.png"

        testFile = SimpleUploadedFile(name=original,content=pngBinary)

        errors = []

        filename = saveFile(testFile, errors)

        self.assertTrue(filename)
        self.assertNotEqual(filename, original)
        self.assertNotIn("<", filename)
        self.assertNotIn(">", filename)
        self.assertNotIn("..", filename)

        return(filename)


