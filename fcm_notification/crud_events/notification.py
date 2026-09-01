# Copyright (c) 2026, Wahni IT Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import strip_html
from fcm_notification.firebase import send_notification


def send_mobile_notification(doc, method=None):
    if doc.from_fcm:
        return
    
    fcm_token = frappe.db.get_value("User", doc.for_user, "fcm_token")
    if not fcm_token:
        return

    # FCM data payloads must be flat string->string maps, so only stamp a
    # reference when both halves are set — lets clients (e.g. the mobile app)
    # deep-link a tapped notification to the doc it's about.
    data = {}
    if doc.document_type and doc.document_name:
        data["reference_doctype"] = doc.document_type
        data["reference_name"] = doc.document_name

    send_notification(
        {
            "title": strip_html(doc.subject or ""),
            "body": strip_html(doc.email_content or ""),
            "token": fcm_token,
            "method": "TOKEN",
            "data": data or None,
        }
    )
