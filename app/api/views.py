from __future__ import annotations

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from app.assets.models import Asset, Collection
from app.assets.selectors import (
    filter_assets_for_user,
    filter_assets_with_form,
    filter_collections_for_user,
    user_allowed_for,
)

from .serializers import AssetSerializer, CollectionSerializer


class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    SORT_MAP = {
        "title": "title",
        "-title": "-title",
        "kind": "kind",
        "-kind": "-kind",
        "updated": "updated_at",
        "-updated": "-updated_at",
        "created": "created_at",
        "-created": "-created_at",
    }

    def get_queryset(self):
        _, qs = filter_assets_with_form(self.request.query_params or None)
        qs = filter_assets_for_user(qs, self.request.user)
        ordering = self.request.query_params.get("ordering") or self.request.query_params.get("sort")
        return qs.order_by(self.SORT_MAP.get(ordering, "-updated_at"))

    def perform_create(self, serializer):
        if not user_allowed_for(self.request.user, "cms.assets.add_asset"):
            raise PermissionDenied("Not allowed")
        serializer.save()

    def perform_update(self, serializer):
        asset: Asset = serializer.instance
        if not user_allowed_for(self.request.user, f"cms.assets.asset.{asset.id}.actions"):
            raise PermissionDenied("Not allowed")
        serializer.save()

    def perform_destroy(self, instance):
        if not user_allowed_for(self.request.user, f"cms.assets.asset.{instance.id}.actions"):
            raise PermissionDenied("Not allowed")
        instance.delete()

    @action(detail=True, methods=["post"], url_path="toggle-visibility")
    def toggle_visibility(self, request, pk=None):
        asset = self.get_object()
        if not user_allowed_for(request.user, f"cms.assets.asset.{asset.id}.actions"):
            raise PermissionDenied("Not allowed")
        asset.visibility = (
            "public" if asset.effective_visibility in ("internal", "groups") else "internal"
        )
        asset.save()
        serializer = self.get_serializer(asset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_queryset(self):
        qs = (
            Collection.objects.select_related("parent")
            .prefetch_related("allowed_groups", "tags", "children")
            .order_by("parent__id", "sort_order", "title")
        )
        return filter_collections_for_user(qs, self.request.user)

    def perform_create(self, serializer):
        if not user_allowed_for(self.request.user, "cms.assets.add_collection"):
            raise PermissionDenied("Not allowed")
        serializer.save()

    def perform_update(self, serializer):
        instance: Collection = serializer.instance
        if not user_allowed_for(self.request.user, f"cms.assets.collection.{instance.id}.actions"):
            raise PermissionDenied("Not allowed")
        serializer.save()

    def perform_destroy(self, instance):
        if not user_allowed_for(self.request.user, f"cms.assets.collection.{instance.id}.actions"):
            raise PermissionDenied("Not allowed")
        instance.delete()

    @action(detail=True, methods=["post"], url_path="toggle-visibility")
    def toggle_visibility(self, request, pk=None):
        collection = self.get_object()
        if not user_allowed_for(request.user, f"cms.assets.collection.{collection.id}.actions"):
            raise PermissionDenied("Not allowed")
        collection.visibility_mode = (
            "public" if collection.visibility_mode != "public" else "internal"
        )
        collection.save()
        serializer = self.get_serializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)
