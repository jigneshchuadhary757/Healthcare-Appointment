import frappe

from frappe import _
 
 
def execute():
 
    # default item for healthcare service
    item_doc = frappe.new_doc("Item")
    item_doc.item_name = "Healthcare Service"
    item_doc.item_code = "Healthcare Service"
    item_doc.item_group = "Services"
    item_doc.stock_uom = "Nos"
    item_doc.is_stock_item = 0
    item_doc.save(ignore_permissions=True)
 
    # default customer for healthcare appointment
    customer_doc = frappe.new_doc("Customer")
    customer_doc.customer_name = "Walk-in Customer"
    customer_doc.customer_type = "Individual"
    customer_doc.save(ignore_permissions=True)
 
    # default healthcare service for healthcare appointment
    service_doc = frappe.new_doc("Healthcare Service")
    service_doc.service_name = "General Consultation"
    service_doc.price = 1000
    service_doc.duration_minutes = 30
    service_doc.save(ignore_permissions=True)