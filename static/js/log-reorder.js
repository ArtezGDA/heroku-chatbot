$(document).ready(function() {
    
    var $chatLog = $('#chat-log');
    var	$sessions = $chatLog.children('div.session');
    
    $("#sort_by_start").click(function(event) {
        event.preventDefault();
        // event.stopPropagation();
        
        $sessions.sort(function(a, b) {
        	var an = a.getAttribute('data-startOrder')
            var bn = b.getAttribute('data-startOrder');

        	if(an > bn) {
        		return 1;
        	}
        	if(an < bn) {
        		return -1;
        	}
        	return 0;
        });
        
        $sessions.detach().appendTo($chatLog);
    });
    
    $("#sort_by_recent").click(function(event) {
        event.preventDefault();
        // event.stopPropagation();
        
        $sessions.sort(function(a, b) {
        	var an = a.getAttribute('data-recentOrder')
            var bn = b.getAttribute('data-recentOrder');

        	if(an > bn) {
        		return 1;
        	}
        	if(an < bn) {
        		return -1;
        	}
        	return 0;
        });

        $sessions.detach().appendTo($chatLog);
    });    
});


