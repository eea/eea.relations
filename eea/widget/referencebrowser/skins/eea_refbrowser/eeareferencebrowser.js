var EEAReferenceBrowser = {version: '1.0.0'};
EEAReferenceBrowser.Widgets = {};

// Events
EEAReferenceBrowser.Events = {};

EEAReferenceBrowser.Widget = function(name){
  this.name = name;
  this.context = jQuery('#' + name + "-widget");
  this.popup = jQuery('#' + name + '-popup', this.context);
  this.workspace = jQuery('.popup-tabs' , this.popup);
  this.basket = jQuery('.popup-selected-items', this.popup);
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

    // Basket
    this.basket.height(this.height - 128);
    this.basket.css('overflow', 'auto');
    jQuery('.tileItem', this.basket).attr('title', 'Click and drag to change order');
    this.basket.sortable({
      items: '.tileItem',
      placeholder: 'ui-state-highlight'
    });
    //this.basket.droppable();

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
    jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function(evt){
      js_context.setup_links();
    });
  },

  setup_links: function(){
    var results = jQuery('#faceted-results', this.panel);
    this.setup_folder_summary_view(results);
    this.setup_tabular_view(results);
    this.setup_album_view(results);
    this.setup_folder_listing(results);

    var items = jQuery('.refbrowser-faceted-addable-item', results);
    var icon = jQuery('<div>').addClass('ui-icon')
                              .addClass('ui-icon-extlink')
                              .addClass('ui-icon-custom-add');
    items.attr('title', 'Click to add it to current relations');
    items.prepend(icon);

  },

  setup_folder_summary_view: function(context){
    // Folder summary view
    jQuery('.tileHeadline a', context).click(function(){
      return false;
    });
    jQuery('a.tileImage', context).click(function(){
      return false;
    });
    jQuery('.tileFooter a', context).attr('target', '_blank');

    // Add working css class
    jQuery('.tileItem', context).addClass('refbrowser-faceted-addable-item');
  },

  setup_tabular_view: function(context){
    // Tabular view
    var table = jQuery('.listing', context);
    jQuery('a', table).click(function(){
      return false;
    });

    jQuery('table', context).css('width', '100%');
    // Add working css class
    jQuery('tr', context).addClass('refbrowser-faceted-addable-item');
  },

  setup_album_view: function(context){
    // Album view
    jQuery('.photoAlbumEntry a', context).click(function(){
      return false;
    });

    // Add working css class
  },

  setup_folder_listing: function(context){
    // Folder listing
    jQuery('dt a', context).click(function(){
      return false;
    });

    // Add working css class
    jQuery('dt', context).addClass('refbrowser-faceted-addable-item');
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
