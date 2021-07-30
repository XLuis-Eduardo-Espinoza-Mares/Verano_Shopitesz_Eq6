formulario = document.querySelector('#formulario-tarjeta');

// * Select Categoria
formulario.selectCategoria.addEventListener('change', (e) => {
    var combo=document.getElementById("selectCategoria")
    var idCategoria=combo.options[combo.options.selectedIndex].value;
	document.getElementById("noTarteja").value=idCategoria;
});