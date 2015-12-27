// $('#id1').submit(function () {
// 	    var demo = "<h5><small>Total:&nbsp" + a.length + "&nbsp news!</small></h5>";   	
//     	if (a.length < 1)
//     		demo = "Sorry, not found! :( </br> Try other keywords please! </br>"
//     	for (var i = 0; i < a.length; i++){
//     		demo += "<blockquote>";
//     		demo += "pole: " + JSON.stringify(a[i]["pole"]) + "</br>";
//     		demo += "<small>appeartime: " + JSON.stringify(a[i]["appeartime"]) + "</br>";
//     		demo += "source: " + a[i]["source"] + "</br>";
//     		demo += "link: " + (a[i]["link"]) + "</small></blockquote></br></br>";    		
//     	}
// 		document.getElementById("hist").innerHTML = demo;
// 		return false;
// });

function ScatterPlot(a) {
	var demo = "<h5><small>Total:&nbsp" + a.length + "&nbsp news!</small></h5>";   	
	if (a.length < 1)
		demo = "Sorry, not found! :( </br> Try other keywords please! </br>"
	for (var i = 0; i < a.length; i++){
		demo += "<blockquote>";
		demo += "pole: " + JSON.stringify(a[i]["pole"]) + "</br>";
		demo += "<small>appeartime: " + JSON.stringify(a[i]["appeartime"]) + "</br>";
		demo += "source: " + a[i]["source"] + "</br>";
		demo += "link: " + (a[i]["link"]) + "</small></blockquote></br></br>";    		
	}
	document.getElementById("hist").innerHTML = demo;  
	return false;  	
}