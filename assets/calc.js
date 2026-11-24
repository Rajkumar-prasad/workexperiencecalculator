/* Калкулатор за трудов стаж - workexperiencecalculator.online
   Логика: крайната дата се включва, припокриващите се периоди се обединяват,
   разликата се смята по календар (години, месеци, дни), а при сумиране
   30 дни = 1 месец и 12 месеца = 1 година. */
(function () {
  "use strict";

  var list = document.getElementById("periods");
  var tpl = document.getElementById("period-tpl");
  var errorBox = document.getElementById("calc-error");
  var resultBox = document.getElementById("result");
  var STORE = "tsk-periods-v1";

  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function todayISO() {
    var d = new Date();
    return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
  }
  function parse(iso) {
    var p = iso.split("-");
    return { y: +p[0], m: +p[1], d: +p[2] };
  }
  function toUTC(o) { return Date.UTC(o.y, o.m - 1, o.d); }
  function fromUTC(t) {
    var d = new Date(t);
    return { y: d.getUTCFullYear(), m: d.getUTCMonth() + 1, d: d.getUTCDate() };
  }
  var DAY = 86400000;
  function daysInMonth(y, m) { return new Date(Date.UTC(y, m, 0)).getUTCDate(); }
  function fmt(o) { return pad(o.d) + "." + pad(o.m) + "." + o.y; }

  // Календарна разлика от start (вкл.) до end (вкл.)
  function diff(start, end) {
    var b = fromUTC(toUTC(end) + DAY); // денят след крайната дата
    var y = b.y - start.y, m = b.m - start.m, d = b.d - start.d;
    if (d < 0) {
      m -= 1;
      var pm = b.m - 1, py = b.y;
      if (pm < 1) { pm = 12; py -= 1; }
      d += daysInMonth(py, pm);
    }
    if (m < 0) { y -= 1; m += 12; }
    return { y: y, m: m, d: d };
  }

  function addRow(data) {
    var node = tpl.content.firstElementChild.cloneNode(true);
    if (data) {
      node.querySelector(".p-start").value = data.s || "";
      node.querySelector(".p-end").value = data.e || "";
      node.querySelector(".p-now").checked = !!data.now;
    }
    list.appendChild(node);
    syncRow(node);
    renumber();
    return node;
  }

  function syncRow(row) {
    var now = row.querySelector(".p-now").checked;
    var end = row.querySelector(".p-end");
    end.disabled = now;
    if (now) end.value = todayISO();
  }

  function renumber() {
    var rows = list.querySelectorAll(".period");
    rows.forEach(function (r, i) {
      r.querySelector(".p-num").textContent = "Период " + (i + 1);
      r.querySelector(".p-remove").hidden = rows.length === 1;
    });
  }

  function save() {
    try {
      var data = [];
      list.querySelectorAll(".period").forEach(function (r) {
        data.push({
          s: r.querySelector(".p-start").value,
          e: r.querySelector(".p-end").value,
          now: r.querySelector(".p-now").checked
        });
      });
      localStorage.setItem(STORE, JSON.stringify(data));
    } catch (e) { /* storage unavailable */ }
  }

  function load() {
    try {
      var data = JSON.parse(localStorage.getItem(STORE) || "null");
      if (Array.isArray(data) && data.length) { data.forEach(addRow); return; }
    } catch (e) { /* ignore */ }
    addRow();
  }

  function showError(msg) {
    errorBox.textContent = msg;
    errorBox.hidden = !msg;
  }

  function plural(n, one, many) { return n === 1 ? one : many; }
  function words(r) {
    return r.y + " " + plural(r.y, "година", "години") + ", " +
      r.m + " " + plural(r.m, "месец", "месеца") + " и " +
      r.d + " " + plural(r.d, "ден", "дни");
  }

  function calculate() {
    showError("");
    var periods = [];
    var rows = list.querySelectorAll(".period");
    for (var i = 0; i < rows.length; i++) {
      var r = rows[i];
      if (r.querySelector(".p-now").checked) r.querySelector(".p-end").value = todayISO();
      var s = r.querySelector(".p-start").value, e = r.querySelector(".p-end").value;
      if (!s || !e) { showError("Моля, попълнете началната и крайната дата за период " + (i + 1) + "."); return; }
      var ps = parse(s), pe = parse(e);
      if (toUTC(pe) < toUTC(ps)) { showError("Период " + (i + 1) + ": крайната дата е преди началната."); return; }
      periods.push({ idx: i + 1, s: ps, e: pe });
    }

    // Обединяване на припокриващи се периоди
    var sorted = periods.slice().sort(function (a, b) { return toUTC(a.s) - toUTC(b.s); });
    var merged = [];
    sorted.forEach(function (p) {
      var last = merged[merged.length - 1];
      if (last && toUTC(p.s) <= toUTC(last.e) + DAY) {
        if (toUTC(p.e) > toUTC(last.e)) last.e = p.e;
        last.overlap = last.overlap || toUTC(p.s) <= toUTC(last.e);
      } else {
        merged.push({ s: p.s, e: p.e, overlap: false });
      }
    });
    var hadOverlap = merged.length < periods.length;

    var Y = 0, M = 0, D = 0, totalDays = 0;
    merged.forEach(function (p) {
      var r = diff(p.s, p.e);
      Y += r.y; M += r.m; D += r.d;
      totalDays += Math.round((toUTC(p.e) - toUTC(p.s)) / DAY) + 1;
    });
    M += Math.floor(D / 30); D = D % 30;
    Y += Math.floor(M / 12); M = M % 12;
    var total = { y: Y, m: M, d: D };

    // Изход
    document.getElementById("r-y").textContent = Y;
    document.getElementById("r-m").textContent = M;
    document.getElementById("r-d").textContent = D;
    document.getElementById("r-words").textContent = words(total);
    document.getElementById("r-days").textContent = totalDays.toLocaleString("bg-BG");

    var tbody = document.getElementById("r-rows");
    tbody.innerHTML = "";
    periods.forEach(function (p) {
      var r = diff(p.s, p.e);
      var tr = document.createElement("tr");
      tr.innerHTML = "<td>" + p.idx + "</td><td>" + fmt(p.s) + " - " + fmt(p.e) +
        "</td><td>" + r.y + " г. " + r.m + " м. " + r.d + " д.</td>";
      tbody.appendChild(tr);
    });
    document.getElementById("r-overlap").hidden = !hadOverlap;

    resultBox.hidden = false;
    resultBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
    save();
  }

  // Събития
  list.addEventListener("change", function (e) {
    var row = e.target.closest(".period");
    if (e.target.classList.contains("p-now")) syncRow(row);
    resultBox.hidden = true;
    save();
  });
  list.addEventListener("click", function (e) {
    if (e.target.closest(".p-remove")) {
      e.target.closest(".period").remove();
      renumber(); resultBox.hidden = true; save();
    }
  });
  document.getElementById("add-period").addEventListener("click", function () {
    var row = addRow();
    row.querySelector(".p-start").focus();
    resultBox.hidden = true;
  });
  document.getElementById("calc-btn").addEventListener("click", calculate);
  document.getElementById("clear-btn").addEventListener("click", function () {
    list.innerHTML = ""; addRow(); showError(""); resultBox.hidden = true;
    try { localStorage.removeItem(STORE); } catch (e) { /* ignore */ }
  });

  // Изнасяме функциите за тестове
  window.__tsk = { diff: diff, parse: parse };

  load();
})();
