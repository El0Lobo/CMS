const DEFAULT_BLOCK_LIBRARY = [
  {
    type: "hero",
    icon: "🌄",
    label: "Hero banner",
    description: "Large hero with background image and primary call-to-actions.",
    defaults: {
      kicker: "",
      title: "Welcome to our space",
      subtitle: "Introduce the vibe of your venue or collective here.",
      background_image: "",
      overlay: 0.45,
      alignment: "center",
      actions: [],
    },
    fields: [
      { key: "kicker", type: "text", label: "Kicker" },
      { key: "title", type: "text", label: "Headline" },
      { key: "subtitle", type: "textarea", label: "Subheadline", rows: 3 },
      {
        key: "background_image",
        type: "url",
        label: "Background image URL",
        help: "Paste an image URL from the media library.",
        assetKinds: ["image"],
      },
      {
        key: "overlay",
        type: "range",
        label: "Overlay strength",
        min: 0,
        max: 0.85,
        step: 0.05,
      },
      {
        key: "alignment",
        type: "select",
        label: "Text alignment",
        options: [
          { value: "left", label: "Left" },
          { value: "center", label: "Center" },
          { value: "right", label: "Right" },
        ],
      },
      {
        key: "actions",
        type: "list",
        label: "Buttons",
        itemLabel: "Button",
        itemDefaults: { label: "Learn more", href: "#", style: "primary", new_tab: false },
        itemFields: [
          { key: "label", type: "text", label: "Label" },
          { key: "href", type: "url", label: "Link" },
          {
            key: "style",
            type: "select",
            label: "Style",
            options: [
              { value: "primary", label: "Primary" },
              { value: "ghost", label: "Outline" },
              { value: "link", label: "Link" },
            ],
          },
          { key: "new_tab", type: "toggle", label: "Open in new tab" },
        ],
      },
    ],
  },
  {
    type: "rich_text",
    icon: "✍️",
    label: "Rich text",
    description: "Free-form HTML section for detailed copy.",
    defaults: {
      html: "<p>Write your story here. This block accepts standard HTML.</p>",
    },
    fields: [
      {
        key: "html",
        type: "textarea",
        label: "Content",
        rows: 8,
        help: "Supports HTML markup. Use paragraphs, headings, lists, etc.",
      },
    ],
  },
  {
    type: "events",
    icon: "🎟️",
    label: "Events",
    description: "Showcase upcoming events pulled from the CMS schedule.",
    defaults: {
      title: "Upcoming events",
      subtitle: "",
      limit: 4,
      include_internal: false,
      layout: "grid",
      show_actions: true,
      open_mode: "link",
    },
    fields: [
      { key: "title", type: "text", label: "Section title" },
      { key: "subtitle", type: "textarea", label: "Subtitle", rows: 2 },
      { key: "limit", type: "number", label: "Number of events", min: 1, max: 16 },
      { key: "include_internal", type: "toggle", label: "Include internal events" },
      {
        key: "layout",
        type: "select",
        label: "Layout",
        options: [
          { value: "grid", label: "Grid" },
          { value: "list", label: "List" },
        ],
      },
      {
        key: "open_mode",
        type: "select",
        label: "Click action",
        options: [
          { value: "link", label: "Go to event page" },
          { value: "modal", label: "Open quick view modal" },
          { value: "none", label: "No action" },
        ],
      },
      { key: "show_actions", type: "toggle", label: "Show “Details” buttons" },
    ],
  },
  {
    type: "menu",
    icon: "🍹",
    label: "Menu",
    description: "Highlight menu categories or dishes from the POS menu.",
    defaults: {
      title: "Menu highlights",
      subtitle: "",
      category_slugs: [],
    },
    fields: [
      { key: "title", type: "text", label: "Section title" },
      { key: "subtitle", type: "textarea", label: "Subtitle", rows: 2 },
      {
        key: "category_slugs",
        type: "sluglist",
        label: "Limit to categories",
        help: "Optional. Enter category slugs separated by commas. Leave empty to show all top-level categories.",
      },
    ],
  },
  {
    type: "opening_hours",
    icon: "⏰",
    label: "Opening hours",
    description: "Display the structured opening hours from site settings.",
    defaults: {
      title: "Opening hours",
      subtitle: "",
      show_contact: true,
    },
    fields: [
      { key: "title", type: "text", label: "Section title" },
      { key: "subtitle", type: "textarea", label: "Subtitle", rows: 2 },
      { key: "show_contact", type: "toggle", label: "Show contact details" },
    ],
  },
  {
    type: "contact",
    icon: "☎️",
    label: "Contact",
    description: "Contact details and social links sourced from site settings.",
    defaults: {
      show_social: true,
    },
    fields: [
      { key: "show_social", type: "toggle", label: "Show social links" },
    ],
  },
  {
    type: "gallery",
    icon: "🖼️",
    label: "Gallery",
    description: "Grid of images with optional captions.",
    defaults: {
      title: "Gallery",
      subtitle: "",
      columns: 3,
      items: [],
    },
    fields: [
      { key: "title", type: "text", label: "Section title" },
      { key: "subtitle", type: "textarea", label: "Subtitle", rows: 2 },
      { key: "columns", type: "number", label: "Columns", min: 1, max: 4 },
      {
        key: "items",
        type: "list",
        label: "Images",
        itemLabel: "Image",
        itemDefaults: { image: "", caption: "", alt: "" },
        itemFields: [
          { key: "image", type: "url", label: "Image URL", assetKinds: ["image"] },
          { key: "caption", type: "text", label: "Caption" },
          { key: "alt", type: "text", label: "Alt text" },
        ],
      },
    ],
  },
  {
    type: "footer",
    icon: "🪪",
    label: "Footer",
    description: "Footer bar with navigation and legal links.",
    defaults: {
      show_social: true,
      links: [],
      legal: [],
    },
    fields: [
      { key: "show_social", type: "toggle", label: "Show social icons" },
      {
        key: "links",
        type: "list",
        label: "Primary links",
        itemLabel: "Link",
        itemDefaults: { label: "About", href: "#", new_tab: false },
        itemFields: [
          { key: "label", type: "text", label: "Label" },
          { key: "href", type: "url", label: "URL" },
          { key: "new_tab", type: "toggle", label: "Open in new tab" },
        ],
      },
      {
        key: "legal",
        type: "list",
        label: "Legal links",
        itemLabel: "Link",
        itemDefaults: { label: "Imprint", href: "#", new_tab: false },
        itemFields: [
          { key: "label", type: "text", label: "Label" },
          { key: "href", type: "url", label: "URL" },
          { key: "new_tab", type: "toggle", label: "Open in new tab" },
        ],
      },
    ],
  },
];

const state = {
  blocks: [],
  selectedId: null,
  dirty: false,
};

function escapeHtml(value = "") {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function cssUrl(value = "") {
  return String(value).replace(/"/g, '\\"');
}

const dom = {};
let config = {};
let previewTimer = null;
let previewInflight = null;

const assetState = {
  modal: null,
  panel: null,
  overlay: null,
  closeButtons: [],
  list: null,
  subtitle: null,
  kinds: [],
  cache: {},
  onSelect: null,
};

function isAssetBrowserOpen() {
  return assetState.modal && !assetState.modal.classList.contains("is-hidden");
}

function closeAssetBrowser() {
  if (!assetState.modal) {
    return;
  }
  assetState.modal.classList.add("is-hidden");
  assetState.modal.setAttribute("aria-hidden", "true");
  assetState.onSelect = null;
  assetState.kinds = [];
}

function renderAssetCards(assets) {
  if (!assetState.list) {
    return;
  }
  assetState.list.innerHTML = "";
  if (!assets.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "No assets available yet.";
    assetState.list.appendChild(empty);
    return;
  }

  assets.forEach((asset) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `asset-card asset-card--${asset.kind}`;
    const title = escapeHtml(asset.title || asset.slug || asset.kind);
    let thumb = "";
    if (asset.kind === "image" && asset.url) {
      thumb = `<div class="asset-card__thumbnail" style="background-image:url(&quot;${cssUrl(asset.url)}&quot;);"></div>`;
    } else {
      const icon = asset.kind ? escapeHtml(asset.kind.slice(0, 1).toUpperCase()) : "•";
      thumb = `<div class="asset-card__thumbnail asset-card__thumbnail--icon">${icon}</div>`;
    }
    const kindLabel = escapeHtml((asset.kind || "").toUpperCase());
    const mimeLabel = asset.mime_type ? ` · ${escapeHtml(asset.mime_type)}` : "";
    const meta = `
      <div class="asset-card__meta">
        <strong>${title}</strong>
        <span>${kindLabel}${mimeLabel}</span>
      </div>
    `;
    button.innerHTML = `${thumb}${meta}`;
    button.addEventListener("click", () => {
      if (typeof assetState.onSelect === "function") {
        assetState.onSelect(asset);
      }
      closeAssetBrowser();
    });
    assetState.list.appendChild(button);
  });
}

async function loadAssets(kinds) {
  if (!assetState.list) {
    return;
  }
  const key = kinds && kinds.length ? kinds.slice().sort().join(",") : "all";
  if (!assetState.cache[key]) {
    if (!config.urls || !config.urls.assets) {
      assetState.list.innerHTML = "<p class=\"muted\">Asset library unavailable.</p>";
      return;
    }
    const params = new URLSearchParams();
    (kinds || []).forEach((kind) => params.append("kind", kind));
    const url = `${config.urls.assets}${params.toString() ? `?${params.toString()}` : ""}`;
    assetState.list.innerHTML = "<p class=\"muted\">Loading assets…</p>";
    try {
      const response = await fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });
      if (!response.ok) {
        throw new Error(`Failed to load assets (${response.status})`);
      }
      const data = await response.json();
      assetState.cache[key] = data.assets || [];
    } catch (error) {
      console.error(error);
      assetState.list.innerHTML = "<p class=\"muted\">Could not load assets.</p>";
      return;
    }
  }
  renderAssetCards(assetState.cache[key]);
}

function openAssetBrowser({ kinds = [], onSelect }) {
  if (!assetState.modal) {
    return;
  }
  assetState.kinds = kinds;
  assetState.onSelect = onSelect;
  if (assetState.subtitle) {
    assetState.subtitle.textContent = kinds.length
      ? `Showing ${kinds.join(", ")} assets`
      : "Showing all public assets";
  }
  assetState.modal.classList.remove("is-hidden");
  assetState.modal.setAttribute("aria-hidden", "false");
  if (assetState.panel) {
    assetState.panel.focus();
  }
  loadAssets(kinds);
}

function uuid() {
  if (window.crypto && window.crypto.randomUUID) {
    return window.crypto.randomUUID();
  }
  return `blk_${Math.random().toString(16).slice(2)}${Date.now()}`;
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function getBlueprint(type) {
  return DEFAULT_BLOCK_LIBRARY.find((b) => b.type === type);
}

function normaliseBlock(block) {
  const blueprint = getBlueprint(block.type);
  if (!blueprint) {
    return block;
  }
  const props = { ...clone(blueprint.defaults), ...clone(block.props || {}) };

  // Type conversions
  blueprint.fields.forEach((field) => {
    const key = field.key;
    if (!(key in props)) {
      return;
    }
    const value = props[key];
    switch (field.type) {
      case "number":
      case "range":
        props[key] = value === "" || value === null ? null : Number(value);
        break;
      case "toggle":
        props[key] = Boolean(value);
        break;
      case "sluglist":
        if (Array.isArray(value)) {
          props[key] = value;
        } else if (typeof value === "string") {
          props[key] = value
            .split(",")
            .map((item) => item.trim())
            .filter(Boolean);
        } else {
          props[key] = [];
        }
        break;
      case "list":
        if (!Array.isArray(value)) {
          props[key] = [];
        } else {
          props[key] = value.map((item) => ({
            ...clone(field.itemDefaults || {}),
            ...item,
          }));
        }
        break;
      default:
        break;
    }
  });

  return {
    id: block.id || uuid(),
    type: block.type,
    props,
  };
}

function normaliseBlocks(blocks) {
  return (blocks || []).map(normaliseBlock);
}

function getSelectedBlock() {
  return state.blocks.find((b) => b.id === state.selectedId) || null;
}

function persistBlocks() {
  if (!dom.blocksInput) {
    return;
  }
  dom.blocksInput.value = JSON.stringify(state.blocks);
}

function schedulePreview(immediate = false) {
  persistBlocks();
  if (!config.urls || !config.urls.preview) {
    return;
  }
  if (immediate) {
    return fetchPreview();
  }
  if (previewTimer) {
    window.clearTimeout(previewTimer);
  }
  previewTimer = window.setTimeout(fetchPreview, 450);
}

function setPreviewHTML(html) {
  if (!dom.previewFrame) {
    return;
  }
  const content =
    html && html.trim()
      ? html
      : "<!doctype html><html><head><meta charset='utf-8'><style>body{margin:0;padding:2rem;font-family:system-ui;background:#0b1118;color:#f0f4f8;} .muted{color:rgba(255,255,255,0.6);}</style></head><body><p class='muted'>Preview will appear here once you add blocks.</p></body></html>";
  if (dom.previewFrame.srcdoc !== content) {
    dom.previewFrame.srcdoc = content;
  }
}

function getCsrfToken() {
  const input = document.querySelector('input[name="csrfmiddlewaretoken"]');
  return input ? input.value : "";
}

async function fetchPreview() {
  if (!config.urls || !config.urls.preview) {
    return;
  }
  const navField = document.getElementById("id_custom_nav_items");
  const showNavField = document.getElementById("id_show_navigation_bar");
  let navItems = [];
  if (navField) {
    try {
      navItems = JSON.parse(navField.value || "[]");
    } catch (error) {
      console.warn("Could not parse navigation items for preview", error);
      navItems = [];
    }
  }
  const showNav = showNavField ? !!showNavField.checked : false;
  const bodyField = document.getElementById("id_body");
  const renderRawField = document.getElementById("id_render_body_only");
  const payload = {
    blocks: state.blocks,
    custom_nav_items: navItems,
    show_navigation_bar: showNav,
    render_body_only: renderRawField ? !!renderRawField.checked : false,
    body: bodyField ? bodyField.value : "",
  };
  if (previewInflight) {
    previewInflight.abort();
  }
  const controller = new AbortController();
  previewInflight = controller;
  try {
    const response = await fetch(config.urls.preview, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken(),
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new Error(`Preview failed with status ${response.status}`);
    }
    const data = await response.json();
    setPreviewHTML(data.html || "");
  } catch (error) {
    if (error.name === "AbortError") {
      return;
    }
    console.error(error);
  } finally {
    previewInflight = null;
  }
}

function renderLibrary() {
  if (!dom.library) {
    return;
  }
  dom.library.innerHTML = "";
  DEFAULT_BLOCK_LIBRARY.forEach((block) => {
    const button = document.createElement("button");
    button.className = "builder-library-item";
    button.type = "button";
    button.dataset.blockType = block.type;
    button.innerHTML = `
      <span class="builder-library-item__icon">${block.icon}</span>
      <span>
        <strong>${block.label}</strong>
        <small class="muted">${block.description}</small>
      </span>
    `;
    button.addEventListener("click", () => {
      addBlock(block.type);
    });
    dom.library.appendChild(button);
  });
}

function renderBlockList() {
  if (!dom.blockList) {
    return;
  }
  dom.blockList.innerHTML = "";
  if (!state.blocks.length) {
    const empty = document.createElement("li");
    empty.className = "builder-empty";
    empty.textContent = "No blocks yet. Add one from the sidebar.";
    dom.blockList.appendChild(empty);
    return;
  }

  state.blocks.forEach((block, index) => {
    const blueprint = getBlueprint(block.type);
    const item = document.createElement("li");
    item.className = `builder-block${block.id === state.selectedId ? " is-selected" : ""}`;
    item.dataset.blockId = block.id;
    item.innerHTML = `
      <div class="builder-block__title">
        <strong>${blueprint ? blueprint.label : block.type}</strong>
        <span class="muted">#${index + 1}</span>
      </div>
      <div class="builder-block__controls">
        <button type="button" class="builder-block__btn" data-action="select">Edit</button>
        <button type="button" class="builder-block__btn" data-action="up">↑</button>
        <button type="button" class="builder-block__btn" data-action="down">↓</button>
        <button type="button" class="builder-block__btn builder-block__btn--danger" data-action="delete">✕</button>
      </div>
    `;
    item.addEventListener("click", (event) => {
      event.preventDefault();
      const action = event.target.dataset.action;
      if (action === "up") {
        event.stopPropagation();
        moveBlock(block.id, -1);
      } else if (action === "down") {
        event.stopPropagation();
        moveBlock(block.id, 1);
      } else if (action === "delete") {
        event.stopPropagation();
        removeBlock(block.id);
      } else {
        selectBlock(block.id);
      }
    });
    dom.blockList.appendChild(item);
  });
}

function renderSettings() {
  if (!dom.settings) {
    return;
  }
  dom.settings.innerHTML = "";
  const block = getSelectedBlock();
  if (!block) {
    const message = document.createElement("p");
    message.className = "muted";
    message.textContent = "Select a block to configure it.";
    dom.settings.appendChild(message);
    return;
  }
  const blueprint = getBlueprint(block.type);
  if (!blueprint) {
    dom.settings.textContent = "Unknown block type.";
    return;
  }

  const form = document.createElement("div");
  form.className = "builder-settings__panel";

  blueprint.fields.forEach((field) => {
    form.appendChild(renderField(block, field));
  });

  dom.settings.appendChild(form);
}

function renderField(block, field) {
  const container = document.createElement("div");
  container.className = "builder-field";

  const label = document.createElement("label");
  label.textContent = field.label;
  container.appendChild(label);

  if (field.help) {
    const hint = document.createElement("small");
    hint.className = "muted";
    hint.textContent = field.help;
    container.appendChild(hint);
  }

  const value = block.props[field.key];
  let input;

  switch (field.type) {
    case "text":
    case "url":
      input = document.createElement("input");
      input.type = field.type === "url" ? "url" : "text";
      input.value = value || "";
      input.addEventListener("input", (event) => {
        updateBlockProp(block.id, field.key, event.target.value);
      });
      break;
    case "number":
      input = document.createElement("input");
      input.type = "number";
      if (field.min !== undefined) input.min = field.min;
      if (field.max !== undefined) input.max = field.max;
      if (field.step !== undefined) input.step = field.step;
      input.value = value ?? "";
      input.addEventListener("input", (event) => {
        const val = event.target.value;
        updateBlockProp(block.id, field.key, val === "" ? null : Number(val));
      });
      break;
    case "range":
      input = document.createElement("input");
      input.type = "range";
      input.min = field.min ?? 0;
      input.max = field.max ?? 1;
      input.step = field.step ?? 0.05;
      input.value = value ?? field.min ?? 0;
      const rangeValue = document.createElement("span");
      rangeValue.className = "muted";
      rangeValue.textContent = Number(input.value).toFixed(2);
      input.addEventListener("input", (event) => {
        const val = Number(event.target.value);
        rangeValue.textContent = val.toFixed(2);
        updateBlockProp(block.id, field.key, val);
      });
      container.appendChild(rangeValue);
      break;
    case "textarea":
      input = document.createElement("textarea");
      input.rows = field.rows || 4;
      input.value = value || "";
      input.addEventListener("input", (event) => {
        updateBlockProp(block.id, field.key, event.target.value);
      });
      break;
    case "select":
      input = document.createElement("select");
      (field.options || []).forEach((option) => {
        const opt = document.createElement("option");
        opt.value = option.value;
        opt.textContent = option.label;
        input.appendChild(opt);
      });
      input.value = value || (field.options && field.options[0] && field.options[0].value) || "";
      input.addEventListener("change", (event) => {
        updateBlockProp(block.id, field.key, event.target.value);
      });
      break;
    case "toggle":
      input = document.createElement("input");
      input.type = "checkbox";
      input.checked = Boolean(value);
      input.addEventListener("change", (event) => {
        updateBlockProp(block.id, field.key, event.target.checked);
      });
      break;
    case "sluglist":
      input = document.createElement("input");
      input.type = "text";
      input.value = Array.isArray(value) ? value.join(", ") : value || "";
      input.placeholder = "category-one, category-two";
      input.addEventListener("input", (event) => {
        const raw = event.target.value;
        const items = raw
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean);
        updateBlockProp(block.id, field.key, items);
      });
      break;
    case "list":
      return renderListField(block, field);
    default:
      input = document.createElement("input");
      input.type = "text";
      input.value = value || "";
      input.addEventListener("input", (event) => {
        updateBlockProp(block.id, field.key, event.target.value);
      });
  }

  if (input) {
    container.appendChild(input);
    if (field.assetKinds && field.assetKinds.length) {
      const picker = document.createElement("button");
      picker.type = "button";
      picker.className = "btn btn-sm builder-field__asset-btn";
      picker.textContent = "Choose from library";
      picker.addEventListener("click", (event) => {
        event.preventDefault();
        openAssetBrowser({
          kinds: field.assetKinds,
          onSelect: (asset) => {
            const url = asset.url || "";
            input.value = url;
            updateBlockProp(block.id, field.key, url);
            schedulePreview(true);
          },
        });
      });
      container.appendChild(picker);
    }
  }

  return container;
}

function renderListField(block, field) {
  const container = document.createElement("div");
  container.className = "builder-actions";
  const items = Array.isArray(block.props[field.key]) ? block.props[field.key] : [];

  const list = document.createElement("div");
  list.className = "builder-actions-list";

  items.forEach((item, index) => {
    const itemCard = document.createElement("div");
    itemCard.className = "builder-actions-item";

    const header = document.createElement("header");
    header.innerHTML = `<strong>${field.itemLabel || "Item"} #${index + 1}</strong>`;

    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "builder-block__btn builder-block__btn--danger";
    remove.textContent = "Remove";
    remove.addEventListener("click", () => {
      const nextItems = items.slice(0, index).concat(items.slice(index + 1));
      updateBlockProp(block.id, field.key, nextItems);
      renderSettings();
      schedulePreview();
    });

    header.appendChild(remove);
    itemCard.appendChild(header);

    (field.itemFields || []).forEach((subField) => {
      const subContainer = document.createElement("div");
      subContainer.className = "builder-field";
      const label = document.createElement("label");
      label.textContent = subField.label;
      subContainer.appendChild(label);

      const currentValue = item[subField.key];
      let input;
      if (subField.type === "toggle") {
        input = document.createElement("input");
        input.type = "checkbox";
        input.checked = Boolean(currentValue);
        input.addEventListener("change", (event) => {
          const next = clone(items);
          next[index][subField.key] = event.target.checked;
          updateBlockProp(block.id, field.key, next);
          schedulePreview();
        });
      } else if (subField.type === "select") {
        input = document.createElement("select");
        (subField.options || []).forEach((option) => {
          const opt = document.createElement("option");
          opt.value = option.value;
          opt.textContent = option.label;
          input.appendChild(opt);
        });
        input.value = currentValue || (subField.options && subField.options[0] && subField.options[0].value) || "";
        input.addEventListener("change", (event) => {
          const next = clone(items);
          next[index][subField.key] = event.target.value;
          updateBlockProp(block.id, field.key, next);
          schedulePreview();
        });
      } else {
        input = document.createElement("input");
        input.type = subField.type === "url" ? "url" : "text";
        input.value = currentValue || "";
        input.addEventListener("input", (event) => {
          const next = clone(items);
          next[index][subField.key] = event.target.value;
          updateBlockProp(block.id, field.key, next);
          schedulePreview();
        });
      }
      subContainer.appendChild(input);
      if (subField.assetKinds && subField.assetKinds.length) {
        const picker = document.createElement("button");
        picker.type = "button";
        picker.className = "btn btn-sm builder-field__asset-btn";
        picker.textContent = "Choose from library";
        picker.addEventListener("click", (event) => {
          event.preventDefault();
          openAssetBrowser({
            kinds: subField.assetKinds,
            onSelect: (asset) => {
              const url = asset.url || "";
              input.value = url;
              const next = clone(items);
              next[index][subField.key] = url;
              updateBlockProp(block.id, field.key, next);
              schedulePreview(true);
            },
          });
        });
        subContainer.appendChild(picker);
      }
      itemCard.appendChild(subContainer);
    });

    list.appendChild(itemCard);
  });

  const addButton = document.createElement("button");
  addButton.type = "button";
  addButton.className = "btn btn-sm";
  addButton.textContent = `Add ${field.itemLabel || "item"}`;
  addButton.addEventListener("click", () => {
    const next = clone(items);
    next.push(clone(field.itemDefaults || {}));
    updateBlockProp(block.id, field.key, next);
    renderSettings();
    schedulePreview(true);
  });

  container.appendChild(list);
  container.appendChild(addButton);
  return container;
}

function updateBlockProp(blockId, key, value) {
  const block = state.blocks.find((item) => item.id === blockId);
  if (!block) {
    return;
  }
  block.props = { ...block.props, [key]: value };
  state.dirty = true;
  persistBlocks();
  schedulePreview();
}

function addBlock(type) {
  const blueprint = getBlueprint(type);
  if (!blueprint) {
    return;
  }
  const block = {
    id: uuid(),
    type,
    props: clone(blueprint.defaults),
  };
  state.blocks.push(block);
  state.selectedId = block.id;
  state.dirty = true;
  renderBlockList();
  renderSettings();
  persistBlocks();
  schedulePreview(true);
}

function selectBlock(blockId) {
  state.selectedId = blockId;
  renderBlockList();
  renderSettings();
}

function moveBlock(blockId, direction) {
  const index = state.blocks.findIndex((block) => block.id === blockId);
  if (index === -1) {
    return;
  }
  const targetIndex = index + direction;
  if (targetIndex < 0 || targetIndex >= state.blocks.length) {
    return;
  }
  const updated = state.blocks.slice();
  const [removed] = updated.splice(index, 1);
  updated.splice(targetIndex, 0, removed);
  state.blocks = updated;
  state.dirty = true;
  renderBlockList();
  renderSettings();
  persistBlocks();
  schedulePreview();
}

function removeBlock(blockId) {
  const next = state.blocks.filter((block) => block.id !== blockId);
  state.blocks = next;
  if (state.selectedId === blockId) {
    state.selectedId = next.length ? next[0].id : null;
  }
  state.dirty = true;
  renderBlockList();
  renderSettings();
  persistBlocks();
  schedulePreview();
}

function handleFormSubmit(event) {
  persistBlocks();
  if (!config.urls || !config.urls.save) {
    return;
  }
  // Default form submission handles hero image uploads, keep behaviour.
}

function handlePreviewButton(event) {
  event.preventDefault();
  schedulePreview(true);
}

function bootstrap() {
  const root = document.getElementById("page-builder");
  if (!root) {
    return;
  }
  config = window.__PAGE_BUILDER__ || {};

  dom.form = document.getElementById("page-form");
  dom.blocksInput = document.getElementById("id_blocks");
  dom.library = document.getElementById("builder-library");
  dom.blockList = document.getElementById("builder-block-list");
  dom.settings = document.getElementById("builder-settings");
  dom.previewFrame = document.getElementById("builder-preview-frame");
  dom.saveButton = document.getElementById("builder-save-btn");
  dom.previewButton = document.getElementById("builder-preview-btn");

  assetState.modal = document.getElementById("asset-browser");
  if (assetState.modal) {
    assetState.overlay = assetState.modal.querySelector(".asset-browser__overlay");
    assetState.panel = assetState.modal.querySelector(".asset-browser__panel");
    assetState.list = document.getElementById("asset-browser-list");
    assetState.subtitle = document.getElementById("asset-browser-subtitle");
    assetState.closeButtons = Array.from(assetState.modal.querySelectorAll("[data-asset-close]"));
    assetState.closeButtons.forEach((btn) => btn.addEventListener("click", closeAssetBrowser));
    if (assetState.overlay) {
      assetState.overlay.addEventListener("click", closeAssetBrowser);
    }
  }

  const initialBlocks = normaliseBlocks((config.page && config.page.blocks) || []);
  if (!initialBlocks.length && config.page && config.page.body) {
    const fallback = getBlueprint("rich_text");
    if (fallback) {
      initialBlocks.push({
        id: uuid(),
        type: "rich_text",
        props: { ...clone(fallback.defaults), html: config.page.body },
      });
    }
  }

  state.blocks = initialBlocks;
  if (state.blocks.length) {
    state.selectedId = state.blocks[0].id;
  }
  persistBlocks();

  renderLibrary();
  renderBlockList();
  renderSettings();

  if (dom.form) {
    dom.form.addEventListener("submit", handleFormSubmit);
  }
  if (dom.previewButton) {
    dom.previewButton.addEventListener("click", handlePreviewButton);
  }
  if (dom.saveButton) {
    dom.saveButton.addEventListener("click", persistBlocks);
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && isAssetBrowserOpen()) {
      event.preventDefault();
      closeAssetBrowser();
    }
  });

  setPreviewHTML(config.preview_html || "");

  if (state.blocks.length) {
    schedulePreview(true);
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", bootstrap);
} else {
  bootstrap();
}
