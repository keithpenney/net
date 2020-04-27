// ECMAScript 2015 getters and setters

class SneakyFish {
  constructor(name, weight) {
    this.name = name;
    this._weight = weight;      // Here we mangle the name 'weight' so it doesn't get
  }                             // clobbered by the getters/setters

  get weight() {
    return this._weight;        // We won't modify the getter in this example
  }                             // Apparently this don't need a ';'

  set weight(newWeight) {
    newWeight = Number(newWeight);  // We'll sanitize the input a little
    this._weight = Math.abs(newWeight); // Can't have a negative weight, can we?
  }                             // This neither...
}

let martin = new SneakyFish("Martin", 5);
console.log(`${martin.name} weighs ${martin.weight}lbs.`);

martin.weight = "-25";          // This input should be sanitized.
console.log(`Ol' ${martin.name} got fat and now weighs ${martin.weight}lbs!`);
