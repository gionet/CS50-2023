
let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navbar.classList.toggle('open');
}

const sr = ScrollReveal ({
    distance: '65px',
    duration: 2600,
    delay: 450,
    reset: true
});

sr.reveal('.home-content h2', {delay:200, origin:'right'});
sr.reveal('.btn-box', {delay:450, origin:'right'});
sr.reveal('.social-icons', {delay:450, origin:'bottom'});
