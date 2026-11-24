(function () {
  'use strict';
  var root = document.documentElement;

  // --- Tema claro / oscuro ---
  var temaBtn = document.getElementById('theme-toggle');
  function pintarTema() {
    var oscuro = root.getAttribute('data-bs-theme') === 'dark';
    if (temaBtn) {
      temaBtn.querySelector('i').className = 'bi ' + (oscuro ? 'bi-sun-fill' : 'bi-moon-stars-fill');
      temaBtn.setAttribute('aria-label', oscuro ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro');
    }
  }
  if (temaBtn) {
    temaBtn.addEventListener('click', function () {
      var nuevo = root.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-bs-theme', nuevo);
      try { localStorage.setItem('theme', nuevo); } catch (e) {}
      pintarTema();
    });
  }
  pintarTema();

  // --- Vista tarjetas / tabla ---
  var botonesVista = document.querySelectorAll('[data-vista-btn]');
  function pintarVista() {
    var actual = root.getAttribute('data-vista');
    botonesVista.forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-vista-btn') === actual);
    });
  }
  botonesVista.forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.getAttribute('data-vista-btn');
      root.setAttribute('data-vista', v);
      try { localStorage.setItem('vista', v); } catch (e) {}
      pintarVista();
    });
  });
  pintarVista();

  // --- Filtros: enviar al cambiar un select ---
  document.querySelectorAll('select[data-autosubmit]').forEach(function (s) {
    s.addEventListener('change', function () { s.form.submit(); });
  });

  // --- Atajo "/" para buscar ---
  var buscador = document.getElementById('buscador');
  document.addEventListener('keydown', function (e) {
    var tag = (document.activeElement && document.activeElement.tagName) || '';
    if (e.key === '/' && buscador && !/INPUT|TEXTAREA|SELECT/.test(tag)) {
      e.preventDefault();
      buscador.focus();
      buscador.select();
    }
  });

  // --- Alertas: se cierran solas a los 6 segundos ---
  if (window.bootstrap) {
    document.querySelectorAll('.alert-dismissible').forEach(function (a) {
      setTimeout(function () {
        if (document.body.contains(a)) { bootstrap.Alert.getOrCreateInstance(a).close(); }
      }, 6000);
    });
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
      new bootstrap.Tooltip(el);
    });
  }
})();
