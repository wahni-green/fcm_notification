# Copyright (c) 2026, Wahni IT Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import os
import frappe
import firebase_admin
from frappe.utils import get_datetime_in_timezone, add_to_date
from firebase_admin import messaging, credentials
from firebase_admin.messaging import UnregisteredError

def send_notification(data):
	if not frappe.get_single_value("FCM Settings", "enabled"):
		return

	if not firebase_admin._apps:
		relative_path = frappe.db.get_single_value(
			"FCM Settings", "service_account_json"
		)

		if not relative_path:
			frappe.throw("FCM Settings: Service Account JSON is not configured")

		file_doc = frappe.get_doc("File", {"file_url": relative_path})

		if not file_doc.is_private:
			frappe.throw("FCM Service Account file must be private")

		full_path = file_doc.get_full_path()

		cred = credentials.Certificate(full_path)

		firebase_admin.initialize_app(cred)

	apns_expiration = str(int(add_to_date(get_datetime_in_timezone("UTC"), days=1).timestamp()))
	message = messaging.Message(
		notification=messaging.Notification(
			title=data.get("title") or None,
			body=data.get("body") or None,
		),
		apns=messaging.APNSConfig(
			headers={
				"apns-expiration": apns_expiration
			}
		),
		android=messaging.AndroidConfig(ttl=86400),
		data=data.get("data") or None,
		token=data.get("token") if data.get("method") == "TOKEN" else None,
		topic=data.get("topic") if data.get("method") == "TOPIC" else None,
	)

	try:
		messaging.send(message)
	except UnregisteredError as e:
		# The device uninstalled the app or its token rotated — not worth
		# logging as an error, and the caller should stop retrying it.
		return {"success": False, "error": "unregistered", "message": str(e)}
	except Exception as e:
		frappe.log_error(message=str(frappe.get_traceback()), title="FCM Error")
		return {"success": False, "message": str(e)}