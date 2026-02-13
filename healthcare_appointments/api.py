import frappe

@frappe.whitelist(allow_guest=True)
def get_service_details(service):
    service_doc = frappe.get_doc("Healthcare Service", service)
    return {
        "rate": service_doc.rate,
        "duration": service_doc.duration
    }
