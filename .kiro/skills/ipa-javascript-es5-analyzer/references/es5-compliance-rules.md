# ES5 Compliance Rules for IPA JavaScript

## Critical Rule

**IPA JavaScript executes in ES5 environment. Modern ES6+ syntax causes immediate runtime errors.**

## Forbidden ES6+ Features

### 1. Variable Declarations

**FORBIDDEN:**
```javascript
let count = 0;
const MAX_VALUE = 100;
```

**REQUIRED:**
```javascript
var count = 0;
var MAX_VALUE = 100;
```

### 2. Arrow Functions

**FORBIDDEN:**
```javascript
var result = items.map(item => item.value);
var sum = numbers.reduce((acc, n) => acc + n, 0);
var filtered = data.filter(x => x.status === "Active");
```

**REQUIRED:**
```javascript
var result = [];
for (var i = 0; i < items.length; i++) {
    result.push(items[i].value);
}

var sum = 0;
for (var i = 0; i < numbers.length; i++) {
    sum += numbers[i];
}

var filtered = [];
for (var i = 0; i < data.length; i++) {
    if (data[i].status === "Active") {
        filtered.push(data[i]);
    }
}
```

### 3. Template Literals

**FORBIDDEN:**
```javascript
var message = `Hello ${name}, you have ${count} items`;
var multiline = `Line 1
Line 2
Line 3`;
```

**REQUIRED:**
```javascript
var message = "Hello " + name + ", you have " + count + " items";
var multiline = "Line 1\n" +
                "Line 2\n" +
                "Line 3";
```

### 4. Destructuring

**FORBIDDEN:**
```javascript
var {firstName, lastName} = person;
var [first, second] = array;
var {id, ...rest} = object;
```

**REQUIRED:**
```javascript
var firstName = person.firstName;
var lastName = person.lastName;

var first = array[0];
var second = array[1];

var id = object.id;
// No spread operator in ES5
```

### 5. Default Parameters

**FORBIDDEN:**
```javascript
function calculate(amount, rate = 0.05) {
    return amount * rate;
}
```

**REQUIRED:**
```javascript
function calculate(amount, rate) {
    if (typeof rate === "undefined") {
        rate = 0.05;
    }
    return amount * rate;
}
```

### 6. Spread Operator

**FORBIDDEN:**
```javascript
var combined = [...array1, ...array2];
var copy = [...original];
var obj = {...defaults, ...overrides};
```

**REQUIRED:**
```javascript
var combined = array1.concat(array2);
var copy = original.slice();
// Object spread not directly supported in ES5
var obj = {};
for (var key in defaults) {
    obj[key] = defaults[key];
}
for (var key in overrides) {
    obj[key] = overrides[key];
}
```

### 7. Classes

**FORBIDDEN:**
```javascript
class Person {
    constructor(name) {
        this.name = name;
    }
    
    greet() {
        return "Hello " + this.name;
    }
}
```

**REQUIRED:**
```javascript
function Person(name) {
    this.name = name;
}

Person.prototype.greet = function() {
    return "Hello " + this.name;
};
```

### 8. Promises and Async/Await

**FORBIDDEN:**
```javascript
async function fetchData() {
    var response = await fetch(url);
    return response.json();
}

var promise = new Promise((resolve, reject) => {
    // ...
});
```

**REQUIRED:**
```javascript
// Promises not supported in IPA ES5
// Use synchronous operations or callbacks
function fetchData(callback) {
    // Synchronous operation
    var data = getData();
    callback(data);
}
```

### 9. For...of Loops

**FORBIDDEN:**
```javascript
for (var item of items) {
    console.log(item);
}
```

**REQUIRED:**
```javascript
for (var i = 0; i < items.length; i++) {
    var item = items[i];
    console.log(item);
}
```

### 10. Object Shorthand

**FORBIDDEN:**
```javascript
var name = "John";
var age = 30;
var person = {name, age};

var obj = {
    method() {
        return "value";
    }
};
```

**REQUIRED:**
```javascript
var name = "John";
var age = 30;
var person = {name: name, age: age};

var obj = {
    method: function() {
        return "value";
    }
};
```

### 11. Computed Property Names

**FORBIDDEN:**
```javascript
var key = "dynamicKey";
var obj = {
    [key]: "value"
};
```

**REQUIRED:**
```javascript
var key = "dynamicKey";
var obj = {};
obj[key] = "value";
```

### 12. Import/Export

**FORBIDDEN:**
```javascript
import {module} from "./module";
export default MyClass;
export {function1, function2};
```

**REQUIRED:**
```javascript
// Modules not supported in IPA
// All code must be in single file or use global variables
```

## Allowed ES5 Features

### Variables
```javascript
var x = 1;
var name = "John";
var isActive = true;
var obj = {key: "value"};
var arr = [1, 2, 3];
```

### Functions
```javascript
function myFunction(param1, param2) {
    return param1 + param2;
}

var myFunc = function(param) {
    return param * 2;
};
```

### Conditionals
```javascript
if (condition) {
    // code
} else if (otherCondition) {
    // code
} else {
    // code
}

switch (value) {
    case 1:
        // code
        break;
    case 2:
        // code
        break;
    default:
        // code
}

var result = condition ? valueIfTrue : valueIfFalse;
```

### Loops
```javascript
for (var i = 0; i < array.length; i++) {
    // code
}

while (condition) {
    // code
}

do {
    // code
} while (condition);
```

### Objects and Arrays
```javascript
var obj = {
    property: "value",
    method: function() {
        return this.property;
    }
};

var arr = [1, 2, 3];
arr.push(4);
arr.pop();
arr.slice(0, 2);
arr.concat([4, 5]);
```

### String Operations
```javascript
var str = "Hello";
var upper = str.toUpperCase();
var lower = str.toLowerCase();
var sub = str.substring(0, 3);
var index = str.indexOf("l");
var replaced = str.replace("Hello", "Hi");
var split = str.split("");
var joined = arr.join(",");
```

### Type Checking
```javascript
typeof variable === "string"
typeof variable === "number"
typeof variable === "boolean"
typeof variable === "undefined"
typeof variable === "object"
typeof variable === "function"

Array.isArray(variable)
variable instanceof Object
```

### Math Operations
```javascript
Math.round(num)
Math.floor(num)
Math.ceil(num)
Math.abs(num)
Math.pow(base, exponent)
Math.sqrt(num)
Math.max(a, b, c)
Math.min(a, b, c)
```

### JSON Operations
```javascript
JSON.parse(jsonString)
JSON.stringify(object)
```

## Common Conversion Patterns

### Array.map() → for loop
```javascript
// ES6
var doubled = numbers.map(n => n * 2);

// ES5
var doubled = [];
for (var i = 0; i < numbers.length; i++) {
    doubled.push(numbers[i] * 2);
}
```

### Array.filter() → for loop
```javascript
// ES6
var active = items.filter(item => item.status === "Active");

// ES5
var active = [];
for (var i = 0; i < items.length; i++) {
    if (items[i].status === "Active") {
        active.push(items[i]);
    }
}
```

### Array.find() → for loop
```javascript
// ES6
var found = items.find(item => item.id === targetId);

// ES5
var found = null;
for (var i = 0; i < items.length; i++) {
    if (items[i].id === targetId) {
        found = items[i];
        break;
    }
}
```

### Array.reduce() → for loop
```javascript
// ES6
var sum = numbers.reduce((acc, n) => acc + n, 0);

// ES5
var sum = 0;
for (var i = 0; i < numbers.length; i++) {
    sum += numbers[i];
}
```

### Array.forEach() → for loop
```javascript
// ES6
items.forEach(item => {
    processItem(item);
});

// ES5
for (var i = 0; i < items.length; i++) {
    processItem(items[i]);
}
```

### String.includes() → indexOf()
```javascript
// ES6
if (str.includes("substring")) {
    // code
}

// ES5
if (str.indexOf("substring") !== -1) {
    // code
}
```

### String.startsWith() → indexOf()
```javascript
// ES6
if (str.startsWith("prefix")) {
    // code
}

// ES5
if (str.indexOf("prefix") === 0) {
    // code
}
```

### String.endsWith() → substring()
```javascript
// ES6
if (str.endsWith("suffix")) {
    // code
}

// ES5
if (str.substring(str.length - "suffix".length) === "suffix") {
    // code
}
```

## Validation Checklist

- [ ] No `let` or `const` declarations
- [ ] No arrow functions `() => {}`
- [ ] No template literals `` `${var}` ``
- [ ] No destructuring `{prop} = obj`
- [ ] No default parameters `function(x = 1)`
- [ ] No spread operator `...arr`
- [ ] No `class` keyword
- [ ] No `async`/`await`
- [ ] No `Promise`
- [ ] No `for...of` loops
- [ ] No object shorthand `{prop}`
- [ ] No computed property names `{[key]: value}`
- [ ] No `import`/`export`
- [ ] No ES6+ array methods without conversion
- [ ] All functions use `function` keyword
- [ ] All variables use `var`
- [ ] All strings use quotes (single or double)

