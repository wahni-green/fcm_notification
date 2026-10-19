# Copyright (c) 2026, Wahni IT Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import strip_html
from fcm_notification.firebase import send_notification


def send_mobile_notification(doc, method=None):
    if doc.from_fcm:
        return

    tokens = frappe.get_all(
        "FCM User", filters={"user": doc.for_user}, pluck="registration_token"
    )
    if not tokens:
        return

    # FCM data payloads must be flat string->string maps, so only stamp a
    # reference when both halves are set — lets clients (e.g. the mobile app)
    # deep-link a tapped notification to the doc it's about.
    data = {}
    if doc.document_type and doc.document_name:
        data["reference_doctype"] = doc.document_type
        data["reference_name"] = doc.document_name

    # Callers that insert a Notification Log in-process can set
    # `doc.flags.fcm_extra` to tailor the push: `android_channel` (notification
    # channel, i.e. sound), `ios_sound` (sound file bundled with the app) and
    # `route` (in-app route to open on tap, overriding the reference mapping).
    extra = doc.flags.get("fcm_extra") or {}
    for key in ("android_channel", "route"):
        if extra.get(key):
            data[key] = extra[key]

    # Also sent in `data` (not just the APNs sound) so the app can honor it
    # when it displays the push itself while open. "" means silent.
    if extra.get("ios_sound") is not None:
        data["ios_sound"] = extra["ios_sound"]

    for token in tokens:
        result = send_notification(
            {
                "title": strip_html(doc.subject or ""),
                "body": strip_html(doc.email_content or ""),
                "token": token,
                "method": "TOKEN",
                "data": data or None,
                "ios_sound": extra.get("ios_sound"),
            }
        )
        if isinstance(result, dict) and result.get("error") == "unregistered":
            frappe.db.delete("FCM User", {"registration_token": token})
