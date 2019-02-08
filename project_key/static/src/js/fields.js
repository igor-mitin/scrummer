odoo.define('project_key.TextUrlField', function (require) {
"use strict";

    var basic_fields = require('web.basic_fields'),
        fieldRegistry = require('web.field_registry');

    var TextUrlField = basic_fields.UrlWidget.extend({

        _renderReadonly: function () {
            var urlField = this.nodeOptions.url_field || this.field.url_field || 'url',
                url = this.record.data[urlField];
            this.$el.text(this.value)
                .addClass('o_form_uri o_text_overflow')
                .attr('target', '_blank')
                .attr('href', url || '#');
        }
    });
    fieldRegistry.add('text_url', TextUrlField);

    return TextUrlField;

});
