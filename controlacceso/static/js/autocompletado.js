document.getElementById('txtidentificacion').addEventListener('input', function(e) {
    const identificacion = this.value.trim();
    
    if (identificacion.length >= 5) {
        setTimeout(() => {
            console.log("ENVIANDO BUSQUEDA PARA:", identificacion);

            fetch(`/buscar_por_identificacion/?txtidentificacion=${encodeURIComponent(identificacion)}`)
                .then(response => {
                    console.log("STATUS:", response.status);
                    return response.text();
                })
                .then(text => {
                    console.log("RESPUESTA RAW:", text);

                    let data;
                    try {
                        data = JSON.parse(text);
                        console.log("RESPUESTA JSON:", data);
                    } catch (e) {
                        console.error("No es JSON válido:", e);
                        return; // Salimos si no es JSON válido
                    }

                    if (!data.error) {
                        const fieldsToAutocomplete = {
                            
                            'txtnombre': data.txtnombre,
                            'txtapellido': data.txtapellido,
                            'txttelefono': data.txttelefono,
                            'txtempresa': data.txtempresa,
                            'txtcargo': data.txtcargo,
                            'txtingresavehiculo': data.txtingresavehiculo,
                            'txtplaca': data.txtplaca,                            

                        };

                        for (const [fieldId, value] of Object.entries(fieldsToAutocomplete)) {
                            const element = document.getElementById(fieldId);
                            if (element) {
                                element.value = value || '';
                            }
                        }

                        const vehicleSelect = document.getElementById('txtingresavehiculo');
                        if (vehicleSelect) {
                            vehicleSelect.value = data.txtingresavehiculo ? "1" : "0";
                            document.getElementById('txtplaca').disabled = vehicleSelect.value !== "1";
                        }
                    }
                })
                .catch(error => console.error('Error:', error));
        }, 300);
    } else {
        // Si está vacío o con pocos caracteres, limpiar campos
        const fieldsToClear = [
            'txtnombre', 'txtapellido', 'txttelefono',
            'txtempresa', 'txtcargo', 'txtplaca'
        ];

        fieldsToClear.forEach(fieldId => {
            const element = document.getElementById(fieldId);
            if (element) element.value = '';
        });

        const vehicleSelect = document.getElementById('txtingresavehiculo');
        if (vehicleSelect) {
            vehicleSelect.value = "0";
            document.getElementById('txtplaca').disabled = true;
        }
    }
});
