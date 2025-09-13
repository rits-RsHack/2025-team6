(function () {
  const STORAGE_KEY = "theme";
  const root = document.documentElement;
  const btn = document.querySelector(".image-mode");

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    if (btn) {
      btn.textContent = theme === "dark" ? "light" : "dark";
    }
  }

  function initTheme() {
    const first = localStorage.getItem(STORAGE_KEY);
    if (first === "light" || first === "dark") {
      applyTheme(first);
    } else {
      applyTheme("light");
    }
  }

  function toggleTheme() {
    const current = root.getAttribute("data-theme") || "light";
    const next = current === "dark" ? "light" : "dark";
    applyTheme(next);
    localStorage.setItem(STORAGE_KEY, next);
  }
  initTheme();
  if (btn) btn.addEventListener("click", toggleTheme);
})();
