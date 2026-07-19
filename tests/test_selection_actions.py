import os
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox

from app.main import MainWindow, RecipientTableDelegate
from app.storage import make_saved_data, parse_saved_data
from core.groups import DEFAULT_GROUP, checked_recipient_indexes


def app() -> QApplication:
    return QApplication.instance() or QApplication([])


def recipient(phone: str, group: str = DEFAULT_GROUP, selected: bool = False) -> dict:
    return {"phone": phone, "group": group, "groups": [group], "notes": "", "selected": selected}


class SelectionActionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app()

    def make_window(self) -> MainWindow:
        with patch("app.main.load_recipient_data", return_value=([], [DEFAULT_GROUP], {}, None)):
            window = MainWindow()
        window.recipients = [
            recipient("+14151111111", "Caregivers"),
            recipient("+16282222222", "Caregivers"),
            recipient("+17073333333", "Follow-up"),
        ]
        window.groups = [DEFAULT_GROUP, "Caregivers", "Follow-up"]
        window.settings = {}
        window.save_and_update = lambda selected_group=None: (
            window.refresh_group_list(selected_group),
            window.refresh_table(),
        )
        window.refresh_group_list()
        window.refresh_table()
        return window

    def select_group(self, window: MainWindow, group: str) -> None:
        for row in range(window.group_list.count()):
            if window.group_list.item(row).data(Qt.UserRole) == group:
                window.group_list.setCurrentRow(row)
                window.refresh_table()
                return
        raise AssertionError(f"group not found: {group}")

    def test_checkbox_delegate_toggles_integer_checked_state_off(self):
        class Event:
            def type(self):
                return QEvent.MouseButtonRelease

        class Index:
            def column(self):
                return 0

            def data(self, _role):
                return Qt.Checked.value

        class Model:
            def __init__(self):
                self.value = None

            def setData(self, _index, value, role):
                self.value = (value, role)

        model = Model()
        handled = RecipientTableDelegate().editorEvent(Event(), model, None, Index())

        self.assertTrue(handled)
        self.assertEqual(model.value, (Qt.Unchecked, Qt.CheckStateRole))

    def test_checkbox_toggles_on_and_off(self):
        window = self.make_window()
        self.addCleanup(window.close)
        item = window.table.item(0, 0)

        item.setCheckState(Qt.Checked)
        self.assertTrue(window.recipients[0]["selected"])

        item = window.table.item(0, 0)
        item.setCheckState(Qt.Unchecked)
        self.assertFalse(window.recipients[0]["selected"])

        item = window.table.item(0, 0)
        item.setCheckState(Qt.Checked)
        self.assertTrue(window.recipients[0]["selected"])

        item = window.table.item(0, 0)
        item.setCheckState(Qt.Unchecked)
        self.assertFalse(window.recipients[0]["selected"])

    def test_selection_survives_list_refresh(self):
        window = self.make_window()
        self.addCleanup(window.close)
        window.table.item(1, 0).setCheckState(Qt.Checked)

        window.refresh_table()

        self.assertTrue(window.recipients[1]["selected"])
        self.assertEqual(window.table.item(1, 0).checkState(), Qt.Checked)

    def test_delete_uses_checked_rows_without_highlighted_row(self):
        window = self.make_window()
        self.addCleanup(window.close)
        window.recipients[0]["selected"] = True
        window.recipients[2]["selected"] = True
        window.refresh_table()
        window.table.clearSelection()

        with patch("app.main.DeleteConfirmationDialog") as confirmation:
            confirmation.Accepted = QDialog.Accepted
            confirmation.return_value.exec.return_value = QDialog.Accepted
            window.delete_selected()

        confirmation.assert_called_once_with(2, window)
        self.assertEqual([recipient["phone"] for recipient in window.recipients], ["+16282222222"])
        self.assertEqual(checked_recipient_indexes(window.recipients), [])

    def test_delete_ignores_highlighted_unchecked_rows(self):
        window = self.make_window()
        self.addCleanup(window.close)
        window.table.selectRow(0)

        with patch("app.main.QMessageBox.information") as information, patch("app.main.DeleteConfirmationDialog") as confirmation:
            window.delete_selected()

        information.assert_called_once()
        self.assertEqual(information.call_args.args[2], "No recipients are checked. Select one or more recipients in the Select column, then try again.")
        confirmation.assert_not_called()
        self.assertEqual([recipient["phone"] for recipient in window.recipients], ["+14151111111", "+16282222222", "+17073333333"])

    def test_single_recipient_deletion_uses_highlighted_row(self):
        window = self.make_window()
        self.addCleanup(window.close)
        window.recipients[2]["selected"] = True
        window.refresh_table()
        window.table.selectRow(1)

        with patch("app.main.QMessageBox.question", return_value=QMessageBox.Yes):
            window.delete_highlighted_recipient()

        self.assertEqual([recipient["phone"] for recipient in window.recipients], ["+14151111111", "+17073333333"])
        self.assertTrue(window.recipients[1]["selected"])

    def test_canceling_single_recipient_deletion_leaves_data_unchanged(self):
        window = self.make_window()
        self.addCleanup(window.close)
        window.table.selectRow(0)
        before = [dict(recipient) for recipient in window.recipients]

        with patch("app.main.QMessageBox.question", return_value=QMessageBox.No):
            window.delete_highlighted_recipient()

        self.assertEqual(window.recipients, before)

    def test_select_all_affects_only_visible_recipients(self):
        window = self.make_window()
        self.addCleanup(window.close)
        self.select_group(window, "Caregivers")

        window.set_all_visible(True)

        self.assertTrue(window.recipients[0]["selected"])
        self.assertTrue(window.recipients[1]["selected"])
        self.assertFalse(window.recipients[2]["selected"])

    def test_clear_selection_affects_only_visible_recipients(self):
        window = self.make_window()
        self.addCleanup(window.close)
        for recipient in window.recipients:
            recipient["selected"] = True
        self.select_group(window, "Caregivers")

        window.set_all_visible(False)

        self.assertFalse(window.recipients[0]["selected"])
        self.assertFalse(window.recipients[1]["selected"])
        self.assertTrue(window.recipients[2]["selected"])

    def test_search_filtered_select_all(self):
        window = self.make_window()
        self.addCleanup(window.close)
        window.search.setText("628")

        window.set_all_visible(True)

        self.assertFalse(window.recipients[0]["selected"])
        self.assertTrue(window.recipients[1]["selected"])
        self.assertFalse(window.recipients[2]["selected"])

    def test_delete_selected_deletes_only_checked_recipients(self):
        window = self.make_window()
        self.addCleanup(window.close)
        window.recipients[0]["selected"] = True
        window.recipients[2]["selected"] = True
        window.refresh_table()

        with patch("app.main.DeleteConfirmationDialog") as confirmation:
            confirmation.Accepted = QDialog.Accepted
            confirmation.return_value.exec.return_value = QDialog.Accepted
            window.delete_selected()

        self.assertEqual([recipient["phone"] for recipient in window.recipients], ["+16282222222"])
        self.assertFalse(window.recipients[0]["selected"])

    def test_delete_key_deletes_highlighted_recipient(self):
        window = self.make_window()
        self.addCleanup(window.close)
        window.table.setFocus()
        window.table.selectRow(0)
        event = QKeyEvent(QEvent.KeyPress, Qt.Key_Delete, Qt.NoModifier)

        with patch.object(window, "recipient_table_has_focus", return_value=True), patch("app.main.QMessageBox.question", return_value=QMessageBox.Yes):
            handled = window.eventFilter(window.table, event)

        self.assertTrue(handled)
        self.assertEqual([recipient["phone"] for recipient in window.recipients], ["+16282222222", "+17073333333"])

    def test_ctrl_a_is_not_intercepted_in_search_field(self):
        window = self.make_window()
        self.addCleanup(window.close)
        window.search.setFocus()
        event = QKeyEvent(QEvent.KeyPress, Qt.Key_A, Qt.ControlModifier)

        handled = window.eventFilter(window.search, event)

        self.assertFalse(handled)
        self.assertEqual(checked_recipient_indexes(window.recipients), [])

    def test_action_states_follow_highlight_checks_search_group_and_deletion(self):
        window = self.make_window()
        self.addCleanup(window.close)

        self.assertFalse(window.menu_edit_action.isEnabled())
        self.assertFalse(window.menu_delete_recipient_action.isEnabled())
        self.assertFalse(window.menu_delete_selected_action.isEnabled())
        self.assertTrue(window.menu_select_all_action.isEnabled())
        self.assertFalse(window.menu_clear_selection_action.isEnabled())

        window.table.selectRow(0)
        self.app.processEvents()
        self.assertTrue(window.menu_edit_action.isEnabled())
        self.assertTrue(window.menu_delete_recipient_action.isEnabled())

        window.table.item(0, 0).setCheckState(Qt.Checked)
        self.app.processEvents()
        self.assertTrue(window.menu_delete_selected_action.isEnabled())
        self.assertTrue(window.menu_clear_selection_action.isEnabled())
        self.assertFalse(window.menu_edit_action.isEnabled())

        window.search.setText("707")
        self.app.processEvents()
        self.assertTrue(window.menu_select_all_action.isEnabled())
        self.assertFalse(window.menu_clear_selection_action.isEnabled())
        self.assertTrue(window.menu_delete_selected_action.isEnabled())

        window.search.clear()
        self.select_group(window, "Follow-up")
        self.app.processEvents()
        self.assertFalse(window.menu_clear_selection_action.isEnabled())
        self.assertTrue(window.menu_delete_selected_action.isEnabled())
        self.assertFalse(window.menu_edit_action.isEnabled())

        with patch("app.main.DeleteConfirmationDialog") as confirmation:
            confirmation.Accepted = QDialog.Accepted
            confirmation.return_value.exec.return_value = QDialog.Accepted
            window.delete_selected()

        self.assertFalse(window.menu_delete_selected_action.isEnabled())
        self.assertFalse(window.menu_clear_selection_action.isEnabled())

    def test_search_clears_highlight_but_preserves_checked_recipients_for_deletion(self):
        window = self.make_window()
        self.addCleanup(window.close)

        window.table.selectRow(0)
        self.assertEqual(window.selected_visible_index(), 0)

        window.table.item(1, 0).setCheckState(Qt.Checked)
        window.table.item(2, 0).setCheckState(Qt.Checked)
        self.app.processEvents()
        self.assertEqual(checked_recipient_indexes(window.recipients), [1, 2])

        window.search.setText("628")
        self.app.processEvents()
        self.assertIsNone(window.selected_visible_index())
        self.assertEqual(checked_recipient_indexes(window.recipients), [1, 2])

        window.search.clear()
        self.app.processEvents()
        self.assertIsNone(window.selected_visible_index())
        self.assertFalse(window.menu_edit_action.isEnabled())
        self.assertFalse(window.menu_delete_recipient_action.isEnabled())
        self.assertTrue(window.menu_delete_selected_action.isEnabled())

        with patch("app.main.DeleteConfirmationDialog") as confirmation:
            confirmation.Accepted = QDialog.Accepted
            confirmation.return_value.exec.return_value = QDialog.Accepted
            window.delete_selected()

        self.assertEqual([recipient["phone"] for recipient in window.recipients], ["+14151111111"])
        self.assertIsNone(window.selected_visible_index())

    def test_empty_state_after_deleting_last_recipient(self):
        window = self.make_window()
        self.addCleanup(window.close)
        window.recipients = [recipient("+14151111111")]
        window.refresh_group_list()
        window.refresh_table()
        window.table.selectRow(0)

        with patch("app.main.QMessageBox.question", return_value=QMessageBox.Yes):
            window.delete_highlighted_recipient()

        self.assertEqual(window.recipients, [])
        self.assertEqual(window.table_stack.currentWidget(), window.empty_state)
        self.assertEqual(window.workspace_meta.text(), "0 recipients")

    def test_deletion_persists_after_reload_through_save_path(self):
        saved = {}

        def fake_save(recipients, groups, settings):
            saved["recipients"] = [dict(recipient) for recipient in recipients]
            saved["groups"] = list(groups)
            saved["settings"] = dict(settings)
            return None

        window = self.make_window()
        self.addCleanup(window.close)
        window.save_and_update = MainWindow.save_and_update.__get__(window, MainWindow)
        window.table.selectRow(0)

        with patch("app.main.save_recipient_data", side_effect=fake_save), patch("app.main.QMessageBox.question", return_value=QMessageBox.Yes):
            window.delete_highlighted_recipient()

        self.assertEqual([recipient["phone"] for recipient in saved["recipients"]], ["+16282222222", "+17073333333"])
        reloaded_recipients, _groups = parse_saved_data(make_saved_data(saved["recipients"], saved["groups"], saved["settings"]))
        self.assertEqual([recipient["phone"] for recipient in reloaded_recipients], ["+16282222222", "+17073333333"])


if __name__ == "__main__":
    unittest.main()
