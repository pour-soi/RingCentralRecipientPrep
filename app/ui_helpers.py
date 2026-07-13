from __future__ import annotations

from core.groups import ALL_RECIPIENTS, DEFAULT_GROUP, recipient_matches_group, recipient_phone_key, valid_recipient_groups


def group_display_text(groups: list[str]) -> str:
    return " · ".join(valid_recipient_groups({"groups": groups}))


def checked_status_text(count: int) -> str:
    if count == 1:
        return "1 recipient checked"
    return f"{count} recipients checked"


def group_recipient_count(recipients: list[dict], group: str) -> int:
    if group == ALL_RECIPIENTS:
        return len(_deduped_recipients(recipients))
    return sum(1 for recipient in _deduped_recipients(recipients) if recipient_matches_group(recipient, group))


def workspace_title(group_filter: str) -> str:
    if group_filter == ALL_RECIPIENTS:
        return "All Recipients"
    return group_filter or DEFAULT_GROUP


def empty_state_message(query: str, has_recipients: bool = True) -> tuple[str, str]:
    if not has_recipients:
        return "No recipients found", "Add recipients manually, paste a list, or import a file to get started."
    if query.strip():
        return "No recipients found", "No recipients match the current search. Try different search terms or filters."
    return "No recipients found", "No recipients match the current view."


def _deduped_recipients(recipients: list[dict]) -> list[dict]:
    seen: set[str] = set()
    deduped: list[dict] = []
    for recipient in recipients:
        phone = recipient_phone_key(recipient)
        if phone and phone in seen:
            continue
        if phone:
            seen.add(phone)
        deduped.append(recipient)
    return deduped
