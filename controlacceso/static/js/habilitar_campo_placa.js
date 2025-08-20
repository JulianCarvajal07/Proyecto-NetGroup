            document.addEventListener("DOMContentLoaded", function() {
                const selectVehiculo = document.getElementById("txtingresavehiculo");
                const inputPlaca = document.getElementById("txtplaca");

                selectVehiculo.addEventListener("change", function() {
                    if (this.value === "1") {  // Si es "SI"
                        inputPlaca.disabled = false;
                        inputPlaca.focus();
                    } else {
                        inputPlaca.disabled = true;
                        inputPlaca.value = "";
                    }
                });
            });