	# Copyright (c) 2026, Wahni IT Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import os
import frappe
import firebase_admin

from frappe.utils import get_datetime_in_timezone, add_to_date

from firebase_admin import messaging, credentials


def send_notification(data):
	if not firebase_admin._apps:
		relative_path = frappe.db.get_single_value(
			"FCM Settings", "service_account_json"
		)
		full_path = os.path.join(frappe.get_site_path(), relative_path.strip("/"))

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
	except Exception as e:
		frappe.log_error(message=str(frappe.get_traceback()), title="FCM Error")
		return {"success": False, "message": str(e)}