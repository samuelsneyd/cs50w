'use strict';
const button = document.querySelector('button');
const counter = document.querySelector('h1');

button.addEventListener('click', () => {
    counter.innerHTML = parseInt(counter.innerHTML) + 1;
});
