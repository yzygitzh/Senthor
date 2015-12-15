d3.selectAll("p").style("color", "red"); 
//var dataset = [ 5, 10, 15, 20, 25 ];
var dataset = [];                        //Initialize empty array
for (var i = 0; i < 25; i++) {           //Loop 25 times
    var newNumber = Math.random() * 30;  //New random number (0-30)
    dataset.push(newNumber);             //Add new number to array
}

// d3.select("body").selectAll("p")
// 	.data(dataset)
// 	.enter()
// 	.append("p")
// 	.text(function(d) {return "I can count up to " + d;})
// 	.style("color", function(d) {
// 	    if (d > 15) {   //Threshold of 15
// 	        return "red";
// 	    } else {
// 	        return "blue";
// 	    }
// 	});

d3.select("body").selectAll("div")
    .data(dataset)
    .enter()
    .append("div")
    .attr("class", "bar")
    .style("height", function(d) {
    	return d*10 + "px";
	})
	.style("width", "20px")
	.style("color", "red");
