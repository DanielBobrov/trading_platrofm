$(document).ready(function(){
    $('.login').keyup(function(){
        var value = this.value;
        if (value === "") {
            let submit = document.getElementById("form_submit");
            submit.classList.add("no_login");
            if (submit.classList.length == 0) {
                submit.type = "submit";
            } else {
                submit.type = "button";
            }
        } else {
            let submit = document.getElementById("form_submit");
            submit.classList.remove("no_login");
            if (submit.classList.length == 0) {
                submit.type = "submit";
            } else {
                submit.type = "button";
            }
        }
    });
    $('.password').keyup(function(){
        var value = this.value;
        if (value === "") {
            let submit = document.getElementById("form_submit");
            submit.classList.add("no_password");
            if (submit.classList.length == 0) {
                submit.type = "submit";
            } else {
                submit.type = "button";
            }
        } else {
            let submit = document.getElementById("form_submit");
            submit.classList.remove("no_password");
            if (submit.classList.length == 0) {
                submit.type = "submit";
            } else {
                submit.type = "button";
            }
        }
    });
  });


const buttonLogin = document.querySelector('.button_login');
const background = document.querySelector('.background');

buttonLogin.addEventListener('click', () => {
  background.classList.remove("hidden");
});

background.addEventListener('click', (event) => {
  if (event.target === background) {
    background.classList.add("hidden");
  }
});