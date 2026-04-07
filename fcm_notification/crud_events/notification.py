# Copyright (c) 2026, Wahni IT Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import frappe

from frappe.utils import strip_html

from fcm_notification.firebase import send_notification


def send_mobile_notification(doc, method=None):
    data = {
        "title": "",
        "body": "",
        "token": "",
        "method": "TOKEN"
    }
    fcm_token = frappe.db.get_value("User", doc.for_user, "fcm_token")
    if not fcm_token:
        return

    data.update({
        "title": strip_html(str(doc.subject)),
        "body": strip_html(str(doc.email_content)),
        "token": fcm_token
    })

    send_notification(data)
