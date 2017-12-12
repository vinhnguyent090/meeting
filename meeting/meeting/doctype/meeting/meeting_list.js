frappe.listview_settings['Meeting'] = {
    add_fields: ["status"],
	get_indicator: function(doc) {
        return [__(doc.status),{
            "Planned" : "blue",
            "In Progress" : "orange",
            "Completed" : "green",
            "Canceled": "darkgrey"
        }[doc.status],"status,=," + doc.status];
    }
};
