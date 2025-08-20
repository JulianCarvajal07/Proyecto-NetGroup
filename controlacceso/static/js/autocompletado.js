document.getElementById('txtidentificacion').addEventListener('input', function(e) {
    // Usamos 'input' en lugar de 'change' para mayor sensibilidad
    const identificacion = this.value.trim();
    
    // Esperamos a que tenga una longitud mínima (ej: 4 caracteres)
    if (identificacion.length >= 4) {
        // Agregamos un pequeño delay para evitar múltiples peticiones
        setTimeout(() => {
            fetch(`/buscar-identificacion/?txtidentificacion=${encodeURIComponent(identificacion)}`)
                .then(response => {
                    if (!response.ok) throw new Error('Error en la respuesta');
                    return response.json();
                })
                .then(data => {
                    if (!data.error) {
                        // Autocompletar campos
                        const fieldsToAutocomplete = {
                            'txttipoidentificacion': data.txttipoidentificacion,
                            'txtnombre': data.txtnombre,
                            'txtapellido': data.txtapellido,
                            'txttelefono': data.txttelefono,
                            'txtempresa': data.txtempresa,
                            'txtcargo': data.txtcargo,
                            'txtplaca': data.txtplaca,
                            'txtnotarjeta': data.txtnotarjeta,
                            'txtautoriza': data.txtautoriza
                        };
                        
                        // Recorremos todos los campos
                        for (const [fieldId, value] of Object.entries(fieldsToAutocomplete)) {
                            const element = document.getElementById(fieldId);
                            if (element) {
                                element.value = value || '';
                            }
                        }
                        
                        // Manejo especial para checkbox
                        const vehicleCheckbox = document.getElementById('txtingresavehiculo');
                        if (vehicleCheckbox) {
                            vehicleCheckbox.checked = Boolean(data.txtingresavehiculo);
                            document.getElementById('txtplaca').disabled = !data.txtingresavehiculo;
                        }
                    }
                })
                .catch(error => console.error('Error:', error));
        }, 300); // Delay de 300ms
    }
});
