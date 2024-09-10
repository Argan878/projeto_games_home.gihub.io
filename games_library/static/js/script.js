 // Função para animar o Objeto 1
 function animarObjeto1() {
    var objeto2 = document.getElementById('objeto2');
    objeto2.classList.toggle('animate');
}

// Função para animar o Objeto 2
function animarObjeto2() {
    var objeto2 = document.getElementById('objeto2');
    objeto2.classList.toggle('animate');
}

function menuShow() {
    let menuMobile = document.querySelector('.menu-mobile');
    let icon = document.querySelector('.icon');
    if (menuMobile.classList.contains('open')) {
        menuMobile.classList.remove('open');
        icon.src = "/static/img/menu_white_36dp.svg"; // Use o caminho correto aqui
    } else {
        menuMobile.classList.add('open');
        icon.src = "/static/img/close_white_36dp.svg"; // Caminho correto para a imagem de fechar
    }
}