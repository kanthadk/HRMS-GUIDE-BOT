# Copyright (c) 2024, Surendhar Nadh Cherukuri and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class NavIndex(Document):
	pass

def rebuild_nav_index():
	"""
	Nightly job to rebuild NavIndex from:
	- Workspaces
	- Pages
	- DocTypes
	- Reports
	"""
	frappe.db.delete("NavIndex")
	
	# Index DocTypes
	doctypes = frappe.get_all("DocType", filters={"istable": 0, "issingle": 0}, fields=["name", "module"])
	for dt in doctypes:
		frappe.get_doc({
			"doctype": "NavIndex",
			"label": [dt.name],
			"route": f"/app/{frappe.scrub(dt.name)}",
			"create_route": f"/app/{frappe.scrub(dt.name)}/new",
			"reference_doctype": dt.name,
			"type": "DocType",
			"popularity_score": 0
		}).insert(ignore_permissions=True)

	# TODO: Index Reports, Pages, Workspaces
	
	frappe.db.commit()
