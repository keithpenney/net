// A simple JavaScript script to practice with classes/objects

// Create a simple class constructor
function UiItem(name, x = 0, y = 0, height = 100, width = 100) {
  this.name = name;
  this.coords = {
    x : x,
    y : y
  }
  this.dims = {
    height : height,
    width : width
  }
  this.getDims = function() {
    return this.dims;
  }
  this.setDims = function(dims) {
    this.dims = dims;
  }
  this.getName = function() {
    return this.name;
  }
  this.setName = function(name) {
    this.name = name;
  }
  this.getDescription = function() {
    var itemList = [];
    itemList.push("name = " + this.name);
    itemList.push("coords = (" + this.coords.x + "," + this.coords.y + ")");
    itemList.push("dims = (" + this.dims.height + "," + this.dims.width + ")");
    return itemList.join('\n');
  }
}

const box = new UiItem('Box', 10, 15);
const kite = new UiItem('Kite', height = 50, width = 200);

console.log(box.getDescription());
console.log(kite.getDescription());

kite.setName("bigass Kite!");
kite.setDims({height : 200, width : 800});

console.log(kite.getDescription());


