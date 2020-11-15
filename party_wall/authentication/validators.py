import string
from abc import ABC, abstractmethod
from typing import Any

from marshmallow.exceptions import ValidationError

from party_wall.authentication.exceptions import ValidationFailed


class Validator(ABC):
    @abstractmethod
    def validate(self, value: Any) -> Any:
        pass


# this class should probably go to some integration layer module
class MarshmallowValidator(ABC):
    def __call__(self, value: Any) -> Any:
        try:
            return self.validate(value)
        except ValidationFailed as err:
            raise ValidationError(err.message)

    @abstractmethod
    def validate(self, value: Any) -> Any:
        pass


# eventually we could create one validator that would iterate over characters and do all checks every iteration
# instead of iterating multiple times over same string (just to save some computation time)
class PasswordDigitValidator(Validator):
    @staticmethod
    def validate(value: str) -> str:
        for character in value:
            if character.isdigit():
                return value

        raise ValidationFailed("Passoword should contain at least one digit")


class PasswordUpperCaseLetterValidator(Validator):
    @staticmethod
    def validate(value: str) -> str:
        for character in value:
            if character.isupper():
                return value

        raise ValidationFailed("Password should contain at least one upper case letter")


class PasswordLowerCaseLetterValidator(Validator):
    @staticmethod
    def validate(value: str) -> str:
        for character in value:
            if character.islower():
                return value

        raise ValidationFailed("Password should contain at least one lower case letter")


# this could be called PasswordCharacterRangeValidator beacuse it takes arbitrary characters and checks if
# value contains one of it
class PasswordSpecialCharacterValidator(Validator):
    def __init__(self, characters: str = string.punctuation):
        # or these characters could be passed as keyword argument to .validate method
        self.characters = characters

    def validate(self, value: str) -> str:
        for character in value:
            if character in self.characters:
                return value

        raise ValidationFailed(
            f"Password should contain at least one special character: '{self.characters}'"
        )


class MarshmallowPasswordDigitValidator(PasswordDigitValidator, MarshmallowValidator):
    pass


class MarshmallowPasswordLowerCaseLetterValidator(
    PasswordLowerCaseLetterValidator, MarshmallowValidator
):
    pass


class MarshmallowPasswordUpperCaseLetterValidator(
    PasswordUpperCaseLetterValidator, MarshmallowValidator
):
    pass


class MarshmallowPasswordSpecialCharacterValidator(
    PasswordSpecialCharacterValidator, MarshmallowValidator
):
    pass
