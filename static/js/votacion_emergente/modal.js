
function fn_datos_para_mdl(p,e) {
    // Hacer lo que desees con el parámetro recibido (ID de la viña)
    id_vina = p
    if (id_vina)
        $.ajax({
            type: "GET",
            url: "cargar_mdl_vinna/",
            data: { id_vina: id_vina },
            dataType: "json",
            success: function (response) {
                var link_instagram = response.link_instagram;
                var link_facebook = response.link_facebook;
                var link_pagina = response.link_pagina;
                var link_video = response.link_video;

                console.log("Instagram: ",link_instagram,"n, facebook: ", link_facebook, "n, pagina: ", link_pagina,"n, video: ", link_video)

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

                var contenedor_logos = document.getElementById('contenedor_logos');
                 contenedor_logos.innerHTML = 
                `

                `
                if (link_instagram != ''){
                    contenedor_logos.innerHTML+= 
                    `
                    <a id="direccion-instagram" href="https://www.facebook.com/centroturisticocoopcapel?mibextid=LQQJ4d"><img src="https://premiosenoturismochile.cl/wp-content/uploads/2023/08/insta.png" alt=""></a>
                    `
                }
                if (link_facebook != ''){
                    contenedor_logos.innerHTML+= 
                    `
                    <a id="direccion-facebook" href=""><img src="https://premiosenoturismochile.cl/wp-content/uploads/2023/08/facebook.png" alt=""></a>

                    `
                }
                if (link_pagina != ''){
                    contenedor_logos.innerHTML+= 
                    `
                    <a id="direccion-pagina" href=""><img src="https://premiosenoturismochile.cl/wp-content/uploads/2023/08/pagina.png" alt=""></a>

                    `
                }
                if (link_video != ''){
                    contenedor_logos.innerHTML+= 
                    `
                    <a id="direccion-video" href=""><img src="https://premiosenoturismochile.cl/wp-content/uploads/2023/08/video.png" alt=""></a>

                    `
                }

                // Cambiar el contenido del elemento

                descripcion_vinna_elemento.innerText = descripcion_vinna;
                titulo_superior_vinna_elemento.innerText = titulo_vinna;

                var nuevo_contenido = response.nombre_vinna;
                titulo_vinna_elemento.innerText = nuevo_contenido;
                var modal = document.getElementById("mdl-vista_vinna");
                $('#mdl-vista_vinna').modal('show');
                modal.style.top = e.getBoundingClientRect().top + "px";

            }
        });

}





