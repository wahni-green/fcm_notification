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
