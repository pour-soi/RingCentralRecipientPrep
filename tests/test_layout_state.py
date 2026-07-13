import os
import unittest
from typing import Optional
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QLabel

from app.main import LayoutMetrics, MainWindow
from core.groups import DEFAULT_GROUP


def app() -> QApplication:
    return QApplication.instance() or QApplication([])


def recipient(phone: str, selected: bool = False) -> dict:
    return {"phone": phone, "groups": [DEFAULT_GROUP], "notes": "", "selected": selected}


class LayoutStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app()

    def make_window(self, recipients: Optional[list[dict]] = None) -> MainWindow:
        with patch("app.main.load_recipient_data", return_value=([], [DEFAULT_GROUP], {}, None)):
            window = MainWindow()
        window.recipients = recipients or []
        window.groups = [DEFAULT_GROUP]
        window.refresh_group_list()
        window.refresh_table()
        return window

    def test_empty_database_shows_centered_empty_state_actions(self):
        window = self.make_window([])
        self.addCleanup(window.close)

        self.assertIs(window.table_stack.currentWidget(), window.empty_state)
        self.assertFalse(window.empty_actions.isHidden())
        self.assertTrue(window.action_bar.isHidden())

    def test_brand_logo_loads_in_header(self):
        window = self.make_window([])
        self.addCleanup(window.close)

        app_icon = window.findChild(QLabel, "AppIcon")
        self.assertIsNotNone(app_icon)
        self.assertIsNotNone(app_icon.pixmap())
        self.assertFalse(app_icon.pixmap().isNull())

    def test_populated_table_shows_action_bar_without_bulk_actions_until_checked(self):
        window = self.make_window([recipient("+14151111111"), recipient("+16282222222")])
        self.addCleanup(window.close)

        self.assertIs(window.table_stack.currentWidget(), window.table)
        self.assertFalse(window.action_bar.isHidden())
        self.assertTrue(window.bulk_actions.isHidden())
        self.assertTrue(all(button.isEnabled() for button in window.table_action_buttons))

    def test_checked_recipient_enables_bulk_action_row(self):
        window = self.make_window([recipient("+14151111111", selected=True), recipient("+16282222222")])
        self.addCleanup(window.close)

        self.assertFalse(window.action_bar.isHidden())
        self.assertFalse(window.bulk_actions.isHidden())
        self.assertEqual(window.bulk_count_label.text(), "1 recipient checked")

    def test_search_empty_hides_database_empty_actions(self):
        window = self.make_window([recipient("+14151111111")])
        self.addCleanup(window.close)
        window.search.setText("no-match")
        window.refresh_table()

        self.assertIs(window.table_stack.currentWidget(), window.empty_state)
        self.assertTrue(window.empty_actions.isHidden())
        self.assertTrue(window.action_bar.isHidden())

    def test_filter_toolbar_uses_responsive_column_counts(self):
        window = self.make_window([recipient("+14151111111")])
        self.addCleanup(window.close)

        window.resize(1600, 900)
        window.arrange_filter_toolbar()
        self.assertEqual(window.filter_bar_columns, LayoutMetrics.FILTER_COLUMNS_WIDE)

        window.resize(1280, 720)
        window.arrange_filter_toolbar()
        self.assertEqual(window.filter_bar_columns, LayoutMetrics.FILTER_COLUMNS_MEDIUM)


if __name__ == "__main__":
    unittest.main()
