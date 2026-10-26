// Research-page reading level: shows the gen / orgo / adv version of each description.
// Order of precedence: ?level= in the URL, then the visitor's saved choice, then "orgo".
(function () {
  var LEVELS = ["gen", "orgo", "adv"];
  var KEY = "layfield-lab-level";
  var picker = document.getElementById("level-picker");
  if (!picker) return;

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

  var fromUrl = new URLSearchParams(location.search).get("level");
  var start = LEVELS.indexOf(fromUrl) >= 0 ? fromUrl : saved();
  apply(LEVELS.indexOf(start) >= 0 ? start : "orgo");

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
