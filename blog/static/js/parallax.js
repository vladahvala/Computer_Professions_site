document.addEventListener('DOMContentLoaded', function() {
    var elemsSidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(elemsSidenav, {});

    var elemsParallax = document.querySelectorAll('.parallax');
    var instancesParallax = M.Parallax.init(elemsParallax, {});
});
