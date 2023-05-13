let menu = document.getElementById('menu__celular');
let nav = document.getElementById("open");
nav.addEventListener('click', e => {
  menu.classList.toggle('mostrar');
});