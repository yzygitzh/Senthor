//d3.selectAll("p").style("color", "red"); 
//var dataset = [ 5, 10, 15, 20, 25 ];
// var dataset = [];                        //Initialize empty array
// for (var i = 0; i < 25; i++) {           //Loop 25 times
//     var newNumber = Math.random() * 30;  //New random number (0-30)
//     dataset.push(newNumber);             //Add new number to array
// }
var dataset = [ 5, 10, 13, 19, 21, 25, 22, 18, 15, 13,
                11, 12, 15, 20, 18, 17, 16, 18, 23, 25 ];

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

var h = 100;
var w = 500;
var svg = d3.select("body")
  .append("svg")
  .attr("width", w)
  .attr("height", h);

var rects = svg.selectAll("rect")
    .data(dataset)
    .enter()
    .append("rect");

rects.attr("x", function(d, i) {
    return i * 20;  //Bar width of 20 plus 1 for padding
})
   .attr("y", function(d) {return h - d*2;})
   .attr("width", w / dataset.length - 10)
   .attr("height", function(d) {
    return d*2;
})
   .attr("fill", function(d) {
    return "rgb(0, "+ (d * 10) + "," + (d * 10) + ")";
});

svg.selectAll("text")
   .data(dataset)
   .enter()
   .append("text")
   .text(function(d) {
        return d;
   })
   .attr("x", function(d, i) {
        return i * 20;
   })
   .attr("y", function(d) {
        return h - (d * 2) + 10;
   })
   .attr("font-family", "sans-serif")
	.attr("font-size", "11px")
	.attr("fill", "white");;
