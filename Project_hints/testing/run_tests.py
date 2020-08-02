import unittest
import simple_functions


class Part1Tests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.maxDiff = None
    
    def test_function_1_correct_output(self):
        result_output = simple_functions.function_1()
        expected_output = "Output for function 1."
        self.assertEqual(result_output, expected_output)
    
    def test_function_2_correct_output(self):
        result_output = simple_functions.function_2()
        expected_output = "Correct output for function 2."
        self.assertEqual(result_output, expected_output)
    
    def test_function_3_correct_output_1(self):
        result_output = simple_functions.function_3(3)
        expected_output = "x = 3"
        self.assertEqual(result_output, expected_output)
    
    def test_function_3_correct_output_2(self):
        result_output = simple_functions.function_3("9.00")
        expected_output = "x = 9.00"
        self.assertEqual(result_output, expected_output)
    
    def test_function_4_correct_output_1(self):
        result_output = simple_functions.function_4(3, 5)
        expected_output = 8
        self.assertEqual(result_output, expected_output)

    def test_function_4_correct_output_2(self):
        result_output = simple_functions.function_4("-1", "0")
        expected_output = -1
        self.assertEqual(result_output, expected_output)

    def test_function_4_correct_output_3(self):
        result_output = simple_functions.function_4(9.00, "3.2")
        expected_output = 12.2
        self.assertEqual(result_output, expected_output)


runner = unittest.TextTestRunner()
print('Running Tests...\n')
runner.run(unittest.TestSuite((unittest.makeSuite(Part1Tests))))
