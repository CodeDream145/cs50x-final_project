function alert_fun (menu_id) {
    menu = document.getElementById(menu_id+"d");
    menubutton = document.getElementById(menu_id);
    menu.style.textDecoration = "line-through";
    menubutton.classList.add("disabled");
}