
var dataset = [ 5, 11, 15, 19, 21, 23, 21, 19, 16, 12,
                8, 5, 4, 3, 5, 7, 9, 12, 16, 18 ];

var h = 150;
var svg = d3.select("#title_logo")
  .append("svg")
  .attr("width", "50%")
  .attr("height", "50%");

var rects = svg.selectAll("rect")
    .data(dataset)
    .enter()
    .append("rect");

rects.attr("x", function(d, i) {
    var a = 5 * i
    return a + "%";  
})
   .attr("y", function(d) {

    return (100 - d*3) + "%";
    })
   .attr("width", function() {
      return "4.5%"
   })
   .attr("height", function(d) {
    return (d*3) + "%";
})
   .attr("fill", function(d) {
    return "rgb(0, "+ (d * 10) + "," + (d * 10) + ")";
});
