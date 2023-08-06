// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

#pragma once

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Creates the MSALRUNTIME_AUTH_PARAMETERS_HANDLE that is used for all signIn and authentication operations.
 *
 * @in-param const os_char* clientId - the id for the application.
 * @in-param const os_char* authority - authority the application is requesting for.
 * @in-out-param MSALRUNTIME_AUTH_PARAMETERS_HANDLE* - pointer to the MSALRUNTIME_AUTH_PARAMETERS_HANDLE to be created.
 *
 * @return - success if null handle, otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API MSALRUNTIME_CreateAuthParameters(
    const os_char* clientId,
    const os_char* authority,
    MSALRUNTIME_AUTH_PARAMETERS_HANDLE* authParameters);

/*
 * Releases the allocated MSALRUNTIME_AUTH_PARAMETERS_HANDLE in the MSALRuntime.
 *
 * @in-param MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters - handle for the authentication parameter.
 *
 * @return - success if null handle, otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API
MSALRUNTIME_ReleaseAuthParameters(MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters);

/*
 * Sets the scopes on the given MSALRUNTIME_AUTH_PARAMETERS_HANDLE.
 * The scopes are required to be in a JSON Array format: ex: ["scope1", "scope2"]
 *
 * @in-param MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters - MSALRUNTIME_AUTH_PARAMETERS_HANDLE to set the scopes
 * on.
 * @in-param const os_char* scopes - Scopes to be set.
 *
 * @return - success if null handle, otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API
MSALRUNTIME_SetRequestedScopes(MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters, const os_char* scopes);

/*
 * Sets the redirectUri on the given MSALRUNTIME_AUTH_PARAMETERS_HANDLE.
 *
 * @in-param MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters - MSALRUNTIME_AUTH_PARAMETERS_HANDLE to set the scopes
 * on.
 * @in-param const os_char* redirectUri - redirect Uri to be set.
 *
 * @return - success if null handle, otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API
MSALRUNTIME_SetRedirectUri(MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters, const os_char* redirectUri);

/*
 * Sets the SelectAccountOption on the given MSALRUNTIME_AUTH_PARAMETERS_HANDLE.
 *
 * @in-param MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters - MSALRUNTIME_AUTH_PARAMETERS_HANDLE to set the
 * SelectAccountOption on.
 * @in-param cconst MSALRUNTIME_SELECT_ACCOUNT_OPTION - selectAccountOption to be set.
 *
 * @return - 0 -- success, otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API MSALRUNTIME_SetSelectAccountOption(
    MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters,
    const MSALRUNTIME_SELECT_ACCOUNT_OPTION selectAccountOption);

/*
 * Sets the claims on the given MSALRUNTIME_AUTH_PARAMETERS_HANDLE.
 *
 * @in-param MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters - MSALRUNTIME_AUTH_PARAMETERS_HANDLE to set the claims
 * on.
 * @in-param const os_char* claims - Claims to be set.
 *
 * @return - success if null handle, otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API
MSALRUNTIME_SetDecodedClaims(MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters, const os_char* claims);

/*
 * Sets the accessToken on the given MSALRUNTIME_AUTH_PARAMETERS_HANDLE to be invalidated.
 *
 * @in-param MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters - MSALRUNTIME_AUTH_PARAMETERS_HANDLE to set the
 * accessToken to renew on.
 * @in-param const os_char* accessTokenToRenew - accessTokenToRenew to be set.
 *
 * @return - success if null handle, otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API
MSALRUNTIME_SetAccessTokenToRenew(MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters, const os_char* accessTokenToRenew);

/*
 * Sets an additional parameter on the given MSALRUNTIME_AUTH_PARAMETERS_HANDLE.
 *
 * @in-param MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters - MSALRUNTIME_AUTH_PARAMETERS_HANDLE to set the
 * additional parameter on.
 * @in-param const os_char* key - key of the parameter to be set.
 * @in-param const os_char* value - value of the parameter to be set.
 *
 * @return - success if null handle, otherwise fail.
 */
MSALRUNTIME_ERROR_HANDLE MSALRUNTIME_API MSALRUNTIME_SetAdditionalParameter(
    MSALRUNTIME_AUTH_PARAMETERS_HANDLE authParameters,
    const os_char* key,
    const os_char* value);

#ifdef __cplusplus
}
#endif
