(function () {
  const body = document.body;
  const btn = document.getElementById("navToggle");
  const backdrop = document.querySelector("[data-nav-close]");
  const MINI_KEY = "cmsNavMini";

  function isMobile() {
    return window.matchMedia("(max-width: 900px)").matches;
  }

  function setMini(on) {
    body.classList.toggle("nav-mini", !!on);
    try { localStorage.setItem(MINI_KEY, on ? "1" : "0"); } catch(e){}
  }

  function restoreMini() {
    try {
      const v = localStorage.getItem(MINI_KEY);
      if (v === "1") setMini(true);
    } catch(e){}
  }

  function openMobileNav() {
    body.classList.add("nav-open");
    if (btn) btn.setAttribute("aria-expanded", "true");
  }
  function closeMobileNav() {
    body.classList.remove("nav-open");
    if (btn) btn.setAttribute("aria-expanded", "false");
  }

  function toggle() {
    if (isMobile()) {
      if (body.classList.contains("nav-open")) closeMobileNav(); else openMobileNav();
    } else {
      setMini(!body.classList.contains("nav-mini"));
    }
  }

  function normalisePath(path) {
    if (!path) return "/";
    try {
      const url = new URL(path, window.location.origin);
      path = url.pathname;
    } catch (e) {
      // leave as-is
    }
    if (path.length > 1 && path.endsWith("/")) {
      path = path.slice(0, -1);
    }
    return path || "/";
  }

  function highlightActiveNav() {
    const current = normalisePath(window.location.pathname);
    const links = document.querySelectorAll(".cms-nav nav a[href]");
    let winner = null;
    let bestScore = 0;

    links.forEach((link) => {
      const href = link.getAttribute("href");
      if (!href || href.startsWith("#")) {
        return;
      }
      let target = normalisePath(href);
      if (target === "/") {
        return;
      }
      const match =
        current === target || current.startsWith(target + "/");
      if (match && target.length > bestScore) {
        winner = link;
        bestScore = target.length;
      }
    });

    if (winner) {
      winner.classList.add("is-active");
      winner.setAttribute("aria-current", "page");
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    restoreMini();
    if (btn) btn.addEventListener("click", toggle);
    if (backdrop) backdrop.addEventListener("click", closeMobileNav);
    window.addEventListener("resize", () => {
      // leave mobile open state when resizing back to desktop
      if (!isMobile()) closeMobileNav();
    });
    highlightActiveNav();
  });
  document.addEventListener('click', function(e){
  const pop = e.target.closest('.popover');
  if (!pop && !e.target.classList.contains('cfg-cog')) {
    document.querySelectorAll('.popover').forEach(p=>p.remove());
  }
});
})();
document.body.addEventListener('htmx:configRequest', (e) => {
  const name = 'csrftoken';
  const match = document.cookie.match(new RegExp('(^|;)\\s*' + name + '=([^;]+)'));
  if (match) e.detail.headers['X-CSRFToken'] = match.pop();
});

function initClearableFileButtons() {
  document.addEventListener('click', (event) => {
    const btn = event.target.closest('[data-file-clear]');
    if (!btn) return;

    const checkboxId = btn.getAttribute('data-file-clear');
    if (!checkboxId) return;

    const checkbox = document.getElementById(checkboxId);
    if (!checkbox) return;

    const shouldClear = !checkbox.checked;
    checkbox.checked = shouldClear;

    const inputId = btn.getAttribute('data-file-input');
    const fileInput = inputId ? document.getElementById(inputId) : null;
    if (shouldClear && fileInput) {
      fileInput.value = '';
      fileInput.dispatchEvent(new Event('change', { bubbles: true }));
    }

    const removeLabel = btn.dataset.labelRemove || 'Remove file';
    const undoLabel = btn.dataset.labelUndo || 'Undo remove';
    btn.textContent = shouldClear ? undoLabel : removeLabel;
    btn.setAttribute('aria-pressed', shouldClear ? 'true' : 'false');
  });
}

document.addEventListener('DOMContentLoaded', function () {
  // Detect unread on the inbox page you’re already rendering
  const hasUnread = !!document.querySelector('.thread-list .thread-item.unread');
  const navLink = document.querySelector('a.nav-link-inbox');
  if (navLink) navLink.classList.toggle('has-unread', hasUnread);

  // OPTIONAL: if you mark threads read via JS, also update the nav live:
  document.addEventListener('thread:read-state-changed', function (e) {
    // Dispatch this custom event wherever you toggle read state
    const anyUnread = !!document.querySelector('.thread-list .thread-item.unread');
    const link = document.querySelector('a.nav-link-inbox');
    if (link) link.classList.toggle('has-unread', anyUnread);
  });
  initClearableFileButtons();
});
