/* ==========================================================================
   site.js — Sanvi
   Mejora progresiva. Sin este archivo el sitio sigue siendo utilizable: los
   enlaces de WhatsApp del header, del FAB y de cada CTA son <a> reales, el
   acordeon del FAQ es <details> nativo y la navegacion completa esta ademas
   en el footer, que no depende de JavaScript.
   Se carga con `defer` como ultimo elemento del <body> de las 4 paginas.
   ========================================================================== */
(function () {
  'use strict';

  /* Numero E.164 sin '+' para los enlaces wa.me. Unica fuente de verdad del JS.
     Si cambia el telefono hay que actualizarlo tambien en el HTML de las 4
     paginas (header, FAB, CTA y footer) y en el JSON-LD. */
  var WA_NUMBER = '56978833741';

  /* --- 1. Menu movil ---
     Alterna la clase `nav-open` sobre #site-nav (components.css espera la
     clase EN EL NAV, no en el header) y mantiene sincronizado el
     aria-expanded del boton, del que components.css cuelga la animacion del
     icono hamburguesa -> X.
     El acordeon del FAQ no aparece aqui a proposito: <details>/<summary>
     abren y cierran solos, con teclado incluido. Anadir JS solo empeoraria
     el INP sin aportar nada. */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  if (toggle && nav) {
    var closeNav = function () {
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('nav-open');
    };

    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList
    .toggle('nav-open', !open);
    });

    nav.addEventListener('click', function (event) {
      if (event.target.closest('a')) closeNav();
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        closeNav();
        toggle.focus();
      }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth >= 900) closeNav();
    });
  }

  /* --- 2. Sombra del header al hacer scroll --- */
  var header = document.getElementById('site-header');
  if (header) {
    var syncHeader = function () {
      header.classList.toggle('is-stuck', window.scrollY > 8);
    };
    syncHeader();
    window.addEventListener('scroll', syncHeader, { passive: true });
  }

  /* --- 3. Formulario de contacto -> WhatsApp --- */
  var form = document.querySelector('[data-wa-form]');
  if (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var data = new FormData(form);
      var value = function (key) { return String(data.get(key) || '').trim(); };

      var lines = [
        'Hola Sanvi, quiero agendar una atencion de enfermeria a domicilio en Calama.',
        'Nombre: ' + value('nombre'),
        'Servicio: ' + value('servicio'),
        'Sector de Calama: ' + value('sector'),
        'Dia y hora preferidos: ' + value('horario')
      ];
      if (value('mensaje')) lines.push('Comentario: ' + value('mensaje'));

      window.location.href =
        'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(lines.join('\n'));
    });
  }
})();
