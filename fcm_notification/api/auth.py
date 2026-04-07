# Copyright (c) 2026, Wahni IT Solutions and contributors
# For license information, please see license.txt

import base64

import frappe
from frappe.utils import flt
from fcm_notification.api.utils import daily_expense_claim_reminder
from frappe.utils.password import get_decrypted_password


@frappe.whitelist(allow_guest=True, methods=["POST"])
def login(username, password, fcm_token, device_id=None):
	try:
		if device_id and frappe.db.get_single_value('FCM Settings', 'device_id_validation'):
			if user_device_id := frappe.get_value(
				"User", 
				username,
				"device_id",
			):
				if device_id != user_device_id:
					frappe.local.response["status_code"] = 400
					return {"success": False, "message": "Device ID not matching"}
		try:
			login_manager = frappe.auth.LoginManager()
			login_manager.authenticate(user=username, pwd=password)
		except Exception as e:
			frappe.local.response["status_code"] = 400
			return {"success": False, "message": "Invalid username or password"}
		
		login_manager.post_login()
		employee = frappe.get_value(
			"Employee", 
			{"user_id": username},
		)
		if not employee:
			return {
				"success": False,
				"message": f"Login Failed: The user {username} is not assigned to any employee",
			}
	
		token = generate_keys(username)
		settlement_amount, advance_amount, settlement_approved = get_adv_settlment_amount(username)
		employee_details = get_employee_details(user_id=username)
		if employee_details.get("image"):
			img = frappe.get_doc("File", {"file_url": employee_details.image})
			employee_details["image"] = base64.b64encode(img.get_content()).decode()

		projects = get_projects_with_locaton().get("message", [])
		employee_details["user_type"] = frappe.get_value("User", {"email":username}, "user_role")

		# set device id in user
		frappe.db.set_value("User", username, 
			{
				"device_id": device_id,
				"fcm_token": fcm_token,
			}
		)

		return {
			"success": True,
			"token": token,
			"employee_details": employee_details,
			"message": "Logged In Successfully",
			"username": username,
			"settlement_amount": flt(settlement_amount, 2),
			"advance_amount": flt(advance_amount, 2),
			"projects": projects,
			"expense_claim_reminder": daily_expense_claim_reminder(),
		}
	except Exception as e:
		frappe.log_error(message=str(frappe.get_traceback()), title="Authentication Error")
		return {"success": False, "message": str(e)}


def generate_keys(user):
	api_secret = get_decrypted_password(
		"User", user, "api_secret", raise_exception=False
	)
	if not api_secret:
		user_details = frappe.get_doc('User', user)
		api_secret = frappe.generate_hash(length=15)

		if not user_details.api_key:
			api_key = frappe.generate_hash(length=15)
			user_details.api_key = api_key

		user_details.api_secret = api_secret
		user_details.save()
	else:
		api_key = frappe.db.get_value("User", user, "api_key")

	return base64.b64encode(
		("{}:{}".format(api_key, api_secret)).encode("utf-8")
	).decode("utf-8")
 
 
 def get_adv_settlment_amount(username=None, employee=None):
	if not username and not employee:
		frappe.throw("Username or Employee ID is required")

	if not employee:
		employee = frappe.get_value("Employee", {"user_id": username})

	if not employee:
		return 0, 0

	settlement_amount = frappe.get_all(
		"Expense Claim",
		filters={
			"employee": employee,
			"approval_status": ("!=", "Rejected"),
			"docstatus": 0
		},
		fields=["sum(total_claimed_amount)"],
		group_by="employee",
		as_list=True
	)
	settlement_amount = settlement_amount[0][0] if settlement_amount else 0

	settlement_approved = frappe.get_all(
		"Expense Claim",
		filters={
			"employee": employee,
			"approval_status": "Approved",
			"docstatus": 1
		},
		fields=["sum(total_claimed_amount)"],
		group_by="employee",
		as_list=True
	)
	settlement_approved = settlement_approved[0][0] if settlement_approved else 0

	advance_amount = frappe.get_all(
		"Employee Advance",
		filters={
			"employee": employee,
			"docstatus": 1
		},
		fields=["sum(paid_amount-claimed_amount-return_amount)"],
		group_by="employee",
		as_list=True
	)
	advance_amount = advance_amount[0][0] if advance_amount else 0
	return flt(settlement_amount, 2), flt(advance_amount, 2), flt(settlement_approved, 2)


def get_employee_details(user_id):
	emp = frappe.qb.DocType("Employee")
	edu = frappe.qb.DocType("Employee Education")
	
	emp_details = (
			frappe.qb.from_(emp)
			.select(
				emp.name,
				emp.employee,
				emp.employee_name,
				emp.gender,
				emp.date_of_birth,
				emp.date_of_joining,
				emp.status,
				emp.user_id,
				emp.company,
				emp.image,
				emp.department,
				emp.reports_to,
				emp.employment_type,
				emp.employee_number,			
				emp.health_insurance_provider,
				emp.health_insurance_no,
				emp.cell_number,
				emp.designation,
				emp.pan_number,
				emp.personal_email,
				emp.company_email,
				emp.prefered_email				
			)
			.where(emp.user_id == user_id)
	).run(as_dict = 1)	
	emp_details[0].update({"qualification" : []})
	
	qualification_list = (
			frappe.qb.from_(emp)
			.inner_join(edu)
			.on( edu.parent == emp.name )
			.select(
				edu.qualification
			)
			.where(emp.user_id == user_id)
		).run(as_dict=1)
	
	for row in qualification_list:
		emp_details[0]["qualification"].append(row["qualification"])
		
	return emp_details[0]