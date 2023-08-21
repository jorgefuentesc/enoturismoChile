
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
                var descripcion_vinna_elemento = document.getElementById('descripcion_vinna');
                var titulo_superior_vinna_elemento = document.getElementById('titulo_superior');

                // var contenido_actual = titulo_vinna_elemento.innerText;
                var titulo_vinna = response.titulo_vinna;
                var descripcion_vinna = response.descripcion_vinna;

                var img_vinna = response.img_vinna;

                var contenedor_img = document.getElementById('contenedor_img_vinna');
                contenedor_img.innerHTML = `
                <img style="width: -webkit-fill-available;
                border-radius: 0px 73px 0px 0px;"
                src="${img_vinna}" alt="">
                `;

                // Cambiar el contenido del elemento

                descripcion_vinna_elemento.innerText = descripcion_vinna;
                titulo_superior_vinna_elemento.innerText = titulo_vinna;

                var nuevo_contenido = response.nombre_vinna;
                titulo_vinna_elemento.innerText = nuevo_contenido;
                $('#mdl-vista_vinna').modal('show');

            }
        });

}





