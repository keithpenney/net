// A quick JavaScript exploration of inheritance pre-ECMAScript2015

function SceneObject(height, width, collidable = true) {
  this.height = height;
  this.width = width;
  this.collidable = collidable;
  this.nonsense = function() {
    console.log("Why not just define everything within the constructor?");
  };
  this.greeting = function() {
    console.log("I am merely a scene object.");
  }
}

SceneObject.prototype.nonsense = function() {
  console.log("This prototype stuff is clunky at best.");
}

function Character(name, height, width) {
  SceneObject.call(this, height, width, collidable = true);
  this.name = name;
  this.coords = [0, 0];
  this.setCoords = function(x, y) {
    this.coords[0] = x;
    this.coords[1] = y;
  };
  this.move = function(dx, dy) {
    this.coords[0] += dx;
    this.coords[1] += dy;
  };
  this.greeting = function() {
    console.log("Greetings from character " + this.name);
  }
}

// Now if we're to inherit, we need to establish this 'prototype' property before
// defining any methods on it or they will be clobbered
Character.prototype = new SceneObject();  // One syntax of doing it

Character.prototype.move2 = function(dx, dy) {
  this.coords[0] += dx;
  this.coords[1] += dy;
}

function Protagonist(name, height, width) {
  Character.call(this, name, height, width);
  this.greeting = function() {
    console.log("Never fear! " + this.name + " is here!");
  };
  this.attack = function() {
    console.log(this.name + " attacks!");
  };
}

// Again, establish the 'prototype' property
Protagonist.prototype = Object.create(Character.prototype); // An alternate syntax

console.log("Character.prototype.constructor.name = " + Character.prototype.constructor.name);
console.log("Protagonist.prototype.constructor.name = " + Protagonist.prototype.constructor.name);

// /* --- =+=+=+=+ Uncomment this line to test without constructor reassignment +=+=+=+=+=
// The below restores the 'constructor' properties which were clobbered above
Character.prototype.constructor = Character;
// Alternatively, we can use this more verbose assignment:
Object.defineProperty(Protagonist.prototype, 'constructor', {
  value: Protagonist,
  enumerable: false, // prevent it from appearing in a 'for...in' loop
  writable: true
  });
//Protagonist.prototype.constructor = Protagonist;  // This is way shorter
// --- */
console.log("Character.prototype.constructor.name = " + Character.prototype.constructor.name);
console.log("Protagonist.prototype.constructor.name = " + Protagonist.prototype.constructor.name);

const keef = new Protagonist("Keef", 100, 40);
keef.greeting();

console.log("keef.height = " + keef.height);  // Properties inherit properly?
console.log("keef.coords = " + keef.coords);

keef.setCoords(200, 400);                     // Does setCoords() inherit?
console.log("keef.coords = " + keef.coords);

keef.move(100, 100);                          // Does move() inherit?
console.log("keef.coords = " + keef.coords);

keef.nonsense();                              // Which nonsense() is inherited?

console.log("keef.move2 = " + keef.move2);    // Does move2() inherit?
keef.move2(100, 100);
console.log("keef.coords = " + keef.coords);

const cecee = new keef.constructor("Cecee", 200, 80);
cecee.greeting();
 