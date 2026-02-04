# Copyright (c) 2024, Surendhar Nadh Cherukuri and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PolicyVersion(Document):
	def validate(self):
		if self.status == "Approved":
			# Ensure only one active version per PolicyDocument
			# (Or define supersedes logic)
			pass

	def on_submit(self):
		pass
