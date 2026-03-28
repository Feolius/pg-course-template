from prompt_toolkit.validation import Validator, ValidationError


class PriceValidator(Validator):
    def validate(self, document):
        text = document.text.strip()
        if text:
            try:
                price = float(text)
                if price <= 0:
                    raise ValidationError(
                        message="Цена должна быть больше 0", cursor_position=len(text)
                    )
            except ValueError as e:
                raise ValidationError(
                    message="Введите число", cursor_position=len(text)
                ) from e


class NonEmptyValidator(Validator):
    def __init__(self, message="Поле не может быть пустым"):
        self.message = message

    def validate(self, document):
        text = document.text.strip()
        if not text:
            raise ValidationError(message=self.message, cursor_position=0)


class YesNoValidator(Validator):
    def validate(self, document):
        text = document.text.lower()
        if text not in ["y", "n", "yes", "no", "д", "н", "да", "нет"]:
            raise ValidationError(message="Введите y/n (yes/no)")
