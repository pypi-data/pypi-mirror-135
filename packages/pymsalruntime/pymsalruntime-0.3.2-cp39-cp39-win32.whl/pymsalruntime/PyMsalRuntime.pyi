# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from typing import Callable
from enum import Enum

# Public interface file for the pymsalruntime

class SelectAccountOption(Enum):
    NONE: int
    SHOWLOCALACCOUNTSCONTROL: int

class Response_Status(Enum):
    Status_Unexpected: int
    Status_Reserved: int
    Status_InteractionRequired: int
    Status_NoNetwork: int
    Status_NetworkTemporarilyUnavailable: int
    Status_ServerTemporarilyUnavailable: int
    Status_ApiContractViolation: int
    Status_UserCanceled: int
    Status_ApplicationCanceled: int
    Status_IncorrectConfiguration: int
    Status_InsufficientBuffer: int
    Status_AuthorityUntrusted: int
    Status_UserSwitch: int
    Status_AccountUnusable: int

class MSALRuntimeAsyncHandle:
    pass

class MSALRuntimeError:
    def get_status(self) -> str: ...
    def get_error_code(self) -> int: ...
    def get_tag(self) -> int: ...
    def get_context(self) -> str: ...

class MSALRuntimeAccount:
    def get_account_id(self) -> str: ...
    def get_client_info(self) -> str: ...
    def get_account_property(self, key: str) -> str: ...

class MSALRuntimeAuthParameters:
    def set_requested_scopes(self, scopes: list[str]) -> None: ...
    def set_redirect_uri(self, redirect_uri: str) -> None: ...
    def set_decoded_claims(self, claims: str) -> None: ...
    def set_select_account_option(self, option: SelectAccountOption) -> None: ...
    def set_access_token_to_renew(self, access_token: str) -> None: ...
    def set_additional_parameter(self, key: str, value: str) -> None: ...

class MSALRuntimeAuthResult:
    def get_account(self) -> MSALRuntimeAccount: ...
    def get_id_token(self) -> str: ...
    def get_access_token(self) -> str: ...
    def get_granted_scopes(self) -> list[str]: ...
    def get_access_token_expiry_time(self) -> int: ...
    def get_error(self) -> MSALRuntimeError: ...

def cancel_async_operation(asyncHandle: MSALRuntimeAsyncHandle) -> None: ...
def read_account_by_id(
    accountid: str,
    correlationId: str,
    callback: Callable[[MSALRuntimeAuthResult], None],
) -> MSALRuntimeAsyncHandle: ...
def signin(
    parentWindowHandle: int,
    auth_params: MSALRuntimeAuthParameters,
    correlationId: str,
    callback: Callable[[MSALRuntimeAuthResult], None],
) -> MSALRuntimeAsyncHandle: ...
def signin_silently(
    auth_params: MSALRuntimeAuthParameters,
    correlationId: str,
    callback: Callable[[MSALRuntimeAuthResult], None],
) -> MSALRuntimeAsyncHandle: ...
def signin_interactively(
    parentWindowHandle: int,
    auth_params: MSALRuntimeAuthParameters,
    correlationId: str,
    accountHint: str,
    callback: Callable[[MSALRuntimeAuthResult], None],
) -> MSALRuntimeAsyncHandle: ...
def acquire_token_silently(
    auth_params: MSALRuntimeAuthParameters,
    correlationId: str,
    account: MSALRuntimeAccount,
    callback: Callable[[MSALRuntimeAuthResult], None],
) -> MSALRuntimeAsyncHandle: ...
def acquire_token_interactively(
    parentWindowHandle: int,
    auth_params: MSALRuntimeAuthParameters,
    correlationId: str,
    account: MSALRuntimeAccount,
    callback: Callable[[MSALRuntimeAuthResult], None],
) -> MSALRuntimeAsyncHandle: ...
def get_console_window() -> int: ...
def get_desktop_window() -> int: ...
