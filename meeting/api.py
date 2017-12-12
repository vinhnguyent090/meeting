import frappe
from frappe import _
from frappe.utils import nowdate, add_days 

@frappe.whitelist()

def send_inviations_emails(meeting):
    meeting = frappe.get_doc("Meeting", meeting);

    meeting.status = "In Progress"
    meeting.save()

    return meeting.invitation_message;


@frappe.whitelist()
def get_meetings(start, end):

	data = frappe.db.sql(""" 
        select
            timestamp(`date`, `from_time`) as start,
            timestamp(`date`, `to_time`) as end,
            name,
            title,
            status,
            0 as allDay
        from `tabMeeting`
        where `date` between %(start)s and %(end)s""",{
            "start" : start,
            "end" :  end
        }, as_dict=True)

	return data    


def make_orientation_meeting(doc, method):

    meeting = frappe.get_doc({
        "doctype"   : "Meeting",
        "title"     : "Orientation for {0}".format(doc.first_name),
        "date"      : add_days(nowdate(),1),
        "from_time" : "09:00",
        "to_time"   : "09:30",
        "status"    : "Planned",
        "attendees" :[{
            "attendee": doc.name
        }]
    })

    meeting.flags.ignore_permissions = True
    meeting.insert()

    frappe.msgprint(_("Orientation meeting created"))
