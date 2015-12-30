var data = '[{"link": "linkt2", "pole": [0.5, 0.5], "extract": "Cellphone google apple android...", "source": "crawler_yahoo", "title": "t2"}, {"link": "linkt3", "pole": [0.5, 0.5], "extract": "Cellphone microsoft windows phone ...", "source": "crawler_yahoo", "title": "t3"}]';
var a = JSON.parse(data);
console.log(a[0]["link"]);
LOCAL = "http://127.0.0.1:27015";
REMOTE = "http://104.236.131.71:27015"; 
TARGET = REMOTE;

function NewsComment(a) {
	var demo = "<h5><small>Total:&nbsp" + a.length + "&nbsp news...</small></h5>";   	
	if (a.length < 1)
		demo = "Sorry, not found! :( </br> Try other keywords please! </br>"
	for (var i = 0; i < a.length; i++){
		demo += "<h6><a href=\"" + a[i]["link"] + "\" target=\"_blank\">" + a[i]["title"] + "</a></h6>";
		demo += "<blockquote><p>" + a[i]["extract"] + "</br>";

		var myDate=a[i]["appeartime"];
		var newDate=myDate[0]+"/"+myDate[1]+"/"+myDate[2]+" "+myDate[3]+":"+myDate[4]+":"+myDate[5];
		newDate = new Date(newDate);
		demo += "<small>appeartime: " + newDate + "</br>";
		demo += "source: " + a[i]["source"] + "</small></p></blockquote></br>";
		console.log(a[i]);	    		
	}
	document.getElementById("new").innerHTML = demo;
	console.log("Return data is " + a[0]);
	return false;
}

function formSubmit() {
	var value = document.getElementById("id2").value
	console.log(value)
	$.get(TARGET, {method:"demo", id:value}, function(data,status){
		var decodeData = decodeURIComponent(encodeURI(data));
		decodeData = unescape(decodeData.replace(/\\u/g, "%u"));
		console.log(decodeData);
		a = JSON.parse(decodeData);
		NewsComment(a);	// present news in "news" tab
		ScatterPlot(a);	// present scatter char in "scatter" tab
	});
	return false;
 }
