class Chart:

  def __init__(self):
    self.obj = {
      "chart": {
        "zoomType": "x"
      },
      "title": {
        "text": "Title of graph"
      },
      "xAxis": {
        "crosshair": True,
        "title": {
          "text": "X axis title"
        },
        "scrollbar": {
          "enabled": True
        },
      },
      "yAxis": [],
      "tooltip": {
        "shared": True,
        # "pointFormat": "{point.y:,.0f}"
      },
      "legend": {
        "layout": "horizontal",
        "align": "left"
      },
      "series": []
    }
    self.series_map = {}



  def title(self, title):
    self.obj["title"]["text"] = title
    return self

  def xcategories(self, c):
    self.obj["xAxis"]["categories"] = c
    return self

  def xtitle(self, title):
    self.obj["xAxis"]["title"]["text"] = title
    return self


  def ytitle(self, title):
    self.obj["yAxis"].append({
        "title": {
          "text": title
        },
        "format": "{value:,.0f}"
      })
    return self



  def series(self, name, data):
    series_obj = {
      "name": name,
      "type": "line",
      "data": data,
      "yAxis": len(self.obj["series"])
    }

    self.obj["series"].append(series_obj)
    self.series_map[name] = series_obj

    return self
  def add_point(self, name, data):
    if name not in self.series_map:
      self.series(name, [])
    series_obj = self.series_map[name]
    series_obj["data"].append(data)
