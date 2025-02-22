document.addEventListener('DOMContentLoaded', function() {
    // Initialize dropdowns for sidenav and navbar
    var sidebarDropdowns = document.querySelectorAll('.dropdown-trigger');
    M.Dropdown.init(sidebarDropdowns, {
        outDuration: 1000,
        hover: true
    });

    var navbarDropdowns = document.querySelectorAll('.dropdown-trigger-mob');
    M.Dropdown.init(navbarDropdowns, {
        outDuration: 1000,
        hover: true
    });

    // Initialize sidenav
    const slide_menu = document.querySelectorAll(".sidenav");
    M.Sidenav.init(slide_menu, {});
});
