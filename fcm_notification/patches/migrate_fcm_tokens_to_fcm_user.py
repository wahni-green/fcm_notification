# Copyright (c) 2026, Wahni IT Solutions and contributors
# For license information, please see license.txt


import frappe


def execute():
    users_with_tokens = frappe.get_all(
        "User",
        filters={"fcm_token": ["is", "set"]},
        fields=["name", "fcm_token"],
    )

    for row in users_with_tokens:
        if frappe.db.exists("FCM User", {"registration_token": row.fcm_token}):
            continue

        frappe.get_doc(
            {
                "doctype": "FCM User",
                "user": row.name,
                "registration_token": row.fcm_token,
            }
        ).insert(ignore_permissions=True)

    frappe.delete_doc("Custom Field", "User-fcm_token", ignore_missing=True)
