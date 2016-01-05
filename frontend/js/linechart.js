var margin = {top: 120, right: 140, bottom: 250, left: 60},
    width = 800 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;

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
    xAxis = d3.svg.axis().scale(xScale).orient("bottom").ticks(12).tickFormat(d3.time.format("%x %H:%M"));

// setup y
var yValue = function(d) { return d.pole;}, // data -> value
    yScale = d3.scale.linear().range([height, 0]), // value -> display
    yMap = function(d) { return yScale(yValue(d));}, // data -> display
    yAxis = d3.svg.axis().scale(yScale).orient("left").ticks(5);

// setup fill color
var cValue = function(d) { 
		return d["source"];
	},
    color = d3.scale.category10().domain(["a", "b", "c",  "d","crawler_yahoo","e", "f","g","crawler_fox","crawler_theguardian", ]);

// add the graph canvas to the body of the webpage
var svgLine = d3.select("#lineChart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  	.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// add the tooltip area to the webpage
var tooltip = d3.select("#lineChart").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

var line = d3.svg.line()
	.x(function(d) { 
		return xScale(xValue(d));; //利用尺度運算資料索引，傳回x的位置
	})
	.y(function(d) { 
		return yScale(yValue(d));; //利用尺度運算資料的值，傳回y的位置
	}); 

function LineChart(a) {

	// don't want dots overlapping axis, so add in buffer to data domain
	document.getElementById("lineChart").innerHTML="";
	// add the graph canvas to the body of the webpage
	var svgLine = d3.select("#lineChart").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  	.append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	// add the tooltip area to the webpage
	var tooltip = d3.select("#lineChart").append("div")
	    .attr("class", "tooltip")
	    .style("opacity", 0);
	var data = [];
	for (var i = 0; i < a.length; i++) {
		var myDate=a[i]["appeartime"];
		var newDate=myDate[0]+"/"+myDate[1]+"/"+myDate[2]+" "+myDate[3]+":"+myDate[4]+":"+myDate[5];
		newDate = new Date(newDate).getTime();
		var curTime = newDate;
		var lineData = [];
		for (var j = 0; j < a[i]["pole"].length && j < 72; j++) {
			if (a[i]["pole"].length < 24)
				break;
			if (Math.abs(a[i]["pole"][j] - 0) < 0.001 )
				continue;
			var tmp_data = {};
			tmp_data["appeartime"] = +curTime;
			tmp_data["source"] = a[i]["source"];
			tmp_data["pole"] = +a[i]["pole"][j];
			data.push(tmp_data);
			lineData.push(tmp_data);
			curTime += 3600000;
		}
	}

	// xScale.domain(d3.extent(data, function(d) { return d.appeartime; }));
	// yScale.domain(d3.extent(data, function(d) { return d.pole; }));
	xScale.domain([d3.min(data, xValue)-3600000, d3.max(data, xValue)+36000000]);
	//yScale.domain([-1, 1]);
	yScale.domain([d3.min(data, yValue)-0.05, d3.max(data, yValue)+0.05]);


  svgLine.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
	  .selectAll("text")
	  .style("text-anchor", "end")
	  .attr("dx", "-.8em")
      .attr("dy", ".15em")
	  .attr("transform", function(d) {
	    	return "rotate(-65)" 
	    })
    .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("Time");

	// y-axis
	svgLine.append("g")
	  .attr("class", "y axis")
	  .call(yAxis)
	.append("text")
	  .attr("class", "label")
	  .attr("transform", "rotate(-90)")
	  .attr("y", 6)
	  .attr("dy", ".71em")
	  .style("text-anchor", "end")
	  .text("Polarity");

	// draw lines
	for (var i = 0; i < a.length; i++) {
		var myDate=a[i]["appeartime"];
		var newDate=myDate[0]+"/"+myDate[1]+"/"+myDate[2]+" "+myDate[3]+":"+myDate[4]+":"+myDate[5];
		newDate = new Date(newDate).getTime();
		var curTime = newDate;
		var lineData = [];
		for (var j = 0; j < a[i]["pole"].length && j < 72; j++) {
			if (a[i]["pole"].length < 24)
				break;
			if (Math.abs(a[i]["pole"][j] - 0) < 0.001 )
				continue;
			var tmp_data = {};
			tmp_data["appeartime"] = +curTime;
			tmp_data["source"] = a[i]["source"];
			tmp_data["pole"] = +a[i]["pole"][j];
			data.push(tmp_data);
			lineData.push(tmp_data);
			curTime += 3600000;
		}
		console.log(lineData);

		var onepath = svgLine.append("path")
			.datum(lineData)
			.attr("class", "line")
			.attr('d', line)
			.attr("stroke-width", 3)
			.style("opacity", 0.8)
			.attr("fill", "none");
		if (a[i]["source"] == "crawler_yahoo") {
			onepath.style("stroke", color("crawler_yahoo"));
		}
		if (a[i]["source"] == "crawler_theguardian") {
			onepath.style("stroke", color("crawler_theguardian"));
		}
		if (a[i]["source"] == "crawler_fox") {
			onepath.style("stroke", color("crawler_fox"));
		}
	}


	// draw dots
	// svgLine.selectAll(".dot")
	//   .data(data)
	//   .enter().append("circle")
	//   .attr("class", "dot")
	//   .attr("r", 1.5)
	//   .attr("cx", xMap)
	//   .attr("cy", yMap)
	//   .style("fill", function(d) { return color(cValue(d));}) 
	//   .style("opacity", 0.8)
	//   .on("mouseover", function(d) {
	//       tooltip.transition()
	//            .duration(200)
	//            .style("opacity", .9);
	//       tooltip.html(d["source"] + "<br/> (" + (new Date(xValue(d)))
	//         + ", " + yValue(d) + ")")
	//            .style("left", (d3.event.pageX + 5) + "px")
	//            .style("top", (d3.event.pageY - 28) + "px");
	//   })
	//   .on("mouseout", function(d) {
	//       tooltip.transition()
	//            .duration(500)
	//            .style("opacity", 0);
	//   });

	// draw legend
	var legend = svgLine.selectAll(".legend")
	  .data(["crawler_yahoo", "crawler_theguardian", "crawler_fox"])
	.enter().append("g")
	  .attr("class", "legend")
	  .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

	// draw legend colored rectangles
	legend.append("rect")
	  .attr("x", width - 18)
	  .attr("y", -100)
	  .attr("dy", ".35em")
	  .attr("width", 18)
	  .attr("height", 18)
	  .style("fill", color)
	  .style("opacity", 0.8);

	// draw legend text
	legend.append("text")
	  .attr("x", width - 24)
	  .attr("y", -90)
	  .attr("dy", ".35em")
	  .style("text-anchor", "end")
	  .text(function(d) { return d;})

	return false;  	
}