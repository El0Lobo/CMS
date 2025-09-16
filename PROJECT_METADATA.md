# Project URL & Model Reference

_This file was generated automatically._

## URL Patterns

Total: **212**

| Pattern | Name | Callback |
|---|---|---|
|  | `index` | `django.contrib.admin.sites.AdminSite.index` |
| login/ | `login` | `django.contrib.admin.sites.AdminSite.login` |
| logout/ | `logout` | `django.contrib.admin.sites.AdminSite.logout` |
| password_change/ | `password_change` | `django.contrib.admin.sites.AdminSite.password_change` |
| password_change/done/ | `password_change_done` | `django.contrib.admin.sites.AdminSite.password_change_done` |
| autocomplete/ | `autocomplete` | `django.contrib.admin.sites.AdminSite.autocomplete_view` |
| jsi18n/ | `jsi18n` | `django.contrib.admin.sites.AdminSite.i18n_javascript` |
| r/<path:content_type_id>/<path:object_id>/ | `view_on_site` | `django.contrib.contenttypes.views.shortcut` |
|  | `auth_group_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `auth_group_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `auth_group_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `auth_group_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `auth_group_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
| <path:object_id>/ |  | `django.views.generic.base.RedirectView` |
| <id>/password/ | `auth_user_password_change` | `django.contrib.auth.admin.UserAdmin.user_change_password` |
|  | `auth_user_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `auth_user_add` | `django.contrib.auth.admin.UserAdmin.add_view` |
| <path:object_id>/history/ | `auth_user_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `auth_user_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `auth_user_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `axes_accessattempt_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `axes_accessattempt_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `axes_accessattempt_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `axes_accessattempt_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `axes_accessattempt_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `axes_accesslog_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `axes_accesslog_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `axes_accesslog_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `axes_accesslog_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `axes_accesslog_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `axes_accessfailurelog_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `axes_accessfailurelog_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `axes_accessfailurelog_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `axes_accessfailurelog_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `axes_accessfailurelog_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
| <int:pk>/config/ | `otp_totp_totpdevice_config` | `django_otp.plugins.otp_totp.admin.TOTPDeviceAdmin.config_view` |
| <int:pk>/qrcode/ | `otp_totp_totpdevice_qrcode` | `django_otp.plugins.otp_totp.admin.TOTPDeviceAdmin.qrcode_view` |
|  | `otp_totp_totpdevice_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `otp_totp_totpdevice_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `otp_totp_totpdevice_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `otp_totp_totpdevice_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `otp_totp_totpdevice_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `setup_sitesettings_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `setup_sitesettings_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `setup_sitesettings_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `setup_sitesettings_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `setup_sitesettings_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `setup_visibilityrule_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `setup_visibilityrule_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `setup_visibilityrule_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `setup_visibilityrule_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `setup_visibilityrule_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `users_userprofile_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `users_userprofile_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `users_userprofile_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `users_userprofile_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `users_userprofile_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `users_badgedefinition_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `users_badgedefinition_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `users_badgedefinition_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `users_badgedefinition_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `users_badgedefinition_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `users_fieldpolicy_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `users_fieldpolicy_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `users_fieldpolicy_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `users_fieldpolicy_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `users_fieldpolicy_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `menu_unit_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `menu_unit_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `menu_unit_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `menu_unit_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `menu_unit_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `menu_category_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `menu_category_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `menu_category_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `menu_category_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `menu_category_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `menu_item_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `menu_item_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `menu_item_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `menu_item_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `menu_item_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `bands_band_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `bands_band_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `bands_band_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `bands_band_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `bands_band_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `assets_collection_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `assets_collection_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `assets_collection_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `assets_collection_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `assets_collection_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `assets_tag_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `assets_tag_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `assets_tag_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `assets_tag_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `assets_tag_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
|  | `assets_asset_changelist` | `django.contrib.admin.options.ModelAdmin.changelist_view` |
| add/ | `assets_asset_add` | `django.contrib.admin.options.ModelAdmin.add_view` |
| <path:object_id>/history/ | `assets_asset_history` | `django.contrib.admin.options.ModelAdmin.history_view` |
| <path:object_id>/delete/ | `assets_asset_delete` | `django.contrib.admin.options.ModelAdmin.delete_view` |
| <path:object_id>/change/ | `assets_asset_change` | `django.contrib.admin.options.ModelAdmin.change_view` |
| ^(?P<app_label>auth\|axes\|otp_totp\|setup\|users\|menu\|bands\|assets)/$ | `app_list` | `django.contrib.admin.sites.AdminSite.app_index` |
| (?P<url>.*)$ |  | `django.contrib.admin.sites.AdminSite.catch_all_view` |
| health/ | `health` | `app.core.views.health` |
| login/ | `login` | `django.contrib.auth.views.LoginView` |
| logout/ | `logout` | `django.contrib.auth.views.LogoutView` |
| password_change/ | `password_change` | `django.contrib.auth.views.PasswordChangeView` |
| password_change/done/ | `password_change_done` | `django.contrib.auth.views.PasswordChangeDoneView` |
| password_reset/ | `password_reset` | `django.contrib.auth.views.PasswordResetView` |
| password_reset/done/ | `password_reset_done` | `django.contrib.auth.views.PasswordResetDoneView` |
| reset/<uidb64>/<token>/ | `password_reset_confirm` | `django.contrib.auth.views.PasswordResetConfirmView` |
| reset/done/ | `password_reset_complete` | `django.contrib.auth.views.PasswordResetCompleteView` |
|  | `home` | `app.pages.views_public.home` |
| events/ | `events` | `app.pages.views_public.events` |
| blog/ | `blog` | `app.pages.views_public.blog` |
| about/ | `about` | `app.pages.views_public.about` |
| contact/ | `contact` | `app.pages.views_public.contact` |
| menu/ | `menu` | `app.pages.views_public.menu` |
| gallery/ | `gallery` | `app.pages.views_public.gallery` |
| shows/ | `shows` | `app.pages.views_public.shows` |
| music/ | `music` | `app.pages.views_public.music` |
| videos/ | `videos` | `app.pages.views_public.videos` |
| store/ | `store` | `app.pages.views_public.store` |
| posts/ | `posts` | `app.pages.views_public.posts` |
| archive/ | `archive` | `app.pages.views_public.archive` |
| ^(?P<slug>[-a-z0-9]+)/$ | `page-detail` | `app.pages.views_public.page_detail` |
| store/ | `shop_index` | `app.merch.views.store_index` |
| store/c/<slug:slug>/ | `shop_category` | `app.merch.views.store_category` |
| store/p/<slug:slug>/ | `shop_detail` | `app.merch.views.store_detail` |
|  | `menu` | `app.pages.views_public.menu` |
| dashboard/ | `dashboard` | `app.cms.views.dashboard` |
| account/ | `account` | `app.cms.views.account` |
|  | `pages_index` | `app.pages.views.index` |
| create/ | `pages_create` | `app.pages.views.create` |
| <slug:slug>/edit/ | `pages_edit` | `app.pages.views.edit` |
|  | `blog_index` | `app.blog.views.index` |
| create/ | `blog_create` | `app.blog.views.create` |
| <slug:slug>/edit/ | `blog_edit` | `app.blog.views.edit` |
|  | `events_index` | `app.events.views.index` |
| create/ | `events_create` | `app.events.views.create` |
| <slug:slug>/edit/ | `events_edit` | `app.events.views.edit` |
|  | `shifts_index` | `app.shifts.views.index` |
| create/ | `shifts_create` | `app.shifts.views.create` |
| <slug:slug>/edit/ | `shifts_edit` | `app.shifts.views.edit` |
|  | `door_index` | `app.door.views.index` |
| create/ | `door_create` | `app.door.views.create` |
| <slug:slug>/edit/ | `door_edit` | `app.door.views.edit` |
|  | `manage` | `app.merch.views.manage` |
| category/new/ | `category_new` | `app.merch.views.category_new` |
| category/<int:pk>/edit/ | `category_edit` | `app.merch.views.category_edit` |
| category/<int:pk>/delete/ | `category_delete` | `app.merch.views.category_delete` |
| product/new/ | `product_create` | `app.merch.views.product_create` |
| product/<slug:slug>/edit/ | `product_edit` | `app.merch.views.product_edit` |
| product/<slug:slug>/delete/ | `product_delete` | `app.merch.views.product_delete` |
|  | `inventory_index` | `app.inventory.views.index` |
| create/ | `inventory_create` | `app.inventory.views.create` |
| <slug:slug>/edit/ | `inventory_edit` | `app.inventory.views.edit` |
|  | `accounting_index` | `app.accounting.views.index` |
| create/ | `accounting_create` | `app.accounting.views.create` |
| <slug:slug>/edit/ | `accounting_edit` | `app.accounting.views.edit` |
|  | `social_index` | `app.social.views.index` |
| create/ | `social_create` | `app.social.views.create` |
| <slug:slug>/edit/ | `social_edit` | `app.social.views.edit` |
|  | `automation_index` | `app.automation.views.index` |
| create/ | `automation_create` | `app.automation.views.create` |
| <slug:slug>/edit/ | `automation_edit` | `app.automation.views.edit` |
|  | `maps_index` | `app.maps.views.index` |
| create/ | `maps_create` | `app.maps.views.create` |
| <slug:slug>/edit/ | `maps_edit` | `app.maps.views.edit` |
| setup/ | `setup` | `app.setup.views.setup_view` |
| visibility/ | `visibility_list` | `app.setup.views.visibility_list` |
| visibility/edit/ | `visibility_edit` | `app.setup.views.visibility_edit` |
| visibility/delete/<int:rule_id>/ | `visibility_delete` | `app.setup.views.visibility_delete` |
| visibility/picker/ | `visibility_picker` | `app.setup.views.visibility_picker` |
|  | `index` | `app.users.views.index` |
| create/ | `create` | `app.users.views.create_user` |
| profile/<int:user_id>/ | `profile` | `app.users.views.profile_detail` |
| profile/<int:user_id>/edit/ | `profile_edit` | `app.users.views.profile_edit` |
| cms/users/<int:user_id>/delete/ | `delete` | `app.users.views.user_delete` |
| badges/ | `badges_list` | `app.users.views.badges_list` |
| badges/new/ | `badges_create` | `app.users.views.badges_create` |
| badges/<int:pk>/edit/ | `badges_edit` | `app.users.views.badges_edit` |
| badges/<int:pk>/delete/ | `badges_delete` | `app.users.views.badges_delete` |
| groups/hierarchy/ | `group_hierarchy` | `app.users.views.group_hierarchy` |
| cms/bands/ | `index` | `app.bands.views.index` |
| cms/bands/new/ | `new` | `app.bands.views.edit` |
| cms/bands/<int:pk>/edit/ | `edit` | `app.bands.views.edit` |
| cms/bands/<int:pk>/delete/ | `delete` | `app.bands.views.delete` |
| bands/<slug:slug>/ | `public_detail` | `app.bands.views.public_detail` |
| bands/ | `public_list` | `app.bands.public_views.public_list` |
| bands/<slug:slug>/ | `public_detail` | `app.bands.public_views.public_detail` |
|  | `manage` | `app.menu.views.manage_menu` |
| items/ | `items_list` | `app.menu.views.items_list` |
| categories/new/<slug:root>/ | `category_create_root` | `app.menu.views.category_create` |
| categories/new/sub/<slug:parent_slug>/ | `category_create_sub` | `app.menu.views.category_create` |
| categories/<slug:slug>/edit/ | `category_edit` | `app.menu.views.category_edit` |
| categories/<slug:slug>/delete/ | `category_delete` | `app.menu.views.category_delete` |
| items/new/<slug:parent_slug>/ | `item_create_here` | `app.menu.views.item_create` |
| items/<slug:slug>/edit/ | `item_edit` | `app.menu.views.item_edit` |
| item/<slug:slug>/delete/ | `item_delete` | `app.menu.views.item_delete` |
|  | `index` | `app.assets.views.assets_index` |
| toggle/<int:pk>/ | `toggle_visibility` | `app.assets.views.asset_toggle_visibility` |
| rename/<int:pk>/ | `rename` | `app.assets.views.asset_rename` |
| collections/toggle/<int:pk>/ | `collection_toggle_visibility` | `app.assets.views.collection_toggle_visibility` |
| collections/rename/<int:pk>/ | `collection_rename` | `app.assets.views.collection_rename` |
| collections/update/<int:pk>/ | `collection_update` | `app.assets.views.collection_update` |
| collection/<int:pk>/delete/ | `collection_delete` | `app.assets.views.collection_delete` |
| asset/<int:pk>/data/ | `asset_data` | `app.assets.views.asset_data` |
| asset/<int:pk>/update/ | `asset_update` | `app.assets.views.asset_update` |
| asset/<int:pk>/delete/ | `asset_delete` | `app.assets.views.asset_delete` |
| ^media/(?P<path>.*)$ |  | `django.views.static.serve` |

## Models

### App: `admin`

### admin.LogEntry

- **DB table:** `django_admin_log`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.AutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| action_time | action_time | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |  |  |  |  | `django.utils.timezone.now()` |  |  |  |  |  |
| user | user_id | `django.db.models.fields.related.ForeignKey` | `integer` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `auth.User` |  |  | [None] |
| content_type | content_type_id | `django.db.models.fields.related.ForeignKey` | `integer` | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `contenttypes.ContentType` |  |  | ['id'] |
| object_id | object_id | `django.db.models.fields.TextField` | `text` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| object_repr | object_repr | `django.db.models.fields.CharField` | `varchar(200)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| action_flag | action_flag | `django.db.models.fields.PositiveSmallIntegerField` | `smallint unsigned` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `1`: Addition
    - `2`: Change
    - `3`: Deletion

</details>
| change_message | change_message | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |

### App: `assets`

### assets.Asset

- **DB table:** `assets_asset`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| collection | collection_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `assets.Collection` |  |  | ['id'] |
| title | title | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| slug | slug | `django.db.models.fields.SlugField` | `varchar(255)` | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| visibility | visibility | `django.db.models.fields.CharField` | `varchar(20)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 20 |  |  | `inherit` |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `inherit`: Inherit from collection
    - `public`: Public
    - `internal`: Internal

</details>
| description | description | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| file | file | `django.db.models.fields.files.FileField` | `varchar(100)` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 100 |  |  |  |  |  |  |  |  |
| url | url | `django.db.models.fields.URLField` | `varchar(200)` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| text_content | text_content | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| appears_on | appears_on | `django.db.models.fields.CharField` | `varchar(500)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 500 |  |  |  |  |  |  |  |  |
| mime_type | mime_type | `django.db.models.fields.CharField` | `varchar(100)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 100 |  |  |  |  |  |  |  |  |
| kind | kind | `django.db.models.fields.CharField` | `varchar(20)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 20 |  |  | `other` |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `image`: Image
    - `video`: Video
    - `audio`: Audio
    - `pdf`: PDF
    - `doc`: Document
    - `archive`: Archive
    - `link`: Link
    - `note`: Text/Note
    - `font`: Font
    - `other`: Other

</details>
| size_bytes | size_bytes | `django.db.models.fields.BigIntegerField` | `bigint` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| width | width | `django.db.models.fields.IntegerField` | `integer` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| height | height | `django.db.models.fields.IntegerField` | `integer` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| duration_seconds | duration_seconds | `django.db.models.fields.FloatField` | `real` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| pages | pages | `django.db.models.fields.IntegerField` | `integer` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| created_at | created_at | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| updated_at | updated_at | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| tags | tags | `django.db.models.fields.related.ManyToManyField` |  | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  | ManyToManyRel | `assets.Tag` | `assets.Asset_tags` |  |  |

### assets.Collection

- **DB table:** `assets_collection`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| children | children | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `assets.Collection` |  | `CASCADE` |  |
| assets | assets | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `assets.Asset` |  | `CASCADE` |  |
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| title | title | `django.db.models.fields.CharField` | `varchar(200)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| slug | slug | `django.db.models.fields.SlugField` | `varchar(200)` | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| parent | parent_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `assets.Collection` |  |  | [None] |
| visibility_mode | visibility_mode | `django.db.models.fields.CharField` | `varchar(20)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 20 |  |  | `public` |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `public`: Public
    - `internal`: Internal (staff)
    - `groups`: Groups

</details>
| description | description | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| sort_order | sort_order | `django.db.models.fields.IntegerField` | `integer` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `0` |  |  |  |  |  |
| created_at | created_at | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| updated_at | updated_at | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| allowed_groups | allowed_groups | `django.db.models.fields.related.ManyToManyField` |  | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  | ManyToManyRel | `auth.Group` | `assets.Collection_allowed_groups` |  |  |
| tags | tags | `django.db.models.fields.related.ManyToManyField` |  | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  | ManyToManyRel | `assets.Tag` | `assets.Collection_tags` |  |  |

### assets.Tag

- **DB table:** `assets_tag`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| collections | collections | `django.db.models.fields.reverse_related.ManyToManyRel` |  | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ManyToManyField | `assets.Collection` |  | `None` |  |
| assets | assets | `django.db.models.fields.reverse_related.ManyToManyRel` |  | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ManyToManyField | `assets.Asset` |  | `None` |  |
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| name | name | `django.db.models.fields.CharField` | `varchar(64)` | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |  | 64 |  |  |  |  |  |  |  |  |

### App: `auth`

### auth.Group

- **DB table:** `auth_group`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| user | user | `django.db.models.fields.reverse_related.ManyToManyRel` |  | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ManyToManyField | `auth.User` |  | `None` |  |
| groupobjectpermission | groupobjectpermission | `django.db.models.fields.reverse_related.ManyToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `guardian.GroupObjectPermission` |  | `CASCADE` |  |
| visibilityrule | visibilityrule | `django.db.models.fields.reverse_related.ManyToManyRel` |  | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ManyToManyField | `setup.VisibilityRule` |  | `None` |  |
| meta | meta | `django.db.models.fields.reverse_related.OneToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | OneToOneField | `users.GroupMeta` |  | `CASCADE` |  |
| primary_members | primary_members | `django.db.models.fields.reverse_related.ManyToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `users.UserProfile` |  | `SET_NULL` |  |
| asset_collections | asset_collections | `django.db.models.fields.reverse_related.ManyToManyRel` |  | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ManyToManyField | `assets.Collection` |  | `None` |  |
| id | id | `django.db.models.fields.AutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| name | name | `django.db.models.fields.CharField` | `varchar(150)` | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |  | 150 |  |  |  |  |  |  |  |  |
| permissions | permissions | `django.db.models.fields.related.ManyToManyField` |  | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  | ManyToManyRel | `auth.Permission` | `auth.Group_permissions` |  |  |

### auth.Permission

- **DB table:** `auth_permission`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| group | group | `django.db.models.fields.reverse_related.ManyToManyRel` |  | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ManyToManyField | `auth.Group` |  | `None` |  |
| user | user | `django.db.models.fields.reverse_related.ManyToManyRel` |  | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ManyToManyField | `auth.User` |  | `None` |  |
| userobjectpermission | userobjectpermission | `django.db.models.fields.reverse_related.ManyToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `guardian.UserObjectPermission` |  | `CASCADE` |  |
| groupobjectpermission | groupobjectpermission | `django.db.models.fields.reverse_related.ManyToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `guardian.GroupObjectPermission` |  | `CASCADE` |  |
| id | id | `django.db.models.fields.AutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| name | name | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| content_type | content_type_id | `django.db.models.fields.related.ForeignKey` | `integer` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `contenttypes.ContentType` |  |  | ['id'] |
| codename | codename | `django.db.models.fields.CharField` | `varchar(100)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 100 |  |  |  |  |  |  |  |  |

### auth.User

- **DB table:** `auth_user`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| logentry | logentry | `django.db.models.fields.reverse_related.ManyToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `admin.LogEntry` |  | `CASCADE` |  |
| userobjectpermission | userobjectpermission | `django.db.models.fields.reverse_related.ManyToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `guardian.UserObjectPermission` |  | `CASCADE` |  |
| totpdevice | totpdevice | `django.db.models.fields.reverse_related.ManyToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `otp_totp.TOTPDevice` |  | `CASCADE` |  |
| profile | profile | `django.db.models.fields.reverse_related.OneToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | OneToOneField | `users.UserProfile` |  | `CASCADE` |  |
| id | id | `django.db.models.fields.AutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| password | password | `django.db.models.fields.CharField` | `varchar(128)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 128 |  |  |  |  |  |  |  |  |
| last_login | last_login | `django.db.models.fields.DateTimeField` | `datetime` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| is_superuser | is_superuser | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| username | username | `django.db.models.fields.CharField` | `varchar(150)` | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |  | 150 |  |  |  |  |  |  |  |  |
| first_name | first_name | `django.db.models.fields.CharField` | `varchar(150)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 150 |  |  |  |  |  |  |  |  |
| last_name | last_name | `django.db.models.fields.CharField` | `varchar(150)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 150 |  |  |  |  |  |  |  |  |
| email | email | `django.db.models.fields.EmailField` | `varchar(254)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 254 |  |  |  |  |  |  |  |  |
| is_staff | is_staff | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| is_active | is_active | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `True` |  |  |  |  |  |
| date_joined | date_joined | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `django.utils.timezone.now()` |  |  |  |  |  |
| groups | groups | `django.db.models.fields.related.ManyToManyField` |  | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  | ManyToManyRel | `auth.Group` | `auth.User_groups` |  |  |
| user_permissions | user_permissions | `django.db.models.fields.related.ManyToManyField` |  | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  | ManyToManyRel | `auth.Permission` | `auth.User_user_permissions` |  |  |

### App: `axes`

### axes.AccessAttempt

- **DB table:** `axes_accessattempt`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.AutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| user_agent | user_agent | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| ip_address | ip_address | `django.db.models.fields.GenericIPAddressField` | `char(39)` | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |  | 39 |  |  |  |  |  |  |  |  |
| username | username | `django.db.models.fields.CharField` | `varchar(255)` | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| http_accept | http_accept | `django.db.models.fields.CharField` | `varchar(1025)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 1025 |  |  |  |  |  |  |  |  |
| path_info | path_info | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| attempt_time | attempt_time | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| get_data | get_data | `django.db.models.fields.TextField` | `text` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| post_data | post_data | `django.db.models.fields.TextField` | `text` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| failures_since_start | failures_since_start | `django.db.models.fields.PositiveIntegerField` | `integer unsigned` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |

### axes.AccessFailureLog

- **DB table:** `axes_accessfailurelog`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.AutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| user_agent | user_agent | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| ip_address | ip_address | `django.db.models.fields.GenericIPAddressField` | `char(39)` | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |  | 39 |  |  |  |  |  |  |  |  |
| username | username | `django.db.models.fields.CharField` | `varchar(255)` | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| http_accept | http_accept | `django.db.models.fields.CharField` | `varchar(1025)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 1025 |  |  |  |  |  |  |  |  |
| path_info | path_info | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| attempt_time | attempt_time | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| locked_out | locked_out | `django.db.models.fields.BooleanField` | `bool` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |

### axes.AccessLog

- **DB table:** `axes_accesslog`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.AutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| user_agent | user_agent | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| ip_address | ip_address | `django.db.models.fields.GenericIPAddressField` | `char(39)` | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |  | 39 |  |  |  |  |  |  |  |  |
| username | username | `django.db.models.fields.CharField` | `varchar(255)` | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| http_accept | http_accept | `django.db.models.fields.CharField` | `varchar(1025)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 1025 |  |  |  |  |  |  |  |  |
| path_info | path_info | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| attempt_time | attempt_time | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| logout_time | logout_time | `django.db.models.fields.DateTimeField` | `datetime` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |

### App: `bands`

### bands.Band

- **DB table:** `bands_band`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| performer_type | performer_type | `django.db.models.fields.CharField` | `varchar(10)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 10 |  |  | `band` |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `band`: Band
    - `dj`: DJ
    - `solo`: Solo artist

</details>
| name | name | `django.db.models.fields.CharField` | `varchar(200)` | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| slug | slug | `django.db.models.fields.SlugField` | `varchar(220)` | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |  | 220 |  |  |  |  |  |  |  |  |
| description | description | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| photo | photo | `django.db.models.fields.files.ImageField` | `varchar(100)` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 100 |  |  |  |  |  |  |  |  |
| contact_type | contact_type | `django.db.models.fields.CharField` | `varchar(10)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 10 |  |  |  |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `email`: Email
    - `phone`: Phone
    - `url`: Website/Link
    - `other`: Other

</details>
| contact_value | contact_value | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| contact_notes | contact_notes | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| compensation_type | compensation_type | `django.db.models.fields.CharField` | `varchar(10)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 10 |  |  | `unpaid` |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `fixed`: Fixed fee
    - `door`: Door deal
    - `unpaid`: Unpaid / promo

</details>
| fee_amount | fee_amount | `django.db.models.fields.DecimalField` | `decimal` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  | 9 | 2 |  |  |  |  |  |  |
| entry_price | entry_price | `django.db.models.fields.DecimalField` | `decimal` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  | 6 | 2 |  |  |  |  |  |  |
| payout_amount | payout_amount | `django.db.models.fields.DecimalField` | `decimal` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  | 9 | 2 |  |  |  |  |  |  |
| comment_internal | comment_internal | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| is_published | is_published | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `True` |  |  |  |  |  |
| published_at | published_at | `django.db.models.fields.DateTimeField` | `datetime` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| last_performed_on | last_performed_on | `django.db.models.fields.DateField` | `date` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| seo_title | seo_title | `django.db.models.fields.CharField` | `varchar(70)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 70 |  |  |  |  |  |  |  |  |
| seo_description | seo_description | `django.db.models.fields.CharField` | `varchar(160)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 160 |  |  |  |  |  |  |  |  |
| og_image_override | og_image_override | `django.db.models.fields.files.ImageField` | `varchar(100)` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 100 |  |  |  |  |  |  |  |  |
| website | website | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| instagram | instagram | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| facebook | facebook | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| youtube | youtube | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| bandcamp | bandcamp | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| soundcloud | soundcloud | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| created_at | created_at | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| updated_at | updated_at | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |

### App: `contenttypes`

### contenttypes.ContentType

- **DB table:** `django_content_type`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| logentry | logentry | `django.db.models.fields.reverse_related.ManyToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `admin.LogEntry` |  | `SET_NULL` |  |
| permission | permission | `django.db.models.fields.reverse_related.ManyToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `auth.Permission` |  | `CASCADE` |  |
| userobjectpermission | userobjectpermission | `django.db.models.fields.reverse_related.ManyToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `guardian.UserObjectPermission` |  | `CASCADE` |  |
| groupobjectpermission | groupobjectpermission | `django.db.models.fields.reverse_related.ManyToOneRel` | `integer` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `guardian.GroupObjectPermission` |  | `CASCADE` |  |
| id | id | `django.db.models.fields.AutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| app_label | app_label | `django.db.models.fields.CharField` | `varchar(100)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 100 |  |  |  |  |  |  |  |  |
| model | model | `django.db.models.fields.CharField` | `varchar(100)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 100 |  |  |  |  |  |  |  |  |

### App: `guardian`

### guardian.GroupObjectPermission

- **DB table:** `guardian_groupobjectpermission`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.AutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| permission | permission_id | `django.db.models.fields.related.ForeignKey` | `integer` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `auth.Permission` |  |  | ['id'] |
| content_type | content_type_id | `django.db.models.fields.related.ForeignKey` | `integer` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `contenttypes.ContentType` |  |  | ['id'] |
| object_pk | object_pk | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| group | group_id | `django.db.models.fields.related.ForeignKey` | `integer` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `auth.Group` |  |  | ['id'] |
| content_object | content_object | `django.contrib.contenttypes.fields.GenericForeignKey` |  | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |

### guardian.UserObjectPermission

- **DB table:** `guardian_userobjectpermission`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.AutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| permission | permission_id | `django.db.models.fields.related.ForeignKey` | `integer` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `auth.Permission` |  |  | ['id'] |
| content_type | content_type_id | `django.db.models.fields.related.ForeignKey` | `integer` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `contenttypes.ContentType` |  |  | ['id'] |
| object_pk | object_pk | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| user | user_id | `django.db.models.fields.related.ForeignKey` | `integer` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `auth.User` |  |  | [None] |
| content_object | content_object | `django.contrib.contenttypes.fields.GenericForeignKey` |  | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |

### App: `menu`

### menu.Category

- **DB table:** `menu_category`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| children | children | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `menu.Category` |  | `CASCADE` |  |
| items | items | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `menu.Item` |  | `PROTECT` |  |
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| name | name | `django.db.models.fields.CharField` | `varchar(120)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 120 |  |  |  |  |  |  |  |  |
| slug | slug | `django.db.models.fields.SlugField` | `varchar(140)` | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |  | 140 |  |  |  |  |  |  |  |  |
| parent | parent_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `menu.Category` |  |  | [None] |
| kind | kind | `django.db.models.fields.CharField` | `varchar(16)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 16 |  |  |  |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `drink`: Drink
    - `food`: Food

</details>
| unit_group | unit_group_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `menu.UnitGroup` |  |  | ['id'] |

### menu.Item

- **DB table:** `menu_item`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| variants | variants | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `menu.ItemVariant` |  | `CASCADE` |  |
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| name | name | `django.db.models.fields.CharField` | `varchar(160)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 160 |  |  |  |  |  |  |  |  |
| slug | slug | `django.db.models.fields.SlugField` | `varchar(180)` | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |  | 180 |  |  |  |  |  |  |  |  |
| category | category_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `menu.Category` |  |  | ['id'] |
| description | description | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| allergens_note | allergens_note | `django.db.models.fields.CharField` | `varchar(240)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 240 |  |  |  |  |  |  |  |  |
| vegan | vegan | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| vegetarian | vegetarian | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| gluten_free | gluten_free | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| sugar_free | sugar_free | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| lactose_free | lactose_free | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| nut_free | nut_free | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| halal | halal | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| kosher | kosher | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| visible_public | visible_public | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `True` |  |  |  |  |  |
| featured | featured | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| sold_out_until | sold_out_until | `django.db.models.fields.DateTimeField` | `datetime` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| new_until | new_until | `django.db.models.fields.DateTimeField` | `datetime` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| unit_group_override | unit_group_override_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `menu.UnitGroup` |  |  | ['id'] |

### menu.ItemVariant

- **DB table:** `menu_itemvariant`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| item | item_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `menu.Item` |  |  | ['id'] |
| label | label | `django.db.models.fields.CharField` | `varchar(64)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 64 |  |  |  |  |  |  |  |  |
| quantity | quantity | `django.db.models.fields.DecimalField` | `decimal` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  | 8 | 3 |  |  |  |  |  |  |
| unit | unit_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `menu.Unit` |  |  | ['id'] |
| price | price | `django.db.models.fields.DecimalField` | `decimal` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  | 8 | 2 |  |  |  |  |  |  |
| abv | abv | `django.db.models.fields.DecimalField` | `decimal` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  | 5 | 2 |  |  |  |  |  |  |

### menu.Unit

- **DB table:** `menu_unit`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| unitgroup | unitgroup | `django.db.models.fields.reverse_related.ManyToManyRel` |  | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ManyToManyField | `menu.UnitGroup` |  | `None` |  |
| itemvariant | itemvariant | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `menu.ItemVariant` |  | `PROTECT` |  |
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| code | code | `django.db.models.fields.CharField` | `varchar(16)` | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |  | 16 |  |  |  |  |  |  |  |  |
| display | display | `django.db.models.fields.CharField` | `varchar(32)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 32 |  |  |  |  |  |  |  |  |
| kind | kind | `django.db.models.fields.CharField` | `varchar(16)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 16 |  |  |  |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `volume`: Volume
    - `mass`: Mass
    - `count`: Count

</details>

### menu.UnitGroup

- **DB table:** `menu_unitgroup`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| category | category | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `menu.Category` |  | `SET_NULL` |  |
| item | item | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `menu.Item` |  | `SET_NULL` |  |
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| name | name | `django.db.models.fields.CharField` | `varchar(64)` | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |  | 64 |  |  |  |  |  |  |  |  |
| allowed_units | allowed_units | `django.db.models.fields.related.ManyToManyField` |  | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  | ManyToManyRel | `menu.Unit` | `menu.UnitGroup_allowed_units` |  |  |

### App: `merch`

### merch.Category

- **DB table:** `merch_category`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| children | children | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `merch.Category` |  | `CASCADE` |  |
| products | products | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `merch.Product` |  | `PROTECT` |  |
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| name | name | `django.db.models.fields.CharField` | `varchar(160)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 160 |  |  |  |  |  |  |  |  |
| slug | slug | `django.db.models.fields.SlugField` | `varchar(180)` | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |  | 180 |  |  |  |  |  |  |  |  |
| parent | parent_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `merch.Category` |  |  | [None] |
| order | order | `django.db.models.fields.PositiveIntegerField` | `integer unsigned` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `0` |  |  |  |  |  |

### merch.Product

- **DB table:** `merch_product`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| images | images | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `merch.ProductImage` |  | `CASCADE` |  |
| variants | variants | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `merch.ProductVariant` |  | `CASCADE` |  |
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| name | name | `django.db.models.fields.CharField` | `varchar(200)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| slug | slug | `django.db.models.fields.SlugField` | `varchar(220)` | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |  | 220 |  |  |  |  |  |  |  |  |
| category | category_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `merch.Category` |  |  | ['id'] |
| description | description | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| visible_public | visible_public | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `True` |  |  |  |  |  |
| featured | featured | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| base_price | base_price | `django.db.models.fields.DecimalField` | `decimal` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  | 10 | 2 |  |  |  |  |  |  |
| created_at | created_at | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| updated_at | updated_at | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |

### merch.ProductImage

- **DB table:** `merch_productimage`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| product | product_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `merch.Product` |  |  | ['id'] |
| image | image | `django.db.models.fields.files.ImageField` | `varchar(100)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 100 |  |  |  |  |  |  |  |  |
| alt_text | alt_text | `django.db.models.fields.CharField` | `varchar(160)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 160 |  |  |  |  |  |  |  |  |
| is_primary | is_primary | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| order | order | `django.db.models.fields.PositiveIntegerField` | `integer unsigned` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `0` |  |  |  |  |  |

### merch.ProductVariant

- **DB table:** `merch_productvariant`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| product | product_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `merch.Product` |  |  | ['id'] |
| size_label | size_label | `django.db.models.fields.CharField` | `varchar(32)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 32 |  |  |  |  |  |  |  |  |
| color | color | `django.db.models.fields.CharField` | `varchar(40)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 40 |  |  |  |  |  |  |  |  |
| length_cm | length_cm | `django.db.models.fields.DecimalField` | `decimal` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  | 6 | 2 |  |  |  |  |  |  |
| width_cm | width_cm | `django.db.models.fields.DecimalField` | `decimal` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  | 6 | 2 |  |  |  |  |  |  |
| sku | sku | `django.db.models.fields.CharField` | `varchar(64)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 64 |  |  |  |  |  |  |  |  |
| price | price | `django.db.models.fields.DecimalField` | `decimal` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  | 10 | 2 |  |  |  |  |  |  |
| stock | stock | `django.db.models.fields.IntegerField` | `integer` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `0` |  |  |  |  |  |

### App: `otp_totp`

### otp_totp.TOTPDevice

- **DB table:** `otp_totp_totpdevice`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.AutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| user | user_id | `django.db.models.fields.related.ForeignKey` | `integer` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `auth.User` |  |  | [None] |
| name | name | `django.db.models.fields.CharField` | `varchar(64)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 64 |  |  |  |  |  |  |  |  |
| confirmed | confirmed | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `True` |  |  |  |  |  |
| throttling_failure_timestamp | throttling_failure_timestamp | `django.db.models.fields.DateTimeField` | `datetime` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| throttling_failure_count | throttling_failure_count | `django.db.models.fields.PositiveIntegerField` | `integer unsigned` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `0` |  |  |  |  |  |
| key | key | `django.db.models.fields.CharField` | `varchar(80)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 80 |  |  | `django_otp.plugins.otp_totp.models.default_key()` |  |  |  |  |  |
| step | step | `django.db.models.fields.PositiveSmallIntegerField` | `smallint unsigned` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `30` |  |  |  |  |  |
| t0 | t0 | `django.db.models.fields.BigIntegerField` | `bigint` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `0` |  |  |  |  |  |
| digits | digits | `django.db.models.fields.PositiveSmallIntegerField` | `smallint unsigned` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `6` |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `6`: 6
    - `8`: 8

</details>
| tolerance | tolerance | `django.db.models.fields.PositiveSmallIntegerField` | `smallint unsigned` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `1` |  |  |  |  |  |
| drift | drift | `django.db.models.fields.SmallIntegerField` | `smallint` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `0` |  |  |  |  |  |
| last_t | last_t | `django.db.models.fields.BigIntegerField` | `bigint` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `-1` |  |  |  |  |  |

### App: `sessions`

### sessions.Session

- **DB table:** `django_session`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `session_key`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| session_key | session_key | `django.db.models.fields.CharField` | `varchar(40)` | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |  | 40 |  |  |  |  |  |  |  |  |
| session_data | session_data | `django.db.models.fields.TextField` | `text` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| expire_date | expire_date | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  |  |  |  |  |  |

### App: `setup`

### setup.MembershipTier

- **DB table:** `setup_membershiptier`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| settings | settings_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `setup.SiteSettings` |  |  | ['id'] |
| name | name | `django.db.models.fields.CharField` | `varchar(120)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 120 |  |  |  |  |  |  |  |  |
| months | months | `django.db.models.fields.PositiveIntegerField` | `integer unsigned` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `12` |  |  |  |  |  |
| price_minor | price_minor | `django.db.models.fields.PositiveIntegerField` | `integer unsigned` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `0` |  |  |  |  |  |
| active | active | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `True` |  |  |  |  |  |

### setup.OpeningHour

- **DB table:** `setup_openinghour`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| settings | settings_id | `django.db.models.fields.related.ForeignKey` | `bigint` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `setup.SiteSettings` |  |  | ['id'] |
| weekday | weekday | `django.db.models.fields.IntegerField` | `integer` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `0` |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `0`: Mon
    - `1`: Tue
    - `2`: Wed
    - `3`: Thu
    - `4`: Fri
    - `5`: Sat
    - `6`: Sun

</details>
| closed | closed | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| open_time | open_time | `django.db.models.fields.TimeField` | `time` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| close_time | close_time | `django.db.models.fields.TimeField` | `time` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |

### setup.SiteSettings

- **DB table:** `setup_sitesettings`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| tiers | tiers | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `setup.MembershipTier` |  | `CASCADE` |  |
| hours | hours | `django.db.models.fields.reverse_related.ManyToOneRel` | `bigint` | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ForeignKey | `setup.OpeningHour` |  | `CASCADE` |  |
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| mode | mode | `django.db.models.fields.CharField` | `varchar(10)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 10 |  |  | `VENUE` |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `VENUE`: Venue / Club
    - `BAND`: Band / Artist
    - `PERSON`: Person / Blog

</details>
| org_name | org_name | `django.db.models.fields.CharField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| logo | logo | `django.db.models.fields.files.ImageField` | `varchar(100)` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 100 |  |  |  |  |  |  |  |  |
| address_street | address_street | `django.db.models.fields.CharField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| address_number | address_number | `django.db.models.fields.CharField` | `varchar(20)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 20 |  |  |  |  |  |  |  |  |
| address_postal_code | address_postal_code | `django.db.models.fields.CharField` | `varchar(20)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 20 |  |  |  |  |  |  |  |  |
| address_city | address_city | `django.db.models.fields.CharField` | `varchar(120)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 120 |  |  |  |  |  |  |  |  |
| address_country | address_country | `django.db.models.fields.CharField` | `varchar(120)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 120 |  |  |  |  |  |  |  |  |
| address_autocomplete | address_autocomplete | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| contact_email | contact_email | `django.db.models.fields.EmailField` | `varchar(254)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 254 |  |  |  |  |  |  |  |  |
| contact_phone | contact_phone | `django.db.models.fields.CharField` | `varchar(64)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 64 |  |  |  |  |  |  |  |  |
| website_url | website_url | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| social_facebook | social_facebook | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| social_instagram | social_instagram | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| social_twitter | social_twitter | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| social_tiktok | social_tiktok | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| social_youtube | social_youtube | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| social_spotify | social_spotify | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| social_soundcloud | social_soundcloud | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| social_bandcamp | social_bandcamp | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| social_linkedin | social_linkedin | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| social_mastodon | social_mastodon | `django.db.models.fields.URLField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| same_as | same_as | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| geo_lat | geo_lat | `django.db.models.fields.DecimalField` | `decimal` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  | 9 | 6 |  |  |  |  |  |  |
| geo_lng | geo_lng | `django.db.models.fields.DecimalField` | `decimal` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  | 9 | 6 |  |  |  |  |  |  |
| price_range | price_range | `django.db.models.fields.CharField` | `varchar(20)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 20 |  |  |  |  |  |  |  |  |
| default_currency | default_currency | `django.db.models.fields.CharField` | `varchar(8)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 8 |  |  | `EUR` |  |  |  |  |  |
| membership_enabled | membership_enabled | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| membership_hint | membership_hint | `django.db.models.fields.CharField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| required_pages | required_pages | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| created_at | created_at | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| updated_at | updated_at | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| smoking_allowed | smoking_allowed | `django.db.models.fields.BooleanField` | `bool` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| pets_allowed_text | pets_allowed_text | `django.db.models.fields.CharField` | `varchar(120)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 120 |  |  |  |  |  |  |  |  |
| typical_age_range | typical_age_range | `django.db.models.fields.CharField` | `varchar(20)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 20 |  |  |  |  |  |  |  |  |
| acc_step_free | acc_step_free | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| acc_wheelchair | acc_wheelchair | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| acc_accessible_wc | acc_accessible_wc | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| acc_visual_aid | acc_visual_aid | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| acc_service_animals | acc_service_animals | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| accessibility_summary | accessibility_summary | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| lgbtq_friendly | lgbtq_friendly | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| minors_policy_note | minors_policy_note | `django.db.models.fields.CharField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| maximum_attendee_capacity | maximum_attendee_capacity | `django.db.models.fields.PositiveIntegerField` | `integer unsigned` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| awareness_team_available | awareness_team_available | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| awareness_contact | awareness_contact | `django.db.models.fields.CharField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| publish_opening_times | publish_opening_times | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |

### setup.VisibilityRule

- **DB table:** `setup_visibilityrule`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| key | key | `django.db.models.fields.CharField` | `varchar(120)` | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |  | 120 |  |  |  |  |  |  |  |  |
| label | label | `django.db.models.fields.CharField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| is_enabled | is_enabled | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `True` |  |  |  |  |  |
| notes | notes | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 255 |  |  |  |  |  |  |  |  |
| allowed_groups | allowed_groups | `django.db.models.fields.related.ManyToManyField` |  | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  | ManyToManyRel | `auth.Group` | `setup.VisibilityRule_allowed_groups` |  |  |

### App: `users`

### users.BadgeDefinition

- **DB table:** `users_badgedefinition`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| userprofile | userprofile | `django.db.models.fields.reverse_related.ManyToManyRel` |  | ✅ |  | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  | ManyToManyField | `users.UserProfile` |  | `None` |  |
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| name | name | `django.db.models.fields.CharField` | `varchar(100)` | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |  | 100 |  |  |  |  |  |  |  |  |
| emoji | emoji | `django.db.models.fields.CharField` | `varchar(8)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 8 |  |  |  |  |  |  |  |  |
| description | description | `django.db.models.fields.CharField` | `varchar(255)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 255 |  |  |  |  |  |  |  |  |

### users.FieldPolicy

- **DB table:** `users_fieldpolicy`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| field_name | field_name | `django.db.models.fields.CharField` | `varchar(100)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 100 |  |  |  |  |  |  |  |  |
| visibility | visibility | `django.db.models.fields.CharField` | `varchar(20)` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  | 20 |  |  | `AUTHENTICATED` |  |  |  |  |  |
<br/>
<details><summary>Choices</summary>

    - `ADMIN_ONLY`: Admins only
    - `STAFF_ONLY`: Staff users
    - `AUTHENTICATED`: All logged-in users
    - `PUBLIC`: Public/Anyone

</details>

### users.GroupMeta

- **DB table:** `users_groupmeta`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| group | group_id | `django.db.models.fields.related.OneToOneField` | `integer` | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |  |  |  |  |  | OneToOneRel | `auth.Group` |  |  | ['id'] |
| rank | rank | `django.db.models.fields.PositiveIntegerField` | `integer unsigned` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `1000` |  |  |  |  |  |

### users.UserProfile

- **DB table:** `users_userprofile`
- **Managed:** ✅
- **Proxy:** ❌
- **Abstract:** ❌
- **Primary key field:** `id`

| name | attname | type | db_type | null | blank | pk | unique | index | editable | db_column | max_len | digits | places | default | relation | related_model | through | on_delete | to_field |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|---|---|---|---|---|---|---|---|---|
| id | id | `django.db.models.fields.BigAutoField` | `integer` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| user | user_id | `django.db.models.fields.related.OneToOneField` | `integer` | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |  |  |  |  |  | OneToOneRel | `auth.User` |  |  | [None] |
| legal_name | legal_name | `django.db.models.fields.CharField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| chosen_name | chosen_name | `django.db.models.fields.CharField` | `varchar(200)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 200 |  |  |  |  |  |  |  |  |
| pronouns | pronouns | `django.db.models.fields.CharField` | `varchar(64)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 64 |  |  |  |  |  |  |  |  |
| birth_date | birth_date | `django.db.models.fields.DateField` | `date` | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| email | email | `django.db.models.fields.EmailField` | `varchar(254)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 254 |  |  |  |  |  |  |  |  |
| phone | phone | `django.db.models.fields.CharField` | `varchar(64)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 64 |  |  |  |  |  |  |  |  |
| address | address | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| role_title | role_title | `django.db.models.fields.CharField` | `varchar(120)` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  | 120 |  |  |  |  |  |  |  |  |
| duties | duties | `django.db.models.fields.TextField` | `text` | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  |  |  |  |  |  |
| primary_group | primary_group_id | `django.db.models.fields.related.ForeignKey` | `integer` | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |  |  |  |  |  | ManyToOneRel | `auth.Group` |  |  | ['id'] |
| force_password_change | force_password_change | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `True` |  |  |  |  |  |
| has_selected_visibility | has_selected_visibility | `django.db.models.fields.BooleanField` | `bool` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |  |  |  |  | `False` |  |  |  |  |  |
| created_at | created_at | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| updated_at | updated_at | `django.db.models.fields.DateTimeField` | `datetime` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |  |  |  |  |  |  |  |  |  |  |
| badges | badges | `django.db.models.fields.related.ManyToManyField` |  | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |  |  |  |  |  | ManyToManyRel | `users.BadgeDefinition` | `users.UserProfile_badges` |  |  |

