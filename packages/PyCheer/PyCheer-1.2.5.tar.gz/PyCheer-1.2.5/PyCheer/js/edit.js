function save()
{
	var bottom_div=document.getElementById("main-control2").contentWindow.document.getElementById("bottom_div");
	var left_span=document.getElementById("main-control2").contentWindow.document.getElementById("left-span");
	bottom_div.style.background="#0033FF";
	left_span.innerHTML="￥{LanguageCode:3001}￥";
	editor=ace.edit("editor");
	var save_value=editor.getValue();
	console.log(save_value);
	var send_value=encodeURIComponent(save_value);
	//console.log(GetQueryString("path"));
	try
	{
	    axios.post("/save?path="+encodeURIComponent(GetQueryString("path")),data=send_value).
		then(function(response)
			{
				console.log(response);
				if(response.status==200)
				{
					bottom_div.style.background="#38b400";
					left_span.innerHTML="￥{LanguageCode:3002}￥";
				}
				else
				{
					bottom_div.style.background="red";
					left_span.innerHTML="￥{LanguageCode:3003}￥";
				}
			}
		);
	}
	catch(err)
	{
	    bottom_div.style.background="red";
		left_span.innerHTML="￥{LanguageCode:3003}￥";
	}
}