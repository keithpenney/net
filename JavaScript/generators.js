// A quick script to practice using generators in JavaScript


// Define a generator function to count up to a maximum 'max' value
// Its 'next()' method takes an optional argument to reset the counter to some arbitrary value.
function* countTo(max) {
  let i = 0;
  let v = 0;
  while (i < max) {
    v = yield i;
    if (isNaN(v)) {
      i += 1;
    } else {
      i = v;
    }
  }
  return i;
}

// Another example; an accumulator.  It initializes to value 'init' and then sums the
// arguments passed to the generator's 'next()' method.
function* accumulator(init = 0) {
  var acc = init;
  let v = 0;
  while (true) {
    v = yield acc;
    if (!isNaN(v)) {
      acc += v;
    }
  }
}

var myCounter = countTo(100);   // Create a generator object from the countTo() generator function

var v;                          // First we'll count from 0 to 19
for (var n = 0; n < 20; n++) {
    v = myCounter.next();
    console.log(v.value, v.done);
    if (v.done) {
        break;
    }
}

console.log(myCounter.next(95).value);  // Then we'll jump ahead to a count of 95

for (var n = 0; n < 10; n++) {          // Then we'll keep counting for 10 more (5 of which should be 'undefined')
    v = myCounter.next();
    console.log(v.value, v.done);
    if (v.done) {
        break;
    }
}

// Let's create an accumulator initialized to value 5
var myAcc = accumulator(5);
myAcc.next();                           // Gotta kick it off with a 'next()' call apparently

console.log(myAcc.next(1).value);       // Now let's sum some values
console.log(myAcc.next(25).value);
console.log(myAcc.next(8).value);
console.log(myAcc.next(100).value);




