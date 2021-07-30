function obtenerID(){
    var combo=document.getElementById("categoria");
    var idCategoria=combo.options[combo.options.selectedIndex].value;
    var ajax=new XMLHttpRequest();
    var url='/productos/categoria/'+idCategoria;
    ajax.open('get',url,true);
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
           llenarTabla(this.responseText);
        }
    };
    ajax.send();
}
function imprimirMsg(){
    alert('Documento cargado');
}
function llenarTabla(datos){
    var tabla=document.getElementById("datos");
    var productos=JSON.parse(datos);
    eliminarTabla();
    for(i=0;i<productos.length;i++){
        var tr=document.createElement("tr");
        var prod=productos[i];
        for (propiedad in prod){
            //alert(propiedad);
            //alert(prod[propiedad]);
            var td=document.createElement("td");
            var texto=document.createTextNode(prod[propiedad]);
            td.appendChild(texto);
            tr.appendChild(td);
        }
        var link=crearLink(prod.idProducto);
        td=document.createElement("td");
        td.appendChild(link);
        tr.appendChild(td);
        tabla.appendChild(tr);
        
        
    }
}
function eliminarTabla(){
    var tabla=document.getElementById("datos");
    //alert(tabla.rows.length);
    for(i=tabla.rows.length-1;i>0;i--){
		tabla.removeChild(tabla.rows[i]);
	}
}
function crearLink(id){
    var link=document.createElement("a");
    link.setAttribute("onclick","mostrarProducto("+id+")");
    link.setAttribute("data-toggle","modal");
    link.setAttribute("data-target","#producto");
    var span=document.createElement("span");
    span.setAttribute("class","glyphicon glyphicon-shopping-cart");
    link.appendChild(span);
    return link;
}
function mostrarProducto(id){
    
    var ajax=new XMLHttpRequest();
    url='/producto/'+id;
    ajax.open('get',url,true);
    ajax.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4){
            var producto=JSON.parse(this.responseText);
            llenarCamposProductos(producto);
        }
    };
    ajax.send();   
}
function llenarCamposProductos(producto){
    if(producto.estatus!='error'){
        document.getElementById("cantidad").value=1;
        validarCantidad(producto.existencia,producto.precio);
        document.getElementById("id").value=producto.idProducto;
        document.getElementById("nombre").value=producto.nombre;
        document.getElementById("descripcion").value=producto.descripcion;
        document.getElementById("precio").value=producto.precio;
        document.getElementById("existencia").value=producto.existencia;
        var cantidad=document.getElementById("cantidad").value;
        document.getElementById("cantidad").setAttribute("max",producto.existencia);
        document.getElementById("cantidad").setAttribute("onchange","validarCantidad("+producto.existencia+","+producto.precio+")");
        document.getElementById("imagen").setAttribute("src","/productos/foto/"+producto.idProducto);
        document.getElementById("total").value=producto.precio*cantidad;
        document.getElementById("total").style.color="blue";
    }
    else{
        document.getElementById("agregar").setAttribute("disabled",true);
        document.getElementById("notificaciones").innerHTML=producto.mensaje;
        document.getElementById("notificaciones").style.color="red"; 
    }
}
function validarCantidad(existencia,precio){
    var cantidad=document.getElementById("cantidad").value;
    if(cantidad<=existencia && cantidad>0){
        document.getElementById("total").value=precio*cantidad;
        document.getElementById("agregar").removeAttribute("disabled");
        document.getElementById("notificaciones").innerHTML="";
    }
    else{
        document.getElementById("agregar").setAttribute("disabled",true);
        document.getElementById("notificaciones").innerHTML="No hay suficiente cantidad en existencia";
        document.getElementById("notificaciones").style.color="red";
    }
}
function agregarCarrito(){
    var carrito={idProducto:document.getElementById("id").value,
                 cantidad:document.getElementById("cantidad").value};
    var json=JSON.stringify(carrito);
    var url='/carrito/agregar/'+encodeURI(json);
    var ajax=new XMLHttpRequest();
    ajax.open("get",url,true);
    ajax.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4){
            var mensaje=JSON.parse(this.responseText);
            if(mensaje.estatus=='ok'){
                document.getElementById("notificaciones").style.color="green";
                document.getElementById("notificaciones").innerHTML=mensaje.mensaje;
            }
            else{
                document.getElementById("notificaciones").style.color="red";
                document.getElementById("notificaciones").innerHTML=mensaje.mensaje;
            }
        }
    };
    ajax.send();         
}