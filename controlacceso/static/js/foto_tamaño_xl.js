function mostrarImagen(src) {
    document.getElementById("imagenGrande").src = src;
    document.getElementById("modalImagen").style.display = "flex";
}

function cerrarModal() {
    document.getElementById("modalImagen").style.display = "none";
}