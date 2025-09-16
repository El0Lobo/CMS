// app/static/assets/assets.js
(function () {
  "use strict";

  /* =========================
   *  FIT TEXT TO THUMB WRAP
   * ========================= */
  function fitTextToBox(el, opts) {
    if (!el) return;
    const parent = el.closest(".thumb-wrap") || el.parentElement;
    if (!parent) return;

    const pad = (opts && opts.pad) || 8;
    const minPx = (opts && opts.min) || 8;
    let   maxPx = (opts && opts.max) || 256;

    const pb = parent.getBoundingClientRect();
    const maxW = Math.max(0, pb.width  - pad * 2);
    const maxH = Math.max(0, pb.height - pad * 2);
    if (maxW === 0 || maxH === 0) return;
    maxPx = Math.min(maxPx, Math.floor(maxH));

    const cs = getComputedStyle(el);
    const measure = document.createElement("span");
    measure.textContent = el.textContent || el.innerText || "";
    Object.assign(measure.style, {
      position: "fixed", left: "-99999px", top: "-99999px",
      whiteSpace: "nowrap",
      fontFamily: cs.fontFamily, fontWeight: cs.fontWeight,
      fontStyle: cs.fontStyle, letterSpacing: cs.letterSpacing,
      lineHeight: cs.lineHeight === "normal" ? "1.1" : cs.lineHeight,
      padding: "0", margin: "0", border: "0",
    });
    document.body.appendChild(measure);

    let low = minPx, high = maxPx, best = minPx;
    while (low <= high) {
      const mid = (low + high) >> 1;
      measure.style.fontSize = mid + "px";
      const r = measure.getBoundingClientRect();
      if (r.width <= maxW && r.height <= maxH) { best = mid; low = mid + 1; }
      else { high = mid - 1; }
    }

    el.style.fontSize = best + "px";
    document.body.removeChild(measure);
  }

  // -------------------- helpers --------------------
  function rootEl() { return document.getElementById("assets-root"); }
  function getBase() {
    const el = rootEl();
    let base = el ? el.getAttribute("data-base") : "";
    if (!base) base = "/cms/assets/";
    if (!base.endsWith("/")) base += "/";
    return base;
  }
  function getCookie(name) {
    const m = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return m ? decodeURIComponent(m[2]) : "";
  }
  const CSRF = () => getCookie("csrftoken");

  async function postJSON(url, data) {
    const body =
      data instanceof FormData ? data :
      data ? new URLSearchParams(data) : undefined;
    const headers = { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": CSRF() };
    const res = await fetch(url, { method: "POST", headers, body });
    let payload = {};
    try { payload = await res.json(); } catch {}
    if (!res.ok || payload.ok === false) {
      throw new Error(payload.error || `Request failed: ${res.status}`);
    }
    return payload;
  }

  const ucfirst = (s) => (s ? s.charAt(0).toUpperCase() + s.slice(1) : s);
  const toast = (msg) => console.log(msg);

  function updateVisPill(scopeEl, newState, isCollection) {
    const pill = scopeEl.querySelector(".vis-pill");
    if (!pill) return;
    pill.textContent = newState === "groups" && isCollection ? "Groups" : ucfirst(newState);
    pill.classList.remove("vis-public", "vis-internal", "vis-groups");
    pill.classList.add("vis-" + newState);
  }

  // -------------------- copy text (notes) --------------------
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".js-copy-text");
    if (!btn) return;
    const text = btn.getAttribute("data-text") || "";
    navigator.clipboard.writeText(text).then(() => {
      const old = btn.textContent;
      btn.textContent = "Copied!";
      setTimeout(() => (btn.textContent = old || "Copy Text"), 1100);
    });
  });

  // -------------------- modals (open/close + prefill) --------------------
  function openModal(sel) { const el = document.querySelector(sel); if (el) el.hidden = false; }
  function closeModal(el) { if (el) el.hidden = true; }

  // Prefill "Edit Collection" from a section block
  function prefillCollectionEditFromSection(section) {
    const form = document.querySelector(".js-collection-edit-form");
    if (!form || !section) return;
    form.dataset.colId = section.getAttribute("data-collection-id");
    form.querySelector('[name="title"]').value = section.getAttribute("data-col-title") || "";
    form.querySelector('[name="slug"]').value  = section.getAttribute("data-col-slug")  || "";
    form.querySelector('[name="visibility_mode"]').value =
      section.getAttribute("data-col-visibility") || "public";

    const parentSel = form.querySelector('[name="parent"]');
    const parentVal = section.getAttribute("data-col-parent") || "";
    if (parentSel) parentSel.value = parentVal;

    const selected = (section.getAttribute("data-col-groups") || "").split(",").filter(Boolean);
    const groupSelect = form.querySelector('[name="allowed_groups"]');
    if (groupSelect) {
      Array.from(groupSelect.options).forEach((opt) => { opt.selected = selected.includes(opt.value); });
    }
  }

  document.addEventListener("click", (e) => {
    const opener = e.target.closest("[data-open-modal]");
    if (opener) {
      e.preventDefault();
      const sel = opener.getAttribute("data-open-modal");
      openModal(sel);

      // Prefill "Edit Collection"
      if (sel === "#modal-collection-edit") {
        prefillCollectionEditFromSection(opener.closest(".collection-group"));
      }

      // Prefill "Add Asset" -> collection
      if (sel === "#modal-asset") {
        const form = document.querySelector("#modal-asset form");
        if (form) {
          const colId = opener.getAttribute("data-collection") || "";
          const colTitle = opener.getAttribute("data-collection-title") || "";
          const csel = form.querySelector('select[name="collection"]');
          if (csel && colId) csel.value = String(colId);
          const h2 = document.getElementById("modal-asset-title");
          if (h2) h2.textContent = colTitle ? `Add Asset to ${colTitle}` : "Add Asset";
        }
      }

      // Prefill "New Collection" -> parent
      if (sel === "#modal-collection-new") {
        const form = document.querySelector("#modal-collection-new form");
        if (form) {
          const parentId = opener.getAttribute("data-parent") || opener.getAttribute("data-collection") || "";
          const parentTitle = opener.getAttribute("data-parent-title") || opener.getAttribute("data-collection-title") || "";
          const psel = form.querySelector('select[name="parent"]');
          if (psel && parentId) psel.value = String(parentId);
          const h2 = document.getElementById("modal-collection-title");
          if (h2 && parentTitle) h2.textContent = `New Subcategory of ${parentTitle}`;
        }
      }
    }

    const closer = e.target.closest("[data-close-modal]");
    if (closer) { e.preventDefault(); closeModal(closer.closest(".modal-overlay")); }
  });

  // Click outside modal card to close
  document.addEventListener("mousedown", (e) => {
    const overlay = e.target.closest(".modal-overlay");
    if (overlay && !e.target.closest(".modal-card")) overlay.hidden = true;
  });

  // ESC to close any open modal
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.querySelectorAll(".modal-overlay:not([hidden])").forEach((el) => (el.hidden = true));
    }
  });

  // Save collection edits
  document.addEventListener("click", async (e) => {
    const btn = e.target.closest(".js-collection-edit-save");
    if (!btn) return;
    const form = document.querySelector(".js-collection-edit-form");
    const id = form && form.dataset.colId;
    if (!id) return;
    try {
      const res = await postJSON(`${getBase()}collections/update/${id}/`, new FormData(form));
      if (res.ok) window.location.reload();
    } catch (err) { alert(err.message || "Save failed"); }
  });

  // -------------------- asset + collection actions --------------------
  document.addEventListener("click", async (e) => {
    // Toggle ASSET visibility
    const tAsset = e.target.closest(".js-toggle-vis");
    if (tAsset) {
      e.preventDefault();
      const card = tAsset.closest(".asset-card[data-id], .asset-card[data-asset-id]");
      if (!card) return;
      const id = card.getAttribute("data-id") || card.getAttribute("data-asset-id");
      try {
        const data = await postJSON(tAsset.dataset.url || `${getBase()}toggle/${id}/`);
        updateVisPill(card, data.visibility, false);
        toast("Visibility: " + data.visibility);
      } catch (err) { alert(err.message || "Toggle failed"); }
      return;
    }

    // Delete ASSET
    const dAsset = e.target.closest(".js-asset-delete");
    if (dAsset) {
      e.preventDefault();
      if (!confirm("Delete this asset?")) return;
      const card = dAsset.closest(".asset-card[data-id], .asset-card[data-asset-id]");
      if (!card) return;
      const id = card.getAttribute("data-id") || card.getAttribute("data-asset-id");
      try {
        const data = await postJSON(dAsset.dataset.url || `${getBase()}asset/${id}/delete/`);
        if (data.ok) card.remove();
        toast("Asset deleted");
      } catch (err) { alert(err.message || "Delete failed"); }
      return;
    }

    // Edit ASSET (prefill modal)
    const eAsset = e.target.closest(".js-asset-edit");
    if (eAsset) {
      e.preventDefault();
      const modalSel = eAsset.dataset.openModal || "#modal-asset";
      const modal = document.querySelector(modalSel);
      const form = modal ? modal.querySelector("form") : null;
      if (!modal || !form) return;

      const dataUrl = eAsset.dataset.editUrl;
      const updateUrl = eAsset.dataset.updateUrl;
      if (!dataUrl || !updateUrl) { alert("Missing edit URLs"); return; }

      try {
        const res = await fetch(dataUrl, { headers: { "X-Requested-With": "XMLHttpRequest" } });
        const payload = await res.json();
        if (!res.ok || payload.ok === false) throw new Error(payload.error || "Failed");

        const a = payload.asset;
        form.action = updateUrl;

        const f = (sel) => form.querySelector(sel);
        const set = (sel, v) => { const el = f(sel); if (el) el.value = v ?? ""; };

        set('input[name="title"]', a.title);
        set('input[name="slug"]', a.slug);
        set('textarea[name="description"]', a.description);
        set('input[name="url"]', a.url);
        set('textarea[name="text_content"]', a.text_content);

        const csel = f('select[name="collection"]'); if (csel) csel.value = (a.collection || "").toString();
        const vsel = f('select[name="visibility"]'); if (vsel) vsel.value = a.visibility || "inherit";

        const tset = new Set((a.tags || []).map(String));
        form.querySelectorAll('input[name="tags"]').forEach((inp) => { inp.checked = tset.has(String(inp.value)); });

        const h2 = modal.querySelector("h2"); if (h2) h2.textContent = "Edit Asset";
        modal.hidden = false;
      } catch (err) { alert(err.message || "Failed to load asset"); }
      return;
    }

    // Toggle COLLECTION visibility
    const tCol = e.target.closest(".js-toggle-col-vis");
    if (tCol) {
      e.preventDefault();
      const section = tCol.closest(".collection-group[data-collection-id]");
      if (!section) return;
      const id = section.getAttribute("data-collection-id");
      try {
        const data = await postJSON(tCol.dataset.url || `${getBase()}collections/toggle/${id}/`);
        updateVisPill(section, data.visibility, true);
        section.setAttribute("data-col-visibility", data.visibility);
      } catch (err) { alert(err.message || "Toggle failed"); }
      return;
    }

    // Delete COLLECTION
    const dCol = e.target.closest(".js-collection-delete");
    if (dCol) {
      e.preventDefault();
      if (!confirm("Delete this collection (and all its assets)?")) return;
      const section = dCol.closest(".collection-group[data-collection-id]");
      if (!section) return;
      const id = section.getAttribute("data-collection-id");
      try {
        const data = await postJSON(dCol.dataset.url || `${getBase()}collection/${id}/delete/`);
        if (data.ok) section.remove();
        toast("Collection deleted");
      } catch (err) { alert(err.message || "Delete failed"); }
      return;
    }
  });

  // -------------------- font previews --------------------
  function assetsBrandTextFallback() {
    const root = document.getElementById("assets-root");
    return (root && root.getAttribute("data-brand")) || document.title || "Brand";
  }
  function guessFontFormat(url) {
    const u = (url || "").toLowerCase();
    if (u.endsWith(".woff2")) return "woff2";
    if (u.endsWith(".woff"))  return "woff";
    if (u.endsWith(".ttf"))   return "truetype";
    if (u.endsWith(".otf"))   return "opentype";
    return "";
  }
  async function addFontToDocument(family, url) {
    try {
      const f1 = new FontFace(family, `url("${url}")`);
      const loaded1 = await f1.load(); document.fonts.add(loaded1); return true;
    } catch (e1) {
      try {
        const fmt = guessFontFormat(url);
        const src = fmt ? `url("${url}") format("${fmt}")` : `url("${url}")`;
        const f2 = new FontFace(family, src);
        const loaded2 = await f2.load(); document.fonts.add(loaded2); return true;
      } catch (e2) {
        try {
          const res = await fetch(url, { cache: "reload" });
          if (!res.ok) throw new Error("HTTP " + res.status);
          const blob = await res.blob();
          const blobUrl = URL.createObjectURL(blob);
          const f3 = new FontFace(family, `url("${blobUrl}")`);
          const loaded3 = await f3.load();
          document.fonts.add(loaded3);
          URL.revokeObjectURL(blobUrl);
          return true;
        } catch (e3) {
          console.error("Font preview failed:", { e1, e2, e3, url, family });
          return false;
        }
      }
    }
  }

  async function setupFontThumb(el) {
    const url = el.getAttribute("data-font-url");
    if (!url) return;

    const family = el.getAttribute("data-font-family") || ("assetFont" + Math.round(Math.random() * 1e9));
    const sample = el.getAttribute("data-sample") || assetsBrandTextFallback();

    const ok = await addFontToDocument(family, url);
    if (!ok) { el.innerHTML = `<div class="file-pill">Font</div>`; return; }

    el.innerHTML = `<div class="font-sample" style="font-family:'${family}', system-ui, sans-serif;">${sample}</div>`;
    const sampleEl = el.querySelector(".font-sample");

    await new Promise(r => requestAnimationFrame(r));
    fitTextToBox(sampleEl, { min: 8, max: 256, pad: 10 });

    const parent = sampleEl.closest(".thumb-wrap") || el;
    const ro = new ResizeObserver(() => fitTextToBox(sampleEl, { min: 8, max: 256, pad: 10 }));
    ro.observe(parent);
    window.addEventListener("resize", () => fitTextToBox(sampleEl, { min: 8, max: 256, pad: 10 }), { passive: true });
  }

  async function setupFontPreviewLegacy(el) {
    const url = el.getAttribute("data-font-url");
    if (!url) return;
    const id = el.getAttribute("data-font-id") || Math.random().toString(36).slice(2);
    const family = `assetfont-${id}`;
    const ok = await addFontToDocument(family, url);
    if (ok) {
      const text = el.textContent.trim() || assetsBrandTextFallback();
      el.innerHTML = `<div class="font-sample" style="font-family:'${family}', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;">${text}</div>`;
      const fs = el.querySelector(".font-sample");
      fitTextToBox(fs, { min: 8, max: 256, pad: 10 });
      const parent = fs.closest(".thumb-wrap") || el;
      const ro = new ResizeObserver(() => fitTextToBox(fs, { min: 8, max: 256, pad: 10 }));
      ro.observe(parent);
      window.addEventListener("resize", () => fitTextToBox(fs, { min: 8, max: 256, pad: 10 }), { passive: true });
    } else {
      el.textContent = "Preview unavailable";
      el.style.opacity = "0.7";
    }
  }

  function initFontPreviews() {
    document.querySelectorAll(".font-thumb[data-font-url]").forEach(setupFontThumb);
    document.querySelectorAll(".font-preview[data-font-url]").forEach(setupFontPreviewLegacy);
  }
  document.addEventListener("DOMContentLoaded", initFontPreviews);

  /* =========================
   *  VISIBILITY COG POPOVER
   * =========================
   * render returned .popover into a fixed portal to avoid clipping
   */
  let lastCog = null;
  document.addEventListener("click", (e) => {
    const cog = e.target.closest(".cfg-cog");
    if (cog) lastCog = cog;
  });

  function ensureVisPort() {
    let port = document.getElementById("vis-popover-port");
    if (!port) {
      port = document.createElement("div");
      port.id = "vis-popover-port";
      port.style.position = "fixed";
      port.style.zIndex = "9999";
      port.style.pointerEvents = "none";
      document.body.appendChild(port);
    }
    return port;
  }
  function positionPopoverRelativeToCog(pop, cog) {
    if (!pop || !cog) return;
    pop.style.position = "fixed";
    pop.style.visibility = "hidden";
    pop.style.left = "-10000px";
    pop.style.top = "0px";
    pop.style.pointerEvents = "auto";
    void pop.offsetWidth;

    const t = cog.getBoundingClientRect();
    const pw = pop.offsetWidth, ph = pop.offsetHeight;
    const vw = window.innerWidth, vh = window.innerHeight;
    let left = t.left, top = t.bottom + 6;
    if (left + pw + 8 > vw) left = vw - pw - 8;
    if (left < 8) left = 8;
    if (top + ph + 8 > vh) top = t.top - ph - 6;
    if (top < 8) top = Math.min(vh - ph - 8, t.bottom + 6);
    pop.style.left = Math.round(left) + "px";
    pop.style.top  = Math.round(top) + "px";
    pop.style.visibility = "visible";
  }
  function closePopover() {
    const port = document.getElementById("vis-popover-port");
    if (port) port.innerHTML = "";
  }

  document.addEventListener("htmx:afterSwap", (e) => {
    const target = e.detail && e.detail.target;
    if (!target) return;
    const pop = target.querySelector(".popover[data-vis-popover]") || target.querySelector(".popover");
    if (!pop) return;

    const port = ensureVisPort();
    port.innerHTML = "";
    port.appendChild(pop);

    const trigger =
      (lastCog && document.body.contains(lastCog))
        ? lastCog
        : document.querySelector(".cfg-cog:focus") || target;

    positionPopoverRelativeToCog(pop, trigger);

    const onOutside = (ev) => { if (!pop.contains(ev.target) && !ev.target.closest(".cfg-cog")) cleanup(); };
    const onKey     = (ev) => { if (ev.key === "Escape") cleanup(); };
    const onMove    = () => positionPopoverRelativeToCog(pop, trigger);

    function cleanup() {
      document.removeEventListener("click", onOutside, true);
      window.removeEventListener("keydown", onKey, true);
      window.removeEventListener("resize", onMove);
      window.removeEventListener("scroll", onMove, { capture: false });
      closePopover();
    }

    document.addEventListener("click", onOutside, true);
    window.addEventListener("keydown", onKey, true);
    window.addEventListener("resize", onMove);
    window.addEventListener("scroll", onMove, { passive: true });
  });

})();
