# Copyright (c) 2026, Wahni IT Solutions and contributors
# For license information, please see license.txt


from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    create_custom_fields(
        {
            "User": [
                {
                    "fieldname": "user_role",
                    "fieldtype": "Select",
                    "label": "User Type",
                    "options": "\nSite Engineer\nLabour",
                    "insert_after": "username",
                },
                {
                    "fieldname": "fcm_token",
                    "fieldtype": "Small Text",
                    "label": "FCM Token",
                    "insert_after": "user_role",
                    "read_only" 1,
                },
            ]
        }
    )
