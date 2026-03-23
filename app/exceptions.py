class AppError(Exception):
    pass


class NameAlreadyTakenError(AppError):
    pass


class RabotyagaByIdNotFound(AppError):
    pass
