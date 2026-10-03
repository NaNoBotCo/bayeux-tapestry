/* Bayeux Tapestry, Unrolled — the strip, the travels, the comet, the stitches. Data in window.D. */
(function () {
  "use strict";
  var D = window.D, U = D.ui, TH = D.lang === "th";
  var DPR = Math.min(window.devicePixelRatio || 1, 2);
  var RM = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var CARD = document.documentElement.classList.contains("card");
  var $ = function (s) { return document.getElementById(s); };
  var C = { linen: "#efe5cf", ink: "#2a2420", red: "#a8442a", ochre: "#c99a3b", green: "#6f7f4f", teal: "#2f4f53", blue: "#3e5c7a", sea: "#c9d6d2", land: "#e6dcc3", back: "#1f1d1b" };
  function fit(cv, h) {
    var w = cv.clientWidth || cv.parentNode.clientWidth;
    cv.width = Math.round(w * DPR); cv.height = Math.round(h * DPR); cv.style.height = h + "px";
    var x = cv.getContext("2d"); x.setTransform(DPR, 0, 0, DPR, 0, 0); return { x: x, w: w, h: h };
  }
  function fmt(n, d) { return n.toLocaleString(TH ? "th-TH" : "en-GB", { maximumFractionDigits: d || 0, minimumFractionDigits: d || 0 }); }
  function yr(n) { return String(Math.floor(n)); }

  /* ---------- the strip ---------- */
  var S = D.strip, SW = D.W;
  var SC = D.scenes;
  function sceneAt(p) { var k = 0; for (var i = 0; i < SC.length; i++) if (SC[i].s <= p) k = i; return k; }
  function metres(p) { return Math.max(0, Math.min(D.len, (p - D.x0) / (D.x1 - D.x0) * D.len)); }

  function Reel(el, opts) {
    var r = this; r.el = el; r.pos = opts.pos || 0; r.h = 0; r.imgs = [];
    var track = document.createElement("div"); track.className = "track"; el.appendChild(track); r.track = track;
    S.forEach(function (t) {
      var im = document.createElement("img"); im.alt = ""; im.decoding = "async"; im.draggable = false;
      im.dataset.src = D.root + "img/strip/" + t.f; track.appendChild(im); r.imgs.push(im);
    });
    r.layout = function () {
      // the photographs carry black margins: rows 0–11 and 342–359 are cropped away
      r.h = el.clientHeight; r.k = r.h / 330; r.vw = el.clientWidth;
      S.forEach(function (t, i) { var s = r.imgs[i].style; s.left = (t.x * r.k) + "px"; s.width = (t.w * r.k) + "px"; s.height = (360 * r.k) + "px"; s.top = (-12 * r.k) + "px"; });
      r.set(r.pos);
    };
    r.max = function () { return SW - r.vw / r.k; };
    r.set = function (p) {
      r.pos = Math.max(0, Math.min(r.max(), p));
      track.style.transform = "translate3d(" + (-r.pos * r.k).toFixed(1) + "px,0,0)";
      var a = r.pos - 400, b = r.pos + r.vw / r.k + 1800;
      S.forEach(function (t, i) { if (t.x < b && t.x + t.w > a && !r.imgs[i].src) r.imgs[i].src = r.imgs[i].dataset.src; });
      if (opts.onmove) opts.onmove(r.pos);
    };
    // drag to pan
    var drag = null;
    el.addEventListener("pointerdown", function (e) { drag = { x: e.clientX, p: r.pos, t: performance.now() }; r.v = 0; if (opts.ongrab) opts.ongrab(); el.setPointerCapture(e.pointerId); el.classList.add("grab"); });
    el.addEventListener("pointermove", function (e) {
      if (!drag) return; var now = performance.now(), np = drag.p - (e.clientX - drag.x) / r.k;
      r.v = (np - r.pos) / Math.max(8, now - drag.t) * 16; drag.t = now; r.set(np);
    });
    function up() { if (!drag) return; drag = null; el.classList.remove("grab"); r.fling(); }
    el.addEventListener("pointerup", up); el.addEventListener("pointercancel", up);
    el.addEventListener("wheel", function (e) { var d = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : 0; if (d) { e.preventDefault(); if (opts.ongrab) opts.ongrab(); r.set(r.pos + d / r.k); } }, { passive: false });
    r.fling = function () { var v = r.v || 0; (function f() { if (Math.abs(v) < 0.3 || drag) return; r.set(r.pos + v); v *= 0.93; requestAnimationFrame(f); })(); };
    r.glide = function (to, ms) {
      var from = r.pos, t0 = performance.now(); ms = RM ? 1 : (ms || 900); to = Math.max(0, Math.min(r.max(), to));
      (function g(now) { var u = Math.min(1, (now - t0) / ms), e = u < .5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2; r.set(from + (to - from) * e); if (u < 1) requestAnimationFrame(g); })(t0);
    };
    addEventListener("resize", r.layout); r.layout();
  }

  // hero: the tapestry slides by
  var hero = $("hreel");
  if (hero) {
    var hp = D.heroStart, run = !RM && !CARD, last = 0;
    var hr = new Reel(hero, { pos: hp, ongrab: function () { run = false; $("hplay").textContent = U.play; } });
    var hb = $("hplay");
    hb.addEventListener("click", function () { run = !run; hb.textContent = run ? U.pause : U.play; });
    if (!run) hb.textContent = U.play;
    (function tick(now) {
      var dt = Math.min(64, now - (last || now)); last = now;
      if (run) { var p = hr.pos + dt * 0.045; if (p >= hr.max()) p = 0; hr.set(p); }
      requestAnimationFrame(tick);
    })(performance.now());
  }

  // the scene reader
  var rd = $("reel");
  if (rd) {
    var lab = $("rscene"), lat = $("rlatin"), say = $("rsay"), mm = $("rm"), rng = $("rpos"), cur = -1;
    rng.max = SW;
    var reel = new Reel(rd, {
      onmove: function (p) {
        var mid = p + rd.clientWidth / (rd.clientHeight / 330) / 2, k = sceneAt(mid);
        rng.value = Math.round(p);
        mm.textContent = fmt(metres(mid), 1) + " m";
        if (k !== cur) {
          cur = k; var s = SC[k];
          lab.textContent = U.scene + " " + s.n;
          lat.textContent = s.la; say.textContent = s.t;
          var on = document.querySelector(".scenes li.on"); if (on) on.classList.remove("on");
          var li = document.querySelector('.scenes li[data-k="' + k + '"]'); if (li) li.classList.add("on");
        }
      }
    });
    rng.addEventListener("input", function () { reel.set(+rng.value); });
    function go(k) { k = Math.max(0, Math.min(SC.length - 1, k)); var s = SC[k]; reel.glide(s.s - 30, 900); }
    $("rprev").addEventListener("click", function () { go(cur - 1); });
    $("rnext").addEventListener("click", function () { go(cur + 1); });
    document.querySelectorAll(".scenes li").forEach(function (li) {
      li.addEventListener("click", function () { go(+li.dataset.k); rd.scrollIntoView({ behavior: RM ? "auto" : "smooth", block: "center" }); });
    });
    var h = location.hash.match(/^#scene-(\d+)/);
    if (h) { var n = +h[1]; SC.forEach(function (s, i) { if (s.n === n) go(i); }); }
  }

  /* ---------- how long: songthaews and your screen ---------- */
  var lc = $("long");
  function drawLong() {
    if (!lc) return; var f = fit(lc, 178), x = f.x, w = f.w;
    var L = D.len, m = w - 24, k = m / 105, y = 30;
    // a football pitch, 105 m, as the ruler
    x.fillStyle = "#6f8f4f"; x.fillRect(12, y, 105 * k, 34); x.strokeStyle = "#fff"; x.lineWidth = 1.5; x.strokeRect(12, y, 105 * k, 34);
    x.beginPath(); x.moveTo(12 + 52.5 * k, y); x.lineTo(12 + 52.5 * k, y + 34); x.stroke();
    x.save(); x.beginPath(); x.rect(12, y, 105 * k, 34); x.clip(); x.beginPath(); x.arc(12 + 52.5 * k, y + 17, 9.15 * k, 0, 7); x.stroke(); x.restore();
    x.fillStyle = C.ink; x.font = "600 13px system-ui,sans-serif"; x.fillText(U.pitch, 12, y - 8);
    // the tapestry, to the same scale
    var ty = y + 52; x.fillStyle = C.linen; x.fillRect(12, ty, L * k, Math.max(3, 0.5 * k)); x.strokeStyle = C.red; x.strokeRect(12, ty, L * k, Math.max(3, 0.5 * k));
    var acc = 0; x.strokeStyle = C.ink; x.lineWidth = 1;
    D.panels.forEach(function (pl, i) { acc += pl; if (i < D.panels.length - 1) { x.beginPath(); x.moveTo(12 + acc * k, ty - 4); x.lineTo(12 + acc * k, ty + Math.max(3, 0.5 * k) + 4); x.stroke(); } });
    x.fillStyle = C.ink; x.fillText(U.tap_len, 12, ty + 22);
    // red songthaews, 5.3 m each
    var sy = ty + 34, n = Math.ceil(L / 5.3);
    for (var i = 0; i < n; i++) {
      var sx = 12 + i * 5.3 * k, sw = Math.min(5.3, L - i * 5.3) * k - 1.5;
      x.fillStyle = "#c8312b"; x.fillRect(sx, sy, sw, 12); x.fillStyle = "#222"; x.beginPath(); x.arc(sx + sw * .22, sy + 13, 2.4, 0, 7); x.arc(sx + sw * .78, sy + 13, 2.4, 0, 7); x.fill();
    }
    x.fillStyle = C.ink; x.fillText(U.songthaew.replace("{n}", fmt(L / 5.3, 0)), 12, sy + 32);
  }
  var scr = $("onscreen");
  function screenLen() {
    if (!scr || !rd) return; var k = rd.clientHeight / 330, px = SW * k;
    // CSS px are 1/96 inch: 0.2646 mm
    scr.textContent = U.screen.replace("{h}", fmt(rd.clientHeight * 0.2646 / 10, 1)).replace("{m}", fmt(px * 0.0002646, 1));
  }

  /* ---------- the map: where it has been ---------- */
  var mc = $("map"), TL = D.timeline, P = D.places, sel = TL.length - 1;
  function proj(f, lon, lat) {
    var b = D.mapbox;
    var c = Math.cos(50 * Math.PI / 180), sx = (b[2] - b[0]) * c, sy = b[3] - b[1];
    var s = Math.min(f.w / sx, f.h / sy), ox = (f.w - sx * s) / 2, oy = (f.h - sy * s) / 2;
    return [ox + (lon - b[0]) * c * s, oy + (b[3] - lat) * s];
  }
  function drawMap() {
    if (!mc) return;
    var f = fit(mc, Math.min(560, Math.max(340, mc.clientWidth * 0.72))), x = f.x;
    x.fillStyle = C.sea; x.fillRect(0, 0, f.w, f.h);
    // sea ripples, stitched
    x.strokeStyle = "rgba(62,92,122,.18)"; x.lineWidth = 1;
    for (var yy = 14; yy < f.h; yy += 18) { x.beginPath(); for (var xx = 0; xx <= f.w; xx += 6) x.lineTo(xx, yy + Math.sin(xx / 14 + yy) * 2.2); x.stroke(); }
    x.fillStyle = C.land; x.strokeStyle = "#8a7a5a"; x.lineWidth = 1.2;
    D.land.polys.forEach(function (pl) { x.beginPath(); pl.forEach(function (q, i) { var p = proj(f, q[0], q[1]); i ? x.lineTo(p[0], p[1]) : x.moveTo(p[0], p[1]); }); x.closePath(); x.fill(); x.stroke(); });
    x.font = "italic 600 13px Georgia,serif"; x.fillStyle = "rgba(47,79,83,.75)";
    var mp = proj(f, -2.3, 50.15); x.fillText(U.channel, mp[0], mp[1]);
    // path through the places, in order, up to the selected row
    var seen = {}, path = [];
    for (var i = 0; i <= sel; i++) { var id = TL[i].p; if (P[id] && (!path.length || path[path.length - 1] !== id)) path.push(id); seen[id] = (seen[id] || 0) + 1; }
    x.strokeStyle = C.red; x.lineWidth = 2.2; x.setLineDash([7, 5]);
    for (var j = 1; j < path.length; j++) {
      var a = proj(f, P[path[j - 1]][0], P[path[j - 1]][1]), b = proj(f, P[path[j]][0], P[path[j]][1]);
      if (a[0] === b[0] && a[1] === b[1]) continue;
      var mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1], bend = 0.18;
      x.beginPath(); x.moveTo(a[0], a[1]); x.quadraticCurveTo(mx - dy * bend, my + dx * bend, b[0], b[1]); x.stroke();
    }
    x.setLineDash([]);
    // every place
    Object.keys(P).forEach(function (id) {
      var q = P[id], p = proj(f, q[0], q[1]), on = TL[sel].p === id, been = !!seen[id];
      if (p[0] < -20 || p[0] > f.w + 20 || p[1] < -20 || p[1] > f.h + 20) return;
      x.beginPath(); x.arc(p[0], p[1], on ? 8 : been ? 5.5 : 4, 0, 7);
      x.fillStyle = on ? C.red : been ? C.teal : "#fff"; x.fill(); x.lineWidth = 1.5; x.strokeStyle = C.ink; x.stroke();
      x.font = (on ? "700 " : been ? "600 " : "400 ") + (on ? 15 : 13) + "px system-ui,sans-serif";
      x.fillStyle = been ? C.ink : "rgba(42,36,32,.55)";
      var t = q[2], tw = x.measureText(t).width, lx = q[3] === "l" ? p[0] - tw - 10 : p[0] + 10, ly = p[1] + (q[3] === "u" ? -8 : 5);
      lx = Math.max(4, Math.min(f.w - tw - 4, lx));
      x.strokeStyle = "rgba(239,229,207,.9)"; x.lineWidth = 4; x.strokeText(t, lx, ly); x.fillText(t, lx, ly);
    });
    // scale bar: 50 km
    var s0 = proj(f, 0, 47.2), s1 = proj(f, 50 / (111.32 * Math.cos(50 * Math.PI / 180)), 47.2);
    var sbx = 14, sby = f.h - 16; x.strokeStyle = C.ink; x.lineWidth = 2; x.beginPath(); x.moveTo(sbx, sby); x.lineTo(sbx + s1[0] - s0[0], sby); x.stroke();
    x.fillStyle = C.ink; x.font = "12px system-ui,sans-serif"; x.fillText("50 km", sbx, sby - 6);
  }
  function pick(i) {
    sel = i; drawMap();
    var on = document.querySelector(".tl li.on"); if (on) on.classList.remove("on");
    var li = document.querySelector('.tl li[data-i="' + i + '"]'); if (li) li.classList.add("on");
    $("mnow").textContent = TL[i].d + " · " + P[TL[i].p][2];
  }
  if (mc) {
    document.querySelectorAll(".tl li").forEach(function (li) { li.addEventListener("click", function () { stopTour(); pick(+li.dataset.i); }); });
    var tour = null, tb = $("mtour");
    function stopTour() { if (tour) { clearInterval(tour); tour = null; tb.textContent = U.tour; } }
    tb.addEventListener("click", function () {
      if (tour) return stopTour();
      var i = 0; pick(0); tb.textContent = U.pause;
      tour = setInterval(function () { i++; if (i >= TL.length) return stopTour(); pick(i); }, 1600);
    });
    pick(sel);
  }

  /* ---------- the comet ---------- */
  var cc = $("comet");
  // Halley's elements (J2000 ecliptic): Ω 58.42°, i 162.26°, ω 111.33°, e 0.96714, q 0.586 AU
  var EL = { O: 58.42, i: 162.26, w: 111.33, e: 0.96714, q: 0.586 }, R = Math.PI / 180;
  var PERI = D.perihelia; // decimal years
  function comet(t) {
    var k = 0; while (k < PERI.length - 2 && PERI[k + 1] <= t) k++;
    var T0 = PERI[k], T1 = PERI[k + 1], M = 2 * Math.PI * (t - T0) / (T1 - T0);
    var e = EL.e, E = M; for (var n = 0; n < 60; n++) E = E - (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
    var a = EL.q / (1 - e), xv = a * (Math.cos(E) - e), yv = a * Math.sqrt(1 - e * e) * Math.sin(E);
    var v = Math.atan2(yv, xv), r = Math.hypot(xv, yv);
    var O = EL.O * R, I = EL.i * R, W = EL.w * R;
    var X = r * (Math.cos(O) * Math.cos(v + W) - Math.sin(O) * Math.sin(v + W) * Math.cos(I));
    var Y = r * (Math.sin(O) * Math.cos(v + W) + Math.cos(O) * Math.sin(v + W) * Math.cos(I));
    var Z = r * Math.sin(v + W) * Math.sin(I);
    return { x: X, y: Y, z: Z, r: r, k: k };
  }
  function orbitAt(E) {
    var e = EL.e, a = EL.q / (1 - e), xv = a * (Math.cos(E) - e), yv = a * Math.sqrt(1 - e * e) * Math.sin(E);
    var v = Math.atan2(yv, xv), r = Math.hypot(xv, yv), O = EL.O * R, I = EL.i * R, W = EL.w * R;
    return { x: r * (Math.cos(O) * Math.cos(v + W) - Math.sin(O) * Math.sin(v + W) * Math.cos(I)), y: r * (Math.sin(O) * Math.cos(v + W) + Math.cos(O) * Math.sin(v + W) * Math.cos(I)) };
  }
  function earth(t) { var d = (t - 2000.0) * 365.25, L = (100.46 + 0.985647 * d) * R; return { x: Math.cos(L), y: Math.sin(L) }; }
  var cy = $("cyear"), ct = 1066.35, crun = false;
  function squash(p) { var r = Math.hypot(p.x, p.y); if (!r) return p; var s = Math.sqrt(r) / r; return { x: p.x * s, y: p.y * s }; }
  function drawComet() {
    if (!cc) return;
    var f = fit(cc, Math.min(460, Math.max(320, cc.clientWidth * .78))), x = f.x;
    x.fillStyle = "#14161b"; x.fillRect(0, 0, f.w, f.h);
    for (var s = 0; s < 140; s++) { var sx = (s * 97.3) % f.w, sy = (s * 53.7 + s * s * 0.31) % f.h; x.fillStyle = "rgba(255,255,255," + (0.15 + (s % 5) * 0.1) + ")"; x.fillRect(sx, sy, 1.2, 1.2); }
    var cxp = f.w * 0.56, cyp = f.h * 0.5, sc = Math.min(f.w, f.h) / 2 / 6.3; // sqrt(35 AU) ≈ 5.9
    function P2(p) { var q = squash(p); return [cxp + q.x * sc, cyp - q.y * sc]; }
    // orbit
    x.strokeStyle = "rgba(201,154,59,.55)"; x.lineWidth = 1.3; x.beginPath();
    var k = comet(ct).k;
    for (var u = 0; u <= 360; u += 1) { var q = P2(orbitAt(u * R)); u ? x.lineTo(q[0], q[1]) : x.moveTo(q[0], q[1]); }
    x.stroke();
    // planets' orbits for scale: Earth 1, Jupiter 5.2, Saturn 9.5, Uranus 19.2, Neptune 30.1 AU
    [[1, U.earth], [5.2, U.jupiter], [9.5, U.saturn], [19.2, U.uranus], [30.1, U.neptune]].forEach(function (o, i) {
      x.strokeStyle = i ? "rgba(255,255,255,.14)" : "rgba(120,180,220,.6)"; x.lineWidth = 1; x.beginPath(); x.arc(cxp, cyp, Math.sqrt(o[0]) * sc, 0, 7); x.stroke();
      if (i) { x.fillStyle = "rgba(255,255,255,.4)"; x.font = "11px system-ui,sans-serif"; x.fillText(o[1], cxp + Math.sqrt(o[0]) * sc * .71 + 3, cyp - Math.sqrt(o[0]) * sc * .71 - 3); }
    });
    // sun
    var g = x.createRadialGradient(cxp, cyp, 0, cxp, cyp, 16); g.addColorStop(0, "#fff6c8"); g.addColorStop(1, "rgba(255,200,80,0)");
    x.fillStyle = g; x.beginPath(); x.arc(cxp, cyp, 16, 0, 7); x.fill();
    // earth
    var ep = P2(earth(ct)); x.fillStyle = "#6fb3e0"; x.beginPath(); x.arc(ep[0], ep[1], 4.5, 0, 7); x.fill();
    x.fillStyle = "#cfe6f5"; x.font = "12px system-ui,sans-serif"; x.fillText(U.earth, ep[0] + 7, ep[1] - 6);
    // comet with a tail pointing away from the sun
    var c = comet(ct), cp = P2(c), ang = Math.atan2(cp[1] - cyp, cp[0] - cxp), tl = Math.max(0, 70 * (1.8 - c.r)) + 6;
    var tg = x.createLinearGradient(cp[0], cp[1], cp[0] + Math.cos(ang) * tl, cp[1] + Math.sin(ang) * tl);
    tg.addColorStop(0, "rgba(255,240,200,.9)"); tg.addColorStop(1, "rgba(255,240,200,0)");
    x.strokeStyle = tg; x.lineWidth = 5; x.lineCap = "round"; x.beginPath(); x.moveTo(cp[0], cp[1]); x.lineTo(cp[0] + Math.cos(ang) * tl, cp[1] + Math.sin(ang) * tl); x.stroke();
    x.fillStyle = "#fff"; x.beginPath(); x.arc(cp[0], cp[1], 3.5, 0, 7); x.fill();
    var ee = earth(ct), dE = Math.sqrt(Math.pow(c.x - ee.x, 2) + Math.pow(c.y - ee.y, 2) + c.z * c.z);
    $("cdist").textContent = fmt(dE, 2) + " AU";
    $("csun").textContent = fmt(c.r, 2) + " AU";
    $("cret").textContent = fmt(Math.max(0, k), 0);
    var nx = PERI.filter(function (p) { return p > ct; })[0];
    $("cnext").textContent = nx ? yr(nx) : "–";
    cy.textContent = yr(ct);
    $("cslide").value = ct;
  }
  if (cc) {
    var cs = $("cslide"); cs.min = PERI[0]; cs.max = PERI[PERI.length - 1] + 1; cs.step = 0.01; cs.value = ct;
    cs.addEventListener("input", function () { ct = +cs.value; crun = false; $("cplay").textContent = U.play; drawComet(); });
    document.querySelectorAll("[data-yr]").forEach(function (b) { b.addEventListener("click", function () { ct = +b.dataset.yr; drawComet(); }); });
    $("cplay").addEventListener("click", function () { crun = !crun; this.textContent = crun ? U.pause : U.play; });
    var cl = 0;
    (function ctick(now) {
      var dt = Math.min(64, now - (cl || now)); cl = now;
      if (crun) { var c = comet(ct); ct += dt / 1000 * (c.r < 3 ? 0.08 : 1.6); if (ct > +cs.max) ct = PERI[0]; drawComet(); }
      requestAnimationFrame(ctick);
    })(performance.now());
  }

  /* ---------- the stitches: laid-and-couched work on a kite shield ---------- */
  var kc = $("stitch"), kstage = 4, kanim = null;
  function shield(u) {
    // a Norman kite shield: round top, sides narrowing to a point; u in [0,1] around the outline
    var a = u * Math.PI * 2, x = Math.sin(a), y = -Math.cos(a);
    var yy = y < 0 ? y * 0.42 : y * 1.25, xx = x * (y < 0 ? 1 : Math.pow(1 - y, 0.85));
    return [xx, yy];
  }
  function inShield(px, py) { // test by sampling the outline width at this height
    if (py < -0.42 || py > 1.25) return false;
    if (py < 0) { var t = py / 0.42; return px * px + t * t <= 1; }
    var y = py / 1.25; return Math.abs(px) <= Math.pow(1 - y, 0.85);
  }
  function drawStitch(progress) {
    if (!kc) return;
    var f = fit(kc, 380), x = f.x, cx = f.w / 2, s = 190, cy = 190 - (1.25 - 0.42) / 2 * s, SX = 0.6;
    x.fillStyle = C.linen; x.fillRect(0, 0, f.w, f.h);
    // linen weave
    x.strokeStyle = "rgba(120,100,70,.10)"; x.lineWidth = 1;
    for (var i = 0; i < f.w; i += 3) { x.beginPath(); x.moveTo(i, 0); x.lineTo(i, f.h); x.stroke(); }
    for (var j = 0; j < f.h; j += 3) { x.beginPath(); x.moveTo(0, j); x.lineTo(f.w, j); x.stroke(); }
    var pr = progress == null ? 1 : progress, total = 0, used = { laid: 0, couch: 0, tie: 0, out: 0 };
    function P(p) { return [cx + p[0] * s * SX, cy + p[1] * s]; }
    // 1 laid threads: long parallel threads across the shape, front only
    if (kstage >= 1) {
      var lines = [], gap = 0.035;
      for (var y = -0.41; y < 1.24; y += gap) {
        var w = y < 0 ? Math.sqrt(Math.max(0, 1 - (y / .42) * (y / .42))) : Math.pow(1 - y / 1.25, .85);
        if (w > 0.01) lines.push([y, w]);
      }
      var n = kstage === 1 ? Math.floor(lines.length * pr) : lines.length;
      x.lineWidth = 3.2; x.lineCap = "round";
      for (var l = 0; l < n; l++) {
        var L = lines[l]; x.strokeStyle = l % 2 ? "#a8442a" : "#b34e33";
        var a = P([-L[1], L[0]]), b = P([L[1], L[0]]); x.beginPath(); x.moveTo(a[0], a[1]); x.lineTo(b[0], b[1]); x.stroke();
        used.laid += 2 * L[1] * s * SX;
      }
    }
    // 2 couching threads: laid the other way, every so often
    if (kstage >= 2) {
      var cols = []; for (var cxx = -0.88; cxx <= 0.89; cxx += 0.22) cols.push(cxx);
      var m = kstage === 2 ? Math.floor(cols.length * pr) : cols.length;
      x.lineWidth = 2.2;
      for (var q = 0; q < m; q++) {
        var X = cols[q], top = null, bot = null;
        for (var yy = -0.42; yy <= 1.25; yy += 0.005) if (inShield(X, yy)) { if (top === null) top = yy; bot = yy; }
        if (top === null) continue;
        x.strokeStyle = "#c99a3b"; var a2 = P([X, top]), b2 = P([X, bot]); x.beginPath(); x.moveTo(a2[0], a2[1]); x.lineTo(b2[0], b2[1]); x.stroke();
        used.couch += (bot - top) * s;
        // 3 tiny tie-down stitches over the couching thread
        if (kstage >= 3) {
          x.strokeStyle = "#6f7f4f"; x.lineWidth = 2;
          var steps = Math.floor((bot - top) / 0.07), shown = kstage === 3 ? Math.floor(steps * pr) : steps;
          for (var tt = 0; tt < shown; tt++) { var ty2 = top + 0.035 + tt * 0.07, c1 = P([X - 0.04, ty2]), c2 = P([X + 0.04, ty2]); x.beginPath(); x.moveTo(c1[0], c1[1]); x.lineTo(c2[0], c2[1]); x.stroke(); used.tie++; }
          x.lineWidth = 2.2;
        }
      }
    }
    // 4 stem-stitch outline: short overlapping slanted stitches
    if (kstage >= 4) {
      var N = 160, shownO = kstage === 4 ? Math.floor(N * pr) : N; x.strokeStyle = "#2a2420"; x.lineWidth = 3;
      for (var o = 0; o < shownO; o++) {
        var p1 = P(shield(o / N)), p2 = P(shield((o + 1.6) / N));
        x.beginPath(); x.moveTo(p1[0] + 1.2, p1[1] - 1.2); x.lineTo(p2[0] - 1.2, p2[1] + 1.2); x.stroke();
        used.out += Math.hypot(p2[0] - p1[0], p2[1] - p1[1]);
      }
    }
    $("kst").textContent = U.stages[kstage - 1];
    // thread on the front, in shield-heights (shield is ~ 1.67 s tall)
    var H = 1.67 * s;
    $("klen").textContent = fmt((used.laid + used.couch + used.out) / H, 1) + " × " + U.kh;
    $("ktie").textContent = fmt(used.tie, 0);
  }
  function stage(n) {
    kstage = n; document.querySelectorAll("[data-st]").forEach(function (b) { b.setAttribute("aria-pressed", +b.dataset.st === n); });
    if (RM) return drawStitch(1);
    var t0 = performance.now(); cancelAnimationFrame(kanim);
    (function a(now) { var p = Math.min(1, (now - t0) / 1600); drawStitch(p); if (p < 1) kanim = requestAnimationFrame(a); })(t0);
  }
  if (kc) document.querySelectorAll("[data-st]").forEach(function (b) { b.addEventListener("click", function () { stage(+b.dataset.st); }); });

  /* ---------- draw everything; redraw on resize ---------- */
  function all() { drawLong(); screenLen(); drawMap(); drawComet(); if (kc) drawStitch(1); }
  var rt; addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(all, 120); });
  all();
  if (kc && !RM) setTimeout(function () { stage(1); var n = 1; var iv = setInterval(function () { n++; if (n > 4) return clearInterval(iv); stage(n); }, 1900); }, 400);
})();
