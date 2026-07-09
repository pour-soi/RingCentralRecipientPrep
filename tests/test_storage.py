import unittest

from app.storage import APP_FOLDER


class StorageTests(unittest.TestCase):
    def test_primary_data_folder_uses_poursend_branding(self):
        self.assertEqual(APP_FOLDER, "poursend_data")


if __name__ == "__main__":
    unittest.main()
