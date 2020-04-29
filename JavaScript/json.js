// A simple script to test the JSON api

let jsobj = {
  'name' : 'Keef',
  'age' : 31,
  'languages' : ['C', 'Python', 'VHDL', 'JavaScript']
  }

function printObj(m) {
  let s = '' + m['name'] + ' is ' + m['age'] + ' and likes';
  let l = m['languages'].length;
  for (let n = 0; n < l; n++) {
    if (n == l - 1) {
      s += ' and ' + m['languages'][n] + '.';
    } else {
      s += ' ' + m['languages'][n] + ',';
    }
  }
  console.log(s);
}

printObj(jsobj);                      // Verify data integrity

let jsonstr = JSON.stringify(jsobj);  // Convert data to JSON string

console.log(jsonstr);                 // Take a look at the string

let jsparsed = JSON.parse(jsonstr);   // Parse the string into a native JavaScript object again

printObj(jsparsed);                   // Verify parsed data integrity
