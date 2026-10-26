// Research-page reading level: shows the gen / orgo / biochem / pchem version of each description.
// Order of precedence: ?level= in the URL, then the visitor's saved choice, then "orgo".
(function () {
  var LEVELS = ["gen", "orgo", "biochem", "pchem"];
  var ALIASES = { adv: "pchem" }; // the first draft had one combined advanced level
  var KEY = "layfield-lab-level";
  var picker = document.getElementById("level-picker");
  if (!picker) return;

  function normalize(level) {
    level = ALIASES[level] || level;
    return LEVELS.indexOf(level) >= 0 ? level : null;
  }
  function saved() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function save(level) {
    try { localStorage.setItem(KEY, level); } catch (e) { /* private mode: choice lasts this page view */ }
  }
  function apply(level) {
    document.documentElement.setAttribute("data-level", level);
    var input = picker.querySelector('input[value="' + level + '"]');
    if (input) input.checked = true;
  }

  var fromUrl = normalize(new URLSearchParams(location.search).get("level"));
  apply(fromUrl || normalize(saved()) || "orgo");

  picker.addEventListener("change", function (event) {
    var level = event.target.value;
    if (LEVELS.indexOf(level) < 0) return;
    apply(level);
    save(level);
    var url = new URL(location.href);
    url.searchParams.set("level", level);
    history.replaceState(null, "", url);
  });
})();
