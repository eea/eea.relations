var EEAReferenceBrowser = {version: '1.0.0'};

EEAReferenceBrowser.Widgets = {};

EEAReferenceBrowser.Widget = function(name){
  this.name = name;
  this.context = jQuery('#' + name + "-widget");
  this.popup = jQuery('#' + name + '-popup', this.context);
  this.workspace = jQuery('.popup-tabs' , this.popup);
  this.button = jQuery('input[type=button]', this.context);
  this.initialize();
};

EEAReferenceBrowser.Widget.prototype = {
  initialize: function(){
    var width = jQuery(window).width() * 0.85;
    var height = jQuery(window).height() * 0.95;
    var js_context = this;

    // Popup dialog
    this.popup.dialog({
      bgiframe: true,
      modal: true,
      autoOpen: false,
      width: width,
      height: height,
      buttons: {
        'Done': function(){
          jQuery(this).dialog('close');
        },
        'Cancel': function(){
          jQuery(this).dialog('close');
        }
      }
    });

    // Tabs
    this.workspace.tabs();

    // Add button
    this.button.click(function(){
      js_context.popup.dialog('open');
    });
  }
};

EEAReferenceBrowser.Load = function(){
  var widgets = jQuery('.eea-widget-referencebrowser');
  widgets.each(function(){
    var context = jQuery(this);
    var name = context.attr('id');
    name = name.replace("-widget", "");
    EEAReferenceBrowser.Widgets[name] = new EEAReferenceBrowser.Widget(name);
  });
};

jQuery(document).ready(EEAReferenceBrowser.Load);
