$(document).ready(function () {
  // Obtener el contenedor que engloba los radio buttons y las etiquetas
  const radioGroup = document.getElementById('radioGroup');

  // Obtener todos los radio buttons con la clase 'radio-input'
  const radioButtons = radioGroup.querySelectorAll('.radio-input');

  // Agregar un event listener para cada radio button
  radioButtons.forEach(radio => {
    radio.addEventListener('change', () => {
      // Obtener el valor del radio button seleccionado
      const valorSeleccionado = radio.value;
      if (valorSeleccionado == 'run') {
        var documento_d = document.getElementById('documento');
        documento_d.removeAttribute('disabled');
        documento_d.value = "";
        documento.setAttribute('oninput', 'checkRut(this)');
      } else {
        const inputElement = document.getElementById('documento');
        inputElement.removeAttribute('oninput');
        inputElement.value = "";
        inputElement.removeAttribute('disabled');
      }
      console.log('Valor seleccionado:', valorSeleccionado);
    });
  });

  function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
  }

  $(document).on('change', '#frm_votacion input[type=email], input[type=text]', function(e) {
    $(this).removeClass('is-invalid');
  });

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

  var valoresSeleccionados = {};

  // Agregar evento de escucha a los radio buttons con la clase "color-radio"
  $(document).on('change', '.color-radio', function () {
    // Obtener el valor seleccionado del radio button
    var valorSeleccionado = $(this).val();
    // Obtener el nombre del radio button, que corresponde al id de la región
    var nombreRadio = $(this).attr('name');

    // Guardar el valor seleccionado en la variable valoresSeleccionados
    valoresSeleccionados[nombreRadio] = valorSeleccionado;
    const cantidadVotos = Object.entries(valoresSeleccionados).length;
    if(cantidadVotos >= 3) {
      $('#msj-votos').remove();
      $('.btn-enviar').removeAttr('disabled');
      return;
    } else {
      const votosRestantes = 3 - cantidadVotos;
      $('#msj-votos').html(`Debes realizar al menos ${ votosRestantes == 1 ? votosRestantes + ' voto más' : votosRestantes + ' votos más' }.`);
    }
  });

  $("#frm_votacion").submit(function (event) {
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
    const csrfToken = getCookie('csrftoken');
    // Obtener los valores de los campos de entrada del formulario
    const documento = $("#documento").val().replaceAll(' ', '');
    const nombre = $("#nombre").val().trim();
    const correo = $("#correo").val().replaceAll(' ', '');
    const url = new URL(window.location.href);
    const searchParams = url.searchParams;

    const datos = {
      documento: documento,
      nombre: nombre,
      correo: correo,
      opciones: JSON.stringify(valoresSeleccionados),
      tipo_categoria: parseInt(searchParams.get('tipo'))
    };

    let errors = false;

    if(valorSeleccionado == 'run') { 
      if(!Fn.validaRut($("#documento").val())){
        const documento_el = $('#documento');
        documento_el.addClass('is-invalid');
        documento_el.next().html(`El ${valorSeleccionado} es inválido.`);
        errors = true;
      }
    } else {
      if(documento == null || documento == undefined || documento == '') {
        const documento_el = $('#documento');
        documento_el.addClass('is-invalid');
        documento_el.next().html('El pasaporte es requerido.');
        errors = true;
      }
    }

    if(nombre == null || nombre == undefined || nombre == '') {
      const nombre_el = $('#nombre');
      nombre_el.addClass('is-invalid');
      nombre_el.next().html('El nombre es requerido.');
      errors = true;
    }

    if(correo == null || correo == undefined || correo == '') { 
      const correo_el = $('#correo');
      correo_el.addClass('is-invalid');
      correo_el.next().html('El correo es requerido.');
      errors = true;
    }

    if(errors) {
      return;
    }

    // Realiza votacion
    $.ajax({
      type: "POST",
      url: "categoria",
      data: datos,
      dataType: "json",
      headers: {
        'X-CSRFToken': csrfToken,  // Incluir el token CSRF como encabezado
      },
      beforeSend: function () {
        mostrarSpinner();
      },
      success: function (response) {
        if(response.ok) { // Si todo esta ok, redirecciona a sitio de votacion exitosa
          window.parent.location.href = datos.tipo_categoria == 1 ? 'https://premiosenoturismochile.cl/votacion-exitosa/' : 'https://premiosenoturismochile.cl/votacion-exitosa-2/';
        } else {
          console.log(response)
          Swal.fire({
            icon: 'warning',
            title: 'Oops...',
            text: response.mensaje,
          });
        }
      },
      error: function (data) {
        console.log(data);
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Ocurrió un error inesperado al almacenar tu voto.',
        });
      },
    });
  });
});