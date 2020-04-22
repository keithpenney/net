// regview.js

// An attempt to port a useful Python utility to JavaScript
// for purely academic purposes

/*
output (depending on which ezbinXX() function is used:
    MSB -> LSB
    0000 0000 0000 0000     # For 16-bit INTEGER or most significant 2 bytes
    [0000 0000 0000 0000]   # next-most significant 2-bytes for 32-bit or 64-bit INTEGER
    [0000 0000 0000 0000]   # next-most significant 2-bytes for 64-bit INTEGER
    [0000 0000 0000 0000]   # least significant 2-bytes for 64-bit INTEGER

Note! I would not suggest using ezbin64() until I figure out
where the reduced precision comes from and how to mitigate it.
*/

function toHexChar(n) {
  var chars = ['A', 'B', 'C', 'D', 'E', 'F'];
  if ((n >= 0) & (n <= 9)) {
    return '' + n;  // Return string version of number
  } else if (n <= 15) {
    return chars[n - 10];
  } else {
    return '';
  }
}

function toBinChar(n) {
  if ((n == 0) | (n == 1)) {
    return '' + n;  // String version of the number
  }
}

function floor(n) {
  let remainder = n % 1;
  return n - remainder;
}

function hex16(h) {
  let n0, n1, n2, n3;
  n0 = h % 16;  // Least-significant nybble
  n1 = floor(h / 16) % 16;
  n2 = floor(h / 256) % 16;
  n3 = floor(h / 4096) % 16;
  return toHexChar(n3) + toHexChar(n2) + toHexChar(n1) + toHexChar(n0);
}

function bin8(h) {
  let c = [];
  for (var n = 0; n < 8; n++) {
    c.unshift(toBinChar(floor(h / (2**n)) % 2));
  }
  return c.join('')
}

function ezbin8(h) {
  let c = bin8(h);
  return c.slice(0, 4) + " " + c.slice(4);
}

function ezbin16(h) {
  let c = [];
  for (var n = 0; n < 2; n++) {
    c.unshift(ezbin8(floor(h / 256**n) % 256)); 
  }
  return c.join(' ')
}

function ezbin32(h) {
  let c = [];
  for (var n = 0; n < 2; n++) {
    c.unshift(ezbin16(floor(h / 65536**n) % 65536)); 
  }
  return c.join('\n')
}

// Don't use this one!  It looks like there's some reduced
// precision in storing integers (less than 64 bit accuracy)
function ezbin64(h) {
  let c = [];
  let d = 4294967296;
  for (var n = 0; n < 2; n++) {
    c.unshift(ezbin32(floor(h / d**n) % d)); 
  }
  return c.join('\n')
}

console.log(hex16(43981));
console.log(ezbin32(4037021450));