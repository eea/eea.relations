var EEAReferenceBrowser = {version: '1.0.0'};

// Events
EEAReferenceBrowser.Events = function(){
  this.BASKET_ADD = 'EEA-REFERENCEBROWSER-BASKET-ADD';
  this.BASKET_DELETE = 'EEA-REFERENCEBROWSER-BASKET-DELETE';
  this.AJAX_START = 'EEA-REFERENCEBROWSER-AJAX-START';
  this.AJAX_STOP = 'EEA-REFERENCEBROWSER-AJAX-STOP';
};

EEAReferenceBrowser.Events.prototype = {};

EEAReferenceBrowser.Tab = function(context, parent){
  this.parent = parent;
  this.context = context;
  this.panel = jQuery(context.panel);
  this.tab = jQuery(context.tab);
  this.name = this.panel.attr('id');
  this.url = jQuery('.tab-url', this.tab).text();
  this.panel.height(parent.height - 180);
  this.panel.css('overflow', 'auto');

  var self = this;
  Faceted.Load(0, this.url + '/');
  jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function(evt){
    self.setup_links();
  });
};

EEAReferenceBrowser.Tab.prototype = {
  setup_links: function(){
    var results = jQuery('#faceted-results', this.panel);
    this.setup_folder_summary_view(results);
    this.setup_tabular_view(results);
    this.setup_album_view(results);
    this.setup_folder_listing(results);

    // Divs
    var items = jQuery('.refbrowser-faceted-addable-item', results);
    var icon = jQuery('<div>').addClass('ui-icon')
                              .addClass('ui-icon-extlink')
                              .addClass('ui-icon-custom-add');
    items.attr('title', 'Click to add it to current relations');
    items.prepend(icon);
  },

  setup_folder_summary_view: function(context){
    // Folder summary view
    var items = jQuery('.tileItem', context);
    jQuery('a', items).click(function(){
      return false;
    });

    // Add working css class
    items.addClass('refbrowser-faceted-addable-item');

    // Handle clicks
    var js_context = this;
    items.click(function(){
      var self = jQuery(this);
      self.effect('transfer', {to: '#' + js_context.parent.name + '-popup-selected-items'}, 'slow', function(){
        jQuery(js_context.parent.events).trigger(
          js_context.parent.events.BASKET_ADD,
          {url: jQuery('.tileHeadline a', self).attr('href')}
        );
      });
    });
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

EEAReferenceBrowser.Basket = function(context, parent){
  this.context = context;
  this.parent = parent;
  this.context.height(this.parent.height - 128);
  this.context.css('overflow', 'auto');
  jQuery('.tileItem', this.context).attr('title', 'Click and drag to change order');
  this.context.sortable({
    items: '.tileItem',
    placeholder: 'ui-state-highlight'
  });

  jQuery('.tileItem', this.context).prepend(this.trash_icon());
  var self = this;

  // Basket add
  jQuery(self.parent.events).bind(self.parent.events.BASKET_ADD,
    function(evt, data){
      self.basket_add_clicked(data);
    }
  );

  // Working in background
  jQuery(self.parent.events).bind(self.parent.events.AJAX_START,
    function(evt, data){
      jQuery('h4', self.context).addClass('ui-state-working');
    }
  );
  jQuery(self.parent.events).bind(self.parent.events.AJAX_STOP,
    function(evt, data){
      jQuery('h4', self.context).removeClass('ui-state-working');
    }
  );
};

EEAReferenceBrowser.Basket.prototype = {
  trash_icon: function(){
    var trash = jQuery('<div>').addClass('ui-icon')
                               .addClass('ui-icon-trash')
                               .addClass('ui-icon-basket-trash')
                               .text('X');
    trash.click(function(){
      var self = jQuery(this);
      self.parent().slideUp(function(){
        jQuery(this).remove();
      });
    });
    return trash;
  },

  basket_add_clicked: function(data){
    var url = data.url;
    var last_slash = url.lastIndexOf('/');
    var query = {};
    query.mode = 'edit';
    query.field = this.parent.name;
    url = url.slice(0, last_slash);
    var self = this;
    jQuery(self.parent.events).trigger(self.parent.events.AJAX_START);
    jQuery.get(url + '/@@eeareferencebrowser-popup-selecteditem.html', query, function(data){
      self.basket_add(data);
      jQuery(self.parent.events).trigger(self.parent.events.AJAX_STOP);
    });
  },

  basket_add: function(data){
    var data_dom = jQuery(data);
    var uid = jQuery('input[type=checkbox]', data_dom).val();
    var exists = jQuery('input[value=' + uid + ']', this.context);
    if(exists.length){
      var parent = exists.parent();
      parent.addClass('ui-pulsate-item');
      parent.effect('pulsate', {}, 200, function(){
        jQuery(this).removeClass('ui-pulsate-item');
      });
    }else{
      data_dom.prepend(this.trash_icon());
      jQuery('.eea-ref-selecteditems', this.context).append(data_dom);
    }
  }
};

EEAReferenceBrowser.Widget = function(name){
  this.name = name;
  this.context = jQuery('#' + name + "-widget");
  this.popup = jQuery('#' + name + '-popup', this.context);
  this.workspace = jQuery('.popup-tabs' , this.popup);
  this.basket = null;
  this.button = jQuery('input[type=button]', this.context);
  this.current_tab = null;

  this.events = new EEAReferenceBrowser.Events();
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
      'Save': function(){
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

  // Basket
  var basket = jQuery('.popup-selected-items', this.popup);
  this.basket = new EEAReferenceBrowser.Basket(basket, this);

  // Add button
  this.button.click(function(){
    js_context.popup.dialog('open');
    jQuery(Faceted.Events).trigger(Faceted.Events.WINDOW_WIDTH_CHANGED);
  });
};

EEAReferenceBrowser.Widget.prototype = {
  tab_selected: function(ui){
    this.current_tab = new EEAReferenceBrowser.Tab(ui, this);
  }
};
