    document.addEventListener('DOMContentLoaded', function () {
    const modalEl = document.getElementById('modal_modificar');
    if (!modalEl) return;

    modalEl.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // <- botón que abrió el modal
        console.log('Abriendo modal para ID:', button?.dataset?.id); // debería verse en la consola

        const setVal = (name, val) => {
        const input = modalEl.querySelector(`[name="${name}"]`);
        if (input) input.value = val ?? '';
        };

        setVal('txtidentificacion', button.getAttribute('data-identificacion'));
        setVal('txtnombre',         button.getAttribute('data-nombre'));
        setVal('txtapellido',       button.getAttribute('data-apellido'));
        setVal('txttelefono',       button.getAttribute('data-telefono'));
        setVal('visitante_id',      button.getAttribute('data-id'));
    });
    });
    