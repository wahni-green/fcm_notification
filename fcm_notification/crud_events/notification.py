# Copyright (c) 2026, Wahni IT Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import frappe

from frappe.utils import strip_html

from fcm_notification.firebase import send_notification


def send_mobile_notification(doc, method=None):
    doctype_list = frappe.db.get_all(
        "Notification Config", {}, ["ref_doctype"], pluck="ref_doctype"
    )

    data = {
        "title": "",
        "body": "",
        "token": "",
        "method": "TOKEN"
    }
    if doc.doctype == "Notification Log" and (not doc.from_fcm):
        fcm_token = frappe.db.get_value("User", doc.for_user, "fcm_token")
        if not fcm_token:
            return

        data.update({
            "title": strip_html(str(doc.subject)),
            "body": strip_html(str(doc.email_content)),
            "token": fcm_token
        })
    elif doc.doctype in doctype_list:
        settings = frappe.get_doc("Notification Config", doc.doctype)
        if not settings.send_notification:
            return

        user_id = frappe.db.get_value(
            "Employee", doc.get(settings.employee_ref_field), "user_id"
        )
        if not user_id:
            return

        user = frappe.db.get_value(
            "User", user_id, ["name", "fcm_token"], as_dict=True
        )
        if not user.get("fcm_token"):
            return

        dict_doc = doc.as_dict()
        data.update({
            "title": frappe.render_template(settings.notification_title, dict_doc),
            "body": frappe.render_template(settings.notification_content, dict_doc),
            "token": user.get("fcm_token")
        })

        n_log_data = {
            "subject": frappe.render_template(settings.notification_title, dict_doc),
            "email_content": frappe.render_template(settings.notification_content, dict_doc),
            "for_user": user.get("name"),
            "from_user": doc.modified_by,
            "type": "Alert",
            "document_type": doc.doctype,
            "document_name": doc.name,
            "from_fcm": 1
        }
        n_log = frappe.new_doc("Notification Log")
        n_log.update(n_log_data)
        n_log.insert(ignore_permissions=True)
    else:
        return

    send_notification(data)