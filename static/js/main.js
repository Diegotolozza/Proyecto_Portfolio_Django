// Abre la imagen full en el modal
document.addEventListener('DOMContentLoaded', function() {
  const modalImg = document.getElementById('lightboxImage');

  document.querySelectorAll('[data-bs-toggle="modal"][data-full]').forEach(el => {
    el.addEventListener('click', function(e) {
      const full = el.getAttribute('data-full');
      modalImg.src = full;
      modalImg.alt = el.querySelector('img')?.alt || 'Foto';
    });
  });

  // Al cerrar el modal, limpiar src (libera memoria)
  const lightboxModal = document.getElementById('lightboxModal');
  lightboxModal.addEventListener('hidden.bs.modal', function () {
    modalImg.src = '';
  });
});

