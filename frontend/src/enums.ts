export const enum Errors {
  Forbidden = "Forbidden",
  Invalid = "Bad Request",
  NotFound = "Not Found",
  Unauthorized = "Unauthorized",
}

export const enum Forbidden {
  NoAdminPermissions = "Insufficient permissions to perform administrator actions.",
  NoDeletePermissions = "Insufficient permissions to delete files.",
  NoLocationPermissions = "Insufficient permissions to access this location.",
  NoMovePermissions = "Insufficient permissions to move files.",
  NoWritePermissions = "Insufficient permissions to write files.",
}

export const enum Invalid {
  BadArchiveType = "Invalid archive type was requested.",
  BadArguments = "Bad argument values were provided.",
  BadFileDownloadEndpoint = "Files cannot be downloaded by this endpoint.",
  BadFolderDownloadEndpoint = "Folders cannot be downloaded by this endpoint.",
  FileFolderExists = "There is already a file/folder with the same name at the destination.",
  NoCredentials = "Credentials were not provided.",
  NoLocation = "Location index was not provided.",
  NoUsername = "Username was not specified.",
  TraversalNotAllowed = "Directory traversal outside of the root location is not allowed.",
}

export const enum NotFound {
  FileFolderNotFound = "File or folder was not found.",
  LocationNotFound = "The provided location was not found.",
  UserNotFound = "Requested user was not found.",
  UUIDNotFound = "The specified UUID was not found.",
}

export const enum Unauthorized {
  BadCredentials = "Given credentials were invalid.",
  BadIssuer = "Invalid token issuer.",
  BadScheme = "Bearer authorization is required.",
  BadUname = "Could not find the user with the provided username.",
  Blacklisted = "This token has been invalidated.",
  DecodeError = "An error occurred while trying to decode the token.",
  Expired = "This token has expired.",
}
