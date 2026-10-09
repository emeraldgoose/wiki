/* Portal interactivity for the generated index pages (static/<lang>/index.html).
 *
 * Source of truth lives here; scripts/wiki_builder.py copies this file to
 * static/en/assets/ and static/ko/assets/ on every build. Vanilla JS, no
 * dependencies. All copy is keyed by <html lang> so one file serves both
 * languages.
 *
 * Wires up:
 *  - kind filter chips (#kind-filter)
 *  - category / source selects (#cat-filter, #src-filter)
 *  - tag cloud filter (#tag-cloud)
 *  - date sort toggle (injected into #recent-table th[data-col="date"])
 *  - pagination (#pager) + result count (#result-count) + empty state (#empty-msg)
 *  - navigator sidebar search (#nav-search over #nav-tree)
 */
(function () {
  "use strict";

  var lang = (document.documentElement.getAttribute("lang") === "ko") ? "ko" : "en";
  var T = {
    en: {
      sortDate: "Sort by date",
      asc: "oldest first",
      desc: "newest first",
      prev: "Prev",
      next: "Next",
      perPage: "per page",
      pageOf: function (p, n) { return "Page " + p + " of " + n; },
      showing: function (a, b, n) { return "Showing " + a + "–" + b + " of " + n + " documents"; },
      filtered: function (n) { return n + " documents"; }
    },
    ko: {
      sortDate: "날짜순 정렬",
      asc: "오래된 순",
      desc: "최신 순",
      prev: "이전",
      next: "다음",
      perPage: "개씩 보기",
      pageOf: function (p, n) { return p + " / " + n + " 페이지"; },
      showing: function (a, b, n) { return n + "개 문서 중 " + a + "–" + b + " 표시"; },
      filtered: function (n) { return n + "개 문서"; }
    }
  }[lang];

  var PER_OPTIONS = [20, 50, 100];

  var state = { kind: "", cat: "", src: "", tag: "", dir: "desc", page: 1, per: 20 };

  function $(id) { return document.getElementById(id); }

  /* ------------------------------------------------------------------ */
  /* recent table                                                        */
  /* ------------------------------------------------------------------ */

  var table = $("recent-table");
  var rows = [];
  if (table && table.tBodies.length) {
    rows = Array.prototype.slice.call(table.tBodies[0].rows);
  }

  function rowMatches(tr) {
    var d = tr.dataset;
    if (state.kind && d.kind !== state.kind) return false;
    if (state.cat && d.category !== state.cat) return false;
    if (state.src && d.blog !== state.src) return false;
    if (state.tag) {
      var tags = (d.tags || "").split(/\s+/);
      if (tags.indexOf(state.tag) === -1) return false;
    }
    return true;
  }

  function sortVisible(list) {
    var mult = state.dir === "asc" ? 1 : -1;
    list.sort(function (a, b) {
      var da = a.dataset.date || "", db = b.dataset.date || "";
      if (!da && !db) return 0;
      if (!da) return 1;   // undated rows always last
      if (!db) return -1;
      if (da === db) return 0;
      return (da < db ? -1 : 1) * mult;
    });
    return list;
  }

  function pageWindow(cur, total) {
    // [1, ..., cur-1, cur, cur+1, ..., total] with a +-2 window
    if (total <= 7) {
      var all = [];
      for (var i = 1; i <= total; i++) all.push(i);
      return all;
    }
    var set = [1];
    for (var p = cur - 2; p <= cur + 2; p++) {
      if (p > 1 && p < total) set.push(p);
    }
    set.push(total);
    return set;
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function renderPager(totalPages) {
    var pager = $("pager");
    if (!pager) return;
    pager.textContent = "";
    if (totalPages <= 1) {
      pager.hidden = true;
      return;
    }
    pager.hidden = false;
    pager.setAttribute("aria-label", T.pageOf(state.page, totalPages));

    var prev = el("button", "page-btn", "‹ " + T.prev);
    prev.disabled = state.page <= 1;
    prev.addEventListener("click", function () {
      if (state.page > 1) { state.page -= 1; render(); }
    });
    pager.appendChild(prev);

    var last = 0;
    pageWindow(state.page, totalPages).forEach(function (p) {
      if (p - last > 1) {
        var dots = el("span", "ellipsis", "…");
        dots.setAttribute("aria-hidden", "true");
        pager.appendChild(dots);
      }
      var b = el("button", "page-btn" + (p === state.page ? " is-current" : ""), String(p));
      if (p === state.page) b.setAttribute("aria-current", "page");
      (function (page) {
        b.addEventListener("click", function () { state.page = page; render(); });
      })(p);
      pager.appendChild(b);
      last = p;
    });

    var next = el("button", "page-btn", T.next + " ›");
    next.disabled = state.page >= totalPages;
    next.addEventListener("click", function () {
      if (state.page < totalPages) { state.page += 1; render(); }
    });
    pager.appendChild(next);

    var wrap = el("label", "per-page");
    var sel = document.createElement("select");
    sel.setAttribute("aria-label", T.perPage);
    PER_OPTIONS.forEach(function (n) {
      var o = document.createElement("option");
      o.value = String(n);
      o.textContent = String(n);
      if (n === state.per) o.selected = true;
      sel.appendChild(o);
    });
    sel.addEventListener("change", function () {
      state.per = parseInt(sel.value, 10) || 50;
      state.page = 1;
      render();
    });
    wrap.appendChild(sel);
    wrap.appendChild(document.createTextNode(" " + T.perPage));
    pager.appendChild(wrap);
  }

  function render() {
    if (!rows.length) return;
    var visible = sortVisible(rows.filter(rowMatches));
    var totalPages = Math.max(1, Math.ceil(visible.length / state.per));
    if (state.page > totalPages) state.page = totalPages;

    var start = (state.page - 1) * state.per;
    var slice = visible.slice(start, start + state.per);
    var onPage = {};
    slice.forEach(function (tr) { onPage[rows.indexOf(tr)] = true; });

    var tbody = table.tBodies[0];
    visible.forEach(function (tr) { tbody.appendChild(tr); }); // keep sorted order in DOM
    rows.forEach(function (tr, i) {
      tr.style.display = onPage[i] ? "" : "none";
    });

    var count = $("result-count");
    var empty = $("empty-msg");
    if (!visible.length) {
      table.style.display = "none";
      if (count) count.textContent = T.filtered(0);
      if (empty) empty.hidden = false;
    } else {
      table.style.display = "";
      if (count) {
        count.textContent = (visible.length === rows.length && state.page === 1 && visible.length <= state.per)
          ? T.filtered(visible.length)
          : T.showing(start + 1, Math.min(start + state.per, visible.length), visible.length);
      }
      if (empty) empty.hidden = true;
    }
    renderPager(visible.length ? totalPages : 0);
  }

  function installSort() {
    if (!table) return;
    var th = table.querySelector('th[data-col="date"]');
    if (!th) return;
    var label = th.textContent.trim();
    th.textContent = "";
    var btn = el("button", "sort-btn");
    btn.type = "button";
    btn.setAttribute("aria-pressed", "true");
    var lab = el("span", null, label + " ");
    var arrow = el("span", "arrow", state.dir === "asc" ? "▲" : "▼");
    btn.appendChild(lab);
    btn.appendChild(arrow);
    function sync() {
      arrow.textContent = state.dir === "asc" ? "▲" : "▼";
      btn.title = T.sortDate + " (" + (state.dir === "asc" ? T.asc : T.desc) + ")";
      btn.setAttribute("aria-pressed", state.dir === "asc" ? "false" : "true");
    }
    btn.addEventListener("click", function () {
      state.dir = state.dir === "asc" ? "desc" : "asc";
      state.page = 1;
      sync();
      render();
    });
    sync();
    th.appendChild(btn);
  }

  function installFilters() {
    var chips = $("kind-filter");
    if (chips) {
      chips.addEventListener("click", function (ev) {
        var btn = ev.target.closest ? ev.target.closest("[data-filter-kind]") : null;
        if (!btn || !chips.contains(btn)) return;
        state.kind = btn.getAttribute("data-filter-kind") || "";
        state.page = 1;
        var all = chips.querySelectorAll("[data-filter-kind]");
        Array.prototype.forEach.call(all, function (c) {
          c.classList.toggle("is-active", c === btn);
        });
        render();
      });
    }
    var cat = $("cat-filter");
    if (cat) cat.addEventListener("change", function () { state.cat = cat.value; state.page = 1; render(); });
    var src = $("src-filter");
    if (src) src.addEventListener("change", function () { state.src = src.value; state.page = 1; render(); });

    var cloud = $("tag-cloud");
    if (cloud) {
      cloud.addEventListener("click", function (ev) {
        var a = ev.target.closest ? ev.target.closest("[data-tag]") : null;
        if (!a || !cloud.contains(a)) return;
        ev.preventDefault();
        var tag = a.getAttribute("data-tag") || "";
        state.tag = (state.tag === tag) ? "" : tag;
        state.page = 1;
        var all = cloud.querySelectorAll("[data-tag]");
        Array.prototype.forEach.call(all, function (c) {
          c.classList.toggle("is-active", c.getAttribute("data-tag") === state.tag && !!state.tag);
        });
        render();
        if (state.tag) {
          var recent = $("recent");
          if (recent && recent.scrollIntoView) recent.scrollIntoView({ block: "start" });
        }
      });
    }
  }

  /* ------------------------------------------------------------------ */
  /* navigator sidebar search                                            */
  /* ------------------------------------------------------------------ */

  function installNavSearch() {
    var input = $("nav-search");
    var tree = $("nav-tree");
    if (!input || !tree) return;
    input.addEventListener("input", function () {
      var q = (input.value || "").trim().toLowerCase();
      var links = tree.querySelectorAll("a");
      Array.prototype.forEach.call(links, function (a) {
        var hit = !q || (a.textContent || "").toLowerCase().indexOf(q) !== -1;
        var li = a.closest ? a.closest("li") : a.parentNode;
        if (li) li.style.display = hit ? "" : "none";
      });
      var subs = tree.querySelectorAll("li.nav-sub, details.nav-group");
      Array.prototype.forEach.call(subs, function (box) {
        var anyVisible = false;
        var as = box.querySelectorAll("a");
        for (var i = 0; i < as.length; i++) {
          var li = as[i].closest ? as[i].closest("li") : as[i].parentNode;
          if (li && li.style.display !== "none") { anyVisible = true; break; }
        }
        box.style.display = anyVisible ? "" : "none";
      });
    });
  }

  installFilters();
  installSort();
  installNavSearch();
  render();
})();
