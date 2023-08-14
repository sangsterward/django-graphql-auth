import graphene
import graphql_jwt

from .bases import DynamicArgsMixin
from .bases import MutationMixin
from .mixins import ArchiveAccountMixin
from .mixins import DeleteAccountMixin
from .mixins import ObtainJSONWebTokenMixin
from .mixins import PasswordChangeMixin
from .mixins import PasswordResetMixin
from .mixins import PasswordSetMixin
from .mixins import RegisterMixin
from .mixins import RemoveSecondaryEmailMixin
from .mixins import ResendActivationEmailMixin
from .mixins import SendPasswordResetEmailMixin
from .mixins import SendSecondaryEmailActivationMixin
from .mixins import SwapEmailsMixin
from .mixins import UpdateAccountMixin
from .mixins import VerifyAccountMixin
from .mixins import VerifyOrRefreshOrRevokeTokenMixin
from .mixins import VerifySecondaryEmailMixin
from .schema import UserNode
from .settings import graphql_auth_settings as app_settings
from .utils import normalize_fields


class Register(MutationMixin, DynamicArgsMixin, RegisterMixin, graphene.Mutation):

    __doc__ = RegisterMixin.__doc__

    password_fields = (
        []
        if app_settings.ALLOW_PASSWORDLESS_REGISTRATION
        else ["password1", "password2"]
    )
    _required_args = normalize_fields(
        app_settings.REGISTER_MUTATION_FIELDS, password_fields
    )
    _args = app_settings.REGISTER_MUTATION_FIELDS_OPTIONAL


class VerifyAccount(
    MutationMixin, DynamicArgsMixin, VerifyAccountMixin, graphene.Mutation
):
    __doc__ = VerifyAccountMixin.__doc__
    _required_args = ["token"]


class ResendActivationEmail(
    MutationMixin, DynamicArgsMixin, ResendActivationEmailMixin, graphene.Mutation
):
    __doc__ = ResendActivationEmailMixin.__doc__
    _required_args = ["email"]


class SendPasswordResetEmail(
    MutationMixin, DynamicArgsMixin, SendPasswordResetEmailMixin, graphene.Mutation
):
    __doc__ = SendPasswordResetEmailMixin.__doc__
    _required_args = ["email"]


class SendSecondaryEmailActivation(
    MutationMixin,
    DynamicArgsMixin,
    SendSecondaryEmailActivationMixin,
    graphene.Mutation,
):
    __doc__ = SendSecondaryEmailActivationMixin.__doc__
    _required_args = ["email", "password"]


class VerifySecondaryEmail(
    MutationMixin, DynamicArgsMixin, VerifySecondaryEmailMixin, graphene.Mutation
):
    __doc__ = VerifySecondaryEmailMixin.__doc__
    _required_args = ["token"]


class SwapEmails(MutationMixin, DynamicArgsMixin, SwapEmailsMixin, graphene.Mutation):
    __doc__ = SwapEmailsMixin.__doc__
    _required_args = ["password"]


class RemoveSecondaryEmail(
    MutationMixin, DynamicArgsMixin, RemoveSecondaryEmailMixin, graphene.Mutation
):
    __doc__ = RemoveSecondaryEmailMixin.__doc__
    _required_args = ["password"]


class PasswordSet(MutationMixin, PasswordSetMixin, DynamicArgsMixin, graphene.Mutation):
    __doc__ = PasswordSetMixin.__doc__
    _required_args = ["token", "new_password1", "new_password2"]


class PasswordReset(
    MutationMixin, DynamicArgsMixin, PasswordResetMixin, graphene.Mutation
):
    __doc__ = PasswordResetMixin.__doc__
    _required_args = ["token", "new_password1", "new_password2"]



class JSONWebTokenMutation(graphql_jwt.JSONWebTokenMutation):
    token = graphene.String()

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class ObtainJSONWebToken(MutationMixin, ObtainJSONWebTokenMixin, JSONWebTokenMutation):
    __doc__ = ObtainJSONWebTokenMixin.__doc__
    user = graphene.Field(UserNode)
    unarchiving = graphene.Boolean(default_value=False)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update({"password": graphene.String(required=True)})
        for field in app_settings.LOGIN_ALLOWED_FIELDS:
            cls._meta.arguments.update({field: graphene.String()})
        return super(JSONWebTokenMutation, cls).Field(*args, **kwargs)


class ArchiveAccount(
    MutationMixin, ArchiveAccountMixin, DynamicArgsMixin, graphene.Mutation
):
    __doc__ = ArchiveAccountMixin.__doc__
    _required_args = ["password"]


class DeleteAccount(
    MutationMixin, DeleteAccountMixin, DynamicArgsMixin, graphene.Mutation
):
    __doc__ = DeleteAccountMixin.__doc__
    _required_args = ["password"]


class PasswordChange(
    MutationMixin, PasswordChangeMixin, DynamicArgsMixin, graphene.Mutation
):
    __doc__ = PasswordChangeMixin.__doc__
    _required_args = ["old_password", "new_password1", "new_password2"]


class UpdateAccount(
    MutationMixin, DynamicArgsMixin, UpdateAccountMixin, graphene.Mutation
):
    __doc__ = UpdateAccountMixin.__doc__
    _args = app_settings.UPDATE_MUTATION_FIELDS


class VerifyToken(MutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.Verify):
    __doc__ = VerifyOrRefreshOrRevokeTokenMixin.__doc__


class RefreshToken(
    MutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.Refresh
):
    __doc__ = VerifyOrRefreshOrRevokeTokenMixin.__doc__


class RevokeToken(MutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.Revoke):
    __doc__ = VerifyOrRefreshOrRevokeTokenMixin.__doc__
