function block_ui() {
return;
    (function($) {
     var w = jQuery(window)
     var scr_x = w.scrollLeft();
     var scr_y = w.scrollTop();
     var dim_x = w.width();
     var dim_y = w.height();

     var overlay = jQuery('<div>');
     overlay.addClass('specification-overlay');

     var loading = jQuery('<div>');
     loading.addClass('specification-loading');

     loading.css({
         'top':dim_y/2-50 + scr_y + 'px',
         'left':dim_x/2-50 + scr_x + 'px',
         'z-index':2001
         });
     overlay.css({
         'top':scr_y+'px',
         'left':scr_x+'px',
         'z-index':2000,
         'width':dim_x+'px',
         'height':dim_y+'px',
         // 'background-color':'white',
         position:'absolute'
         });

     jQuery('body').append(overlay);
     jQuery('body').append(loading);
     overlay.show();
     loading.show();
    })(jQuery);
}

function unblock_ui(){
return;
  jQuery('.specification-overlay').remove();
  jQuery('.specification-loading').remove();
}


function init_tinymce(el){
  // init tinymce edit fields
(function($) {
  $('.mce_editable', el).each(function(){
    var id = $(this).attr('id');

    var config = new TinyMCEConfig(id);
    // TODO: resize tinymce to a more decent size
    config.widget_config.editor_height = 800;
    //config.widget_config.autoresize = true;
    //config.widget_config.resizing = false;
    config.widget_config.resizing_use_cookie = false;
    config.widget_config.buttons = [
      "save",
      "style",
      "bold",
      "italic",
      "justifyleft",
      "justifycenter",
      "justifyright",
      "justifyfull",
      "bullist",
      "numlist",
      "definitionlist",
      "outdent",
      "indent",
      //"image",
      "link",
      "unlink",
      "anchor",
      //"tablecontrols",
      "code",
      "fullscreen",
      ""
    ];
    config.widget_config.styles = [
      "Invisible grid|table|invisible",
      "Fancy listing|table|listing",
      "Fancy grid listing|table|grid listing",
      "Fancy vertical listing|table|vertical listing",
      "Literal|pre",
      "Discreet|span|discreet",
      "Pull-quote|blockquote|pullquote",
      "Call-out|p|callout",
      "Highlight|span|visualHighlight",
      "Disc|ul|listTypeDisc",
      "Square|ul|listTypeSquare",
      "Circle|ul|listTypeCircle",
      "Numbers|ol|listTypeDecimal",
      "Lower Alpha|ol|listTypeLowerAlpha",
      "Upper Alpha|ol|listTypeUpperAlpha",
      "Lower Roman|ol|listTypeLowerRoman",
      "Upper Roman|ol|listTypeUpperRoman",
      "Definition term|dt",
      "Definition description|dd",
      "Odd row|tr|odd",
      "Even row|tr|even",
      "Heading cell|th|",
      "Page break (print only)|div|pageBreak",
      "Clear floats|div|visualClear"
    ];
    delete InitializedTinyMCEInstances[id];
    config.init();
  });
})(jQuery);
}


function schemata_ajaxify(el){
        //console.info("doing schemata ajaxify");

    (function($) {
      //set_actives();
      //init_tinymce(el);

      //set the tags widget
      var widgets = $('.ArchetypesKeywordWidget');
      if(widgets.length){
        widgets.eeatags();
      }


      $("form", el).submit(
        function(e){
          block_ui();
          tinyMCE.triggerSave();
          var form = this;

          var inputs = [];
          $(".widgets-list .widget-name").each(function(){
            inputs.push($(this).text());
          });

          var data = "";
          data = $(form).serialize();
          // data += "&_active_region=" + active_region;
          data += "&form_submit=Save&form.submitted=1";
            //console.info("doing ajax schemata ajaxify");

          $.ajax({
            "data": data,
            url: this.action,
            type:'POST',
            cache:false,
            // timeout: 2000,
            error: function() {
              unblock_ui();
              alert("Failed to submit");
            },
            success: function(r) {
              $(el).html(r);
              schemata_ajaxify(el);
              unblock_ui();
              return false;
            }
          });
          return false;
        });
    })(jQuery);
}


function dialog_edit(url, title, callback, options){
      // Opens a modal dialog with the given title

    (function($) {
      block_ui();
      options = options || {
        'height':null,
        'width':800
      };
      var target = $('#dialog_edit_target');
      $("#dialog-inner").remove();     // temporary, apply real fix
      $(target).append("<div id='dialog-inner'></div>");
      window.onbeforeunload = null; // this disables the form unloaders
      $("#dialog-inner").dialog({
        modal         : true,
        width         : options.width,
        minWidth      : options.width,
        height        : options.height,
        minHeight     : options.height,
        'title'       : title,
        closeOnEscape : true,
        buttons: {
          'Save':function(e){
            var button = e.target;
            $("#dialog-inner form").trigger('submit');
          },
          'Cancel':function(e){
            $("#dialog-inner").dialog("close");
          }
        },
        beforeclose:function(event, ui){ return true; }
      });

      $.ajax({
        'url':url,
        'type':'GET',
        'cache':false,
        'success': function(r){
          console.log("success");
          console.log(r);
          console.log($("#dialog-inner"));
          $("#dialog-inner").html(r);
          //set_inout($("#archetypes-fieldname-themes"));
          callback();
        }
      });
    })(jQuery);
}


function set_creators(){
    // Set handlers for Create buttons

    (function($) {
      $('a.new_content_creator').live('click', function(){
        block_ui();
        var link = $(this).attr('href');
        console.log(link);
        var portal_type = "";
        var title = "Edit new " + portal_type;    // should insert portal type here
        var options = {
          'width':800,
          'height':600
        };
        console.info("doing ajax set creators");
        dialog_edit(link, title, 
                function(text, status, xhr){
                    alert("callback");
                    console.log("got response from ajax");
                    schemata_ajaxify($("#dialog-inner"));   //set someid
                    unblock_ui();
                    console.log("unblocked ui");
                },
                options);

        return false;
      });
    })(jQuery);
}

set_creators();

