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

function ShowHideDiv() {
    var ddlPassport = document.getElementById("purpose");
    var dvPassport = document.getElementById("business");
    dvPassport.style.display = ddlPassport.value == "T" ? "block" : "none";
}
 

