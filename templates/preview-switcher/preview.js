/*
Project: {{PROJECT_NAME}} - Preview Switcher
Developed by: Mohamed Ahmed Abbas
Role: Front-End Development

Copyright (c) {{YEAR}} Mohamed Ahmed Abbas.
All rights reserved.
*/

(function () {
  'use strict';

  var stage = document.getElementById('stage');
  var frame = document.getElementById('app');
  var tabs = document.querySelectorAll('.modes button');
  var note = document.getElementById('note');
  var mode = 'responsive';

  var NOTES = {
    responsive: 'Responsive website. The app uses the full preview area.',
    iphone: 'iPhone simulation: web approximation for preview only. Not native iOS rendering.',
    android: 'Android simulation: web approximation for preview only. Not native Android rendering.'
  };

  // Optional: ?src=../other/index.html
  var params = new URLSearchParams(window.location.search);
  var src = params.get('src');
  if (src && /^[\w./-]+$/.test(src) && src.charAt(0) !== '/' && src.indexOf('//') === -1) {
    frame.src = src;
  }

  function tellApp() {
    try {
      frame.contentWindow.postMessage({ type: 'ui2web:device', device: mode }, '*');
    } catch (e) { /* cross-origin or not loaded yet */ }
  }

  function setMode(next) {
    mode = next;
    stage.setAttribute('data-mode', mode);
    note.textContent = NOTES[mode];
    tabs.forEach(function (t) {
      t.setAttribute('aria-selected', String(t.getAttribute('data-mode') === mode));
    });
    tellApp();
  }

  tabs.forEach(function (t) {
    t.addEventListener('click', function () { setMode(t.getAttribute('data-mode')); });
  });
  frame.addEventListener('load', tellApp);
})();
