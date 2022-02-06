const buttons = document.querySelectorAll('button');
const pages = document.querySelectorAll('div');

function showPage(page) {
  pages.forEach((page) => {
    page.style.display = 'none';
  });
  document.querySelector(`#${page}`).style.display = 'block';
}

buttons.forEach((button) => {
  button.addEventListener('click', () => {
    const page = button.dataset.page;
    showPage(page);
  });
});
