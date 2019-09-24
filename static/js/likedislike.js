
function likepost(id) {

	if(document.getElementById(id).classList.contains("btn-light"))
	{
		var xsrf = $.cookie('_xsrf')
		$.ajax({
		    type: 'POST',
		    url: '/likes',
		    data : id,
		    headers: {'X-XSRFToken' : xsrf },
		    dataType: 'text',
		    success: function(data) {
		    	document.getElementById(id).classList.remove("btn-light");
		        document.getElementById(id).classList.add("btn-primary");
		        document.getElementById(id).disabled=true;
		        alert(data);
			},
			error: function(){
				alert("ajax call failed while liking")
			}
		});	
	}
	else
	{
		var xsrf = $.cookie('_xsrf')
		$.ajax({
		    type: 'POST',
		    url: '/unlike',
		    data : id,
		    headers: {'X-XSRFToken' : xsrf },
		    dataType: 'text',
		    success: function(data) {
		        document.getElementById(id).classList.remove("btn-primary");
		        document.getElementById(id).classList.add("btn-light");
		        document.getElementById("dis"+id).disabled=false;

		        alert(data);
			},
			error: function(){
				alert("ajax call failed")
			}
		});		
	}

}


function dislikepost(id) {
	/*alert(id);*/
	if(document.getElementById(id).classList.contains("btn-light"))
	{
		var xsrf = $.cookie('_xsrf')
		$.ajax({
		    type: 'POST',
		    url: '/dislike',
		    data : id,
		    headers: {'X-XSRFToken' : xsrf },
		    dataType: 'text',
		    success: function(data) {
		    	document.getElementById(id).classList.remove("btn-light");
		        document.getElementById(id).classList.add("btn-primary");
		        document.getElementById(id).disabled=true;
		        alert(data);
			},
			error: function(){
				alert("ajax call failed while liking")
			}
		});	
	}
	else
	{
		var xsrf = $.cookie('_xsrf')
		$.ajax({
		    type: 'POST',
		    url: '/undo_dislike',
		    data : id,
		    headers: {'X-XSRFToken' : xsrf },
		    dataType: 'text',
		    success: function(data) {
		        document.getElementById(id).classList.remove("btn-primary");
		        document.getElementById(id).classList.add("btn-light");
		        document.getElementById(id).disabled=false;
		        alert(data);
			},
			error: function(){
				alert("ajax call failed")
			}
		});		
	}

}