(function () {
  "use strict";

  // Theme toggle: light -> dark -> system
  var KEY = "finance-ai-theme";
  var root = document.documentElement;

  function apply(v) {
    if (v === "light" || v === "dark") root.setAttribute("data-theme", v);
    else root.removeAttribute("data-theme");
  }

  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) { /* storage blocked */ }
  apply(stored);

  var tt = document.getElementById("themetoggle");
  if (tt) {
    tt.addEventListener("click", function () {
      var cur = root.getAttribute("data-theme") || "system";
      var next = cur === "light" ? "dark" : cur === "dark" ? "system" : "light";
      apply(next);
      try {
        if (next === "system") localStorage.removeItem(KEY);
        else localStorage.setItem(KEY, next);
      } catch (e) { /* ignore */ }
      tt.title = "Theme: " + next;
    });
  }

  var nt = document.getElementById("navtoggle");
  var sb = document.getElementById("sidebar");
  if (nt && sb) {
    nt.addEventListener("click", function () {
      var open = sb.classList.toggle("open");
      nt.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Keep the current sidebar entry in view on load.
  var cur = document.querySelector(".sidebar a.current");
  if (cur && cur.scrollIntoView) {
    var box = cur.getBoundingClientRect();
    if (box.top < 60 || box.bottom > window.innerHeight) {
      cur.scrollIntoView({ block: "center" });
    }
  }
})();

/* Glossary explainers: hover and focus are CSS; this adds click/tap toggling
   and keeps the panel inside the viewport. */
(function () {
  "use strict";
  var terms = document.querySelectorAll(".gloss");
  if (!terms.length) return;

  function closeAll(except) {
    document.querySelectorAll(".gloss.open").forEach(function (g) {
      if (g !== except) g.classList.remove("open");
    });
  }

  function place(el) {
    var pop = el.querySelector(".gloss-pop");
    if (!pop) return;
    pop.classList.remove("flip-right", "flip-up");
    var r = pop.getBoundingClientRect();
    if (r.right > window.innerWidth - 8) pop.classList.add("flip-right");
    if (r.bottom > window.innerHeight - 8 && r.top > r.height + 40) {
      pop.classList.add("flip-up");
    }
  }

  terms.forEach(function (el) {
    el.addEventListener("mouseenter", function () { place(el); });
    el.addEventListener("focus", function () { place(el); });
    el.addEventListener("click", function (e) {
      if (e.target.closest(".gloss-pop")) return; // let text in the panel be selected
      e.preventDefault();
      var open = el.classList.contains("open");
      closeAll(el);
      el.classList.toggle("open", !open);
      if (!open) place(el);
    });
    el.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        el.classList.toggle("open");
        place(el);
      } else if (e.key === "Escape") {
        el.classList.remove("open");
        el.blur();
      }
    });
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".gloss")) closeAll(null);
  });
})();

/* Mark the section the reader is in, in the sticky page contents. */
(function () {
  "use strict";
  var links = document.querySelectorAll(".toc a[href^='#']");
  if (!links.length || !window.IntersectionObserver) return;

  var byId = {};
  var heads = [];
  links.forEach(function (a) {
    var id = decodeURIComponent(a.getAttribute("href").slice(1));
    var h = document.getElementById(id);
    if (!h) return;
    byId[id] = a;
    heads.push(h);
  });
  if (!heads.length) return;

  var seen = new Set();
  function mark() {
    // The current section is the last heading at or above the reading line.
    var best = null;
    heads.forEach(function (h) {
      if (seen.has(h.id)) best = h;
    });
    if (!best) best = heads[0];
    links.forEach(function (a) { a.classList.remove("here"); });
    if (byId[best.id]) byId[best.id].classList.add("here");
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) seen.add(e.target.id);
      else if (e.boundingClientRect.top > 0) seen.delete(e.target.id);
      else seen.add(e.target.id);
    });
    mark();
  }, { rootMargin: "-70px 0px -70% 0px", threshold: 0 });

  heads.forEach(function (h) { io.observe(h); });
})();

/* Figure lightbox with pan, zoom and reset.

   Every figure in the prose becomes a button that opens a larger copy. The
   copy is a clone rather than a move, so the page keeps its layout while the
   viewer is open. Diagrams are inlined SVG, which scales without limit;
   photographs are raster and will soften past their natural size, so the
   zoom indicator reports the scale either way. */
(function () {
  "use strict";

  var media = [];
  document.querySelectorAll(".doc figure").forEach(function (fig) {
    var el = fig.querySelector("svg.figsvg, img");
    if (el) media.push({ el: el, fig: fig });
  });
  if (!media.length) return;

  var MIN = 0.15, MAX = 16;
  var box = null, stage = null, canvas = null, zoomLabel = null, capEl = null;
  var scale = 1, tx = 0, ty = 0, natW = 0, natH = 0, baseScale = 1;
  var opener = null, lastFocus = null;
  var pointers = new Map(), pinchDist = 0, pinchMid = null, dragging = false;
  var dragX = 0, dragY = 0, moved = false;

  // ---------------------------------------------------------------- helpers
  function naturalSize(el) {
    if (el.tagName.toLowerCase() === "img") {
      return [el.naturalWidth || el.width || 800, el.naturalHeight || el.height || 600];
    }
    var vb = (el.getAttribute("viewBox") || "").split(/[\s,]+/).map(Number);
    if (vb.length === 4 && vb[2] > 0 && vb[3] > 0) return [vb[2], vb[3]];
    var r = el.getBoundingClientRect();
    return [r.width || 800, r.height || 600];
  }

  /* A caption may contain MathML, whose textContent includes the LaTeX
     annotation as well as the rendered glyphs. Strip the annotation before
     reading text, and copy markup rather than text where maths should still
     render. */
  function captionText(cap) {
    if (!cap) return "";
    var c = cap.cloneNode(true);
    c.querySelectorAll("annotation, annotation-xml").forEach(function (a) {
      a.parentNode.removeChild(a);
    });
    return c.textContent.replace(/\s+/g, " ").trim();
  }

  function cloneInto(host, el) {
    if (el.tagName.toLowerCase() === "img") {
      var img = el.cloneNode(true);
      img.removeAttribute("style");
      img.className = "lb-media";
      host.appendChild(img);
      return;
    }
    // Re-prefix ids so the clone cannot collide with the original's markers.
    var markup = el.outerHTML
      .replace(/\sid="([^"]+)"/g, ' id="lbx-$1"')
      .replace(/url\(#([^)]+)\)/g, "url(#lbx-$1)");
    host.innerHTML = markup;
    var svg = host.firstElementChild;
    if (svg) {
      svg.removeAttribute("width");
      svg.removeAttribute("height");
      svg.classList.add("lb-media");
      svg.style.width = "100%";
      svg.style.height = "100%";
    }
  }

  function apply() {
    canvas.style.transform =
      "translate(" + tx.toFixed(2) + "px," + ty.toFixed(2) + "px) scale(" + scale.toFixed(4) + ")";
    if (zoomLabel) {
      zoomLabel.textContent = Math.round((scale / baseScale) * 100) + "%";
    }
  }

  function fit() {
    var r = stage.getBoundingClientRect();
    var pad = 24;
    var s = Math.min((r.width - pad * 2) / natW, (r.height - pad * 2) / natH);
    if (!isFinite(s) || s <= 0) s = 1;
    baseScale = s;
    scale = s;
    tx = (r.width - natW * s) / 2;
    ty = (r.height - natH * s) / 2;
    apply();
  }

  function zoomAt(px, py, factor) {
    var next = Math.min(MAX, Math.max(MIN, scale * factor));
    if (next === scale) return;
    var k = next / scale;
    tx = px - (px - tx) * k;
    ty = py - (py - ty) * k;
    scale = next;
    apply();
  }

  function stageCentre() {
    var r = stage.getBoundingClientRect();
    return [r.width / 2, r.height / 2];
  }

  // ------------------------------------------------------------------ build
  function ensureBox() {
    if (box) return;
    box = document.createElement("div");
    box.className = "lb";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "Figure viewer");
    box.hidden = true;
    box.innerHTML =
      '<div class="lb-stage"><div class="lb-canvas"></div></div>' +
      '<p class="lb-cap"></p>' +
      '<div class="lb-bar">' +
      '<button type="button" class="lb-btn" data-act="out" aria-label="Zoom out">−</button>' +
      '<span class="lb-zoom" aria-live="polite">100%</span>' +
      '<button type="button" class="lb-btn" data-act="in" aria-label="Zoom in">+</button>' +
      '<button type="button" class="lb-btn lb-word" data-act="reset">Reset</button>' +
      '<button type="button" class="lb-btn lb-word" data-act="close">Close</button>' +
      "</div>";
    document.body.appendChild(box);

    stage = box.querySelector(".lb-stage");
    canvas = box.querySelector(".lb-canvas");
    zoomLabel = box.querySelector(".lb-zoom");
    capEl = box.querySelector(".lb-cap");

    box.querySelector(".lb-bar").addEventListener("click", function (e) {
      var b = e.target.closest("[data-act]");
      if (!b) return;
      var c = stageCentre();
      if (b.dataset.act === "in") zoomAt(c[0], c[1], 1.3);
      else if (b.dataset.act === "out") zoomAt(c[0], c[1], 1 / 1.3);
      else if (b.dataset.act === "reset") fit();
      else close();
    });

    stage.addEventListener("wheel", function (e) {
      e.preventDefault();
      var r = stage.getBoundingClientRect();
      zoomAt(e.clientX - r.left, e.clientY - r.top, e.deltaY < 0 ? 1.12 : 1 / 1.12);
    }, { passive: false });

    stage.addEventListener("dblclick", function (e) {
      var r = stage.getBoundingClientRect();
      var px = e.clientX - r.left, py = e.clientY - r.top;
      if (scale > baseScale * 1.4) fit();
      else zoomAt(px, py, 2.2);
    });

    stage.addEventListener("pointerdown", function (e) {
      stage.setPointerCapture(e.pointerId);
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      moved = false;
      if (pointers.size === 1) {
        dragging = true;
        dragX = e.clientX - tx;
        dragY = e.clientY - ty;
        stage.classList.add("grabbing");
      } else if (pointers.size === 2) {
        dragging = false;
        var p = Array.from(pointers.values());
        pinchDist = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y);
        pinchMid = [(p[0].x + p[1].x) / 2, (p[0].y + p[1].y) / 2];
      }
    });

    stage.addEventListener("pointermove", function (e) {
      if (!pointers.has(e.pointerId)) return;
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pointers.size === 2) {
        var p = Array.from(pointers.values());
        var d = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y);
        if (pinchDist > 0) {
          var r = stage.getBoundingClientRect();
          zoomAt(pinchMid[0] - r.left, pinchMid[1] - r.top, d / pinchDist);
        }
        pinchDist = d;
        pinchMid = [(p[0].x + p[1].x) / 2, (p[0].y + p[1].y) / 2];
        moved = true;
      } else if (dragging) {
        tx = e.clientX - dragX;
        ty = e.clientY - dragY;
        moved = true;
        apply();
      }
    });

    function release(e) {
      pointers.delete(e.pointerId);
      if (pointers.size < 2) pinchDist = 0;
      if (pointers.size === 0) {
        dragging = false;
        stage.classList.remove("grabbing");
      }
    }
    stage.addEventListener("pointerup", release);
    stage.addEventListener("pointercancel", release);

    // A click on the empty stage closes, but not at the end of a drag.
    stage.addEventListener("click", function (e) {
      if (!moved && !e.target.closest(".lb-canvas")) close();
    });

    box.addEventListener("keydown", function (e) {
      var c = stageCentre();
      if (e.key === "Escape") { e.preventDefault(); close(); }
      else if (e.key === "+" || e.key === "=") { e.preventDefault(); zoomAt(c[0], c[1], 1.3); }
      else if (e.key === "-" || e.key === "_") { e.preventDefault(); zoomAt(c[0], c[1], 1 / 1.3); }
      else if (e.key === "0") { e.preventDefault(); fit(); }
      else if (e.key.indexOf("Arrow") === 0) {
        e.preventDefault();
        var step = e.shiftKey ? 120 : 40;
        if (e.key === "ArrowLeft") tx += step;
        else if (e.key === "ArrowRight") tx -= step;
        else if (e.key === "ArrowUp") ty += step;
        else ty -= step;
        apply();
      } else if (e.key === "Tab") {
        // Keep focus inside the dialog.
        var f = box.querySelectorAll("button");
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });

    window.addEventListener("resize", function () { if (!box.hidden) fit(); });
  }

  // ------------------------------------------------------------ open, close
  function open(item, trigger) {
    ensureBox();
    opener = trigger;
    lastFocus = document.activeElement;
    canvas.innerHTML = "";
    cloneInto(canvas, item.el);

    var size = naturalSize(item.el);
    natW = size[0];
    natH = size[1];
    canvas.style.width = natW + "px";
    canvas.style.height = natH + "px";

    var cap = item.fig.querySelector("figcaption");
    capEl.innerHTML = cap ? cap.innerHTML : "";
    capEl.hidden = !cap;

    box.hidden = false;
    document.body.classList.add("lb-open");
    fit();
    box.querySelector('[data-act="close"]').focus();
  }

  function close() {
    if (!box || box.hidden) return;
    box.hidden = true;
    canvas.innerHTML = "";
    document.body.classList.remove("lb-open");
    var back = opener || lastFocus;
    if (back && back.focus) back.focus();
    opener = null;
  }

  // ------------------------------------------------------------- the triggers
  media.forEach(function (item) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "figzoom";
    var words = captionText(item.fig.querySelector("figcaption"))
      .split(/\s+/).slice(0, 9).join(" ") || "figure";
    btn.setAttribute("aria-label", "Open larger view: " + words);
    btn.title = "Click to enlarge";
    item.el.parentNode.insertBefore(btn, item.el);
    btn.appendChild(item.el);
    btn.addEventListener("click", function () { open(item, btn); });
  });
  /* ------------------------------------------------------------- search ---
     The site has no server to ask and must open from file://, where fetch()
     of a local file is refused, so the index is a script that assigns one
     global. It is fetched on the first keystroke and never for a reader who
     does not search, which keeps its weight off every other page view.

     The whole control is built here rather than in the template: with no
     JavaScript there is no index to query, and a search box that cannot
     search is worse than none. */

  (function () {
    var bar = document.querySelector(".topbar");
    var brand = bar && bar.querySelector(".brand");
    if (!bar || !brand || !window.Promise) return;

    var ROOT = document.body.getAttribute("data-root") || "";
    var MAX = 12;

    var form = document.createElement("form");
    form.className = "search";
    form.setAttribute("role", "search");
    form.addEventListener("submit", function (e) { e.preventDefault(); });

    var input = document.createElement("input");
    input.type = "search";
    input.className = "search-in";
    input.placeholder = "Search";
    input.setAttribute("aria-label", "Search this site");
    input.setAttribute("autocomplete", "off");
    input.setAttribute("aria-expanded", "false");
    input.setAttribute("aria-controls", "search-results");

    var panel = document.createElement("div");
    panel.className = "search-panel";
    panel.id = "search-results";
    panel.setAttribute("role", "listbox");
    panel.hidden = true;

    var live = document.createElement("p");
    live.className = "search-live";
    live.setAttribute("aria-live", "polite");

    form.appendChild(input);
    form.appendChild(panel);
    form.appendChild(live);
    brand.parentNode.insertBefore(form, brand.nextSibling);

    // ---- loading the index ------------------------------------------------
    var loading = null;
    function index() {
      if (window.__SEARCH__) return Promise.resolve(window.__SEARCH__);
      if (loading) return loading;
      loading = new Promise(function (resolve, reject) {
        var s = document.createElement("script");
        s.src = ROOT + "assets/search-index.js";
        s.onload = function () {
          window.__SEARCH__ ? resolve(window.__SEARCH__) : reject();
        };
        s.onerror = reject;
        document.head.appendChild(s);
      });
      return loading;
    }

    // ---- query ------------------------------------------------------------
    function tokenize(s) {
      var out = (s || "").toLowerCase().match(/[\wÀ-ÿΑ-ω]+/g) || [];
      return out.filter(function (w) { return w.length > 1; });
    }

    var cache = {};
    function postings(term, idx) {
      if (cache[term]) return cache[term];
      var out = [], id = 0, parts = idx.t[term].split(" ");
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i], dot = p.indexOf(".");
        var gap = parseInt(dot < 0 ? p : p.slice(0, dot), 36);
        var tf = dot < 0 ? 1 : parseInt(p.slice(dot + 1), 36);
        id += gap;
        out.push([id, tf]);
      }
      cache[term] = out;
      return out;
    }

    var termList = null;
    function candidates(tok, idx) {
      // The exact word, plus anything it begins, so a query answers while it
      // is still being typed and plurals need no stemmer.
      if (!termList) termList = Object.keys(idx.t);
      var hits = [];
      if (idx.t[tok]) hits.push(tok);
      for (var i = 0; i < termList.length && hits.length < 48; i++) {
        var t = termList[i];
        if (t !== tok && t.length > tok.length && t.indexOf(tok) === 0) {
          hits.push(t);
        }
      }
      return hits;
    }

    function run(q, idx) {
      var toks = tokenize(q);
      if (!toks.length) return [];
      var N = idx.r.length;
      var avg = idx.avg || 120;
      var acc = null;
      // BM25, so that repetition saturates and a long section does not win on
      // length alone. Without the length term the glossary, one very long
      // passage, outranks the prose for every word it defines.
      var K1 = 1.2, B = 0.6;

      for (var i = 0; i < toks.length; i++) {
        var got = {}, terms = candidates(toks[i], idx);
        for (var j = 0; j < terms.length; j++) {
          var term = terms[j], ps = postings(term, idx);
          // An exact hit counts for more than a word merely begun by it.
          var boost = term === toks[i] ? 1 : 0.45;
          var idf = Math.log(1 + (N - ps.length + 0.5) / (ps.length + 0.5));
          for (var k = 0; k < ps.length; k++) {
            var id = ps[k][0], tf = ps[k][1];
            var dl = (idx.r[id] && idx.r[id].n) || avg;
            var norm = K1 * (1 - B + B * dl / avg);
            var sc = idf * boost * (tf * (K1 + 1)) / (tf + norm);
            if (!got[id] || got[id] < sc) got[id] = sc;
          }
        }
        // Every word must appear somewhere in the passage.
        if (acc === null) {
          acc = got;
        } else {
          var next = {};
          for (var key in got) {
            if (acc[key] !== undefined) next[key] = acc[key] + got[key];
          }
          acc = next;
        }
        if (!Object.keys(acc).length) return [];
      }

      var rows = [];
      for (var id2 in acc) rows.push([Number(id2), acc[id2]]);
      rows.sort(function (a, b) { return b[1] - a[1] || a[0] - b[0]; });
      return rows.slice(0, MAX).map(function (r) { return idx.r[r[0]]; });
    }

    // ---- rendering --------------------------------------------------------
    function esc(s) {
      return String(s).replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    }
    function mark(text, toks) {
      var out = esc(text);
      for (var i = 0; i < toks.length; i++) {
        var safe = toks[i].replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        out = out.replace(new RegExp("(" + safe + "\\w*)", "gi"), "$1");
      }
      return out.replace(//g, "<mark>").replace(//g, "</mark>");
    }

    var sel = -1, items = [];
    function render(results, toks) {
      panel.innerHTML = "";
      items = [];
      sel = -1;
      if (!results.length) {
        panel.innerHTML = '<p class="search-none">No match.</p>';
        live.textContent = "No match.";
      } else {
        results.forEach(function (r) {
          var a = document.createElement("a");
          a.className = "search-hit";
          a.setAttribute("role", "option");
          a.href = ROOT + r.u + (r.a ? "#" + r.a : "");
          a.innerHTML =
            '<span class="search-h">' + mark(r.h || r.p, toks) + "</span>" +
            (r.h ? '<span class="search-p">' + esc(r.p) + "</span>" : "") +
            '<span class="search-x">' + mark(r.x, toks) + "</span>";
          panel.appendChild(a);
          items.push(a);
        });
        live.textContent = results.length === MAX
          ? "Showing the first " + MAX + " matches."
          : results.length + (results.length === 1 ? " match." : " matches.");
      }
      panel.hidden = false;
      input.setAttribute("aria-expanded", "true");
    }

    function close() {
      panel.hidden = true;
      panel.innerHTML = "";
      items = [];
      sel = -1;
      live.textContent = "";
      input.setAttribute("aria-expanded", "false");
    }

    function choose(n) {
      if (!items.length) return;
      if (sel >= 0) items[sel].classList.remove("is-sel");
      sel = (n + items.length) % items.length;
      items[sel].classList.add("is-sel");
      items[sel].scrollIntoView({ block: "nearest" });
    }

    // ---- events -----------------------------------------------------------
    var timer = null;
    function query() {
      var q = input.value.trim();
      if (q.length < 2) { close(); return; }
      index().then(function (idx) {
        if (input.value.trim() !== q) return;   // a later keystroke won
        render(run(q, idx), tokenize(q));
      }).catch(function () {
        panel.innerHTML = '<p class="search-none">Search is unavailable.</p>';
        panel.hidden = false;
      });
    }
    input.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(query, 90);
    });
    input.addEventListener("focus", function () { index().catch(function () {}); });

    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); choose(sel + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); choose(sel - 1); }
      else if (e.key === "Enter" && sel >= 0) { e.preventDefault(); items[sel].click(); }
      else if (e.key === "Escape") { close(); input.blur(); }
    });

    document.addEventListener("click", function (e) {
      if (!form.contains(e.target)) close();
    });

    // A reader with both hands on the keyboard should not have to reach for
    // the pointer to search.
    document.addEventListener("keydown", function (e) {
      var tag = (e.target.tagName || "").toLowerCase();
      var typing = tag === "input" || tag === "textarea" || e.target.isContentEditable;
      if (!typing && (e.key === "/" || ((e.ctrlKey || e.metaKey) && e.key === "k"))) {
        e.preventDefault();
        input.focus();
        input.select();
      }
    });
  })();

})();
