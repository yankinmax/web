//Copyright 2018 Therp BV <https://therp.nl>
//License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
/*global Uint8Array base64js*/

odoo.define('web_drop_target', function(require) {
    var    FormController = require('web.FormController');
           _t = require('web.core')._t;

    // this is the main contribution of this addon: A mixin you can use
    // to make some widget a drop target. Read on how to use this yourself
    var DropTargetMixin = {
        // add the mime types you want to support here, leave empty for
        // all types. For more control, override _get_drop_items in your class
        _drop_allowed_types: [],

        _drop_overlay: null,

        start: function() {
            var result = this._super.apply(this, arguments);
            this.$el.on('drop.widget_events', this.proxy('_on_drop'));
            this.$el.on('dragenter.widget_events', this.proxy('_on_dragenter'));
            this.$el.on('dragover.widget_events', this.proxy('_on_dragenter'));
            this.$el.on('dragleave.widget_events', this.proxy('_on_dragleave'));
            return result;
        },

        _on_drop: function(e) {
            var drop_items = this._get_drop_items(e);
            if(!drop_items) {
                return;
            }
            jQuery(e.delegateTarget).removeClass(this._drag_over_class);
            e.preventDefault();
            this._handle_drop_items(drop_items, e)
        },

        _on_dragenter: function(e) {
            if(this._get_drop_items(e)) {
                e.preventDefault();
                if(!this._drop_overlay){
                    var drop_overlay_message = _t('Drop your files here');
                    var o_content = self.$('.o_content');
                    var view_manager = self.$('.o_view_manager_content');
                    this._drop_overlay = self.$(
                        `<div class="o_drag_over">
                            <div class="o_drag_over_content">
                                <div><i class="fa fa-file-o fa-5x" aria-hidden="true"></i></div>
                                <div><h2>${drop_overlay_message}</h2></div>
                            </div>
                        </div>`
                    );
                    var o_content_position = o_content.position();
                    this._drop_overlay.css({
                        'top': o_content_position.top, 
                        'left': o_content_position.left,
                        'width': view_manager.width(),
                        'height': view_manager.height()
                    });
                    o_content.append(this._drop_overlay);
                }
                return false;
            }
        },

        _on_dragleave: function(e) {
            this._drop_overlay.remove();
            this._drop_overlay = null;
            e.preventDefault();
        },

        _get_drop_items: function(e) {
            var self = this,
                dataTransfer = e.originalEvent.dataTransfer,
                drop_items = [];
            _.each(dataTransfer.items, function(item) {
                if(
                    _.contains(self._drop_allowed_types, item.type) ||
                    _.isEmpty(self._drop_allowed_types)
                ) {
                    drop_items.push(item);
                }
            });
            return drop_items;
        },

        // eslint-disable-next-line no-unused-vars
        _handle_drop_items: function(drop_items, e) {
            // do something here, for example call the helper function below
            // e is the on_load_end handler for the FileReader above,
            // so e.target.result contains an ArrayBuffer of the data
        },

        _handle_file_drop_attach: function(
                item, e, res_model, res_id, extra_data
        ) {
            // helper to upload an attachment and update the sidebar
            var self = this;
            var file = item.getAsFile();
            var reader = new FileReader();
            reader.readAsArrayBuffer(file);
            return this._rpc({
                model: 'ir.attachment',
                method: 'create',
                args: [{
                    'name': file.name,
                    'datas': base64js.fromByteArray(
                            new Uint8Array(reader.result)
                        ),
                    'datas_fname': file.name,
                    'res_model': res_model,
                    'res_id': res_id,
                }],
            })
            .then(function() {
                // try to find a sidebar and update it if we found one
                var p = self;
                while(p && !p.sidebar) {
                    p = p.getParent ? p.getParent() : null;
                }
                if(p) {
                    var sidebar = p.sidebar;
                    if(sidebar && _.isFunction(sidebar._onFileUploaded)) {
                        sidebar._onFileUploaded();
                    }
                }
            });
        }
    };

    // and here we apply the mixin to form views, allowing any files and
    // adding them as attachment
    FormController.include(_.extend(DropTargetMixin, {
        _get_drop_file: function() {
            // disable drag&drop when we're on an unsaved record
            if(!this.datarecord.id) {
                return null;
            }
            return this._super.apply(this, arguments);
        },
        _handle_drop_items: function(drop_items, e) {
            var self = this;
            _.each(drop_items, function(item, e) {
                return self._handle_file_drop_attach(
                    item, e, self.renderer.state.model, self.renderer.state.res_id
                );
            });
        }
    }));

    return {
        'DropTargetMixin': DropTargetMixin,
    };
});
