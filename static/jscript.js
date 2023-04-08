function alert_fun (menu_id) {
    menu = document.getElementById("menu_" + menu_id);
    menubutton = document.getElementById(menu_id);
    menu.style.textDecoration = "line-through";
    menubutton.classList.add("disabled");
    menubutton.setAttribute('name', 'remove_dish')
}

function day_detect (button_id) {
    button = document.getElementById(button_id);
    button.setAttribute("name", "finished_day")
}
