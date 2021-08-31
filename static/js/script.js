<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>


document.getElementById('2').onclick = function changeContent() {

    var elems = document.getElementsByClassName("player");
   for (var i = 0; i < elems.length; i+= 1) {
    elems[i].src = "static/images/player1.jpeg";
    const circle = document.querySelector('.circle');
    circle.style.backgroundColor ="#90EE90";
}
}
document.getElementById('3').onclick = function changeContent() {

    var elems = document.getElementsByClassName("player");
   for (var i = 0; i < elems.length; i+= 1) {
    elems[i].src = "static/images/player5.jpeg";
    const circle = document.querySelector('.circle');
    circle.style.backgroundColor ="	#98FB98";
}
}
document.getElementById('4').onclick = function changeContent() {

    var elems = document.getElementsByClassName("player");
   for (var i = 0; i < elems.length; i+= 1) {
    elems[i].src = "static/images/player6.jpeg";
    const circle = document.querySelector('.circle');
    circle.style.backgroundColor ="#00FA9A";
}
}

/*const hamburger = document.querySelector('#hamburger');
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

});*/


$(document).ready(function(){
    // File type validation
       $("#fileinput").change(function(){
           var match= ["image/jpeg","image/png","image/jpg","image/gif"];
           var file = this.file;
           var imagefile = file.type;
           if(!((imagefile==match[0]) || (imagefile==match[1]) || (imagefile==match[2]) || (imagefile==match[3]))){
                 alert('Please select a valid image file (JPEG/JPG/PNG/GIF).');
                 $("#fileinput").val('');
                 return false;
             }
       });
   });

