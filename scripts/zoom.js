/* Figure zoom: Medium-style expand-from-thumbnail animation.
 *
 * Progressive enhancement over the no-JS CSS :target lightbox emitted by
 * scripts/wiki_builder.py. Clicking a.zoom-in animates the image from its
 * thumbnail rect to a fitted fullscreen rect (FLIP), and back on close.
 * Without JS the :target fallback still opens instantly.
 */
(function () {
  "use strict";

  function fitScale(nw, nh) {
    if (!nw || !nh) return 1;
    return Math.min(window.innerWidth * 0.94 / nw, window.innerHeight * 0.92 / nh);
  }

  function openZoom(opener, overlay) {
    var thumb = opener.querySelector("img");
    var full = overlay.querySelector("img");
    if (!thumb || !full) return;
    var r = thumb.getBoundingClientRect();

    var show = function () {
      var s = fitScale(full.naturalWidth, full.naturalHeight);
      var fw = (full.naturalWidth || r.width) * s;
      var fh = (full.naturalHeight || r.height) * s;
      var dx = (r.left + r.width / 2) - window.innerWidth / 2;
      var dy = (r.top + r.height / 2) - window.innerHeight / 2;
      var k = fw ? (r.width / fw) : 1;

      overlay.classList.add("is-open");
      document.body.style.overflow = "hidden";
      full.style.transition = "none";
      full.style.transform = "translate(" + dx + "px," + dy + "px) scale(" + k + ")";
      void full.offsetWidth; // reflow: commit the start frame
      full.style.transition = "";
      full.style.transform = "";
      overlay._opener = opener;
    };

    if (full.complete && full.naturalWidth) {
      show();
    } else {
      full.onload = show;
      // Cached full-size may already be decoded but load fired earlier.
      setTimeout(function () {
        if (!overlay.classList.contains("is-open")) show();
      }, 1500);
    }
  }

  function closeZoom(overlay) {
    var full = overlay.querySelector("img");
    var opener = overlay._opener;
    var thumb = opener && opener.querySelector("img");
    if (full && thumb) {
      var r = thumb.getBoundingClientRect();
      var s = fitScale(full.naturalWidth, full.naturalHeight);
      var fw = (full.naturalWidth || r.width) * s;
      var fh = (full.naturalHeight || r.height) * s;
      var dx = (r.left + r.width / 2) - window.innerWidth / 2;
      var dy = (r.top + r.height / 2) - window.innerHeight / 2;
      var k = fw ? (r.width / fw) : 1;
      full.style.transform = "translate(" + dx + "px," + dy + "px) scale(" + k + ")";
      setTimeout(function () {
        overlay.classList.remove("is-open");
        document.body.style.overflow = "";
        full.style.transform = "";
      }, 240);
    } else {
      overlay.classList.remove("is-open");
      document.body.style.overflow = "";
    }
  }

  document.addEventListener("click", function (ev) {
    var opener = ev.target.closest ? ev.target.closest("a.zoom-in") : null;
    if (opener) {
      var overlay = document.querySelector(opener.getAttribute("href"));
      if (overlay) {
        ev.preventDefault();
        openZoom(opener, overlay);
        return;
      }
    }
    var overlay = ev.target.closest ? ev.target.closest(".lightbox.is-open") : null;
    if (overlay) closeZoom(overlay);
  });

  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape" || ev.key === "Esc") {
      var open = document.querySelector(".lightbox.is-open");
      if (open) closeZoom(open);
    }
  });

  // Scrolling while zoomed auto-zooms out (reverse animation), like
  // dismissing the zoom to get back to reading. Only click/Esc otherwise.
  document.addEventListener("wheel", function (ev) {
    var open = document.querySelector(".lightbox.is-open");
    if (open) closeZoom(open);
  }, { passive: true });
})();
