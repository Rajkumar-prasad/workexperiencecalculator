/* Калкулатори: сбор на стаж, осигурителен стаж, стаж за пенсия, клас прослужено време */
(function () {
  "use strict";
  var DAY = 86400000;
  function $(id) { return document.getElementById(id); }
  function num(el) { var v = parseFloat(String(el.value).replace(",", ".")); return isNaN(v) ? 0 : v; }
  function int(el) { return Math.max(0, Math.floor(num(el))); }
  function pl(n, one, many) { return n === 1 ? one : many; }
  function ymd(y, m, d) {
    return y + " " + pl(y, "година", "години") + ", " + m + " " + pl(m, "месец", "месеца") + " и " + d + " " + pl(d, "ден", "дни");
  }
  function norm(y, m, d) { // 30 дни = 1 месец, 12 месеца = 1 година
    m += Math.floor(d / 30); d = d % 30;
    y += Math.floor(m / 12); m = m % 12;
    return { y: y, m: m, d: d };
  }
  function toDays(o) { return o.y * 360 + o.m * 30 + o.d; }
  function fromDays(t) { t = Math.floor(t); return { y: Math.floor(t / 360), m: Math.floor((t % 360) / 30), d: t % 30 }; }
  function parse(iso) { var p = iso.split("-"); return { y: +p[0], m: +p[1], d: +p[2] }; }
  function utc(o) { return Date.UTC(o.y, o.m - 1, o.d); }
  function fromUtc(t) { var d = new Date(t); return { y: d.getUTCFullYear(), m: d.getUTCMonth() + 1, d: d.getUTCDate() }; }
  function dim(y, m) { return new Date(Date.UTC(y, m, 0)).getUTCDate(); }
  function diff(a, endIncl) {
    var b = fromUtc(utc(endIncl) + DAY);
    var y = b.y - a.y, m = b.m - a.m, d = b.d - a.d;
    if (d < 0) { m--; var pm = b.m - 1, py = b.y; if (pm < 1) { pm = 12; py--; } d += dim(py, pm); }
    if (m < 0) { y--; m += 12; }
    return { y: y, m: m, d: d };
  }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function fmt(o) { return pad(o.d) + "." + pad(o.m) + "." + o.y; }
  function todayISO() { var d = new Date(); return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function err(box, msg) { box.textContent = msg; box.hidden = !msg; }
  function show(el) { el.hidden = false; el.scrollIntoView({ behavior: "smooth", block: "nearest" }); }
  function eur(v) { return v.toLocaleString("bg-BG", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €"; }

  /* ---------- 1. Сбор на трудов стаж (години/месеци/дни) ---------- */
  if ($("sbor-tool")) (function () {
    var list = $("sbor-rows"), tpl = $("sbor-tpl");
    function add() { list.appendChild(tpl.content.firstElementChild.cloneNode(true)); renum(); }
    function renum() {
      var rows = list.querySelectorAll(".period");
      rows.forEach(function (r, i) { r.querySelector(".p-num").textContent = "Стаж " + (i + 1); r.querySelector(".p-remove").hidden = rows.length === 1; });
    }
    list.addEventListener("click", function (e) { if (e.target.closest(".p-remove")) { e.target.closest(".period").remove(); renum(); $("sbor-result").hidden = true; } });
    $("sbor-add").addEventListener("click", function () { add(); list.lastElementChild.querySelector("input").focus(); });
    $("sbor-clear").addEventListener("click", function () { list.innerHTML = ""; add(); add(); $("sbor-result").hidden = true; });
    $("sbor-calc").addEventListener("click", function () {
      var Y = 0, M = 0, D = 0, any = false;
      list.querySelectorAll(".period").forEach(function (r) {
        var y = int(r.querySelector(".s-y")), m = int(r.querySelector(".s-m")), d = int(r.querySelector(".s-d"));
        if (y || m || d) any = true;
        Y += y; M += m; D += d;
      });
      if (!any) { err($("sbor-error"), "Въведете поне един стаж в години, месеци или дни."); return; }
      err($("sbor-error"), "");
      var t = norm(Y, M, D);
      $("sbor-y").textContent = t.y; $("sbor-m").textContent = t.m; $("sbor-d").textContent = t.d;
      $("sbor-words").textContent = ymd(t.y, t.m, t.d);
      var left = 360 - (t.m * 30 + t.d);
      $("sbor-next").textContent = (t.m || t.d) ? "До " + (t.y + 1) + " пълни години ви остават " + ymd(0, Math.floor(left / 30), left % 30).replace(/^0 години, /, "") + "." : "Имате точно " + t.y + " пълни " + pl(t.y, "година", "години") + ".";
      show($("sbor-result"));
    });
    add(); add();
  })();

  /* ---------- 2. Осигурителен стаж (с часове на ден) ---------- */
  if ($("osig-tool")) (function () {
    var list = $("osig-rows"), tpl = $("osig-tpl");
    function add() { var n = tpl.content.firstElementChild.cloneNode(true); list.appendChild(n); renum(); return n; }
    function renum() {
      var rows = list.querySelectorAll(".period");
      rows.forEach(function (r, i) { r.querySelector(".p-num").textContent = "Период " + (i + 1); r.querySelector(".p-remove").hidden = rows.length === 1; });
    }
    list.addEventListener("change", function (e) {
      if (e.target.classList.contains("p-now")) { var end = e.target.closest(".period").querySelector(".p-end"); end.disabled = e.target.checked; if (e.target.checked) end.value = todayISO(); }
      $("osig-result").hidden = true;
    });
    list.addEventListener("click", function (e) { if (e.target.closest(".p-remove")) { e.target.closest(".period").remove(); renum(); $("osig-result").hidden = true; } });
    $("osig-add").addEventListener("click", function () { add().querySelector(".p-start").focus(); });
    $("osig-clear").addEventListener("click", function () { list.innerHTML = ""; add(); ["osig-py", "osig-pm", "osig-pd"].forEach(function (i) { $(i).value = ""; }); $("osig-result").hidden = true; });
    $("osig-calc").addEventListener("click", function () {
      var rows = list.querySelectorAll(".period"), ps = [], prop = 0, cal = 0;
      for (var i = 0; i < rows.length; i++) {
        var r = rows[i];
        if (r.querySelector(".p-now").checked) r.querySelector(".p-end").value = todayISO();
        var s = r.querySelector(".p-start").value, e = r.querySelector(".p-end").value, h = num(r.querySelector(".p-h"));
        if (!s || !e) { err($("osig-error"), "Попълнете двете дати за период " + (i + 1) + "."); return; }
        if (h <= 0 || h > 8) { err($("osig-error"), "Период " + (i + 1) + ": часовете на ден трябва да са между 1 и 8."); return; }
        var a = parse(s), b = parse(e);
        if (utc(b) < utc(a)) { err($("osig-error"), "Период " + (i + 1) + ": крайната дата е преди началната."); return; }
        var full = toDays(diff(a, b));
        prop += full * h / 8;
        ps.push({ s: a, e: b });
      }
      err($("osig-error"), "");
      // календарно време без застъпване (таван)
      ps.sort(function (x, y) { return utc(x.s) - utc(y.s); });
      var merged = [];
      ps.forEach(function (p) {
        var l = merged[merged.length - 1];
        if (l && utc(p.s) <= utc(l.e) + DAY) { if (utc(p.e) > utc(l.e)) l.e = p.e; }
        else merged.push({ s: p.s, e: p.e });
      });
      merged.forEach(function (p) { cal += toDays(diff(p.s, p.e)); });
      var capped = prop > cal;
      if (capped) prop = cal;
      var prior = toDays(norm(int($("osig-py")), int($("osig-pm")), int($("osig-pd"))));
      var t = fromDays(prop + prior);
      $("osig-y").textContent = t.y; $("osig-m").textContent = t.m; $("osig-d").textContent = t.d;
      $("osig-words").textContent = ymd(t.y, t.m, t.d);
      $("osig-cap").hidden = !capped;
      show($("osig-result"));
    });
    add();
  })();

  /* ---------- 3. Стаж и възраст за пенсия (III категория) ---------- */
  if ($("pen-tool")) (function () {
    // [година]: [жени възраст (месеци), жени стаж (месеци), мъже възраст, мъже стаж] - чл. 68, ал. 1 и 2 КСО
    var T = {
      2026: [750, 442, 777, 478], 2027: [752, 444, 778, 480], 2028: [754, 444, 779, 480],
      2029: [756, 444, 780, 480], 2030: [759, 444, 780, 480], 2031: [762, 444, 780, 480],
      2032: [765, 444, 780, 480], 2033: [768, 444, 780, 480], 2034: [771, 444, 780, 480],
      2035: [774, 444, 780, 480], 2036: [777, 444, 780, 480], 2037: [780, 444, 780, 480]
    };
    function req(year, female) { var r = T[Math.max(2026, Math.min(2037, year))]; return female ? { age: r[0], st: r[1] } : { age: r[2], st: r[3] }; }
    function ym(months) { var y = Math.floor(months / 12), m = months % 12; return y + " " + pl(y, "година", "години") + (m ? " и " + m + " " + pl(m, "месец", "месеца") : ""); }
    function ageMonths(b, d) { var r = diff(b, fromUtc(utc(d) - DAY)); return r.y * 12 + r.m; }
    $("pen-calc").addEventListener("click", function () {
      var bs = $("pen-birth").value;
      var sex = document.querySelector("input[name=pen-sex]:checked");
      if (!bs || !sex) { err($("pen-error"), "Изберете пол и въведете дата на раждане."); return; }
      var female = sex.value === "f", b = parse(bs);
      var stNow = int($("pen-sy")) * 12 + int($("pen-sm"));
      var working = $("pen-working").checked;
      var today = parse(todayISO());
      if (ageMonths(b, today) < 216) { err($("pen-error"), "Проверете датата на раждане - калкулаторът е за хора над 18 години."); return; }
      err($("pen-error"), "");
      var found = null, alt = null, t0 = utc(today);
      for (var k = 0; k <= 18300; k++) {
        var d = fromUtc(t0 + k * DAY);
        var age = ageMonths(b, d), r = req(d.y, female);
        var st = stNow + (working ? (function () { var x = diff(today, fromUtc(utc(d) - DAY)); return x.y * 12 + x.m; })() : 0);
        if (k === 0) st = stNow;
        if (!found && age >= r.age && st >= r.st) found = { d: d, r: r, age: age, st: st };
        if (!alt && age >= 804 && st >= 180) alt = { d: d, age: age, st: st };
        if (found || alt) break;
      }
      var out = $("pen-main"), rows = $("pen-rows");
      rows.innerHTML = "";
      function row(k, v) { var tr = document.createElement("tr"); tr.innerHTML = "<td>" + k + "</td><td>" + v + "</td>"; rows.appendChild(tr); }
      var best = found;
      if (!best || (alt && utc(alt.d) < utc(found.d))) best = alt ? { d: alt.d, alt: true, age: alt.age, st: alt.st } : found;
      if (!best) {
        out.textContent = "С въведения стаж не достигате изискванията в следващите 50 години.";
      } else if (utc(best.d) <= utc(today)) {
        out.textContent = "Вероятно вече имате право на пенсия.";
      } else {
        var left = diff(today, fromUtc(utc(best.d) - DAY)), parts = [];
        if (left.y) parts.push(left.y + " " + pl(left.y, "година", "години"));
        if (left.m) parts.push(left.m + " " + pl(left.m, "месец", "месеца"));
        if (left.d) parts.push(left.d + " " + pl(left.d, "ден", "дни"));
        out.textContent = "Право на пенсия около " + fmt(best.d) + " - след " + (parts.length > 1 ? parts.slice(0, -1).join(", ") + " и " + parts[parts.length - 1] : parts[0]) + ".";
      }
      if (best) {
        row("Основание", best.alt ? "67 години възраст и 15 години действителен стаж (чл. 68, ал. 3 КСО)" : "Възраст и осигурителен стаж (чл. 68, ал. 1 и 2 КСО)");
        if (!best.alt) { row("Изисквана възраст през " + best.d.y + " г.", ym(best.r.age)); row("Изискван стаж през " + best.d.y + " г.", ym(best.r.st)); }
        row("Вашата възраст тогава", ym(best.age));
        row("Вашият стаж тогава", ym(best.st));
      }
      var r0 = req(today.y, female);
      row("Изисквания за " + today.y + " г.", ym(r0.age) + " / " + ym(r0.st));
      $("pen-note").hidden = working;
      show($("pen-result"));
    });
  })();

  /* ---------- 4. Клас прослужено време ---------- */
  if ($("klas-tool")) (function () {
    $("klas-calc").addEventListener("click", function () {
      var years = int($("klas-years")), sal = num($("klas-salary")), pct = num($("klas-pct"));
      if (sal <= 0) { err($("klas-error"), "Въведете основната си заплата в евро."); return; }
      if (pct < 0.6) { err($("klas-error"), "Процентът не може да е под законовия минимум от 0,6% на година."); return; }
      if (years > 60) { err($("klas-error"), "Проверете броя години стаж."); return; }
      err($("klas-error"), "");
      var totalPct = years * pct, add = sal * totalPct / 100;
      $("klas-main").textContent = eur(add) + " на месец";
      $("klas-r-pct").textContent = totalPct.toLocaleString("bg-BG", { maximumFractionDigits: 2 }) + "%";
      $("klas-r-gross").textContent = eur(sal + add);
      $("klas-r-year").textContent = eur(add * 12);
      $("klas-r-next").textContent = "+" + eur(sal * pct / 100) + " на месец";
      show($("klas-result"));
    });
  })();
})();
