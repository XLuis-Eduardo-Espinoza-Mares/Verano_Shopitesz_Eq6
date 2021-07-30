var inicio = 0; //se inicializa una variable en 0

function aumentar(){ // se crean la funcion y se agrega al evento onclick en en la etiqueta button con id aumentar

var cantidad = document.getElementById('cantidad').value = ++inicio; //se obtiene el valor del input, y se incrementa en 1 el valor que tenga.
}

function disminuir(){ // se crean la funcion y se agrega al evento onclick en en la etiqueta button con id disminuir

var cantidad = document.getElementById('cantidad').value = --inicio; //se obtiene el valor del input, y se decrementa en 1 el valor que tenga.
}