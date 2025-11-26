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
    type: "navigation",
    icon: "🧭",
    label: "Navigation bar",
    description: "Configure the main site navigation (brand link + menu).",
    defaults: {
      show_logo: true,
      logo_text: "",
      show_language_switcher: true,
      layout: "center",
      links: [],
    },
    fields: [
      { key: "show_logo", type: "toggle", label: "Show logo image if available" },
      { key: "logo_text", type: "text", label: "Brand text override", help: "Defaults to site name." },
      {
        key: "layout",
        type: "select",
        label: "Alignment",
        options: [
          { value: "center", label: "Centered" },
          { value: "left", label: "Left" },
        ],
      },
      { key: "show_language_switcher", type: "toggle", label: "Show language switcher" },
      {
        key: "links",
        type: "navlinks",
        label: "Navigation links",
        help: "Pick and order the page links for this navigation bar.",
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
      contact_fields: null,
      social_fields: null,
      show_social: true,
    },
    fields: [
      {
        key: "contact_fields",
        type: "checkboxes",
        label: "Contact details to show",
        optionsSource: "contact",
        defaultAll: true,
        help: "Select which address, phone, email, or website info from Site Settings appears.",
      },
      {
        key: "social_fields",
        type: "checkboxes",
        label: "Social profiles",
        optionsSource: "social",
        defaultAll: true,
        help: "Toggle which social links to render. Leave everything unchecked to hide socials.",
      },
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
    icon: "🦶",
    label: "Footer",
    description: "Footer bar with brand, navigation, legal, and social links.",
    defaults: {
      brand_name: "",
      brand_tagline: "",
      brand_logo: "",
      address_html: "",
      links: [],
      legal: [],
      social_links: [],
    },
    fields: [
      { key: "brand_name", type: "text", label: "Brand name" },
      { key: "brand_tagline", type: "text", label: "Tagline", help: "Optional short line that appears under the brand." },
      {
        key: "brand_logo",
        type: "url",
        label: "Logo URL",
        help: "Paste an image URL from the media library.",
        assetKinds: ["image"],
      },
      { key: "address_html", type: "textarea", label: "Address / notes", rows: 3 },
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
      {
        key: "social_links",
        type: "list",
        label: "Social links",
        itemLabel: "Profile",
        itemDefaults: { label: "Instagram", href: "#", new_tab: true },
        itemFields: [
          { key: "label", type: "text", label: "Platform" },
          { key: "href", type: "url", label: "URL" },
          { key: "new_tab", type: "toggle", label: "Open in new tab" },
        ],
      },
    ],
  },
];

const CONTACT_FIELD_BLUEPRINT = [
  { value: "address", label: "Address" },
  { value: "phone", label: "Phone" },
  { value: "email", label: "Email" },
  { value: "website", label: "Website" },
];

const SOCIAL_FIELD_BLUEPRINT = [
  { value: "facebook", label: "Facebook" },
  { value: "instagram", label: "Instagram" },
  { value: "twitter", label: "Twitter" },
  { value: "tiktok", label: "TikTok" },
  { value: "youtube", label: "YouTube" },
  { value: "spotify", label: "Spotify" },
  { value: "soundcloud", label: "SoundCloud" },
  { value: "bandcamp", label: "Bandcamp" },
  { value: "linkedin", label: "LinkedIn" },
  { value: "mastodon", label: "Mastodon" },
];

const state = {
  blocks: [],
  selectedId: null,
  dirty: false,
  siteContext: null,
  siteLoading: false,
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

function formatAddressPreview(address = {}) {
  if (!address) return "";
  const line1 = [address.street, address.number].filter(Boolean).join(" ").trim();
  const line2 = [address.postal_code, address.city].filter(Boolean).join(" ").trim();
  const parts = [line1, line2, address.country].filter(Boolean);
  return parts.join(", ");
}

function buildContactOptions() {
  const site = state.siteContext;
  if (!site) {
    return CONTACT_FIELD_BLUEPRINT;
  }
  const contact = site.contact || {};
  const options = [];
  const addressPreview = formatAddressPreview(site.address || {});
  options.push({
    value: "address",
    label: addressPreview ? `Address - ${addressPreview}` : "Address (not set)",
    disabled: !addressPreview,
  });
  options.push({
    value: "phone",
    label: contact.phone ? `Phone - ${contact.phone}` : "Phone (not set)",
    disabled: !contact.phone,
  });
  options.push({
    value: "email",
    label: contact.email ? `Email - ${contact.email}` : "Email (not set)",
    disabled: !contact.email,
  });
  options.push({
    value: "website",
    label: contact.website ? `Website - ${contact.website}` : "Website (not set)",
    disabled: !contact.website,
  });
  return options;
}

function buildSocialOptions() {
  const site = state.siteContext;
  if (!site) {
    return SOCIAL_FIELD_BLUEPRINT;
  }
  const social = site.social || {};
  return SOCIAL_FIELD_BLUEPRINT.map((option) => {
    const value = social[option.value];
    return {
      value: option.value,
      label: value ? `${option.label} - ${value}` : `${option.label} (not set)`,
      disabled: !value,
    };
  });
}

function getCheckboxOptions(field) {
  if (Array.isArray(field.options)) {
    return field.options;
  }
  if (field.optionsSource === "contact") {
    return buildContactOptions();
  }
  if (field.optionsSource === "social") {
    return buildSocialOptions();
  }
  if (typeof field.getOptions === "function") {
    return field.getOptions(state, field);
  }
  return [];
}

const dom = {};
let config = {};
let previewTimer = null;
let previewInflight = null;
let siteContextRequest = null;

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
      case "checkboxes":
        if (value === null || value === undefined) {
          props[key] = null;
        } else if (Array.isArray(value)) {
          props[key] = value.filter((item) => typeof item === "string");
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
  if (!dom.previewFrames || !dom.previewFrames.length) {
    return;
  }
  const content =
    html && html.trim()
      ? html
      : "<!doctype html><html><head><meta charset='utf-8'><style>body{margin:0;padding:2rem;font-family:system-ui;background:#0b1118;color:#f0f4f8;} .muted{color:rgba(255,255,255,0.6);}</style></head><body><p class='muted'>Preview will appear here once you add blocks.</p></body></html>";
  dom.previewFrames.forEach((frame) => {
    if (frame.srcdoc !== content) {
      frame.srcdoc = content;
    }
  });
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
  let showNav = showNavField ? !!showNavField.checked : false;
  const navBlock = state.blocks.find((block) => block.type === "navigation");
  if (navBlock) {
    showNav = true;
    const blockLinks = Array.isArray(navBlock.props.links) ? navBlock.props.links : [];
    navItems = blockLinks.length ? blockLinks : navItems;
  }
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
    case "navlinks":
      return renderNavLinksField(block, field, container);
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
    case "checkboxes":
      return renderCheckboxField(block, field, container);
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

function renderCheckboxField(block, field, container) {
  const options = getCheckboxOptions(field);
  const wrapper = document.createElement("div");
  wrapper.className = "builder-checkboxes";

  if (!options.length) {
    const message = document.createElement("p");
    message.className = "muted";
    message.textContent = state.siteLoading
      ? "Loading site details..."
      : "No options available. Update Site Settings first.";
    wrapper.appendChild(message);
    container.appendChild(wrapper);
    return container;
  }

  const enabledValues = options.filter((opt) => !opt.disabled).map((opt) => opt.value);
  const stored = block.props[field.key];
  const defaultSelection = field.defaultAll === false ? [] : enabledValues;
  const initialSelection =
    Array.isArray(stored) && stored.length ? stored.filter((val) => enabledValues.includes(val)) : defaultSelection;
  const selected = new Set(initialSelection);
  const checkboxes = [];

  options.forEach((option) => {
    const item = document.createElement("label");
    item.className = "builder-checkboxes__item";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = option.value;
    checkbox.disabled = Boolean(option.disabled);
    checkbox.checked = selected.has(option.value) && !checkbox.disabled;
    checkbox.addEventListener("change", () => {
      if (checkbox.disabled) {
        return;
      }
      if (checkbox.checked) {
        selected.add(option.value);
      } else {
        selected.delete(option.value);
      }
      updateBlockProp(block.id, field.key, Array.from(selected));
    });

    const text = document.createElement("span");
    text.textContent = option.label || option.value;

    item.appendChild(checkbox);
    item.appendChild(text);
    wrapper.appendChild(item);
    checkboxes.push({ checkbox, option });
  });

  container.appendChild(wrapper);

  const actions = document.createElement("div");
  actions.className = "builder-checkboxes__actions";

  const selectAll = document.createElement("button");
  selectAll.type = "button";
  selectAll.className = "btn btn-xs";
  selectAll.textContent = "Select all";
  selectAll.addEventListener("click", () => {
    selected.clear();
    checkboxes.forEach(({ checkbox, option }) => {
      if (option.disabled) {
        checkbox.checked = false;
        return;
      }
      checkbox.checked = true;
      selected.add(option.value);
    });
    updateBlockProp(block.id, field.key, Array.from(selected));
  });
  actions.appendChild(selectAll);

  const clearAll = document.createElement("button");
  clearAll.type = "button";
  clearAll.className = "btn btn-xs btn-outline-secondary";
  clearAll.textContent = "Clear";
  clearAll.addEventListener("click", () => {
    selected.clear();
    checkboxes.forEach(({ checkbox }) => {
      checkbox.checked = false;
    });
    updateBlockProp(block.id, field.key, []);
  });
  actions.appendChild(clearAll);

  const refreshBtn = document.createElement("button");
  refreshBtn.type = "button";
  refreshBtn.className = "btn btn-xs";
  refreshBtn.textContent = "Refresh site info";
  refreshBtn.addEventListener("click", () => {
    refreshBtn.disabled = true;
    refreshBtn.textContent = "Refreshing…";
    fetchSiteContext(true).finally(() => {
      refreshBtn.disabled = false;
      refreshBtn.textContent = "Refresh site info";
    });
  });
  actions.appendChild(refreshBtn);

  container.appendChild(actions);
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

function renderNavLinksField(block, field, container) {
  const items = config.nav_items || [];
  if (!items.length) {
    const message = document.createElement("p");
    message.className = "muted";
    message.textContent = "Add more pages to configure navigation links.";
    container.appendChild(message);
    return container;
  }

  const legacyField = document.getElementById("id_custom_nav_items");
  const legacyToggle = document.getElementById("id_show_navigation_bar");
  if (legacyToggle) legacyToggle.value = "True";

  const stored = Array.isArray(block.props[field.key]) ? block.props[field.key].slice() : null;
  let selectedOrder = Array.isArray(stored) && stored.length
    ? stored.slice()
    : items.filter((item) => item.checked).map((item) => item.slug);
  selectedOrder = Array.from(new Set(selectedOrder));
  const allOrder = selectedOrder.concat(
    items.map((item) => item.slug).filter((slug) => !selectedOrder.includes(slug))
  );

  const list = document.createElement("div");
  list.className = "builder-navlinks__list";
  container.appendChild(list);

  function updateSelection() {
    const checked = [];
    Array.from(list.children).forEach((row) => {
      const slug = row.dataset.slug;
      const checkbox = row.querySelector("input[type='checkbox']");
      if (checkbox && checkbox.checked) {
        checked.push(slug);
      }
    });
    if (legacyField) legacyField.value = JSON.stringify(checked);
    updateBlockProp(block.id, field.key, checked);
  }

  function moveRow(row, direction) {
    if (!row) return;
    if (direction === -1 && row.previousElementSibling) {
      list.insertBefore(row, row.previousElementSibling);
    } else if (direction === 1 && row.nextElementSibling) {
      list.insertBefore(row.nextElementSibling, row);
    }
    updateSelection();
  }

  allOrder.forEach((slug) => {
    const meta = items.find((item) => item.slug === slug) || { slug, title: slug };
    const row = document.createElement("div");
    row.className = "builder-navlinks__item";
    row.dataset.slug = slug;

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked =
      (stored && stored.length ? stored.includes(slug) : undefined) ?? Boolean(meta.checked);
    checkbox.addEventListener("change", updateSelection);

    const name = document.createElement("span");
    name.textContent = meta.title || slug;

    const actions = document.createElement("div");
    actions.className = "builder-navlinks__actions";
    const upBtn = document.createElement("button");
    upBtn.type = "button";
    upBtn.className = "btn btn-xs";
    upBtn.textContent = "▲";
    upBtn.addEventListener("click", () => moveRow(row, -1));
    const downBtn = document.createElement("button");
    downBtn.type = "button";
    downBtn.className = "btn btn-xs";
    downBtn.textContent = "▼";
    downBtn.addEventListener("click", () => moveRow(row, 1));
    actions.appendChild(upBtn);
    actions.appendChild(downBtn);

    row.appendChild(checkbox);
    row.appendChild(name);
    row.appendChild(actions);
    list.appendChild(row);
  });

  const bulk = document.createElement("div");
  bulk.className = "builder-navlinks__bulk";
  const selectAll = document.createElement("button");
  selectAll.type = "button";
  selectAll.className = "btn btn-xs";
  selectAll.textContent = "Select all";
  selectAll.addEventListener("click", () => {
    list.querySelectorAll("input[type='checkbox']").forEach((box) => {
      box.checked = true;
    });
    updateSelection();
  });
  const clearAll = document.createElement("button");
  clearAll.type = "button";
  clearAll.className = "btn btn-xs btn-outline-secondary";
  clearAll.textContent = "Clear";
  clearAll.addEventListener("click", () => {
    list.querySelectorAll("input[type='checkbox']").forEach((box) => {
      box.checked = false;
    });
    updateSelection();
  });
  bulk.appendChild(selectAll);
  bulk.appendChild(clearAll);
  container.appendChild(bulk);

  updateSelection();
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

function fetchSiteContext(force = false) {
  if (!config.urls || !config.urls.site) {
    return Promise.resolve(null);
  }
  if (!force && state.siteContext && !state.siteLoading) {
    return Promise.resolve(state.siteContext);
  }
  if (state.siteLoading && siteContextRequest) {
    return siteContextRequest;
  }
  state.siteLoading = true;
  siteContextRequest = fetch(config.urls.site, { headers: { Accept: "application/json" } })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to load site context");
      }
      return response.json();
    })
    .then((data) => {
      state.siteContext = data;
      return data;
    })
    .catch(() => {
      state.siteContext = null;
      return null;
    })
    .finally(() => {
      state.siteLoading = false;
      renderSettings();
    });
  return siteContextRequest;
}

function bootstrap() {
  const root = document.getElementById("page-builder");
  if (!root) {
    return;
  }
  config = window.__PAGE_BUILDER__ || {};
  config.nav_items = config.nav_items || [];
  state.siteContext = config.site_context || state.siteContext;

  dom.form = document.getElementById("page-form");
  dom.blocksInput = document.getElementById("id_blocks");
  dom.library = document.getElementById("builder-library");
  dom.blockList = document.getElementById("builder-block-list");
  dom.settings = document.getElementById("builder-settings");
  dom.previewFrames = Array.from(document.querySelectorAll("[data-preview-frame]"));
  dom.previewCanvas = document.getElementById("builder-preview-canvas");
  dom.previewToggle = document.getElementById("builder-preview-toggle");
  dom.previewModeButtons = dom.previewToggle
    ? Array.from(dom.previewToggle.querySelectorAll(".preview-toggle__btn"))
    : [];
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

  function setPreviewMode(mode) {
    if (!dom.previewCanvas) {
      return;
    }
    dom.previewCanvas.setAttribute("data-preview-mode", mode);
    dom.previewModeButtons.forEach((btn) => {
      btn.classList.toggle("is-active", btn.dataset.mode === mode);
    });
  }

  if (dom.previewModeButtons.length) {
    dom.previewModeButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        setPreviewMode(btn.dataset.mode || "desktop");
      });
    });
    setPreviewMode("desktop");
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
  fetchSiteContext(!state.siteContext);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", bootstrap);
} else {
  bootstrap();
}
