/* Theme toggle + language menu. Vanilla JS, no dependencies.
 *
 * Source of truth lives here; scripts/wiki_builder.py copies this file to
 * static/<lang>/assets/ on every build (like portal.js / zoom.js).
 * Loaded with defer on every content page, the portal index and pending.html.
 *
 * - #theme-toggle flips an explicit html[data-theme] and persists it in
 *   localStorage. With no stored choice the CSS follows the OS setting, so
 *   the button only ever overrides, never fights, prefers-color-scheme.
 * - details.lang-menu needs no JS to work; the handler below only adds
 *   outside-click dismissal (native <details> has none).
 */
(function () {
  "use strict";

  var KEY = "arkive-theme";
  var root = document.documentElement;

  function stored() {
    try {
      var t = localStorage.getItem(KEY);
      if (t === "dark" || t === "light") return t;
    } catch (e) { /* private mode: fall through to OS */ }
    return "";
  }

  function effective() {
    var t = stored();
    if (t) return t;
    return (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches)
      ? "dark" : "light";
  }

  var btn = document.getElementById("theme-toggle");

  function paint() {
    if (!btn) return;
    var dark = effective() === "dark";
    btn.setAttribute("aria-pressed", dark ? "true" : "false");
    btn.textContent = dark ? "\u2600" : "\u263E";
  }

  if (btn) {
    btn.addEventListener("click", function () {
      var next = effective() === "dark" ? "light" : "dark";
      try { localStorage.setItem(KEY, next); } catch (e) { /* non-persistent */ }
      root.setAttribute("data-theme", next);
      paint();
    });
  }
  paint();

  document.addEventListener("click", function (ev) {
    var menus = document.querySelectorAll("details.lang-menu[open]");
    Array.prototype.forEach.call(menus, function (d) {
      if (!d.contains(ev.target)) d.removeAttribute("open");
    });
  });
})();
