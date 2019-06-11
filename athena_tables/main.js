var data;

$(document).ready(function() {
  $.when($.getJSON({url: "http://127.0.0.1:5000/athena_tables/hello"}))
    .done(function() {
      data = Array.prototype.slice.call(arguments)[0];
      loadCharts(data["chart1"]);
    });

} );

function loadCharts(cobj) {
  var container = $('<div style="width: 5800px; height: 400px; margin: 0 auto"></div>');
//  var container = $('<div style="overflow:auto"></div>');
//  var container = $('<div ></div>');
  $(document.body).append(container);

  container.highcharts(cobj);
}
