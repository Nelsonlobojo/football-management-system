document.getElementById('2').onclick = function changeContent() {

    var elems = document.getElementsByClassName("player");
   for (var i = 0; i < elems.length; i+= 1) {
    elems[i].src = "static/images/player1.jpeg";
    const circle = document.querySelector('.circle');
    circle.style.backgroundColor ="green";
}
}
document.getElementById('3').onclick = function changeContent() {

    var elems = document.getElementsByClassName("player");
   for (var i = 0; i < elems.length; i+= 1) {
    elems[i].src = "static/images/player5.jpeg";
    const circle = document.querySelector('.circle');
    circle.style.backgroundColor ="#6699cc";
}
}
document.getElementById('4').onclick = function changeContent() {

    var elems = document.getElementsByClassName("player");
   for (var i = 0; i < elems.length; i+= 1) {
    elems[i].src = "static/images/player6.jpeg";
    const circle = document.querySelector('.circle');
    circle.style.backgroundColor ="pink";
}
}

const hamburger = document.querySelector('#hamburger');
const header = document.querySelector('header')
const overlay = document.querySelector('.overlay');
hamburger.addEventListener('click', function(){

    if(header.classList.contains('menu')){ // Close hamburger menu
        header.classList.remove('menu')
        overlay.classList.remove('fade-in');
        overlay.classList.add('fade-out');
    }
    else { // Open hamburger menu
        header.classList.add('menu')
        overlay.classList.add('fade-in');
        overlay.classList.remove('fade-out');
    }

});

