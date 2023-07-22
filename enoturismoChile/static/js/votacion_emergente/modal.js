
function fn_datos_para_mdl(p) {
    // Hacer lo que desees con el parámetro recibido (ID de la viña)
    id_vina = p
    if (id_vina)
        $.ajax({
            type: "GET",
            url: "cargar_mdl_vinna/",
            data: { id_vina: id_vina },
            dataType: "json",
            success: function (response) {
                var titulo_vinna_elemento = document.getElementById('titulo-vinna-mdl');
                var contenido_actual = titulo_vinna_elemento.innerText;

                // Cambiar el contenido del elemento
                var nuevo_contenido = response.nombre_vinna;
                titulo_vinna_elemento.innerText = nuevo_contenido;
                $('#mdl-vista_vinna').modal('show');

            }
        });

}





