from pydantic import ConfigDict


class DefaultConfig:
    config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )
