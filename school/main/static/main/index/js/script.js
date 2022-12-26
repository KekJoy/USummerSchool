window.addEventListener('DOMContentLoaded', function () {
    $(".accordion").accordion({
        heightStyle: "content",
        collapsible: true,
        active: false
      });
});


var boxes = document.getElementsByClassName('program__list-items');
var height = 0;

for( var i = 0; i < boxes.length; i++ ){
    var current_height = boxes[i].offsetHeight;
    if(current_height > height) {
        height = current_height;
    }        
}

for( var i = 0; i < boxes.length; i++ ){
    boxes[i].style.height = (height - 30) + 'px';
}


var acc = document.getElementsByClassName("accordions");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    } 
  });
}


let buttons = document.querySelectorAll('.accordions');

for (let button of buttons) {
    button.onclick = function() {
        if (button.classList.contains('activ')) {
            button.classList.remove('activ');
            but = button.querySelector('.data__more');
            but.text = 'Подробнее';
        }
        else {
            button.classList.add('activ');
            but = button.querySelector('.data__more');
            but.text = 'Скрыть';
        }
    }
}

