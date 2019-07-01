export const genGradient = () => {
  var hexValues = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "a",
    "b",
    "c",
    "d",
    "e"
  ];

  function populate(a) {
    for (var i = 0; i < 6; i++) {
      var x = Math.round(Math.random() * 14);
      var y = hexValues[x];
      a += y;
    }
    return a;
  }

  var newColor1 = populate("#");
  var newColor2 = populate("#");
  var angle = Math.round(Math.random() * 360);

  var gradient =
    "linear-gradient(" + angle + "deg, " + newColor1 + ", " + newColor2 + ")";

  return gradient;
};
export const addOrRemove = (array, value) => {
  var index = array.indexOf(value);

  if (index === -1) {
    array.push(value);
  } else {
    array.splice(index, 1);
  }
};
export const arrayUnion = (arr1, arr2, equalityFunc) => {
  let union = arr1.concat(arr2);

  for (let i = 0; i < union.length; i++) {
    for (let j = i + 1; j < union.length; j++) {
      if (equalityFunc(union[i], union[j])) {
        union.splice(j, 1);
        j--;
      }
    }
  }

  return union;
};
