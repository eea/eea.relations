var EEAReferenceBrowser = {version: '1.0.0'};
EEAReferenceBrowser.Widgets = {};

// Events
EEAReferenceBrowser.Events = {};

EEAReferenceBrowser.Widget = function(name){
  this.name = name;
  this.context = jQuery('#' + name + "-widget");
  this.popup = jQuery('#' + name + '-popup', this.context);
  this.workspace = jQuery('.popup-tabs' , this.popup);
  this.button = jQuery('input[type=button]', this.context);
  this.current_tab = null;

  this.initialize();
};

EEAReferenceBrowser.Widget.prototype = {
  initialize: function(){
    this.width = jQuery(window).width() * 0.85;
    this.height = jQuery(window).height() * 0.95;
    var js_context = this;

    // Popup dialog
    this.popup.dialog({
      bgiframe: true,
      modal: true,
      autoOpen: false,
      width: js_context.width,
      height: js_context.height,
      resize: false,
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
    this.workspace.tabs({
      select: function(event, ui){
        Faceted.Cleanup();
        jQuery('.popup-tabs #faceted-form').remove();
      },
      load: function(event, ui){
        js_context.tab_selected(ui);
      }
    });

    // Add button
    this.button.click(function(){
      js_context.popup.dialog('open');
      jQuery(Faceted.Events).trigger(Faceted.Events.WINDOW_WIDTH_CHANGED);
    });
  },

  tab_selected: function(ui){
    this.current_tab = new EEAReferenceBrowser.Tab(ui, this);
  }
};

EEAReferenceBrowser.Tab = function(context, parent){
  this.parent = parent;
  this.context = context;
  this.panel = jQuery(context.panel);
  this.tab = jQuery(context.tab);
  this.name = this.panel.attr('id');
  this.url = jQuery('.tab-url', this.tab).text();
  this.panel.height(parent.height - 180);
  this.panel.css('overflow', 'auto');
  this.initialize();
};

EEAReferenceBrowser.Tab.prototype = {
  initialize: function(){
    var js_context = this;
    Faceted.Load(0, this.url + '/');
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
