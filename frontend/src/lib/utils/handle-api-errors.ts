type ApiErrorParams = Response | Error | string | unknown

export function handleApiError(
  errorSource: ApiErrorParams,
  defaultMessage = 'API request failed',
) {
  if (errorSource instanceof Response) {
    return {
      success: false,
      error: errorSource.statusText || defaultMessage,
      status: errorSource.status,
    }
  } else if (errorSource instanceof Error) {
    return {
      success: false,
      error: errorSource.message || defaultMessage,
      status: 500,
    }
  } else {
    return {
      success: false,
      error: errorSource,
      status: 400,
    }
  }
}
