odoo.define('web.web_charfield_autocomplete', function(require) {
    "use strict";

    var core = require('web.core');
    var FieldChar = core.form_widget_registry.get('char');
    var Model = require('web.DataModel');
    var data = require('web.data');

    // var QWeb = core.qweb;
    var _lt = core._lt;

    var FieldCharAutocomplete = FieldChar.extend({
        widget_class: 'oe_form_field_autocomplete',
        events: {
            'keydown input': function (e) {
                switch (e.which) {
                case $.ui.keyCode.UP:
                case $.ui.keyCode.DOWN:
                    e.stopPropagation();
                }
            },
        },
        init: function(field_manager, node) {
            this._super(field_manager, node);
            this.set({'value': false});
            this.current_display = null;
            this.search_model = this.options.model;
            this.search_field = this.options.search_field || 'name';
            this.search_display_field = this.options.display_field || 'name';
            this.search_value_field = this.options.value_field || 'name';
            this.search_read_fields = this.options.fields || [this.search_value_field, this.search_display_field];
            this.search_limit = this.options.limit || 30;
        },
        initialize_content: function () {
            this._super(),
            this.setup_autocomplete()
        },
        setup_autocomplete: function() {
            var self = this;

            // some behavior for input
            // Inspired by `form_relational_widgets.Many2one`
            var input_changed = function() {
                if (self.current_display !== self.$el.val()) {
                    self.current_display = self.$el.val();
                    if (self.$el.val() === "") {
                        self.internal_set_value(false);
                    } else {
                    }
                }
            };
            this.$el.keydown(input_changed);
            this.$el.change(input_changed);

            var ignore_blur = false;
            this.$el.on({
                focus: function () { self.trigger('focused'); },
                autocompleteopen: function () { ignore_blur = true; },
                autocompleteclose: function () { setTimeout(function() {ignore_blur = false;},0); },
                blur: function () {
                    // autocomplete open
                    if (ignore_blur) { $(this).focus(); return; }
                    self.trigger('blurred');
                    self.trigger('change');
                    self.internal_set_value(self.$el.val());
                }
            });

            var isSelecting = false;
            self.$el.autocomplete({
                source: function(request, response){
                    return self.autocomplete_source(request, response);
                },
                select: function(event, ui) {
                    isSelecting = true;
                    self.internal_set_value(ui.item.value);
                    self.$el.val(ui.item.value);
                    return false;
                },
                focus: function(e, ui) {
                    e.preventDefault();
                }
            });
            // used to correct a bug when selecting an element by pushing 'enter' in an editable list
            this.$el.keyup(function(e) {
                if (e.which === 13) { // ENTER
                    if (isSelecting)
                        e.stopPropagation();
                }
                isSelecting = false;
            });
        },
        get_autocomplete_domain: function(term){
            var self = this;
            var domain = [
                [self.search_field, 'ilike', '%' + term + '%'],
            ];
            // other fields can change our domain, let's consider this
            domain = new data.CompoundDomain(this.build_domain(), domain).eval();
            return domain
        },
        autocomplete_source: function( request, response ) {
            var self = this;
            var term = request.term;
            var domain = self.get_autocomplete_domain(term);
            var def = new Model(self.search_model).call(
                "search_read", [domain], {
                    fields: self.search_read_fields,
                    context: {},
                    limit: this.options.limit || 30
                }
            );
            def.done(function(results){
                var data = [];
                $.each(results, function(){
                    // [ { label: "Choice1", value: "value1" }, ... ]
                    data.push({
                        'label': this[self.search_display_field],
                        'value': this[self.search_value_field]
                    })
                })
                return response(data)
            })
        }

    });

    core.form_widget_registry.add('char_autocomplete', FieldCharAutocomplete);

    return {
        FieldCharAutocomplete: FieldCharAutocomplete
    };
});
