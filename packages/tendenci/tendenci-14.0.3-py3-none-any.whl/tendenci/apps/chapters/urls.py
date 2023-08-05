from django.urls import path, re_path
from . import views
from .feeds import LatestEntriesFeed

urlpatterns = [
    re_path(r'^chapters/$', views.search, name="chapters.search"),
    re_path(r'^chapters/add/$', views.add, name='chapters.add'),
    re_path(r'^chapters/add/(?P<copy_from_id>\d+)/$', views.add, name='chapters.copy_from'),
    re_path(r'^chapters/edit/(?P<id>\d+)/$', views.edit, name='chapters.edit'),
    re_path(r'^chapters/edit/meta/(?P<id>\d+)/$', views.edit_meta, name="chapters.edit.meta"),
    re_path(r'^chapters/delete/(?P<id>\d+)/$', views.delete, name='chapters.delete'),
    re_path(r'^chapters/feed/$', LatestEntriesFeed(), name='chapters.feed'),

    # chapter memberships
    re_path(r'^chapters/edit_app_fields/(?P<id>\d+)/$', views.edit_app_fields, name='chapters.edit_app_fields'),
    re_path(r'^chapters/edit_membership_types/(?P<id>\d+)/$',
            views.edit_membership_types,
            name='chapters.edit_membership_types'),
    re_path(r"^chapters/get_app_fields/$", views.get_app_fields_json,
                            name="chapters.get_app_fields"),
    re_path(r"^chapters/memberships/(?P<chapter_membership_id>\d+)/$",
        views.membership_details,
        name="chapters.membership_details"),
    re_path(r"^chapters/memberships/applications/add/pre/$",
        views.chapter_membership_add_pre,
        name="chapters.membership_add_pre"),
    re_path(r"^chapters/(?P<chapter_id>\d+)/memberships/applications/add/$",
        views.chapter_membership_add,
        name="chapters.membership_add"),
    re_path(r"^chapters/memberships/applications/add_conf/(?P<id>\d+)/$",
        views.chapter_membership_add_conf,
        name="chapters.membership_add_conf"),
    re_path(r"^chapters/memberships/edit/(?P<chapter_membership_id>\d+)/$",
        views.chapter_membership_edit,
        name="chapters.membership_edit"),
    re_path(r"^chapters/memberships/renew/(?P<chapter_membership_id>\d+)/$",
        views.chapter_membership_renew,
        name="chapters.membership_renew"),
    re_path(r"^chapters/memberships/search/(?P<chapter_id>\d+)/$",
        views.chapter_memberships_search,
        name="chapters.memberships_search_single_chapter"),
    re_path(r"^chapters/memberships/search/$",
        views.chapter_memberships_search,
        name="chapters.memberships_search"),
    re_path(r"^chapters/memberships/files/(?P<cm_id>\d+)/$", views.file_display,
            name="chapters.cm_file_display"),

    # chapter memberships import
    re_path(r"^chapters/memberships/import/$",
        views.chapter_memberships_import_upload,
        name="chapters.memberships_import"),
    re_path(r"^chapters/memberships/import/(?P<chapter_id>\d+)/$",
        views.chapter_memberships_import_upload,
        name="chapters.memberships_import_single_chapter"),
    re_path(r"^chapters/memberships/import/preview/(?P<mimport_id>\d+)/$",
        views.chapter_memberships_import_preview,
        name="chapters.memberships_import_preview"),
    re_path(r"^chapters/memberships/import/process/(?P<mimport_id>\d+)/$",
        views.chapter_memberships_import_process,
        name="chapters.memberships_import_process"),
    re_path(r"^chapters/memberships/import/status/(?P<mimport_id>\d+)/$",
        views.chapter_memberships_import_status,
        name="chapters.memberships_import_status"),
    re_path(r"^chapters/memberships/import/get_status/(?P<mimport_id>\d+)/$",
        views.chapter_memberships_import_get_status,
        name="chapters.memberships_import_get_status"),
    re_path(r"^chapters/memberships/import/check_encode_status/(?P<mimport_id>\d+)/$",
        views.chapter_memberships_import_check_preprocess_status,
        name="chapters.memberships_import_check_preprocess_status"),
    re_path(r"^chapters/memberships/import/download_recap/(?P<mimport_id>\d+)/$",
        views.chapter_memberships_import_download_recap,
        name="chapters.memberships_import_download_recap"),
    re_path(r"^chapters/memberships/import/download_template/$",
        views.download_import_template,
        name="chapters.download_import_template"),
    re_path(r"^chapters/memberships/import/download_template/(?P<chapter_id>\d+)/$",
        views.download_import_template,
        name="chapters.download_import_template_single_chapter"),

    re_path(r'^chapters/(?P<slug>[\w\-\/]+)/$', views.detail, name="chapters.detail"),
]
