odoo.define('mtsmte.web_ckeditor4', function(require){
    "use strict";
    var core = require('web.core');
    var web_ckeditor4 = require('web_ckeditor4');
    var FieldCKEditor4 = core.form_widget_registry.get('text_ckeditor4').include({
      _getRemovePlugins: function () {
          // hide templates, font plugin too
          return 'iframe,flash,forms,smiley,pagebreak,stylescombo,templates,font';
      },
    })

});
