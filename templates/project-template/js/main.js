/*
Project: {{PROJECT_NAME}}
Developed by: Mohamed Ahmed Abbas
Role: Front-End Development

Copyright (c) {{YEAR}} Mohamed Ahmed Abbas.
All rights reserved.
*/

(function () {
  'use strict';

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  // Device simulation hook: the preview shell tells the app which device frame it is in.
  window.addEventListener('message', function (e) {
    var d = e.data;
    if (d && d.type === 'ui2web:device') {
      if (d.device === 'iphone' || d.device === 'android') {
        document.documentElement.setAttribute('data-device', d.device);
      } else {
        document.documentElement.removeAttribute('data-device');
      }
    }
  });
})();
