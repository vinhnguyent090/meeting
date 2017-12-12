from __future__ import unicode_literals
import frappe
import unittest

class TestMeeting(unittest.TestCase):

    def test_sync_todos(self):
        
        meeting = make_meeting()

        todos = get_todos(meeting)

        self.assertEquals(todos[0].name, meeting.minutes[0].todo)
        self.assertEquals(todos[0].description, meeting.minutes[0].description)
    
    def test_sync_todos_remove(self):
        meeting = make_meeting()
        meeting.minutes[0].status = "Closed"
        meeting.save()

        todos = get_todos(meeting)

        self.assertEquals(len(todos),0)


def make_meeting():

    meeting = frappe.get_doc({
        "doctype"       : "Meeting",
        "title"         : "Test Meeting",
        "status"        : "Planned",
        "date"          : "2017-08-06",
        "from_time"     : "09:00",
        "to_time"       : "10:00",
        "minutes"   : [
            {
                "description"       : "Test Minute 1",
                "status"            : "Open",
                "assigned_to"       : "user01@yahoo.com"
            }
        ]

    })
    meeting.insert()
    return meeting

def get_todos(meeting):

    return frappe.get_all("ToDo", 
            filters={
                "reference_type"        : meeting.doctype,
                "reference_name"        : meeting.name,
                "owner"                 : "user01@yahoo.com",
            },
            fields=["name", "description"]
        )



