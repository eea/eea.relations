jQuery(function($){
    var relations = $('#relatedItems').find('.visualNoMarker > div');
    var tab_panels = $(".eea-tabs-panel");
    // 13870 sort relations based on given criteria
    $("select[name='sort_by']").change(function(e) {
        var sort_parameter = e.currentTarget.value;
        relations.each(function(){
            var $this = $(this);
            var $children = $this.children().detach();
            // sort based on the data attributes set on the listing elements
            $children.sort(function(a, b) {
                return $(a).data(sort_parameter) > $(b).data(sort_parameter) ? 1 : -1;
            });
            $this.append($children);
        });
        $(window).trigger('relations.sort', sort_parameter);
    });

    $(window).bind('relations.sort', function(ev, sort_parameter) {
        tab_panels.each(function(){
            // sort items differently if we have eea-tabs present
            // this event can be bound by third party code which can supplement different
            // sorting
            var $this = $(this);
            var $listing_entries = $this.find('.photoAlbumEntry, .tileItem').detach();
            $listing_entries.sort(function(a, b) {
                return $(a).data(sort_parameter) > $(b).data(sort_parameter) ? 1 : -1;
            });
            var slice_index = 0;
            $('.page', $this).each(function(i, el){
                var $el = $(el);
                var count = $el.data('count');
                var current_index = slice_index;
                slice_index = slice_index + count;
                $el.append($listing_entries.slice(current_index, slice_index));
            });
        });
    });

});
