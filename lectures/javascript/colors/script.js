'use strict';

const heading = document.querySelector('#heading');
const buttons = document.querySelectorAll('button');
const select = document.querySelector('select');

buttons.forEach((button) => {
    button.addEventListener('click', () => {
        heading.style.color = button.id;
    });
});

// Cannot use arrow function here
select.addEventListener('change', function() {
    heading.style.color = this.value;
    alert(this.value);
});
