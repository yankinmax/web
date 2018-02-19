/* Copyright 2015 Holger Brunn <hbrunn@therp.nl>
 * Copyright 2018 Simone Orsi <simone.orsi@camptocamp.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define('web_widget_x2many_2d_matrix.helpers', function (require) {
    "use strict";

    var Helpers = {
        parse_boolean: function(val) {
            if (val.toLowerCase() === 'true' || val === '1') {
                return true;
            }
            return false;
        },
        // === functions called via template ===>
        // get x axis values in the correct order
        get_x_axis_values: function() {
            return _.keys(this.by_x_axis);
        },
        // get y axis values in the correct order
        get_y_axis_values: function() {
            return _.keys(this.by_y_axis);
        },
        // get the label for a value on the x axis
        get_x_axis_label: function(x) {
            return this.get_field_value(
                _.first(_.values(this.by_x_axis[x])),
                this.field_label_x_axis, true);
        },
        // get the label for a value on the y axis
        get_y_axis_label: function(y) {
            return this.get_field_value(
                _.first(_.values(this.by_y_axis[y])),
                this.field_label_y_axis, true);
        },
        // return the class(es) the inputs should have
        get_xy_value_class: function() {
            var classes = 'oe_form_field oe_form_required';
            if(this.is_numeric)
            {
                classes += ' oe_form_field_float';
            }
            return classes;
        },
        // return row id of a coordinate
        get_xy_id: function(x, y) {
            return this.by_x_axis[x][y]['id'];
        },
        get_xy_att: function(x, y) {
            var vals = {};
            for (var att in this.fields_att) {
                var val = this.get_field_value(
                    this.by_x_axis[x][y], this.fields_att[att]);
                // Discard empty values
                if (val) {
                    vals[att] = val;
                }
            }
            return vals;
        },
        // return the value of a coordinate
        get_xy_value: function(x, y) {
            return this.get_field_value(
                this.by_x_axis[x][y], this.field_value);
        }
    }

    return Helpers;
});
