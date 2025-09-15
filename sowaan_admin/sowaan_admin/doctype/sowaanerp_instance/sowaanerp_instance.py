# Copyright (c) 2025, Sowaan and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe import _
import requests
import json


class SowaanERPInstance(Document):
	pass

@frappe.whitelist()
def fetch_users(docname):
	doc = frappe.get_doc('SowaanERP Instance', docname)
	instance_cred = frappe.get_doc('SowaanERP Instance Credential', doc.instance)
	api_url = instance_cred.name
	api_key = instance_cred.api_key
	api_secret = instance_cred.api_secret

	headers = {
		'Authorization': f'token {api_key}:{api_secret}'
	}
	try:
		response = requests.get(f"{api_url}/api/method/sowaanerp_subscription.api.get_users", headers=headers, timeout=15)
		response.raise_for_status()
		data = response.json().get('message', {})
		if data:
			doc.users = []
			for user in data.get('users', []):
				doc.append("users", {
					"user": user.get('user'),
					"email": user.get('email'),
					"enabled": user.get('enabled'),
					"creation1": user.get('creation'),
					"roles": ', '.join(user.get('roles', [])),
				})
			doc.status = data.get('status')
			doc.valid_till = data.get('valid_till')
			doc.quota = frappe.as_json(data.get('quota'))
			doc.save(ignore_permissions=True)

		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), 'Fetch Users Error')
		frappe.throw(_('Failed to fetch users: {0}').format(str(e)))

@frappe.whitelist()
def enable_disable_users(docname, user_list, action): #action can be 'enable' or 'disable'
	doc = frappe.get_doc('SowaanERP Instance', docname)
	instance_cred = frappe.get_doc('SowaanERP Instance Credential', doc.instance)
	api_url = instance_cred.name
	api_key = instance_cred.api_key
	api_secret = instance_cred.api_secret

	headers = {
		'Authorization': f'token {api_key}:{api_secret}'
	}
	try:
		response = requests.post(f"{api_url}/api/method/sowaanerp_subscription.api.enable_disable_users", headers=headers, json={"user_list": user_list, "action": action}, timeout=15)
		response.raise_for_status()
		data = response.json().get('message', {})
		if data:
			doc.users = []
			for user in data.get('users', []):
				doc.append("users", {
					"user": user.get('user'),
					"email": user.get('email'),
					"enabled": user.get('enabled'),
					"creation1": user.get('creation'),
					"roles": ', '.join(user.get('roles', [])),
				})
			doc.status = data.get('status')
			doc.valid_till = data.get('valid_till')
			doc.quota = frappe.as_json(data.get('quota'))
			doc.save(ignore_permissions=True)

		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f'{action.capitalize()} Users Error')
		frappe.throw(_(f'Failed to {action} users: {0}').format(str(e)))

@frappe.whitelist()
def update_quota(docname):
	doc = frappe.get_doc('SowaanERP Instance', docname)
	instance_cred = frappe.get_doc('SowaanERP Instance Credential', doc.instance)
	api_url = instance_cred.name
	api_key = instance_cred.api_key
	api_secret = instance_cred.api_secret

	headers = {
		'Authorization': f'token {api_key}:{api_secret}'
	}
	try:
		response = requests.post(f"{api_url}/api/method/sowaanerp_subscription.api.update_quota", headers=headers, json={"quota": doc.quota}, timeout=15)
		response.raise_for_status()
		data = response.json().get('message', {})
		if data:
			frappe.msgprint(data.get('message', _('Quota updated successfully')))

		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), 'Update Quota Error')
		frappe.throw(_('Failed to update quota: {0}').format(str(e)))