// Copyright (c) 2025, Sowaan and contributors
// For license information, please see license.txt

frappe.ui.form.on("SowaanERP Instance", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button('🔄 Fetch Users', () => {
				frappe.call({
					method: 'sowaan_admin.sowaan_admin.doctype.sowaanerp_instance.sowaanerp_instance.fetch_users',
					args: {
						docname: frm.doc.name
					},
                    freeze: true,
					freeze_message: __("Fetching Users..."),
					callback: function(r) {
						frm.reload_doc();
					}
				});
			});

			// Add Disable Users button, initially disabled
			let disableBtn = frm.add_custom_button('🚫 Disable Users', () => {
				let selected_row_ids = frm.fields_dict.users.grid.get_selected();
				let selected_users = frm.doc.users
					.filter(row => selected_row_ids.includes(row.name) && (row.enabled == 1 || row.enabled === true || row.enabled === '1'))
					.map(row => row.user);

				frappe.call({
					method: 'sowaan_admin.sowaan_admin.doctype.sowaanerp_instance.sowaanerp_instance.enable_disable_users',
					args: {
						docname: frm.doc.name,
						user_list: selected_users,
                        action: 'disable'
					},
                    freeze: true,
					freeze_message: __("Disabling Users..."),
					callback: function(r) {
						frm.reload_doc();
					}
				});
			});
			disableBtn.prop('disabled', true);

			// Add Enable Users button, initially disabled
			let enableBtn = frm.add_custom_button('✅ Enable Users', () => {
				let selected_row_ids = frm.fields_dict.users.grid.get_selected();
				let selected_users = frm.doc.users
					.filter(row => selected_row_ids.includes(row.name) && (row.enabled == 0 || row.enabled === false || row.enabled === '0'))
					.map(row => row.user);

				frappe.call({
					method: 'sowaan_admin.sowaan_admin.doctype.sowaanerp_instance.sowaanerp_instance.enable_disable_users',
					args: {
						docname: frm.doc.name,
						user_list: selected_users,
						action: 'enable'
					},
                    freeze: true,
					freeze_message: __("Enabling Users..."),
					callback: function(r) {
						frm.reload_doc();
					}
				});
			});
			enableBtn.prop('disabled', true);

			
			// Enable/disable button based on selection in users child table
			frm.fields_dict.users.grid.wrapper.on('click', '.grid-row-check', function() {
				let selected_row_ids = frm.fields_dict.users.grid.get_selected();
				let selected_rows = frm.doc.users.filter(row => selected_row_ids.includes(row.name));
				let has_enabled = selected_rows.some(row => row.enabled == 1 || row.enabled === true || row.enabled === '1');
				let has_disabled = selected_rows.some(row => row.enabled == 0 || row.enabled === false || row.enabled === '0');
				if (selected_rows.length > 0 && has_enabled) {
					disableBtn.prop('disabled', false);
				} else {
					disableBtn.prop('disabled', true);
				}
				if (selected_rows.length > 0 && has_disabled) {
					enableBtn.prop('disabled', false);
				} else {
					enableBtn.prop('disabled', true);
				}
			});

			// Hide Add Row and Delete buttons for users child table
			frm.fields_dict.users.grid.wrapper.find('.grid-add-row, .grid-remove-rows, .grid-delete-row').hide();
			// frm.fields_dict.users.grid.wrapper.find('.btn-open-row').hide();
			frm.fields_dict.users.grid.allow_on_grid_editing = false;
		}
	},
    set_quota_in_instance: function(frm) {
        frappe.confirm(__('Are you sure you want to set the quota in the instance?'), function() {
            frappe.call({
                method: 'sowaan_admin.sowaan_admin.doctype.sowaanerp_instance.sowaanerp_instance.update_quota',
                args: {
                    docname: frm.doc.name
                },
                freeze: true,
                freeze_message: __("Setting Quota in Instance..."),
                callback: function(r) {
                    frm.reload_doc();
                }
            });
        });
    }
});
