require({cache:{
'url:app/ui/dialogs/templates/LabelsDialog.html':"<div class=\"dijitDialog\" role=\"dialog\" aria-labelledby=\"labelsDialog_title\">\n  <div data-dojo-attach-point=\"titleBar\" class=\"dijitDialogTitleBar\">\n    <span data-dojo-attach-point=\"titleNode\" class=\"dijitDialogTitle\" role=\"heading\"></span>\n\t\t<span data-dojo-attach-point=\"closeButtonNode\" class=\"dijitDialogCloseIcon\"\n          data-dojo-attach-event=\"ondijitclick: onCancel\" title=\"Annuleren\" role=\"button\" tabIndex=\"-1\">\n\t\t\t<span data-dojo-attach-point=\"closeText\" class=\"closeText\" title=\"Annuleren\" tabIndex=\"-1\">\n        <i class=\"fa fa-times\"></i></span>\n\t\t</span>\n  </div>\n\n  <div data-dojo-attach-point=\"containerNode\" class=\"dijitDialogPaneContent\">\n    <div class=\"row\">\n      <div class=\"large-6 columns\">\n        <div class=\"placeholder-container\">\n          <label for=\"typeSelectNode-${id}\">Type</label>\n          <select id=\"typeSelectNode-${id}\" data-dojo-attach-point=\"typeSelectNode\"></select>\n        </div>\n      </div>\n      <div class=\"large-6 columns\">\n        <div class=\"placeholder-container\">\n          <label for=\"langSelectNode-${id}\">Language</label>\n          <select id=\"langSelectNode-${id}\" data-dojo-attach-point=\"langSelectNode\"></select>\n        </div>\n      </div>\n    </div>\n    <div class=\"row\">\n      <div class=\"large-12 columns\">\n        <div class=\"placeholder-container\">\n          <label for=\"labelInputNode-${id}\">Label</label>\n          <input type=\"text\" data-dojo-attach-point=\"labelInputNode\" id=\"labelInputNode-${id}\">\n        </div>\n      </div>\n    </div>\n    <div class=\"row footerButtons\">\n      <div class=\"large-12 columns text-center\">\n        <a href=\"#\" data-dojo-attach-event=\"onClick: _okClick\" data-dojo-attach-point=\"okButtonNode\" class=\"button tiny\">Ok</a>\n        <a href=\"#\" data-dojo-attach-event=\"onClick: _cancelClick\" class=\"button tiny\">Cancel</a>\n      </div>\n    </div>\n  </div>\n</div>"}});
define("app/ui/dialogs/LabelsDialog", [
  'dojo/_base/declare',
  'dijit/_TemplatedMixin',
  'dijit/_WidgetsInTemplateMixin',
  'dijit/Dialog',
  'dojo/topic',
  'dojo/dom-construct',
  'dojo/text!./templates/LabelsDialog.html',
  '../../utils/DomUtils'
], function (
  declare,
  _TemplatedMixin,
  _WidgetsInTemplateMixin,
  Dialog,
  topic,
  domConstruct,
  template,
  DomUtils
) {
  return declare([Dialog, _TemplatedMixin, _WidgetsInTemplateMixin], {

    templateString: template,
    parentNode: null,
    baseClass: 'labels-dialog',
    title: 'Add label',
    labelElement: null,
    typeList: null,
    langList: null,
    edit: false,

    postCreate: function () {
      this.inherited(arguments);
      DomUtils.addOptionsToSelect(this.typeSelectNode, {
        data: this.typeList,
        idProperty: 'value',
        labelProperty: 'label'
      });
      DomUtils.addOptionsToSelect(this.langSelectNode, {
        data: this.langList,
        idProperty: 'id',
        labelProperty: 'name'
      });
    },

    startup: function () {
      this.inherited(arguments);
    },

    setData: function(label) {
      this.labelInputNode.value = label.label
      this.langSelectNode.value = label.language;
      this.typeSelectNode.value = label.type;
    },

    hide: function () {
      this.inherited(arguments);
      this.reset();
    },

    show: function (label) {
      this.inherited(arguments);
      this.reset();
      if (label) {
        this.setData(label);
        this.set('title', 'Edit label');
        this.okButtonNode.innerHTML = 'Edit';
        this.edit = true;
        this.labelElement = label;
      } else {
        this.set('title', 'Add new label');
        this.okButtonNode.innerHTML = 'Add';
        this.edit = false;
      }
    },

    updateLanguages: function(langs) {
      // update languagelist and refresh select list
      this.langList = langs;
      domConstruct.empty(this.langSelectNode);
      DomUtils.addOptionsToSelect(this.langSelectNode, {
        data: this.langList,
        idProperty: 'id',
        labelProperty: 'name'
      });
    },

    _okClick: function (evt) {
       0 && console.debug('LabelsDialog::_okClick');
      evt.preventDefault();
      if (this._validate()) {
        if (this.edit) {
          this.emit('edit.label', {
            label: this.labelInputNode.value.trim(),
            lang: this.langSelectNode.value,
            labelType: this.typeSelectNode.value,
            id: this.labelElement.id
          });
        } else {
          this.emit('add.label', {
            label: this.labelInputNode.value.trim(),
            lang: this.langSelectNode.value,
            labelType: this.typeSelectNode.value
          });
        }
        this.hide();
      } else {
        topic.publish('dGrowl', 'Please fill in all fields.', {
          'title': 'Invalid label',
          'sticky': false,
          'channel': 'info'
        });
      }
    },

    _cancelClick: function (evt) {
       0 && console.debug('LabelsDialog::_cancelClick');
      evt.preventDefault();
      this.hide();
    },

    reset: function () {
      this.labelInputNode.value = '';
      this.langSelectNode.selectedIndex = 0;
      this.typeSelectNode.selectedIndex = 0;
    },

    _validate: function () {
      return this.labelInputNode.value.trim() !== '';
    }
  });
});
