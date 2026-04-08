# Copyright (c) 2026, Wahni IT Solutions and contributors
# For license information, please see license.txt

import frappe

def after_install():
    print("Creating custom fields for fcm_notification...")
    create_custom_fields()

def create_custom_fields():
    from fcm_notification.patches.create_custom_fields import execute as create_fcm_fields
    create_fcm_fields()