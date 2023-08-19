

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
  $.ajax({
    type: "GET",
    url: "cargar_datos_votacion/",
    // 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
    success: function (response) {

      var vinnas = response.map(function (regionData) {
        // var mostrar = document.getElementById('cantidad_votos_totales')
        // mostrar.innerHTML = ` <h3 id = "votos_t" hidden> ${regionData.votos_cantidad_experiencia} </h3>` 

        // Acceder a los datos de cada región y sus viñas
        var contenedor_vinna = document.getElementById('contenedor-vinnas')
        contenedor_vinna.innerHTML +=
          ` 
                <section class="contenedor-b row" style=" background: ${regionData.colorFondo} ;">
    <h1 class="col-md-3" style= "color: #FFFFFF;">${regionData.region}</h1>
    <section class=" col-md-3" style="padding: 27px;">
      <div class="row" style="justify-content: center;margin-bottom: 90px;margin-top: 90px;"><img onclick="fn_datos_para_mdl('${regionData.id_viñas[0]}')" src="${regionData.imagenViñas[0]}" style="width: 278px;
        height: 125px;
        /* UI Properties */
        background: #FFFFFF 0% 0% no-repeat padding-box;
        border-radius: 62px;"  class="" type="text" data-parametro= ${regionData.id_viñas[0]}></div>
      <div class="circulo row" style="background: ${regionData.colorInterior} 0% 0% no-repeat padding-box;" >
        <label class="circle" style="background: ${regionData.colorCirculo} 0% 0% no-repeat padding-box;
        opacity: 1;">
          <span></span>
        </label>
  
        <label style="padding-left: 50px;
        display: block;
        margin: 0 !important;">
          <p class="nombre">Empresa finalista <span style="position: relative;">
            <input type="radio" class="color-radio" name="${regionData.id_region}" value = "${regionData.id_viñas[0]}" style = "accent-color: ${regionData.colorCirculo};">
          </span></p>
          
        </label>
      </div>      
    </section>     
    <section class=" col-md-3" style="padding: 27px;">
      <div class="row" style="justify-content: center;margin-bottom: 90px;margin-top: 90px;"><img onclick="fn_datos_para_mdl('${regionData.id_viñas[1]}')" src="${regionData.imagenViñas[1]}" style="width: 278px;
        height: 125px;
        /* UI Properties */
        background: #FFFFFF 0% 0% no-repeat padding-box;
        border-radius: 62px;"  class="" type="text" data-parametro= ${regionData.id_viñas[1]}></div>
      <div class="circulo row" style="background: ${regionData.colorInterior} 0% 0% no-repeat padding-box;" >
        <label class="circle" style="background: ${regionData.colorCirculo} 0% 0% no-repeat padding-box;
        opacity: 1;">
          <span></span>
        </label>
  
        <label style="padding-left: 50px;
        display: block;
        margin: 0 !important;">
          <p class="nombre">Empresa finalista <span style="position: relative;">
            <input type="radio" class="color-radio" name="${regionData.id_region}" value = "${regionData.id_viñas[1]}" style = "accent-color: ${regionData.colorCirculo};">
          </span></p>
          
        </label>
      </div>      
    </section>     
    <section class=" col-md-3" style="padding: 27px;">
      <div class="row" style="justify-content: center;margin-bottom: 90px;margin-top: 90px;"><img  onclick="fn_datos_para_mdl('${regionData.id_viñas[2]}')" src="${regionData.imagenViñas[2]}" style="width: 278px;
        height: 125px;
        /* UI Properties */
        background: #FFFFFF 0% 0% no-repeat padding-box;
        border-radius: 62px;"  class="" type="text" data-parametro= ${regionData.id_viñas[2]}></div>
      <div class="circulo row" style="background: ${regionData.colorInterior} 0% 0% no-repeat padding-box;" >
        <label class="circle" style="background: ${regionData.colorCirculo} 0% 0% no-repeat padding-box;
        opacity: 1;">
          <span></span>
        </label>
  
        <label style="padding-left: 50px;
        display: block;
        margin: 0 !important;">
          <p class="nombre">Empresa finalista <span style="position: relative;">
            <input type="radio" class="color-radio" name="${regionData.id_region}" value = "${regionData.id_viñas[2]}" style = "accent-color: ${regionData.colorCirculo};">
          </span></p>
          
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
    var datos = {
      documento: documento,
      nombre: nombre,
      correo: correo,
      opciones: valoresSeleccionados,
    };

    if (Fn.validaRut($("#documento").val()) && valorSeleccionado == 'run' ) {
      $.ajax({
        type: "POST",
        url: "envio_datos_formulario/",
        data: JSON.stringify(datos),
        dataType: "json",
        headers: {
          'X-CSRFToken': csrfToken,  // Incluir el token CSRF como encabezado
        },
        success: function (response) {
          if(response.data == 0){
            var error_envio = document.getElementById("error_envio")
            error_envio.textContent = response.message;
            error_envio.hidden = false;
          }       
          else{
            // window.location.replace('https://premiosenoturismochile.cl/votacion-exitosa/');
            window.location.href = 'https://premiosenoturismochile.cl/votacion-exitosa/';


          }
        }
      });
    } 
    else if(valorSeleccionado == 'pasaporte'){
      $.ajax({
        type: "POST",
        url: "envio_datos_formulario/",
        data: JSON.stringify(datos),
        dataType: "json",
        headers: {
          'X-CSRFToken': csrfToken,  // Incluir el token CSRF como encabezado
        },
        success: function (response) {
          if(response.data == 0){
            var error_envio = document.getElementById("error_envio")
            error_envio.textContent = response.message;
            error_envio.hidden = false;
          }       
          else{
            window.location.replace('https://premiosenoturismochile.cl/votacion-exitosa/');

          }
        }
      });

    }
    else {
      const labelError = document.getElementById("label-error");
      labelError.hidden = false;
      
    }
  });

 

  const botonMostrar = $('#boton_mostrar');
  const cantidadVotos = $('#cantidad_votos_en');

  // Manejar el evento click del botón
  botonMostrar.click(function() {
    // Alternar el atributo "hidden" al hacer clic (mostrar si está oculto, ocultar si está visible)
    cantidadVotos.attr('hidden', !cantidadVotos.attr('hidden'));
  });




})







