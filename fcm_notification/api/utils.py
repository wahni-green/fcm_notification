# Copyright (c) 2026, Wahni IT Solutions Pvt Ltd and contributors
# For license information, please see license.txt


import frappe
from frappe.utils import (
	getdate, today
)


def log_and_structure(func):
    def wrapper(*args, **kwargs):
        cmd = kwargs.get("cmd")
        try:
            kwargs = frappe.get_newargs(func, kwargs)
            return func(*args, **kwargs)
        except frappe.exceptions.PermissionError as e:
            frappe.local.response["message"] = {
                "error": str(e),
                "log": None,
                "success": False,
            }
            raise e
        except Exception as e:
            log = frappe.log_error(
                title=f"FCM Notification Error: {cmd or func.__name__}",
                message=frappe.get_traceback(),
            )
            frappe.local.response["message"] = {
                "error": str(e),
                "log": log.name if log else None,
                "success": False,
            }
            raise e

    return wrapper


def daily_expense_claim_reminder():
    exp_settings = frappe.db.get_value(
        "HR Settings", 
        "HR Settings", 
        [
            "enable_expense_claim_reminder", 
            "expense_claim_time_period", 
            "exp_claim_reminder_email_template"
        ], 
        as_dict=1
    )

    if (
        not exp_settings.enable_expense_claim_reminder and 
        not exp_settings.expense_claim_time_period
        # not exp_settings.exp_claim_reminder_email_template
    ):
        return

    day = getdate(today()).day
    period = int(exp_settings.expense_claim_time_period)
    
    if (
        day in range(15, 15 + period) or 
        day in range(1, period)
    ):
        days_left = (15 + period) - day
        if day in range(1, period):
            days_left = (period) - day


        message = "Reminder: Please submit expense claims between the 15th-{0}th or 1st-{1}th of the month if you have any outstanding expenses. ({2} days left)".format(15 + period, period, days_left)
        return message
    
        employees = frappe.db.get_all(
            "Employee", 
            {"status":"Active", "user_id": ["is", "Set"]}, 
            ["user_id", "employee_name"]
        )
        for emp in employees:
            frappe.enqueue(
                send_reminder_email,
                recipient=emp.user_id,
                employee_name=emp.employee_name,
                email_template=exp_settings.exp_claim_reminder_email_template,
                days_left=days_left,
                queue='long'
            )
