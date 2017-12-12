# -*- coding: utf-8 -*-
# Copyright (c) 2017, vinhbk2000 and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class Meeting(Document):

	def validate(self):
		""" Set missing name and warn if duplicate"""
		found = []
		for attendee in self.attendees:
			if not attendee.full_name:
				attendee.full_name = get_full_name(attendee.attendee)
			if attendee.attendee in found:
				frappe.throw(_("Attendee {0} entered twice").format(attendee.attendee))
			found.append(attendee.attendee)

	def on_update(self):
		self.sync_todos()
	
	def sync_todos(self):

		todos_added = [todo.name for todo in 
			frappe.get_all("ToDo", 
				filters={
					"reference_type"        : self.doctype,
					"reference_name"        : self.name,
				}
        	)
		]

		print todos_added

		for minute in self.minutes:
			if minute.assigned_to and minute.status=="Open":
				
				if not minute.todo:
					todo = frappe.get_doc({
						"doctype"			: "ToDo",
						"description" 		: minute.description,
						"reference_type" 	: self.doctype,
						"reference_name"	: self.name,
						"owner"				: minute.assigned_to
					})
					todo.insert()

					minute.db_set("todo", todo.name)
				else:
					todos_added.remove(minute.todo)
			else:
				minute.db_set("todo", None)

		for todo in todos_added:
			print todo
			# remove closed or old todos
			frappe.delete_doc("ToDo", todo)




@frappe.whitelist()
def get_full_name(attendee):
	user = frappe.get_doc("User", attendee)
	return  " ".join(filter(None, [user.first_name, user.middle_name, user.last_name]))