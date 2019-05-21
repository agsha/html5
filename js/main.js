
var data;

$(document).ready(function() {
  $.when($.getJSON({url: "http://127.0.0.1:5000/hello"}))
    .done(function() {
      data = Array.prototype.slice.call(arguments)[0];
      loadCharts();
    });

} );

function loadCharts() {
  var container = $('<div style="min-width: 800px; height: 400px; margin: 0 auto"></div>');
  $(document.body).append(container);

  container.highcharts(data);
}
