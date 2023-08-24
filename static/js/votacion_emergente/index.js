

$(document).ready(function () {


  function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
  }

  var Fn = {
    // Valida el rut con su cadena completa "XXXXXXXX-X"
    validaRut: function (rutCompleto) {
      rutCompleto = rutCompleto.replace("‐", "-");
      if (!/^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test(rutCompleto))
        return false;
      var tmp = rutCompleto.split('-');
      var digv = tmp[1];
      var rut = tmp[0];
      if (digv == 'K') digv = 'k';

      return (Fn.dv(rut) == digv);
    },
    dv: function (T) {
      var M = 0, S = 1;
      for (; T; T = Math.floor(T / 10))
        S = (S + T % 10 * (9 - M++ % 6)) % 11;
      return S ? S - 1 : 'k';
    }
  }
  var contenedor_vinna = document.getElementById('contenedor-vinnas')
  contenedor_vinna.innerHTML = "<div style=\"display: flex; justify-content: center; align-items: center; height: 0px;\"><i class='fas fa-spin fa-spinner fa-10x'></i></div>";

  $.ajax({
    type: "GET",
    url: "cargar_datos_votacion/",
    // 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
    success: function (response) {
      contenedor_vinna.innerHTML = ''
      var vinnas = response.map(function (regionData) {

        // Acceder a los datos de cada región y sus viñas
        var contenedor_vinna = document.getElementById('contenedor-vinnas')
        contenedor_vinna.innerHTML +=
        ` 
        <section class="contenedor-b row" style=" background: ${regionData.colorFondo} ;">
<h1 class="col-md-3" style= "color: #FFFFFF;">${regionData.region}</h1>
<section class=" col-md-3" style="padding: 27px;">
<div class="row " style="justify-content: center;margin-bottom: 40px;margin-top: -18px;"><img class="hover-element" onclick="fn_datos_para_mdl('${regionData.id_viñas[0]}',this)" src="${regionData.imagenViñas[0]}" style="width: 200px;
height: 90px;
/* UI Properties */

border-radius: 62px;" type="text" data-parametro= ${regionData.id_viñas[0]}></div>
<div class="circulo row" style="background: ${regionData.colorInterior} 0% 0% no-repeat padding-box;" >
<label class="circle" style="background: ${regionData.colorCirculo} 0% 0% no-repeat padding-box;
opacity: 1;">
<input type="radio" class="color-radio" name="${regionData.id_region}" value="${regionData.id_viñas[0]}" style="accent-color: #617072;margin-top:18px; margin-left:-10px; z-index:3000;">
</label>

<label style="padding: 0%;width: 100%;position: absolute;place-content: center;" class="row">
  <div style="display: contents;position: relative;">
      <div style="position: absolute;bottom: -27px;">
          <p class="nombre" style="margin-left: 24%;padding-bottom: 6px;padding: 10px;">${regionData.viñas[0]}</p>
      </div>
    <span style="position: absolute;width: 100%;left: 106px; bottom: 3px;" class="">       
  </span>
  </div>       
</label>
</div>      
</section>     

<section class=" col-md-3" style="padding: 27px;">
<div class="row " style="justify-content: center;margin-bottom: 40px;margin-top: -18px;"><img class="hover-element" onclick="fn_datos_para_mdl('${regionData.id_viñas[1]}',this)" src="${regionData.imagenViñas[1]}" style="width: 200px;
height: 90px;
/* UI Properties */

border-radius: 62px;" type="text" data-parametro= ${regionData.id_viñas[1]}></div>
<div class="circulo row" style="background: ${regionData.colorInterior} 0% 0% no-repeat padding-box;" >
<label class="circle" style="background: ${regionData.colorCirculo} 0% 0% no-repeat padding-box;
opacity: 1;">
<input type="radio" class="color-radio" name="${regionData.id_region}" value="${regionData.id_viñas[1]}" style="accent-color: #617072;margin-top:18px; margin-left:-10px; z-index:3000;">
</label>

<label style="padding: 0%;width: 100%;position: absolute;place-content: center;" class="row">
  <div style="display: contents;position: relative;">
      <div style="position: absolute;bottom: -27px;">
          <p class="nombre" style="margin-left: 24%;padding-bottom: 6px;padding: 10px;">${regionData.viñas[1]}</p>
      </div>
    <span style="position: absolute;width: 100%;left: 106px; bottom: 3px;" class="">       
  </span>
  </div>       
</label>
</div>      
</section>          

<section class=" col-md-3" style="padding: 27px;">
<div class="row " style="justify-content: center;margin-bottom: 40px;margin-top: -18px;"><img class="hover-element" onclick="fn_datos_para_mdl('${regionData.id_viñas[2]}',this)" src="${regionData.imagenViñas[2]}" style="width: 200px;
height: 90px;
/* UI Properties */

border-radius: 62px;" type="text" data-parametro= ${regionData.id_viñas[2]}></div>
<div class="circulo row" style="background: ${regionData.colorInterior} 0% 0% no-repeat padding-box;" >
<label class="circle" style="background: ${regionData.colorCirculo} 0% 0% no-repeat padding-box;
opacity: 1;">
<input type="radio" class="color-radio" name="${regionData.id_region}" value="${regionData.id_viñas[2]}" style="accent-color: #617072;margin-top:18px; margin-left:-10px; z-index:3000;">
</label>

<label style="padding: 0%;width: 100%;position: absolute;place-content: center;" class="row">
  <div style="display: contents;position: relative;">
      <div style="position: absolute;bottom: -27px;">
          <p class="nombre" style="margin-left: 24%;padding-bottom: 6px;padding: 10px;">${regionData.viñas[2]}</p>
      </div>
    <span style="position: absolute;width: 100%;left: 106px; bottom: 3px;" class="">       
  </span>
  </div>       
</label>
</div>      
</section>         


</section>            
        `
      });
    },
    error: function (error) {
      console.log("Error en la solicitud AJAX:", error);
    }
  });


  var valoresSeleccionados = {};

  // Agregar evento de escucha a los radio buttons con la clase "color-radio"
  $(document).on('change', '.color-radio', function () {
    // Obtener el valor seleccionado del radio button
    var valorSeleccionado = $(this).val();
    // Obtener el nombre del radio button, que corresponde al id de la región
    var nombreRadio = $(this).attr('name');

    // Guardar el valor seleccionado en la variable valoresSeleccionados
    valoresSeleccionados[nombreRadio] = valorSeleccionado;
  });

  $("#envio_formulario").submit(function (event) {

    // Prevenir el comportamiento predeterminado del formulario (enviarlo tradicionalmente)
    event.preventDefault();
    const radioButtons = document.getElementsByName('inp_tipo_id');
    let valorSeleccionado;
    for (const radioButton of radioButtons) {
        if (radioButton.checked) {
            valorSeleccionado = radioButton.value;
            break; // Salir del bucle cuando encuentre el seleccionado
        }
    }

    // Mostrar el valor seleccionado en la consola
    var csrfToken = getCookie('csrftoken');

    var documento = $("#documento").val();
    // Obtener los valores de los campos de entrada del formulario
    var nombre = $("#nombre").val();
    var correo = $("#correo").val();
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    const isValidEmail = emailRegex.test(correo);

    var datos = {
      documento: documento,
      nombre: nombre,
      correo: correo,
      opciones: valoresSeleccionados,
    };

    if (isValidEmail) {
      if (Fn.validaRut($("#documento").val()) && valorSeleccionado == 'run') {
        if (nombre == null || nombre == undefined || nombre == '') {
          var nombreVacio = document.getElementById('label-error_nombre');
          nombreVacio.removeAttribute('hidden');
        } else if (correo == null || correo == undefined || correo == '') {
          var correoVacio = document.getElementById('label-error_correo');
          correoVacio.removeAttribute('hidden');
        } else {
          $.ajax({
            type: "POST",
            url: "envio_datos_formulario/",
            data: JSON.stringify(datos),
            dataType: "json",
            headers: {
              'X-CSRFToken': csrfToken,  // Incluir el token CSRF como encabezado
            },
            success: function (response) {
              if (response.data == 0) {
                var error_envio = document.getElementById("error_envio")
                error_envio.textContent = response.message;
                error_envio.hidden = false;
              }
              else {
                window.parent.location.href = 'https://premiosenoturismochile.cl/votacion-exitosa-2/';

              }
            }
          });
        }

      }
      else if (valorSeleccionado == 'pasaporte') {
        if (nombre == null || nombre == undefined || nombre == '') {
          var nombreVacio = document.getElementById('label-error_nombre');
          nombreVacio.removeAttribute('hidden');
        } else if (correo == null || correo == undefined || correo == '') {
          var correoVacio = document.getElementById('label-error_correo');
          correoVacio.removeAttribute('hidden');
        } else {
          $.ajax({
            type: "POST",
            url: "envio_datos_formulario/",
            data: JSON.stringify(datos),
            dataType: "json",
            headers: {
              'X-CSRFToken': csrfToken,  // Incluir el token CSRF como encabezado
            },
            success: function (response) {
              if (response.data == 0) {
                var error_envio = document.getElementById("error_envio")
                error_envio.textContent = response.message;
                error_envio.hidden = false;
              }
              else {
                window.parent.location.href = 'https://premiosenoturismochile.cl/votacion-exitosa-2/';

              }
            }
          });
        }


      }
      else {
        const labelError = document.getElementById("label-error");
        labelError.hidden = false;

      }
    } else {
      var correoVacio = document.getElementById('label-error_correo');
      correoVacio.removeAttribute('hidden');
    }
    
  });

  const btnMostrar = $('#boton_mostrar');
  const cantidad_Votos = $('#cantidad_votos');

  // Manejar el evento click del botón
  btnMostrar.click(function() {
    // Alternar el atributo "hidden" al hacer clic (mostrar si está oculto, ocultar si está visible)
    cantidad_Votos.attr('hidden', !cantidad_Votos.attr('hidden'));
  });

   $('#boton_mostrar').click(function() {
    console.log("workeando")
    // Alternar el atributo "hidden" al hacer clic (mostrar si está oculto, ocultar si está visible)
    $('#cantidad_votos_em').prop('hidden', function(index, value) {
      return !value;
    });
  });




})





