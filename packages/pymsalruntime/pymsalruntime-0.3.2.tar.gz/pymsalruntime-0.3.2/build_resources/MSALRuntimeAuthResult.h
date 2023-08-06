// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

#pragma once

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Releases the allocated MSALRUNTIME_AUTH_RESULT_HANDLE in the MSALRuntime.
 *
 * @in-param MSALRUNTIME_AUTH_RESULT_HANDLE authResult - MSALRUNTIME_AUTH_RESULT_HANDLE to be released.
 *
 * @return - success if null handle, otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API MSALRUNTIME_ReleaseAuthResult(MSALRUNTIME_AUTH_RESULT_HANDLE authResult);

/*
 * Gets the msalruntimeaccount retrieved from RequestTokenSilently\Interactively() call on the authResult.
 *
 * @in-param MSALRUNTIME_AUTH_RESULT_HANDLE authResult - the authResult handle.
 * @in-out-param MSALRUNTIME_ACCOUNT_HANDLE* account - pointer to the MSALRUNTIME_ACCOUNT_HANDLE to be created.
 *
 * @return - success if null handle, otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API
MSALRUNTIME_GetAccount(MSALRUNTIME_AUTH_RESULT_HANDLE authResult, MSALRUNTIME_ACCOUNT_HANDLE* account);

/*
 * Gets the IdToken retrieved from RequestTokenSilently\Interactively() call on the authResult.
 *
 * @in-param MSALRUNTIME_AUTH_RESULT_HANDLE authResult - the authResult handle.
 * @out-param os_char* IdToken - the buffer that is used to copy the id token into.
 * @in-out-param int32_t* bufferSize - this parameter contains the size of the buffer (number of characters +
 * null terminator) and is updated by the method to indicate the actual size of the buffer.
 *
 * @return - null handle, success.
 * Handle with InsufficientBuffer status, if the buffer is too small, then bufferSize contains the new size to be
 * allocated. Otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API
MSALRUNTIME_GetIdToken(MSALRUNTIME_AUTH_RESULT_HANDLE authResult, os_char* IdToken, int32_t* bufferSize);

/*
 * Gets the AccessToken retrieved from RequestTokenSilently\Interactively() call on the authResult.
 *
 * @in-param MSALRUNTIME_AUTH_RESULT_HANDLE authResult - the authResult handle.
 * @out-param os_char* accessToken - the buffer that is used to copy the access token into.
 * @in-out-param int32_t* bufferSize - this parameter contains the size of the buffer (number of characters +
 * null terminator) and is updated by the method to indicate the actual size of the buffer.
 *
 * @return - null handle, success.
 * Handle with InsufficientBuffer status, if the buffer is too small, then bufferSize contains the new size to be
 * allocated. Otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API
MSALRUNTIME_GetAccessToken(MSALRUNTIME_AUTH_RESULT_HANDLE authResult, os_char* accessToken, int32_t* bufferSize);

/*
 * Gets the granted scopes retrieved from RequestTokenSilently\Interactively() call on the authResult.
 * the granted Scopes are retunred as a JSON Array format. ex: ["scope1", "scope2"]
 *
 * @in-param MSALRUNTIME_AUTH_RESULT_HANDLE authResult - the authResult handle.
 * @out-param os_char* grantedScopes - the buffer that is used to copy the grantedScopes into.
 * @in-out-param int32_t* bufferSize - this parameter contains the size of the buffer (number of characters +
 * null terminator) and is updated by the method to indicate the actual size of the buffer.
 *
 * @return - null handle, success.
 * Handle with InsufficientBuffer status, if the buffer is too small, then bufferSize contains the new size to be
 * allocated. Otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API
MSALRUNTIME_GetGrantedScopes(MSALRUNTIME_AUTH_RESULT_HANDLE authResult, os_char* grantedScopes, int32_t* bufferSize);

/*
 * Gets the tokenExpirationTime retrieved from RequestTokenSilently\Interactively() call on the authResult.
 *
 * @in-param MSALRUNTIME_AUTH_RESULT_HANDLE authResult - the authResult handle.
 * @out-param int32_t tokenExpirationTime - the tokenExpirationTime.
 *
 * @return - success if null handle, otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API
MSALRUNTIME_GetExpiresOn(MSALRUNTIME_AUTH_RESULT_HANDLE authResult, int64_t* accessTokenExpirationTime);

/*
 * Gets the MSALRUNTIME_ERROR_HANDLE retrieved from RequestTokenSilently\Interactively() call on the authResult.
 *
 * @in-param MSALRUNTIME_AUTH_RESULT_HANDLE authResult - the authResult handle.
 * @in-out-param MSALRUNTIME_ERROR_HANDLE* responseError - this parameter will contain the MSALRUNTIME_ERROR_HANDLE.
 *
 * @return - success if null handle, otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API
MSALRUNTIME_GetError(MSALRUNTIME_AUTH_RESULT_HANDLE authResult, MSALRUNTIME_ERROR_HANDLE* responseError);

#ifdef __cplusplus
}
#endif
