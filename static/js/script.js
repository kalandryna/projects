let form = document.querySelector('form');

form.addEventListener('submit', MyFunction);

function MyFunction(event) {
let option = document.querySelector('option');

if (option.disabled && option.selected) {
    event.preventDefault();
}};

// used w3schools for this piece of code
$(document).ready(function(){
    $('[data-toggle="popover"]').popover();
  });

