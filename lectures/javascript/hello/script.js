const nameInput = document.querySelector('#submit-name');
const buttons = document.querySelectorAll('button');

buttons.forEach((button) => {
    button.addEventListener('click', () => {
        alert('Hello, world');
    })
});

nameInput.addEventListener('click', () => {
    const name = document.querySelector('#name').value;
    alert(`Hello, ${name || 'world'}`);
});
