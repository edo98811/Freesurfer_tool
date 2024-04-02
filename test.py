import unittest
from your_module import YourClass

class TestYourClass(unittest.TestCase):
    def setUp(self):
        # Initialize any objects needed for testing
        self.your_class_instance = YourClass()

    def test_get_list_from_folder(self):
        # Define a folder name for testing
        folder_name = "test_folder"

        # Call the method you want to test
        result = self.your_class_instance.get_list_from_folder(folder_name)

        # Define the expected output
        expected_result = ['file1.txt', 'file2.txt', 'file3.txt']  # Example expected output

        # Assert that the result matches the expected output
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()