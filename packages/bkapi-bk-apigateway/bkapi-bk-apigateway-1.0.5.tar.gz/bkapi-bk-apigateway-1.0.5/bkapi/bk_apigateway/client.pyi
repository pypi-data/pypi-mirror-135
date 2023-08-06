# -*- coding: utf-8 -*-
from bkapi_client_core.apigateway import APIGatewayClient, Operation, OperationGroup


class Group(OperationGroup):

    @property
    def add_related_apps(self) -> Operation:
        """
        添加网关关联应用
        """

    @property
    def apply_permissions(self) -> Operation:
        """
        申请网关API访问权限
        """

    @property
    def create_resource_version(self) -> Operation:
        """
        创建资源版本
        """

    @property
    def get_apigw_public_key(self) -> Operation:
        """
        获取网关公钥
        """

    @property
    def get_latest_resource_version(self) -> Operation:
        """
        获取网关最新版本
        """

    @property
    def grant_permissions(self) -> Operation:
        """
        网关为应用主动授权
        """

    @property
    def import_resource_docs_by_archive(self) -> Operation:
        """
        通过文档归档文件导入资源文档
        """

    @property
    def import_resource_docs_by_swagger(self) -> Operation:
        """
        
        """

    @property
    def release(self) -> Operation:
        """
        发布版本
        """

    @property
    def revoke_permissions(self) -> Operation:
        """
        回收应用访问网关 API 的权限
        """

    @property
    def sync_access_strategy(self) -> Operation:
        """
        同步策略
        """

    @property
    def sync_api(self) -> Operation:
        """
        同步网关
        """

    @property
    def sync_resources(self) -> Operation:
        """
        同步资源
        """

    @property
    def sync_stage(self) -> Operation:
        """
        同步环境
        """


class Client(APIGatewayClient):
    """bk-apigateway
    蓝鲸API网关
    """

    @property
    def api(self) -> Group:
        """api resources"""
