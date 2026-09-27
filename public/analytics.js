/* Zentrale Umami-Analytics-Konfiguration.
   Einzige Stelle im Code, an der URL und Website-ID gepflegt werden. */
(function () {
  var s = document.createElement('script');
  s.defer = true;
  s.src = 'https://steinmetz-umami-analytics.vercel.app/script.js';
  s.setAttribute('data-website-id', '5fd8284a-a13f-4d11-bf58-9ffab76594d2');
  document.head.appendChild(s);
})();
