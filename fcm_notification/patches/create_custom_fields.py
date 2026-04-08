# Copyright (c) 2026, Wahni IT Solutions and contributors
# For license information, please see license.txt


from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    create_custom_fields(
        {
            "User": [
                {
                    "fieldname": "fcm_token",
                    "fieldtype": "Small Text",
                    "label": "FCM Token",
                    "insert_after": "username",
                    "read_only": 1,
                },
            ],
            "Role": [
                {
                    "fieldname": "is_fcm_role",
                    "fieldtype": "Check",
                    "label": "Is FCM Role",
                    "insert_after": "two_factor_auth",
                },
            ]
        }
    )
