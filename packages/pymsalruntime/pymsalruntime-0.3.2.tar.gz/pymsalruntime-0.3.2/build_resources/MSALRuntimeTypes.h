// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

#pragma once
#include "stdint.h"

#ifdef __cplusplus
extern "C" {
#endif

#ifndef DECLARE_MSALRUNTIME_HANDLE // Prevent DECLARE_HANDLE macro redefined in winnt.h
#define DECLARE_MSALRUNTIME_HANDLE(name) \
    struct name##__                      \
    {                                    \
        int unused;                      \
    };                                   \
    typedef struct name##__* name
#endif

#ifdef _WIN32
#define MSALRUNTIME_API __stdcall
typedef wchar_t utf16_char;
typedef utf16_char os_char;
typedef void* WINDOW_HANDLE;
#else
#define MSALRUNTIME_API
typedef char utf8_char;
typedef utf8_char os_char;
// On x-plat WINDOW_HANDLE's are defined to be int64_t.
typedef int64_t WINDOW_HANDLE
#endif

typedef int bool_t;

typedef enum
{
    Msalruntime_Response_Status_Unexpected = 0,
    Msalruntime_Response_Status_Reserved = 1,
    Msalruntime_Response_Status_InteractionRequired = 2,
    Msalruntime_Response_Status_NoNetwork = 3,
    Msalruntime_Response_Status_NetworkTemporarilyUnavailable = 4,
    Msalruntime_Response_Status_ServerTemporarilyUnavailable = 5,
    Msalruntime_Response_Status_ApiContractViolation = 6,
    Msalruntime_Response_Status_UserCanceled = 7,
    Msalruntime_Response_Status_ApplicationCanceled = 8,
    Msalruntime_Response_Status_IncorrectConfiguration = 9,
    Msalruntime_Response_Status_InsufficientBuffer = 10,
    Msalruntime_Response_Status_AuthorityUntrusted = 11,
    Msalruntime_Response_Status_UserSwitch = 12,
    Msalruntime_Response_Status_AccountUnusable = 13
} MSALRUNTIME_RESPONSE_STATUS;

typedef enum
{
    Msalruntime_Select_Account_Option_None = 0,
    Msalruntime_Select_Account_Option_ShowLocalAcountsControl = 1,
} MSALRUNTIME_SELECT_ACCOUNT_OPTION;

#ifndef MSALRUNTIME_SUCCEED
// Success case when the error handle is 0 or NULL.
#define MSALRUNTIME_SUCCEED 0
#endif

DECLARE_MSALRUNTIME_HANDLE(MSALRUNTIME_AUTH_PARAMETERS_HANDLE);
DECLARE_MSALRUNTIME_HANDLE(MSALRUNTIME_AUTH_RESULT_HANDLE);
DECLARE_MSALRUNTIME_HANDLE(MSALRUNTIME_ACCOUNT_HANDLE);
DECLARE_MSALRUNTIME_HANDLE(MSALRUNTIME_ERROR_HANDLE);
DECLARE_MSALRUNTIME_HANDLE(MSALRUNTIME_ASYNC_HANDLE);

/*
 * The callback function to inform that async operation has completed and the resource is set.
 *
 * @in-param MSALRUNTIME_AUTH_RESULT_HANDLE authResult - Instance of MSALRUNTIME_AUTH_RESULT_HANDLE created by
 * MSALRUNTIME_RequestTokenInteractively/SilentlyAsync.
 * @in-param void* callbackData - callbackData to be sent by caller to be set by MSALRuntime.
 */
typedef void(MSALRUNTIME_API* MSALRUNTIME_COMPLETION_ROUTINE)(MSALRUNTIME_AUTH_RESULT_HANDLE authResult, void* callbackData);

#ifdef __cplusplus
}
#endif
