/* pytonIta — comportamenti del sito: tema, ingrandimento delle immagini, dati dell'ultima versione da GitHub. */
(function () {
  "use strict";
  var REPO = "LordZenzo/pytonIta";
  var radice = document.documentElement;

  /* ---- tema chiaro/scuro (ricordato, se il browser lo consente) ---- */
  try { var t = localStorage.getItem("tema"); if (t === "light" || t === "dark") radice.setAttribute("data-theme", t); } catch (e) {}
  var bt = document.querySelector(".tema");
  if (bt) bt.addEventListener("click", function () {
    var scuro = radice.getAttribute("data-theme") === "dark" ||
      (!radice.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
    var nuovo = scuro ? "light" : "dark";
    radice.setAttribute("data-theme", nuovo);
    try { localStorage.setItem("tema", nuovo); } catch (e) {}
  });

  /* ---- ingrandimento delle immagini ---- */
  var dlg = document.createElement("dialog");
  dlg.className = "zoom";
  dlg.innerHTML = '<form method="dialog"><button aria-label="Chiudi">Chiudi ✕</button></form><img alt="">';
  document.body.appendChild(dlg);
  dlg.addEventListener("click", function (e) { if (e.target === dlg || e.target.tagName === "IMG") dlg.close(); });
  document.addEventListener("click", function (e) {
    var b = e.target.closest("button.zoom");
    if (!b || !dlg.showModal) return;
    var img = [].filter.call(b.querySelectorAll("img"), function (x) { return x.offsetParent !== null; })[0] || b.querySelector("img");
    var im = dlg.querySelector("img");
    im.src = img.currentSrc || img.src;
    im.alt = img.alt;
    dlg.showModal();
  });

  /* ---- selettore «con / senza assistente» ---- */
  document.querySelectorAll(".fin .sel button").forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.closest(".fin");
      f.setAttribute("data-vista", b.getAttribute("data-v"));
      f.querySelectorAll(".sel button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
    });
  });

  /* ---- dati dell'ultima versione (pagina di download) ---- */
  function mb(n) { return (n / 1048576).toFixed(1).replace(".", ",") + " MB"; }
  function data(s) { return new Date(s).toLocaleDateString("it-IT", { day: "numeric", month: "long", year: "numeric" }); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function inline(s) {
    return esc(s).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  }
  function note(md) {              // conversione minima di Markdown: titoli, elenchi, paragrafi
    var out = [], lista = false;
    md.split(/\r?\n/).forEach(function (r) {
      var m;
      if (/qui sotto/i.test(r)) return;      // frase valida solo nella pagina della Release
      if ((m = /^\s*[-*]\s+(.*)$/.exec(r))) { if (!lista) { out.push("<ul>"); lista = true; } out.push("<li>" + inline(m[1]) + "</li>"); return; }
      if (lista) { out.push("</ul>"); lista = false; }
      if ((m = /^#{1,3}\s+(.*)$/.exec(r))) { out.push("<h3>" + inline(m[1]) + "</h3>"); return; }
      if (r.trim()) out.push("<p>" + inline(r) + "</p>");
    });
    if (lista) out.push("</ul>");
    return out.join("");
  }
  function installatore(rel) {
    var a = (rel.assets || []).filter(function (x) { return /\.exe$/i.test(x.name); })[0];
    return a || null;
  }

  var box = document.getElementById("ultima");
  if (box && window.fetch) {
    fetch("https://api.github.com/repos/" + REPO + "/releases?per_page=12", { headers: { Accept: "application/vnd.github+json" } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (rels) {
        rels = rels.filter(function (r) { return !r.draft && !r.prerelease; });
        if (!rels.length) throw new Error("nessuna versione");
        var r = rels[0], a = installatore(r);
        document.querySelectorAll("[data-versione]").forEach(function (e) { e.textContent = r.tag_name.replace(/^v/, ""); });
        if (a) {
          document.querySelectorAll("[data-scarica]").forEach(function (e) { e.href = a.browser_download_url; });
          var m = document.getElementById("meta");
          var h = a.digest ? String(a.digest).replace(/^sha256:/, "") : "";
          m.innerHTML = "<dt>Versione</dt><dd>" + esc(r.tag_name.replace(/^v/, "")) + "</dd><dt>Data</dt><dd>" + data(r.published_at) +
            "</dd><dt>File</dt><dd>" + esc(a.name) + "</dd><dt>Dimensione</dt><dd>" + mb(a.size) + "</dd><dt>Scaricato</dt><dd>" + a.download_count +
            " volte</dd>" + (h ? '<dt>SHA-256</dt><dd class="hash">' + esc(h) + "</dd>" : "");
        }
        var n = document.getElementById("note-ultima");
        if (n && r.body) n.innerHTML = note(r.body);
        var c = document.getElementById("cronologia");
        if (c) c.innerHTML = rels.map(function (x) {
          var f = installatore(x);
          return "<tr><td><a href=\"" + esc(x.html_url) + "\">" + esc(x.name || x.tag_name) + "</a></td><td>" + data(x.published_at) + "</td><td>" +
            (f ? '<a href="' + esc(f.browser_download_url) + '">Scarica</a> · ' + mb(f.size) : "—") + "</td></tr>";
        }).join("");
        box.classList.remove("caricamento");
      })
      .catch(function () {
        var m = document.getElementById("meta");
        if (m) m.innerHTML = '<dt>Versione</dt><dd>vedi la pagina delle Release</dd>';
        var n = document.getElementById("note-ultima");
        if (n) n.innerHTML = '<p>Non riesco a leggere i dati da GitHub in questo momento. Le novità sono nella <a href="https://github.com/' + REPO + '/releases/latest">pagina della Release</a>.</p>';
        var c = document.getElementById("cronologia");
        if (c) c.innerHTML = '<tr><td colspan="3"><a href="https://github.com/' + REPO + '/releases">Tutte le versioni su GitHub</a></td></tr>';
      });
  }
})();
