let height = document.documentElement.clientHeight;
let body = document.querySelector("body");
if (body.style.height < height) {
    body.style.height = height + 'px';
}


$(document).ready(function(){
    $('.title').keyup(function(){
        var value = this.value;
        if (value === "") {
            let submit = document.getElementById("submit");
            submit.classList.add("no_title")
            if (submit.classList.length == 0) {
                submit.type = "submit";
            } else {
                submit.type = "button";
            }
        } else {
            let submit = document.getElementById("submit");
            submit.classList.remove("no_title")
            if (submit.classList.length == 0) {
                submit.type = "submit";
            } else {
                submit.type = "button";
            }
        }
    });
    $('.description').keyup(function(){
        var value = this.value;
        if (value === "") {
            let submit = document.getElementById("submit");
            submit.classList.add("no_description")
            if (submit.classList.length == 0) {
                submit.type = "submit";
            } else {
                submit.type = "button";
            }
        } else {
            let submit = document.getElementById("submit");
            submit.classList.remove("no_description")
            if (submit.classList.length == 0) {
                submit.type = "submit";
            } else {
                submit.type = "button";
            }
        }
    });
    $('.price').keyup(function(){
        var value = this.value;
        if (isNaN(value)) {
            let submit = document.getElementById("submit");
            submit.type = "button";
            submit.classList.add("invalid_price");
            if (submit.classList.length == 0) {
                submit.type = "submit";
            } else {
                submit.type = "button";
            }
        } else {
            let submit = document.getElementById("submit");
            submit.type = "submit";
            submit.classList.remove("invalid_price");
            if (submit.classList.length == 0) {
                submit.type = "submit";
            } else {
                submit.type = "button";
            }
        }
    });
  });