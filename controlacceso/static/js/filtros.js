document.addEventListener('DOMContentLoaded', function () {

  console.log("INGRESO A LA FUNCION FILTROS")
  const filtrosActivos = document.getElementById('filtros-activos');
  const form = document.getElementById('filtro-form');

  window.agregarFiltro = function () {
    const campo = document.getElementById('campo-select').value;
    const valor = document.getElementById('campo-valor').value;

    if (!campo || !valor) return;

    console.log("SEGUNDO LOG PARA VERIFICAR")

    // Crear input oculto
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = `filtro_${campo}`;
    input.value = valor;
    form.appendChild(input);

    // Crear etiqueta visual
    const tag = document.createElement('span');
    tag.className = 'badge bg-secondary d-flex align-items-center';
    tag.textContent = `${campo}: ${valor}`;

    // Botón para eliminar
    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'btn-close btn-close-white ms-2';
    closeBtn.setAttribute('aria-label', 'Eliminar');
    closeBtn.onclick = () => {
      form.removeChild(input);
      filtrosActivos.removeChild(tag);
    };

    tag.appendChild(closeBtn);
    filtrosActivos.appendChild(tag);

    // Limpiar campo de valor
    document.getElementById('campo-valor').value = '';
  };

});