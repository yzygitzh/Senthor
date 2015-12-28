var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 1000 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

/* 
 * value accessor - returns the value to encode for a given data object.
 * scale - maps value to a visual display encoding, such as a pixel position.
 * map function - maps from data value to display value
 * axis - sets up axis
 */ 

// setup x 
var xValue = function(d) { return d.appeartime;}, // data -> value
    // xScale = d3.scale.linear().range([0, width]), // value -> display
    xScale = d3.time.scale().range([0, width]),
    xMap = function(d) { return xScale(xValue(d));}, // data -> display
    xAxis = d3.svg.axis().scale(xScale).orient("bottom").ticks(5).tickFormat(d3.time.format("%x %H:%M"));

// setup y
var yValue = function(d) { return d.pole;}, // data -> value
    yScale = d3.scale.linear().range([height, 0]), // value -> display
    yMap = function(d) { return yScale(yValue(d));}, // data -> display
    yAxis = d3.svg.axis().scale(yScale).orient("left").ticks(5);

// setup fill color
var cValue = function(d) { return d["source"];},
    color = d3.scale.category10();

// add the graph canvas to the body of the webpage
var svgScatter = d3.select("#scatterChart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  	.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// add the tooltip area to the webpage
var tooltip = d3.select("#scatterChart").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

 

function ScatterPlot(a) {
	// var demo = "<h5><small>Total:&nbsp" + a.length + "&nbsp news!</small></h5>";   	
	// if (a.length < 1)
	// 	demo = "Sorry, not found! :( </br> Try other keywords please! </br>"
	// for (var i = 0; i < a.length; i++){
	// 	demo += "<blockquote>";
	// 	demo += "pole: " + JSON.stringify(a[i]["pole"]) + "</br>";
	// 	demo += "<small>appeartime: " + JSON.stringify(a[i]["appeartime"]) + "</br>";
	// 	demo += "source: " + a[i]["source"] + "</br>";
	// 	demo += "link: " + (a[i]["link"]) + "</small></blockquote></br></br>";    		
	// }
	// document.getElementById("hist").innerHTML = demo;  
	// don't want dots overlapping axis, so add in buffer to data domain
	document.getElementById("scatterChart").innerHTML="";
	// add the graph canvas to the body of the webpage
	var svgScatter = d3.select("#scatterChart").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  	.append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	// add the tooltip area to the webpage
	var tooltip = d3.select("#scatterChart").append("div")
	    .attr("class", "tooltip")
	    .style("opacity", 0);
	var data = [];
	for (var i = 0; i < a.length; i++) {
		var myDate=a[i]["appeartime"];
		var newDate=myDate[0]+"/"+myDate[1]+"/"+myDate[2]+" "+myDate[3]+":"+myDate[4]+":"+myDate[5];
		newDate = new Date(newDate).getTime();
		var curTime = newDate;
		for (var j = 0; j < a[i]["pole"].length; j++) {
			var tmp_data = {};
			tmp_data["appeartime"] = +curTime;
			tmp_data["source"] = a[i]["source"];
			tmp_data["pole"] = +a[i]["pole"][j];
			data.push(tmp_data);
			curTime += 3600;
		}
	}
	console.log(data);
	console.log(d3.min(data, function(d) { return d.appeartime; }));
  	console.log(d3.max(data, function(d) { return d.appeartime; }));
  	console.log(d3.min(data, function(d) { return d.pole; }));
  	console.log(d3.max(data, function(d) { return d.pole; }));
	// xScale.domain(d3.extent(data, function(d) { return d.appeartime; }));
	// yScale.domain(d3.extent(data, function(d) { return d.pole; }));
	xScale.domain([d3.min(data, xValue)-1, d3.max(data, xValue)+1]);
	yScale.domain([-1, 1]);

	// x-axis
	svgScatter.append("g")
	  .attr("class", "x axis")
	  .attr("transform", "translate(0," + height + ")")
	  .call(xAxis)
	.append("text")
	  .attr("class", "label")
	  .attr("x", width)
	  .attr("y", -6)
	  .style("text-anchor", "end")
	  .text("Time");

	// y-axis
	svgScatter.append("g")
	  .attr("class", "y axis")
	  .call(yAxis)
	.append("text")
	  .attr("class", "label")
	  .attr("transform", "rotate(-90)")
	  .attr("y", 6)
	  .attr("dy", ".71em")
	  .style("text-anchor", "end")
	  .text("Polarity");

	// draw dots
	svgScatter.selectAll(".dot")
	  .data(data)
	  .enter().append("circle")
	  .attr("class", "dot")
	  .attr("r", 5)
	  .attr("cx", xMap)
	  .attr("cy", yMap)
	  .style("fill", function(d) { return color(cValue(d));}) 
	  .on("mouseover", function(d) {
	      tooltip.transition()
	           .duration(200)
	           .style("opacity", .9);
	      tooltip.html(d["source"] + "<br/> (" + xValue(d) 
	        + ", " + yValue(d) + ")")
	           .style("left", (d3.event.pageX + 5) + "px")
	           .style("top", (d3.event.pageY - 28) + "px");
	  })
	  .on("mouseout", function(d) {
	      tooltip.transition()
	           .duration(500)
	           .style("opacity", 0);
	  });

	// draw legend
	var legend = svgScatter.selectAll(".legend")
	  .data(color.domain())
	.enter().append("g")
	  .attr("class", "legend")
	  .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

	// draw legend colored rectangles
	legend.append("rect")
	  .attr("x", width - 18)
	  .attr("width", 18)
	  .attr("height", 18)
	  .style("fill", color);

	// draw legend text
	legend.append("text")
	  .attr("x", width - 24)
	  .attr("y", 9)
	  .attr("dy", ".35em")
	  .style("text-anchor", "end")
	  .text(function(d) { return d;})


	return false;  	
}