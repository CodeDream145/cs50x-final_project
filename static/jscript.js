function alert_fun (menu_id) {
    menu = document.getElementById("menu_" + menu_id);
    menubutton = document.getElementById(menu_id);
    menu.style.textDecoration = "line-through";
    menubutton.classList.add("disabled");
    menubutton.setAttribute('name', 'remove_dish')
}
