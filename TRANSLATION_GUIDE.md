# Translation Guide for Bar OS

This guide explains how to translate your website content and the CMS interface itself.

## Quick Start

### 1. Change CMS Language

At the top-right of every CMS page, you'll see a language dropdown:
- **English**
- **Español** (Spanish)
- **Deutsch** (German)
- **Français** (French)

Select your preferred language and the CMS interface will translate immediately.

### 2. Translate Your Website Content (Pages, Menus, Events)

You have **TWO options** for translating your content:

---

## Option A: Django Admin (Simple, Per-Field Translation)

**Best for:** Quick edits, translating individual items

1. Go to Django Admin: `http://localhost:8000/admin/`
2. Navigate to the model you want to translate (Pages, Menu Items, Events, etc.)
3. Click on the item you want to translate
4. You'll see separate fields for each language:
   - `Title (English)`, `Title (Spanish)`, `Title (German)`, `Title (French)`
   - `Slug (English)`, `Slug (Spanish)`, etc.
   - `Body (English)`, `Body (Spanish)`, etc.

5. Fill in the translation fields for each language
6. **Save**

### Example: Translating a Page

```
Title (English): About Us
Title (Spanish): Acerca de Nosotros
Title (German): Über Uns
Title (French): À Propos de Nous

Slug (English): about-us
Slug (Spanish): acerca-de-nosotros
Slug (German): uber-uns
Slug (French): a-propos-de-nous
```

**Important Notes:**
- **English slugs are required** - always fill these in first
- **Non-English slugs are optional** - if you don't provide them, English content will be shown
- **Slugs must be unique per language** - each language needs its own unique slug

---

## Option B: Rosetta (Batch Translation for Interface)

**Best for:** Translating the CMS interface labels, buttons, and common phrases

1. Go to Rosetta: `http://localhost:8000/rosetta/`
2. Select the language you want to translate
3. Select "Bar OS" from the list
4. You'll see a list of English phrases and their translations
5. Edit the translations and click **Save**
6. The changes apply immediately

### Common Phrases to Translate:

- Navigation: "Home", "Menu", "Events", "Contact", "Login"
- Actions: "Save", "Cancel", "Delete", "Edit", "Add", "Search"
- Interface: "Dashboard", "Welcome", "Logout"

---

## Language Behavior

### For Visitors (Public Site)

- URLs are language-prefixed: `/en/about`, `/es/acerca-de`, `/de/uber-uns`, `/fr/a-propos`
- Language is selected from URL prefix
- Language switcher in top navigation allows visitors to change languages
- If translation is missing, English content is shown as fallback

### For CMS Users (Staff/Admin)

- CMS URLs stay in English: `/cms/dashboard`, `/admin/`
- Interface language selected from dropdown (top-right)
- Each field shows language-specific versions when editing content
- Can work in any language regardless of content being edited

---

## Translation Workflow for Your Bar

### Step 1: Set Up Your English Content (Required)

Create all your pages, menus, events in English first:
- Fill in all required fields (title, slug, content)
- English slug MUST be provided
- Save and publish

### Step 2: Add Translations (Optional)

Choose your approach:

**For Content (Pages, Events, Menus):**
→ Use Django Admin to edit each item
→ Fill in language-specific fields
→ Provide unique slugs for each language

**For Interface (Buttons, Labels):**
→ Use Rosetta to translate common phrases
→ Changes apply to all pages using those phrases

### Step 3: Test in Each Language

1. Visit your public site: `http://localhost:8000/en/`
2. Use the language switcher to change languages
3. Verify translations appear correctly
4. Check that language-specific URLs work

---

## FAQ

### Q: Do I need to translate everything?

**No!** English is the fallback language:
- If a Spanish translation is missing, English content is shown
- You can gradually add translations as needed
- Only English slugs are required; others are optional

### Q: How do I translate the seeded content?

The seeded content (sample pages, menus, events) is currently only in English. To translate it:

1. Go to Django Admin
2. Find each item (Pages → Home, Menu → Categories, etc.)
3. Click to edit
4. Fill in the language-specific fields
5. Save

### Q: Can different language versions have different slugs?

**Yes!** In fact, they should:
- English: `/en/about-us`
- Spanish: `/es/acerca-de-nosotros`
- German: `/de/uber-uns`
- French: `/fr/a-propos-de-nous`

This is better for SEO and user experience.

### Q: What if I only want English and one other language?

That's fine! Just leave the other language fields empty. For example:
- Fill in English (required)
- Fill in Spanish (optional)
- Leave German and French empty

Only English and Spanish will be available, and the language switcher will only show those two options.

### Q: How do I add a new language?

Edit `app/core/settings.py` and add to `LANGUAGES` and `MODELTRANSLATION_LANGUAGES`:

```python
LANGUAGES = [
    ("en", "English"),
    ("es", "Español"),
    ("de", "Deutsch"),
    ("fr", "Français"),
    ("it", "Italiano"),  # Add Italian
]

MODELTRANSLATION_LANGUAGES = ("en", "es", "de", "fr", "it")
```

Then run migrations to create the new language fields.

### Q: Can I change which language is default?

Yes! Edit `app/core/settings.py`:

```python
LANGUAGE_CODE = "es"  # Change from "en" to "es"
MODELTRANSLATION_DEFAULT_LANGUAGE = "es"
```

---

## Technical Details

### Database Structure

For each translated field, separate database columns are created:
- `title` → proxy field (returns current language)
- `title_en` → English title (required, has data)
- `title_es` → Spanish title (optional, nullable)
- `title_de` → German title (optional, nullable)
- `title_fr` → French title (optional, nullable)

### How Translations Are Stored

- **Model fields**: Stored in database columns (e.g., `title_en`, `title_es`)
- **Interface strings**: Stored in `.po` files in the `locale/` directory
- **Compiled translations**: Stored as `.mo` files (generated automatically)

### Rosetta vs Django Admin

| Feature | Rosetta | Django Admin |
|---------|---------|--------------|
| Translate content | No | Yes |
| Translate interface | Yes | No |
| Batch editing | Yes | No |
| Per-item editing | No | Yes |
| Real-time preview | Yes | No |

---

## Tips for Bar Owners

### 1. Start Small
Don't try to translate everything at once:
- Start with your homepage
- Add menu items in your local language
- Translate key pages (About, Contact, Events)

### 2. Use Your Native Language
If Spanish/German/French is your first language:
- Write content in your language first
- Add English translations later if needed
- Your customers will appreciate authentic translations

### 3. Get Help from Staff
- Staff members can help translate
- Each person can work in their preferred CMS language
- Use Rosetta for common phrases everyone uses

### 4. SEO Benefits
Language-specific URLs help with local search:
- `/es/menu` ranks better for Spanish searches
- `/de/kontakt` ranks better for German searches

---

## Getting Help

- **CMS Issues**: Check Django admin logs
- **Translation Issues**: Check Rosetta for missing translations
- **Slug Conflicts**: Make sure each language has unique slugs

Remember: **You can always use the CMS in your native language while managing content in any language!**
