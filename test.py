#!/usr/bin/env python

import unittest
import subprocess

PROGRAM_PATH = "bin/53split"
TEST_STR = "Output all lines of STDIN with 1 or more occurance of SUBSTRING.\n"

class Tests(unittest.TestCase):

    def r(self, args, input_data=None):
        cmd = [PROGRAM_PATH] + args
        result = subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            check=False
        )

        return result

    def test_stdout(self):
        result = self.r(["blah"])
        self.assertEqual(result.returncode, 1)
        self.assertIn(TEST_STR, result.stderr)

    def test_multipleSubstring(self):
        s = "hihellohihihihellohellohihelloHello"
        result = self.r(["-N", "hello", "-s"], s)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "hiHELLOhihihiHELLOHELLOhiHELLOHello")
        self.assertEqual(result.stderr, "4\n")

    def test_lengthTrailingNewLine1(self):
        s = "123456789"
        result = self.r(["-L", "3"], s)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "123\n456\n789\n")
        self.assertEqual(result.stderr, "")

    def test_lengthTrailingNewLine2(self):
        s = "12345678910"
        result = self.r(["-L", "3"], s)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "123\n456\n789\n10\n")
        self.assertEqual(result.stderr, "")

    def test_lengthTrailingNoNewLine(self):
        s = "123456789"
        result = self.r(["-L", "3", "-w"], s)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "123\n456\n789")
        self.assertEqual(result.stderr, "")

    def test_lengthTrailingNoNewLine(self):
        s = "12345678910"
        result = self.r(["-L", "3", "-w"], s)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "123\n456\n789\n10")
        self.assertEqual(result.stderr, "")

    def test_trailingSpace(self):
        s = "12345 "
        result = self.r(["-L", "3", "-w"], s)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "123\n45 ")
        self.assertEqual(result.stderr, "")

    def test_trailingSpaceAndLeadingNewLines(self):
        s = "\n\n\n12345 "
        result = self.r(["-L", "3", "-w"], s)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "123\n45 ")
        self.assertEqual(result.stderr, "")

    def test_errorPriority(self):
        result = self.r(["-Q", "{", "}o"], None)
        self.assertEqual(result.returncode, 1)
        self.assertIn(TEST_STR, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_trailingnewlinesC(self):
        s = "\n\n\r\r\f\f  \v\v\t\thel\nl o"
        result = self.r(["-C", "l", "-w"], s)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.stdout, "hel\nl\no")


if __name__ == "__main__":
    with open('./rsrc/test1.txt', "w") as file:
        file.write("\n\n\r\r\f\f  \v\v\t\thel\nl o")
    
    unittest.main()

    
        



