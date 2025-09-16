import frappe
from sowaan_admin.sowaan_admin.doctype.sowaanerp_instance.sowaanerp_instance import fetch_users

@frappe.whitelist()
def fetch_users_for_all_instances():
	instances = frappe.get_all('SowaanERP Instance', pluck='name')
	# results = []
	for name in instances:
		try:
			fetch_users(name)
			# results.append({'instance': name, 'status': 'success'})
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), f'Fetch Users for Instance {name} Error')
			# results.append({'instance': name, 'status': 'error', 'error': str(e)})
	# return results

def daily_fetch_users_for_all_instances():
	frappe.enqueue('sowaan_admin.scheduler.fetch_users_for_all_instances')