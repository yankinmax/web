/* Copyright 2018 Simone Orsi <simone.orsi@camptocamp.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define('web_widget_x2many_2d_matrix.X2Many2dMatrixRenderer', function (require) {
  "use strict";

  // heavily inspired by Odoo's `ListRenderer`
  var BasicRenderer = require('web.BasicRenderer');
  var config = require('web.config');
  var field_utils = require('web.field_utils');
  var utils = require('web.utils');
  var FIELD_CLASSES = {
    // copied from ListRenderer
    float: 'o_list_number',
    integer: 'o_list_number',
    monetary: 'o_list_number',
    text: 'o_list_text',
  };

  var X2Many2dMatrixRenderer = BasicRenderer.extend({

    init: function (parent, state, params) {
      this._super.apply(this, arguments);
      this.editable = params.editable;
      this.columns = params.matrix_data.columns;
      this.rows = params.matrix_data.rows;
      this.matrix_data = params.matrix_data;
    },
    _renderView: function () {
      var self = this;

      this.$el
        .removeClass('table-responsive')
        .empty();

      var $table = $('<table>').addClass('o_list_view table table-condensed table-striped');
      this.$el
        .addClass('table-responsive')
        .append($table);

      this._computeColumnAggregates();
      this._computeRowAggregates();

      $table
        .append(this._renderHeader())
        .append(this._renderBody());
      if (self.matrix_data.show_column_totals) {
        $table.append(this._renderFooter());
      }
      return this._super();
    },
    _renderBody: function () {
      var $body = $('<tbody>').append(this._renderRows());
      _.each($body.find('input'), function (td, i) {
        $(td).attr('tabindex', i);
      });
      return $body;
    },
    _renderHeader: function (isGrouped) {
      var $tr = $('<tr>')
          .append(_.map(this.columns, this._renderHeaderCell.bind(this)));
      // wipe 1st column header
      $tr.find('th:first').empty();
      if (this.matrix_data.show_row_totals) {
        $tr.append($('<th/>', {class: 'total'}));
      }
      return $('<thead>').append($tr);
    },
    _renderHeaderCell: function (node) {
      var name = node.attrs.name;
      var field = this.state.fields[name];
      var $th = $('<th>');
      if (!field) {
          return $th;
      }
      var description;
      if (node.attrs.widget) {
        description = this.state.fieldsInfo.list[name].Widget.prototype.description;
      }
      if (description === undefined) {
        description = node.attrs.string || field.string;
      }
      $th.text(description).data('name', name);

      if (field.type === 'float' || field.type === 'integer' || field.type === 'monetary') {
        $th.addClass('text-right');
      }

      if (config.debug) {
        var fieldDescr = {
          field: field,
          name: name,
          string: description || name,
          record: this.state,
          attrs: node.attrs,
        };
        this._addFieldTooltip(fieldDescr, $th);
      }
      return $th;
    },
    _renderRows: function () {
      return _.map(this.rows, this._renderRow.bind(this));
    },
    _renderRow: function (row) {
      var self = this;
      var $cells = _.map(this.columns, function (node, index) {
        var record = row.data[index];
        // make the widget use our field value for each cell
        node.attrs.name = self.matrix_data.field_value;
        return self._renderBodyCell(record, node, index, {mode: 'readonly'});
      });
      var $tr = $('<tr/>', {class: 'o_data_row'}).append($cells);
      if (row.aggregate) {
        $tr.append(self._renderAggregateRowCell(row));
      }
      return $tr;
    },
    _renderAggregateRowCell: function (row) {
      var $cell = $('<td/>', {class: 'row-total text-right'});
      this._apply_aggregate_value($cell, row.aggregate);
      return $cell;
    },
    _renderBodyCell: function (record, node, colIndex, options) {
      var tdClassName = 'o_data_cell';
      if (node.tag === 'button') {
        tdClassName += ' o_list_button';
      } else if (node.tag === 'field') {
        var typeClass = FIELD_CLASSES[this.state.fields[node.attrs.name].type];
        if (typeClass) {
          tdClassName += (' ' + typeClass);
        }
        if (node.attrs.widget) {
          tdClassName += (' o_' + node.attrs.widget + '_cell');
        }
      }
      var $td = $('<td>', {
        'class': tdClassName,
        'data-form-id': record.id,
        'data-id': record.data.id,
      });
      if (colIndex == 0) {
        var value = record.data[this.matrix_data.field_y_axis];
        if (value.type == 'record') {
          // we have a related record
          value = value.data.display_name;
        }
        // get 1st column filled w/ Y label
        $td.text(value);
        return $td;
      }

      // We register modifiers on the <td> element so that it gets the correct
      // modifiers classes (for styling)
      var modifiers = this._registerModifiers(node, record, $td, _.pick(options, 'mode'));
      // If the invisible modifiers is true, the <td> element is left empty.
      // Indeed, if the modifiers was to change the whole cell would be
      // rerendered anyway.
      if (modifiers.invisible && !(options && options.renderInvisible)) {
          return $td;
      }
      options.mode = 'edit';  // enforce edit mode
      var widget = this._renderFieldWidget(node, record, _.pick(options, 'mode'));
      this._handleAttributes(widget.$el, node);
      return $td.append(widget.$el);
    },
    _renderFooter: function () {
      var $cells = this._renderAggregateColCells();
      if ($cells) {
        return $('<tfoot>').append($('<tr>').append($cells));
      }
      return;
    },
    _renderAggregateColCells: function (aggregateValues) {
      var self = this;
      return _.map(this.columns, function (column, index) {
        var $cell = $('<td>', {class: 'col-total text-right'});
        if (index == 0) {
          // skip 1st column
          return $cell;
        }
        if (column.aggregate) {
          self._apply_aggregate_value($cell, column.aggregate);
        }
        return $cell;
      });
    },
    _computeColumnAggregates: function () {
      if (!this.matrix_data.show_column_totals) {
        return;
      }
      var self = this,
          fname = this.matrix_data.field_value,
          field = this.state.fields[fname];
      if (!field) { return; }
      var type = field.type;
      if (type !== 'integer' && type !== 'float' && type !== 'monetary') {
        return;
      }
      _.each(self.columns, function (column, index) {
        column.aggregate = {
          fname: fname,
          ftype: type,
          // TODO: translate
          help: 'Sum',
          value: 0
        };
        _.each(self.rows, function (row) {
          // var record = _.findWhere(self.state.data, {id: col.data.id});
          column.aggregate.value += row.data[index].data[fname];
        })
      });
    },
    _computeRowAggregates: function () {
      if (!this.matrix_data.show_row_totals) {
        return;
      }
      var self = this,
          fname = this.matrix_data.field_value,
          field = this.state.fields[fname];
      if (!field) { return; }
      var type = field.type;
      if (type !== 'integer' && type !== 'float' && type !== 'monetary') {
          return;
      }
      _.each(self.rows, function (row) {
        row.aggregate = {
          fname: fname,
          ftype: type,
          // TODO: translate
          help: 'Sum',
          value: 0
        };
        _.each(row.data, function (col) {
          row.aggregate.value += col.data[fname];
        })
      });
    },
    _apply_aggregate_value: function ($cell, aggregate) {
      var field = this.state.fields[aggregate.fname],
          formatter = field_utils.format[field.type];
      var formattedValue = formatter(aggregate.value, field, {escape: true, });
      $cell.addClass('total').attr('title', aggregate.help).html(formattedValue);
    },
    confirmUpdate: function (state, id, fields, ev) {
      var self = this;
      this.state = state;
      return this.confirmChange(state, id, fields, ev).then(function () {
        self._refresh(id);
      });
    },
    _refresh: function (id) {
      this._updateRow(id);
      this._refreshColTotals();
      this._refreshRowTotals();
    },
    /*
    Update row data in our internal rows.
    */
    _updateRow: function (id) {
      var self = this,
          record = _.findWhere(self.state.data, {id: id});
      _.each(self.rows, function(row) {
        _.each(row.data, function(col, i) {
          if (col.id == id) {
            row.data[i] = record;
          }
        });
      });
    },
    _refreshColTotals: function () {
      this._computeColumnAggregates();
      this.$('tfoot').replaceWith(this._renderFooter());
    },
    _refreshRowTotals: function () {
      var self = this;
      this._computeRowAggregates();
      var $rows = $('tr.o_data_row');
      _.each(self.rows, function(row, i) {
        if (row.aggregate) {
          $($rows[i]).find('.row-total')
            .replaceWith(self._renderAggregateRowCell(row));
        }
      })
    },
    /*
    x2m fields expect this
    */
    getEditableRecordID: function (){ return false }

  });

  return X2Many2dMatrixRenderer;
});
