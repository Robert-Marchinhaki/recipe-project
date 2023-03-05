function my_scope() {
    const forms = document.querySelectorAll(".form-delete");

    for (const form of forms) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();

            const confirmed = confirm("Are you sure?");

            if (confirmed) {
                form.submit();
            }
        });
    }
}

my_scope();

(() => {
    const btnCloseMenu = document.querySelector(".btn-close-menu");
    const btnShowMenu = document.querySelector(".btn-show-menu");
    const menuContainer = document.querySelector(".menu-container");

    const btnShowMenuVisibleClass = "btn-show-menu-visible";
    const menuHiddenClass = "menu-hidden";

    const closeMenu = () => {
        btnShowMenu.classList.add(btnShowMenuVisibleClass);
        menuContainer.classList.add(menuHiddenClass);
    };

    const showMenu = () => {
        btnShowMenu.classList.remove(btnShowMenuVisibleClass);
        menuContainer.classList.remove(menuHiddenClass);
    };

    if (btnCloseMenu) {
        btnCloseMenu.removeEventListener('click', closeMenu);
        btnCloseMenu.addEventListener('click', closeMenu);  
    };

    if (btnShowMenu) {
        btnShowMenu.removeEventListener('click', showMenu);
        btnShowMenu.addEventListener('click', showMenu);
    };
})();

(() => {
    const formLogoutLinks = document.querySelectorAll('.form-logout-link');
    const formLogout = document.querySelector('.form-logout');

    console.log(formLogoutLinks);
    console.log(formLogout);
    
    for (const link of formLogoutLinks) {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            formLogout.submit();
        });
    }
})();