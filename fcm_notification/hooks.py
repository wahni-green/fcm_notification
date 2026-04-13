app_name = "fcm_notification"
app_title = "FCM Notification"
app_publisher = "Wahni IT Solutions"
app_description = "Firebase Cloud Messaging notification for Frappe"
app_email = "danyrt@wahni.com"
app_license = "agpl-3.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "fcm_notification",
# 		"logo": "/assets/fcm_notification/logo.png",
# 		"title": "FCM Notification",
# 		"route": "/fcm_notification",
# 		"has_permission": "fcm_notification.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/fcm_notification/css/fcm_notification.css"
# app_include_js = "/assets/fcm_notification/js/fcm_notification.js"

# include js, css files in header of web template
# web_include_css = "/assets/fcm_notification/css/fcm_notification.css"
# web_include_js = "/assets/fcm_notification/js/fcm_notification.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "fcm_notification/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "fcm_notification/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "fcm_notification.utils.jinja_methods",
# 	"filters": "fcm_notification.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "fcm_notification.install.before_install"
after_install = "fcm_notification.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "fcm_notification.uninstall.before_uninstall"
# after_uninstall = "fcm_notification.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "fcm_notification.utils.before_app_install"
# after_app_install = "fcm_notification.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "fcm_notification.utils.before_app_uninstall"
# after_app_uninstall = "fcm_notification.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "fcm_notification.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Notification Log": {
        "after_insert": "fcm_notification.crud_events.notification.send_mobile_notification",
    },
    "ToDo": {
		"after_insert": "fcm_notification.crud_events.todo.todo_after_insert",
		"on_update": "fcm_notification.crud_events.todo.todo_on_update",
	}
}


# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"fcm_notification.tasks.all"
# 	],
# 	"daily": [
# 		"fcm_notification.tasks.daily"
# 	],
# 	"hourly": [
# 		"fcm_notification.tasks.hourly"
# 	],
# 	"weekly": [
# 		"fcm_notification.tasks.weekly"
# 	],
# 	"monthly": [
# 		"fcm_notification.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "fcm_notification.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "fcm_notification.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "fcm_notification.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["fcm_notification.utils.before_request"]
# after_request = ["fcm_notification.utils.after_request"]

# Job Events
# ----------
# before_job = ["fcm_notification.utils.before_job"]
# after_job = ["fcm_notification.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"fcm_notification.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
