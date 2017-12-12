frappe.views.calendar["Meeting"] = {
	field_map: {
		"start": "start",
		"end": "end",
		"id": "name",
		"title": "title",
		"status": "status",
        "allDay": "allDay",
	},
	get_events_method: "meeting.api.get_meetings"
}