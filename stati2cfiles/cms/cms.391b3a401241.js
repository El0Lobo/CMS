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

  document.addEventListener("DOMContentLoaded", () => {
    restoreMini();
    if (btn) btn.addEventListener("click", toggle);
    if (backdrop) backdrop.addEventListener("click", closeMobileNav);
    window.addEventListener("resize", () => {
      // leave mobile open state when resizing back to desktop
      if (!isMobile()) closeMobileNav();
    });
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
});

