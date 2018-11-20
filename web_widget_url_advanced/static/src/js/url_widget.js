/* Copyright 2018 Simone Orsi - Camptocamp SA
License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html). */

odoo.define('web_widget_url_advanced', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');

    basic_fields.UrlWidget.include({
        /**
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            // retrieve customized `<a />` text from a field
            // via `text_field` attribute
            var field_value = this.recordData[this.attrs.text_field];
            if (_.isObject(field_value) && _.has(field_value.data)) {
                field_value = field_value.data.display_name;
            }
            if (field_value) {
                this.attrs.text = field_value;
            }
        },
    });

});
