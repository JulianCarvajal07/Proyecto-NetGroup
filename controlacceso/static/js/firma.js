
//CUANDO LA PAGINA SE CARGA COMPLETAMENTE SE ACTIVA LA FUNCION
  document.addEventListener("DOMContentLoaded", function () {


    // INICIALIZA EL CANVAS Y BUSCA EL INPUT OCULTO EN EL BODY DEL MODAL
    const canvas = document.getElementById('canvasfirma');
    const firmainput = document.getElementById('firmainput');
    // CREA EL OBJETO SIGNATUREPAD = Esto convierte el canvas en un área de dibujo interactiva
    const signaturePad = new SignaturePad(canvas); 


    //ESTO BORRA LA FIRMA CADA QUE EL MODAL SE ABRE
    const modalfirma = document.getElementById('modalfirma');
    modalfirma.addEventListener('shown.bs.modal', function () {
    signaturePad.clear();
    });


    window.guardarfirma = function () {
        //Este método verifica si el usuario ha dibujado algo en el canvas.
      if (signaturePad.isEmpty()) {
        alert("Por favor, firme antes de continuar.");
        return false; // evita que se envíe el formulario
      }

      console.log("Firma base64:", firmainput.value);

      const dataURL = signaturePad.toDataURL(); // convierte la firma en base64
      firmainput.value = dataURL; // la guarda en el campo oculto
      return true; // permite que el formulario se envíe
    };

      // Agregar la lógica para actualizar el ID dinámicamente
      modalfirma.addEventListener('show.bs.modal', function (event) {
      const button = event.relatedTarget;
      const visitanteID = button.getAttribute('data-id');
      document.getElementById('firmainputID').value = visitanteID;


        // Cambiar color del botón cuando se firme
      const visitanteid = document.getElementById('firmainputID').value;
      const boton = document.getElementById('botonfirma' + visitanteid);
      if (boton) {
      boton.classList.remove('btn-primary');
      boton.classList.add('btn-success');
      boton.textContent = "FIRMADO";
      }

      return true; // permite que el formulario se envíe    
    
    });


    

  });
  
