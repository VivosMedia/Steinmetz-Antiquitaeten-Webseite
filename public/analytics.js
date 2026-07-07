/* Zentrale Umami-Analytics-Konfiguration.
   Einzige Stelle im Code, an der URL und Website-ID gepflegt werden. */
(function () {
  var s = document.createElement('script');
  s.defer = true;
  s.src = 'https://umami-production-41c4.up.railway.app/script.js';
  s.setAttribute('data-website-id', 'c1449fe2-b7a1-4a31-b701-6fe6916ff8b9');
  document.head.appendChild(s);
})();
