# Copyright (c) 2026, Wahni IT Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import strip_html
from fcm_notification.firebase import send_notification


def send_mobile_notification(doc, method=None):
    if doc.from_fcm:
        return

    tokens = frappe.get_all(
        "FCM User", filters={"user": doc.for_user}, pluck="registration_token"
    )
    if not tokens:
        return

    # FCM data payloads must be flat string->string maps, so only stamp a
    # reference when both halves are set — lets clients (e.g. the mobile app)
    # deep-link a tapped notification to the doc it's about.
    data = {}
    if doc.document_type and doc.document_name:
        data["reference_doctype"] = doc.document_type
        data["reference_name"] = doc.document_name

    for token in tokens:
        result = send_notification(
            {
                "title": strip_html(doc.subject or ""),
                "body": strip_html(doc.email_content or ""),
                "token": token,
                "method": "TOKEN",
                "data": data or None,
            }
        )
        if isinstance(result, dict) and result.get("error") == "unregistered":
            frappe.db.delete("FCM User", {"registration_token": token})
