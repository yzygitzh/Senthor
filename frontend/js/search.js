var data = '[{"link": "linkt2", "pole": [0.5, 0.5], "extract": "Cellphone google apple android...", "source": "crawler_yahoo", "title": "t2"}, {"link": "linkt3", "pole": [0.5, 0.5], "extract": "Cellphone microsoft windows phone ...", "source": "crawler_yahoo", "title": "t3"}]'
var a = JSON.parse(data)
console.log(a[0]["link"])
LOCAL = "http://127.0.0.1:27015";
REMOTE = "http://104.236.131.71:27015"; 
TARGET = REMOTE;


function keywordSearch(args){
	//alert(args.keyword.value);
	var value = args.keyword.value
	console.log("Catch value is "+value);
	console.log("[ATTENTION]: Target is " + TARGET);
  	$.get(TARGET, {method:"demo", id:value}, function(data,status){
    	var decodeData = decodeURI(data);
    	console.log(decodeData);
    	var a = JSON.parse(decodeData);
    	var demo = "Examples: </br>";
    	for (var i = 0; i < a.length; i++){
    		demo += JSON.stringify(a[i]) + "</br></br>";
    		console.log(a[i]);				    		
    	}

    	document.getElementById("new").innerHTML = demo;
    	console.log("Return data is " + a[0]);
  	});
  	return false;
}
$('#id1').submit(function () {
		keywordSearch(this);
		return false;
});