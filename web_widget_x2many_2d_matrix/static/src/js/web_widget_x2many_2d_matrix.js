/* Copyright 2015 Holger Brunn <hbrunn@therp.nl>
 * Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
 * Copyright 2018 Simone Orsi <simone.orsi@camptocamp.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define('web_widget_x2many_2d_matrix.widget', function (require) {
    "use strict";

    var core = require('web.core');
    // var FieldManagerMixin = require('web.FieldManagerMixin');
    var field_registry = require('web.field_registry');
    var relational_fields = require('web.relational_fields');
    var weContext = require('web_editor.context');
    var Helpers = require('web_widget_x2many_2d_matrix.helpers');

    var WidgetX2Many2dMatrix = relational_fields.FieldOne2Many.extend(Helpers, {
        template: 'FieldX2Many2dMatrix',
        widget_class: 'o_form_field_x2many_2d_matrix',

        // those will be filled with rows from the dataset
        by_x_axis: {},
        by_y_axis: {},
        by_id: {},
        // configuration values
        field_x_axis: 'x',
        field_label_x_axis: 'x',
        field_y_axis: 'y',
        field_label_y_axis: 'y',
        field_value: 'value',
        x_axis_clickable: true,
        y_axis_clickable: true,
        // information about our datatype
        is_numeric: false,
        show_row_totals: true,
        show_column_totals: true,
        // this will be filled with the model's fields_get
        fields: {},
        // Store fields used to fill HTML attributes
        fields_att: {},

        // read parameters
        init: function (parent, name, record, options) {
            var res = this._super(parent, name, record, options);
            this.init_params();
            return res;
        },
        init_params: function () {
            var node = this.attrs;
            this.field_x_axis = node.field_x_axis || this.field_x_axis;
            this.field_y_axis = node.field_y_axis || this.field_y_axis;
            this.field_label_x_axis = node.field_label_x_axis || this.field_x_axis;
            this.field_label_y_axis = node.field_label_y_axis || this.field_y_axis;
            this.x_axis_clickable = this.parse_boolean(node.x_axis_clickable || '1');
            this.y_axis_clickable = this.parse_boolean(node.y_axis_clickable || '1');
            this.field_value = node.field_value || this.field_value;
            for (var property in node) {
              if (property.startsWith("field_att_")) {
                  this.fields_att[property.substring(10)] = node[property];
              }
            }
            this.field_editability = node.field_editability || this.field_editability;
            this.show_row_totals = this.parse_boolean(node.show_row_totals || '1');
            this.show_column_totals = this.parse_boolean(node.show_column_totals || '1');
        },
        start: function() {
            var self = this;
            return this._super().then(
                self.proxy(this.setup_fields, self)
            ).then(
                self.proxy(this.setup_many2one_axes, self)
            ).then(
                self.proxy(this._setValue, self)
            );
        },
        setup_fields: function () {
            var self = this;
            return this._rpc({
                model: self.field.relation,
                method: 'fields_get',
                args: []
            }).done(function(fields) {
                self.fields = fields;
                self.is_numeric = fields[self.field_value].type == 'float';
                self.show_row_totals &= self.is_numeric;
                self.show_column_totals &= self.is_numeric;
            })
        },
        // return a field's value, id in case it's a one2many field
        get_field_value: function(row, field, many2one_as_name) {
        // TODO v11: still needed?
        // FIXME looks silly
            if(this.fields[field].type == 'many2one' && _.isArray(row[field])) {
                if(many2one_as_name)
                {
                    return row[field][1];
                }
                else
                {
                    return row[field][0];
                }
            }
            return row[field];
        },
        _setValue: function(value_) {
            var self = this,
                result = this._super(value_);
            self.by_x_axis = {};
            self.by_y_axis = {};
            self.by_id = {};
            return $.when(result).then(
                self.proxy(this._load_values, self)
            );
        },
        _load_values: function() {
            var self = this;
            var rec_ids = self.recordData[self.field.name].res_ids;
            var real_ids = [];
            // filter bad ids
            // If by chance we load records not saved yet (NewId records)
            // we'll get ids like `virtual_1`, `virtual_2`, etc
            // and we cannot read them from db.
            _.each(rec_ids, function(value) {
                if (!isNaN(parseInt(value, 10))) {
                    real_ids.push(parseInt(value, 10));
                }
            });
            var def;
            if (real_ids.length) {
                def = this._rpc({
                    model: self.field.relation,
                    method: 'read',
                    args: [real_ids]
                })
            } else {
                // FIXME: v10 didn't worked with non-existing records
                // Here we can use them but so far we don't have
                // proper machinery to handle such values on changes and save.
                // Still, these few lines make sure that the widget is rendered.
                // Values are not saved tho.
                def = new $.Deferred();
                var rows = [];
                _.each(self.recordData[self.field.name].data, function (item) {
                    rows.push(item.data);
                })
                def.resolve(rows);
            }
            return def.done(function(rows) {
                    // setup data structure
                _.each(rows, function(row){
                    self.add_xy_row(row);
                });
                self.renderElement();
                self.compute_totals();
                self.setup_many2one_axes();
                self.$el.find('.edit').on('change', self.proxy(self.xy_value_change));
            });
        },
        // do whatever needed to setup internal data structure
        add_xy_row: function(row) {
            var x = this.get_field_value(row, this.field_x_axis),
                y = this.get_field_value(row, this.field_y_axis);
            this.by_x_axis[x] = this.by_x_axis[x] || {};
            this.by_y_axis[y] = this.by_y_axis[y] || {};
            this.by_x_axis[x][y] = row;
            this.by_y_axis[y][x] = row;
            this.by_id[row.id] = row;
        },
        // validate a value
        validate_xy_value: function(val) {
            try {
                this.parse_xy_value(val);
            }
            catch(e) {
                return false;
            }
            return true;
        },
        // parse a value from user input
        parse_xy_value: function(val) {
            return val;
        },
        // format a value from the database for display
        format_xy_value: function(val) {
            return val;
        },
        // compute totals
        compute_totals: function() {
            var self = this,
                grand_total = 0,
                totals_x = {},
                totals_y = {},
                rows = this.by_id,
                deferred = $.Deferred();
            _.each(rows, function(row) {
                var key_x = self.get_field_value(row, self.field_x_axis),
                    key_y = self.get_field_value(row, self.field_y_axis);
                totals_x[key_x] = (totals_x[key_x] || 0) + self.get_field_value(row, self.field_value);
                totals_y[key_y] = (totals_y[key_y] || 0) + self.get_field_value(row, self.field_value);
                grand_total += self.get_field_value(row, self.field_value);
            });
            _.each(totals_y, function(total, y) {
                self.$el.find(
                    _.str.sprintf('td.row_total[data-y="%s"]', y)).text(
                        self.format_xy_value(total));
            });
            _.each(totals_x, function(total, x){
                self.$el.find(
                    _.str.sprintf('td.column_total[data-x="%s"]', x)
                ).text(self.format_xy_value(total));
            });
            self.$el.find('.grand_total').text(self.format_xy_value(grand_total));
            deferred.resolve({
                totals_x: totals_x,
                totals_y: totals_y,
                grand_total: grand_total,
                rows: rows,
            });
            return deferred;
        },
        setup_many2one_axes: function() {
            if(this.fields[this.field_x_axis].type == 'many2one' && this.x_axis_clickable)
            {
                this.$el.find('th[data-x]').addClass('oe_link')
                .click(_.partial(
                    this.proxy(this.many2one_axis_click),
                    this.field_x_axis, 'x'));
            }
            if(this.fields[this.field_y_axis].type == 'many2one' && this.y_axis_clickable)
            {
                this.$el.find('tr[data-y] th').addClass('oe_link')
                .click(_.partial(
                    this.proxy(this.many2one_axis_click),
                    this.field_y_axis, 'y'));
            }
        },
        many2one_axis_click: function(field, id_attribute, e) {
            // TODO v11: check if working
            this.do_action({
                type: 'ir.actions.act_window',
                name: this.fields[field].string,
                res_model: this.fields[field].relation,
                res_id: $(e.currentTarget).data(id_attribute),
                views: [[false, 'form']],
                target: 'current',
            })
        },
        xy_value_change: function(e) {
            var self = this,
                $cell = $(e.currentTarget),
                val = $cell.val(),
                is_valid = this.validate_xy_value(val);
            if(!is_valid) {
                $cell.parent().addClass('o_form_invalid');
                return;
            }
            var data = {}, value = this.parse_xy_value(val);
            data[this.field_value] = value;
            $cell.siblings('.read').text(this.format_xy_value(value));
            $cell.val(this.format_xy_value(value));
            var def;
            if ($cell.data('id')) {
                // existing record to update
                def = this._rpc({
                    model: self.field.relation,
                    method: 'write',
                    args: [[$cell.data('id')], data, weContext.get()],
                })
            } else{
                def = new $.Deferred();
                def.resolve();
            }
            return def.done(function() {
                self.by_id[$cell.data('id')][this.field_value] = value;
                $cell.parent().removeClass('o_form_invalid');
                self.compute_totals();
            });
        },
        // TODO v11: still needed?
        // effective_readonly_change: function() {
        //     this.$el
        //         .find('tbody .edit')
        //         .toggle(!this.get('effective_readonly'));
        //     this.$el
        //         .find('tbody .read')
        //         .toggle(this.get('effective_readonly'));
        //     this.$el.find('.edit').first().focus();
        // },

        // TODO v11: still needed?
        // is_syntax_valid: function()
        // {
        //     return this.$el.find('.e_form_invalid').length == 0;
        // },

    });

    field_registry.add('x2many_2d_matrix', WidgetX2Many2dMatrix);

    return {
        WidgetX2Many2dMatrix: WidgetX2Many2dMatrix
    };
});
