class BadRequestException(Exception):
    def __init__(
        self, entity: str, id: int | str, operation: str, custom_message: str | None
    ):
        self.entity = entity
        self.id = id
        self.operation = operation
        self.message = (
            custom_message
            if custom_message
            else f"Operation {operation} cannot be applied on the entity {entity} with id {id}."
        )


class NotFoundException(Exception):
    def __init__(self, entity: str, id: int | str, custom_message: str | None = None):
        self.entity = entity
        self.id = id
        self.message = (
            custom_message
            if custom_message
            else f"Entity {entity} with id {id} does not exist."
        )


class UnauthorizedException(Exception):
    def __init__(self, user_id: str, custom_message: str | None = None):
        self.user_id = user_id
        self.message = (
            custom_message
            if custom_message
            else f"User with id {user_id} is not authorized for this request."
        )
