// Chequea validez de rut
function checkRut(rut) {
  if(rut == "run" || rut != "pasaporte") {
    var valor = rut.value.replace('.', '');
    valor = valor.replace('-', '');
    cuerpo = valor.slice(0, -1);
    dv = valor.slice(-1).toUpperCase();
    rut.value = cuerpo + '-' + dv
    if (cuerpo.length < 7) { rut.setCustomValidity("RUT Incompleto"); return false; }
    suma = 0;
    multiplo = 2;
    for (i = 1; i <= cuerpo.length; i++) {
        index = multiplo * valor.charAt(cuerpo.length - i);
        suma = suma + index;
        if (multiplo < 7) { multiplo = multiplo + 1; } else { multiplo = 2; }
    }
    dvEsperado = 11 - (suma % 11);
    dv = (dv == 'K') ? 10 : dv;
    dv = (dv == 0) ? 11 : dv;
    if (dvEsperado != dv) { rut.setCustomValidity("RUT Inválido"); return false; }
    rut.setCustomValidity('');
  } else {
    console.log("documento")
  }
}

// Despliega spinner de carga
function mostrarSpinner() {
  Swal.fire({
    imageUrl: '/static/img/progress.svg',
    showCancelButton: false,
    showConfirmButton: false,
    allowOutsideClick: false,
  });
  $('.swal2-container.swal2-backdrop-show').css('background', 'rgba(255,255,255,.8)');
  $('.swal2-popup').css('background', 'transparent');
}