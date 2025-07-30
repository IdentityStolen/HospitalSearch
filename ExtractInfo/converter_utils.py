from abc import ABC, abstractmethod
from typing import Optional, Any


TASK_QUEUE = "conversion-queue"


class Converter(ABC):
    def __init__(self, value: Any = None):
        self.value = value

    @abstractmethod
    def convert(self):
        raise NotImplementedError("Subclasses should implement this method.")


class StringConverter(Converter):

    def convert(self) -> str:
        return self.value.strip()


class IntConverter(Converter):
    def __init__(self, value: Optional[str], base=32):
        super().__init__(value)
        self.base = base
        self.upper_bound = 2**self.base - 1
        self.lower_bound = -(2**self.base)

    def convert(self) -> Optional[int]:
        try:
            if isinstance(self.value, str):
                int_value = int(StringConverter(self.value).convert())
                self.value = int_value

            if self.value is None or self.value == "":
                return None

            return (
                self.value
                if self.lower_bound <= self.value <= self.upper_bound
                else None
            )
        except ValueError:
            raise ValueError(f"Cannot convert '{self.value}' to int.")


class Int64Converter(IntConverter):
    def __init__(self, value: Optional[str]):
        super().__init__(value, base=64)

    def convert(self) -> Optional[int]:
        return super().convert()


class FloatConverter(Converter):

    def convert(self) -> Optional[float]:
        if self.value is None:
            return None

        try:
            return float(self.value.strip())
        except ValueError:
            raise ValueError(f"Cannot convert '{self.value}' to float.")


class PhoneConverter(Converter):

    def convert(self) -> Optional[str]:
        if self.value is None:
            return None

        str_val = StringConverter(self.value).convert()
        cleaned_value = "".join(filter(str.isdigit, str_val))

        if not cleaned_value:
            return None

        if len(cleaned_value) == 10:
            return f"+1 {cleaned_value[:3]}-{cleaned_value[3:6]}-{cleaned_value[6:]}"

        if len(cleaned_value) > 10:
            return f"+{cleaned_value[:len(cleaned_value)-10]} {cleaned_value[-10:-7]}-{cleaned_value[-7:-4]}-{cleaned_value[-4:]}"

        raise ValueError(f"Invalid phone number format: '{self.value}'")


class EmailConverter(Converter):

    def convert(self) -> Optional[str]:
        if self.value is None:
            return None

        cleaned_value = StringConverter(self.value).convert()

        email_parts = cleaned_value.split("@")
        if len(email_parts) != 2:
            raise ValueError(f"Invalid email format: '{self.value}'")

        local_part, domain_part = email_parts

        if "." in domain_part:
            domain_parts = domain_part.split(".")
            if (
                all(part.isalnum() or part == "-" for part in domain_parts)
                and len(domain_parts) >= 2
            ):
                return cleaned_value
            else:
                raise ValueError(f"Invalid email domain format: '{self.value}'")
        else:
            raise ValueError(f"Invalid email format: '{self.value}'")


class WebsiteConverter(Converter):

    def convert(self) -> Optional[str]:
        if self.value is None:
            return None

        cleaned_value = StringConverter(self.value).convert()

        if cleaned_value.startswith("http://") or cleaned_value.startswith("https://"):
            return cleaned_value
        else:
            raise ValueError(f"Invalid website format: '{self.value}'")


class TimezoneConverter(Converter):

    ALLOWED_TIMEZONES = {"UTC", "EST", "EDT", "CST", "CDT", "MST", "MDT", "PST", "PDT"}

    def convert(self) -> Optional[str]:
        if self.value is None:
            return None

        cleaned_value = StringConverter(self.value).convert()

        if cleaned_value in self.ALLOWED_TIMEZONES:
            return cleaned_value
        else:
            raise ValueError(f"Invalid timezone format: '{self.value}'")


class NotNullConverter(Converter):
    def convert(self) -> Any:
        if isinstance(self.value, Converter):
            ret = self.value.convert()
            if ret is None:
                raise ValueError(f"Value cannot be None: {self.value}")

            return ret

        if self.value is None:
            raise ValueError(f"Value cannot be None: {self.value}")

        return self.value
