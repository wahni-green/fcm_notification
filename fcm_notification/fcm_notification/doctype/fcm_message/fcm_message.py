# Copyright (c) 2025, Wahni IT Solutions and contributors
# For license information, please see license.txt

# import frappe
import json
from frappe.utils import now
from frappe.model.document import Document
from fcm_notification.utils import FCMNotification


class FCMMessage(Document):
	def validate(self):
		self.notification_time = now()

	def before_submit(self):
		message = json.loads(self.message)
		fcm = FCMNotification()
		self.response = fcm.send_topic_message(self.topic, message)
