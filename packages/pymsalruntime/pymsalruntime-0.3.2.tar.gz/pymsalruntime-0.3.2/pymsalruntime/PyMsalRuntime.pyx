# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

cimport PyMsalRuntime.CPyMSALRuntime as mrt

from enum import IntEnum, Enum
import json

IF UNAME_SYSNAME == "Windows":
    # __stdcall is needed to specify windows .dll calling conventions.
    ctypedef mrt.MSALRUNTIME_ERROR_HANDLE (__stdcall *_string_getter_func)(mrt.MSALRUNTIME_HANDLE* handle, mrt.os_char* buffer, mrt.int32_t* bufferSize) nogil
    cdef void  __stdcall _MSALRUNTIMEAuthCompletionCallback(mrt.MSALRUNTIME_AUTH_RESULT_HANDLE hResponse, void* callbackData) with gil:
        _MSALRUNTIMEAuthCompletionCallbackInternal(hResponse, callbackData)

    def get_console_window():
        cdef void* window_handle = NULL
        cdef mrt.int64_t mrt_window = 0

        with nogil:
            window_handle = mrt.GetConsoleWindow()
            mrt_window = <mrt.int64_t> window_handle
        
        if window_handle is NULL:
            return None
        else:
            return mrt_window

    def get_desktop_window():
        cdef mrt.int64_t mrt_window = 0

        with nogil:
            mrt_window = <mrt.int64_t> mrt.GetDesktopWindow()

        return mrt_window
ELSE:
    ctypedef mrt.MSALRUNTIME_ERROR_HANDLE (*_string_getter_func)(mrt.MSALRUNTIME_HANDLE* handle, mrt.os_char* buffer, mrt.int32_t* bufferSize) nogil
    cdef void  _MSALRUNTIMEAuthCompletionCallback(mrt.MSALRUNTIME_AUTH_RESULT_HANDLE hResponse, void* callbackData) with gil:
        _MSALRUNTIMEAuthCompletionCallbackInternal(hResponse, callbackData)


class SelectAccountOption(IntEnum):
    NONE = 0
    SHOWLOCALACCOUNTSCONTROL = 1

class Response_Status(Enum):
    Status_Unexpected = 0
    Status_Reserved = 1
    Status_InteractionRequired = 2
    Status_NoNetwork = 3
    Status_NetworkTemporarilyUnavailable = 4
    Status_ServerTemporarilyUnavailable = 5
    Status_ApiContractViolation = 6
    Status_UserCanceled = 7
    Status_ApplicationCanceled = 8
    Status_IncorrectConfiguration = 9
    Status_InsufficientBuffer = 10
    Status_AuthorityUntrusted = 11
    Status_UserSwitch = 12
    Status_AccountUnusable = 13

def cancel_async_operation(MSALRuntimeAsyncHandle async_handle):
    cdef MSALRuntimeAsyncHandle coerced_async_handle = async_handle
    cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

    with nogil:
        mrt_error = mrt.MSALRUNTIME_CancelAsyncOperation(coerced_async_handle._handle)
    
    _check_error(mrt_error)

def read_account_by_id(
        str accountid not None,
        str correlationId not None,
        py_callback not None):
    callback_data = _MSALRuntimeCallBackData(py_callback)
    cdef mrt.os_char* coerced_account_id = accountid
    cdef mrt.os_char* coerced_correlationId = correlationId
    cdef void* coerced_callback_data_id = <void*> callback_data.id
    cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL
    cdef MSALRuntimeAsyncHandle async_handle = MSALRuntimeAsyncHandle()

    with nogil:
        mrt_error = mrt.MSALRUNTIME_ReadAccountByIdAsync(
            coerced_account_id,
            coerced_correlationId,
            _MSALRUNTIMEAuthCompletionCallback,
            coerced_callback_data_id,
            &async_handle._handle)

    _check_error(mrt_error)
    return async_handle

def signin(
        mrt.int64_t parentWindowHandle,
        MSALRuntimeAuthParameters auth_params not None,
        str correlationId not None,
        py_callback not None):
    callback_data = _MSALRuntimeCallBackData(py_callback)
    cdef mrt.int64_t castParentWindowHandle = parentWindowHandle
    cdef MSALRuntimeAuthParameters coerced_auth_params = auth_params
    cdef mrt.os_char* coerced_correlationId = correlationId
    cdef void* coerced_callback_data_id = <void*> callback_data.id
    cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL
    cdef MSALRuntimeAsyncHandle async_handle = MSALRuntimeAsyncHandle()

    with nogil:
        mrt_error = mrt.MSALRUNTIME_SignInAsync(
            <mrt.WINDOW_HANDLE> castParentWindowHandle,
            coerced_auth_params._handle,
            coerced_correlationId,
            _MSALRUNTIMEAuthCompletionCallback,
            coerced_callback_data_id,
            &async_handle._handle)

    _check_error(mrt_error)
    return async_handle

def signin_silently(
        MSALRuntimeAuthParameters auth_params not None,
        str correlationId not None,
        py_callback not None):
    callback_data = _MSALRuntimeCallBackData(py_callback)
    cdef MSALRuntimeAuthParameters coerced_auth_params = auth_params
    cdef mrt.os_char* coerced_correlationId = correlationId
    cdef void* coerced_callback_data_id = <void*> callback_data.id
    cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL
    cdef MSALRuntimeAsyncHandle async_handle = MSALRuntimeAsyncHandle()

    with nogil:
        mrt_error = mrt.MSALRUNTIME_SignInSilentlyAsync(
            coerced_auth_params._handle,
            coerced_correlationId,
            _MSALRUNTIMEAuthCompletionCallback,
            coerced_callback_data_id,
            &async_handle._handle)

    _check_error(mrt_error)
    return async_handle

def signin_interactively(
        mrt.int64_t parentWindowHandle,
        MSALRuntimeAuthParameters auth_params not None,
        str correlationId not None,
        str accountHint,
        py_callback not None):
    callback_data = _MSALRuntimeCallBackData(py_callback)
    cdef mrt.int64_t castParentWindowHandle = parentWindowHandle
    cdef MSALRuntimeAuthParameters coerced_auth_params = auth_params
    cdef mrt.os_char* coerced_correlationId = correlationId
    cdef mrt.os_char* coerced_accountHint = "" if not accountHint else accountHint
    cdef void* coerced_callback_data_id = <void*> callback_data.id
    cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL
    cdef MSALRuntimeAsyncHandle async_handle = MSALRuntimeAsyncHandle()

    with nogil:
        mrt_error = mrt.MSALRUNTIME_SignInInteractivelyAsync(
            <mrt.WINDOW_HANDLE> castParentWindowHandle,
            coerced_auth_params._handle,
            coerced_correlationId,
            coerced_accountHint,
            _MSALRUNTIMEAuthCompletionCallback,
            coerced_callback_data_id,
            &async_handle._handle)

    _check_error(mrt_error)
    return async_handle    

def acquire_token_silently(
        MSALRuntimeAuthParameters auth_params not None,
        str correlationId not None,
        MSALRuntimeAccount account not None,
        py_callback not None):
    callback_data = _MSALRuntimeCallBackData(py_callback)
    cdef MSALRuntimeAuthParameters coerced_auth_params = auth_params
    cdef mrt.os_char* coerced_correlationId = correlationId
    cdef MSALRuntimeAccount coerced_account = account
    cdef void* coerced_callback_data_id = <void*> callback_data.id
    cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL
    cdef MSALRuntimeAsyncHandle async_handle = MSALRuntimeAsyncHandle()

    with nogil:
        mrt_error = mrt.MSALRUNTIME_AcquireTokenSilentlyAsync(
            coerced_auth_params._handle,
            coerced_correlationId,
            coerced_account._handle,
            _MSALRUNTIMEAuthCompletionCallback,
            coerced_callback_data_id,
            &async_handle._handle)

    _check_error(mrt_error)
    return async_handle   

def acquire_token_interactively(
        mrt.int64_t parentWindowHandle,
        MSALRuntimeAuthParameters auth_params not None,
        str correlationId not None,
        MSALRuntimeAccount account not None,
        py_callback not None):
    callback_data = _MSALRuntimeCallBackData(py_callback)
    cdef mrt.int64_t castParentWindowHandle = parentWindowHandle
    cdef MSALRuntimeAuthParameters coerced_auth_params = auth_params
    cdef mrt.os_char* coerced_correlationId = correlationId
    cdef MSALRuntimeAccount coerced_account = account
    cdef void* coerced_callback_data_id = <void*> callback_data.id
    cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL
    cdef MSALRuntimeAsyncHandle async_handle = MSALRuntimeAsyncHandle()

    with nogil:
        mrt_error = mrt.MSALRUNTIME_AcquireTokenInteractivelyAsync(
            <mrt.WINDOW_HANDLE> castParentWindowHandle,
            coerced_auth_params._handle,
            coerced_correlationId,
            coerced_account._handle,
            _MSALRUNTIMEAuthCompletionCallback,
            coerced_callback_data_id,
            &async_handle._handle)

    _check_error(mrt_error)
    return async_handle   

cdef class MSALRuntimeAsyncHandle:
    cdef mrt.MSALRUNTIME_ASYNC_HANDLE _handle

    def __cinit__(self):
        self._handle = NULL

cdef class MSALRuntimeAccount:
    cdef mrt.MSALRUNTIME_ACCOUNT_HANDLE _handle

    def __cinit__(self, rawHandle not None):
        cdef mrt.int64_t castHandle = rawHandle
        self._handle = <mrt.MSALRUNTIME_ACCOUNT_HANDLE> castHandle

    def __dealloc__(self):
        if self._handle:
            with nogil:
                # Release* operations are best effort in destructor as exceptions are not gauranteed
                # to be caught in __dealloc__ code.
                mrt.MSALRUNTIME_ReleaseAccount(self._handle)

    def get_account_id(self):
        return _get_string(<_string_getter_func> mrt.MSALRUNTIME_GetAccountId, <mrt.MSALRUNTIME_HANDLE*> self._handle)

    def get_client_info(self):
        return _get_string(<_string_getter_func> mrt.MSALRUNTIME_GetClientInfo, <mrt.MSALRUNTIME_HANDLE*> self._handle)

    def get_account_property(self, str key not None):
        cdef NativeString nstr = NativeString()
        cdef mrt.os_char* coerced_key = key
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_GetAccountProperty(
                self._handle,
                coerced_key,
                NULL,
                &nstr.buffer_size)

        _check_error(mrt_error, expected_status=Response_Status(<int> mrt.MSALRUNTIME_RESPONSE_STATUS.Msalruntime_Response_Status_InsufficientBuffer))
        
        if nstr.is_empty():
            return None

        cdef mrt.os_char* coerced_value_buffer = nstr.allocate()
        
        with nogil:
            mrt_error = mrt.MSALRUNTIME_GetAccountProperty(
                self._handle,
                coerced_key,
                coerced_value_buffer,
                &nstr.buffer_size)

        _check_error(mrt_error)
        return nstr.get_string()

cdef class MSALRuntimeAuthParameters:
    cdef mrt.MSALRUNTIME_AUTH_PARAMETERS_HANDLE _handle

    def __init__(self, str clientid not None, str authority not None):
        self._handle = NULL
        cdef mrt.os_char* coerced_clientid = clientid
        cdef mrt.os_char* coerced_authority = authority
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_CreateAuthParameters(
                coerced_clientid,
                coerced_authority,
                &self._handle)

        _check_error(mrt_error)

    def __dealloc__(self):
        if self._handle:
            with nogil:
                # Release* operations are best effort in destructor as exceptions are not gauranteed
                # to be caught in __dealloc__ code.
                mrt.MSALRUNTIME_ReleaseAuthParameters(self._handle)

    def set_requested_scopes(self, scopes not None):
        if not isinstance(scopes, list):
            raise TypeError('scopes must be an list type')
        scopes_list_string = "[" + ",".join(list(map(lambda scope : "\"" + scope + "\"", scopes))) + "]"
        cdef mrt.os_char* coerced_scopes = scopes_list_string
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_SetRequestedScopes(self._handle, coerced_scopes)

        _check_error(mrt_error)

    def set_redirect_uri(self, str redirect_uri not None):
        cdef mrt.os_char* coerced_redirect_uri = redirect_uri
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_SetRedirectUri(self._handle, coerced_redirect_uri)

        _check_error(mrt_error)

    def set_select_account_option(self, option not None):
        if not isinstance(option, SelectAccountOption):
            raise TypeError('option must be an instance of SelectAccountOption IntEnum')

        cdef mrt.MSALRUNTIME_SELECT_ACCOUNT_OPTION coerced_option = option
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_SetSelectAccountOption(self._handle, coerced_option)

        _check_error(mrt_error)

    def set_decoded_claims(self, str claims not None):
        cdef mrt.os_char* coerced_claims = claims
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_SetDecodedClaims(self._handle, coerced_claims)

        _check_error(mrt_error)

    def set_access_token_to_renew(self, str access_token_to_renew not None):
        cdef mrt.os_char* coerced_access_token_to_renew = access_token_to_renew
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_SetAccessTokenToRenew(self._handle, coerced_access_token_to_renew)

        _check_error(mrt_error)

    def set_additional_parameter(self, str key not None, str value not None):
        cdef mrt.os_char* coerced_key = key
        cdef mrt.os_char* coerced_value = value
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_SetAdditionalParameter(
                self._handle,
                coerced_key,
                coerced_value)

        _check_error(mrt_error)

cdef class MSALRuntimeAuthResult:
    cdef mrt.MSALRUNTIME_AUTH_RESULT_HANDLE _handle
    def __cinit__(self, rawHandle not None):
        cdef mrt.int64_t castHandle = rawHandle
        self._handle = <mrt.MSALRUNTIME_AUTH_RESULT_HANDLE> castHandle

    def __dealloc__(self):
        if self._handle:
            with nogil:
                # Release* operations are best effort in destructor as exceptions are not gauranteed
                # to be caught in __dealloc__ code.
                mrt.MSALRUNTIME_ReleaseAuthResult(self._handle)

    def get_account(self):
        cdef mrt.MSALRUNTIME_ACCOUNT_HANDLE account_handle = NULL
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_GetAccount(self._handle, &account_handle)

        _check_error(mrt_error)

        if account_handle == NULL:
            return None

        cdef MSALRuntimeAccount account = MSALRuntimeAccount(<long long> account_handle)
        return account

    def get_id_token(self):
        return _get_string(<_string_getter_func> mrt.MSALRUNTIME_GetIdToken, <mrt.MSALRUNTIME_HANDLE*> self._handle)

    def get_access_token(self):
        return _get_string(<_string_getter_func> mrt.MSALRUNTIME_GetAccessToken, <mrt.MSALRUNTIME_HANDLE*> self._handle)

    def get_granted_scopes(self):
        json_py_string = _get_string(<_string_getter_func> mrt.MSALRUNTIME_GetGrantedScopes, <mrt.MSALRUNTIME_HANDLE*> self._handle)
        if not json_py_string:
            return None
        return json.loads(json_py_string)

    def get_access_token_expiry_time(self):
        cdef mrt.int64_t expiry_time = 0
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_GetExpiresOn(
                self._handle,
                &expiry_time)

        _check_error(mrt_error)
        return <int> expiry_time

    def get_error(self):
        cdef mrt.MSALRUNTIME_ERROR_HANDLE error_handle = NULL
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_GetError(self._handle, &error_handle)

        _check_error(mrt_error)

        if error_handle == NULL:
            return None

        cdef MSALRuntimeError msalruntime_error = MSALRuntimeError()
        msalruntime_error._handle = error_handle
        return msalruntime_error


cdef class MSALRuntimeError:
    cdef mrt.MSALRUNTIME_ERROR_HANDLE _handle
    def __cinit__(self):
        self._handle = NULL

    def __dealloc__(self):
        if self._handle:
            with nogil:
                # Release* operations are best effort in destructor as exceptions are not gauranteed
                # to be caught in __dealloc__ code.
                mrt.MSALRUNTIME_ReleaseError(self._handle)

    def get_status(self):
        cdef mrt.MSALRUNTIME_RESPONSE_STATUS status
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_GetStatus(self._handle, &status)
        _raise_if_error(mrt_error, "get_status")

        return Response_Status(<int> status)

    def get_error_code(self):
        cdef mrt.int32_t error_code = 0
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_GetErrorCode(self._handle, &error_code)
        _raise_if_error(mrt_error, "get_error_code")

        return <int> error_code

    def get_tag(self):
        cdef mrt.int32_t tag = 0
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

        with nogil:
            mrt_error = mrt.MSALRUNTIME_GetTag(self._handle, &tag)
        _raise_if_error(mrt_error, "get_tag")

        return tag

    def get_context(self):
        cdef NativeString nstr = NativeString()
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_first_error = NULL
        cdef MSALRuntimeError msalruntime_error = MSALRuntimeError()

        with nogil:
            mrt_first_error = mrt.MSALRUNTIME_GetContext(
                self._handle,
                NULL,
                &nstr.buffer_size)

        if mrt_first_error:
            msalruntime_error._handle = mrt_first_error
            errorStatus = msalruntime_error.get_status();
            if (errorStatus != Response_Status(<int> mrt.MSALRUNTIME_RESPONSE_STATUS.Msalruntime_Response_Status_InsufficientBuffer)):
                raise RuntimeError("Get Context return unexpected status: %s" % Response_Status(errorStatus))  
        
        if nstr.is_empty():
            return None

        cdef mrt.os_char* coerced_buffer = nstr.allocate()
        cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_second_error = NULL

        with nogil:
            mrt_second_error = mrt.MSALRUNTIME_GetContext(
                self._handle,
                coerced_buffer,
                &nstr.buffer_size)

        _raise_if_error(mrt_second_error, "get_context")
        return nstr.get_string()

# Error helper functions
cdef _raise_if_error(mrt.MSALRUNTIME_ERROR_HANDLE error, name):
    cdef MSALRuntimeError msalruntime_error = MSALRuntimeError()
    
    if error:
        # assign the handle to the error for proper clean up
        msalruntime_error._handle = error 
        # Raise generic error to prevent recursively getting error properties.
        raise RuntimeError("%s return unexpected" % name) 


cdef _check_error(mrt.MSALRUNTIME_ERROR_HANDLE error, expected_status=None):
    cdef MSALRuntimeError msalruntime_error = MSALRuntimeError()

    if error:
        msalruntime_error._handle = error
        errorStatus = msalruntime_error.get_status();
        if (errorStatus == expected_status):
            return

        errorCode = msalruntime_error.get_error_code()
        errorTag = msalruntime_error.get_tag();
        errorContext = msalruntime_error.get_context()
        
        raise RuntimeError("ErrorTag: %d, ErrorCode: %d, ErrorContext: %s, ErrorStatus: %s" % (errorTag, errorCode, errorContext, Response_Status(errorStatus)))

# Private startup/shutdown functions which pin/unpin the .dll
def _startup_msalruntime():
    cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL
    with nogil:
        mrt_error = mrt.MSALRUNTIME_Startup()

    _check_error(mrt_error)

def _shutdown_msalruntime():

    with nogil:
        mrt.MSALRUNTIME_Shutdown()

# String helper functions
cdef class NativeString:
    cdef mrt.int32_t buffer_size
    cdef bytearray buffer

    def __cinit__(self):
        self.buffer_size = 0

    cdef mrt.os_char* allocate(self):
        self.buffer = bytearray(self.buffer_size * sizeof(mrt.os_char))
        return <mrt.os_char*><unsigned char*> self.buffer

    def get_string(self):
        return self.buffer[:(self.buffer_size - 1) * sizeof(mrt.os_char)].decode("utf-16-le")

    def is_empty(self):
        return self.buffer_size == 0

cdef str _get_string(_string_getter_func func, mrt.MSALRUNTIME_HANDLE* handle):
    cdef NativeString nstr = NativeString()
    cdef mrt.MSALRUNTIME_ERROR_HANDLE mrt_error = NULL

    with nogil:
        mrt_error = func(
            handle,
            NULL,
            &nstr.buffer_size)

    _check_error(mrt_error, expected_status=Response_Status(<int> mrt.MSALRUNTIME_RESPONSE_STATUS.Msalruntime_Response_Status_InsufficientBuffer))

    if nstr.is_empty():
        return None

    cdef mrt.os_char* coerced_buffer = nstr.allocate()

    with nogil:
        mrt_error = func(
            handle,
            coerced_buffer,
            &nstr.buffer_size)

    _check_error(mrt_error)
    return nstr.get_string()

# Callback helper functions
_callbackStorage = {}

cdef void  _MSALRUNTIMEAuthCompletionCallbackInternal(mrt.MSALRUNTIME_AUTH_RESULT_HANDLE hResponse, void* callbackData) with gil:
    callbackId = <object> callbackData

    callback_data = _callbackStorage.pop(callbackId, None)
    if callback_data:
        if (hResponse == NULL):
            raise RuntimeError("Callback result handle is NULL")

        callback_data.callback(MSALRuntimeAuthResult(<long long> hResponse))

class _MSALRuntimeCallBackData:
    def __init__(self, callback):
        self.callback = callback
        self.id = id(self)

        _callbackStorage[self.id] = self