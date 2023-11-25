from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class CombinableListOperation(Generic[T]):
    def __init__(
        self,
        *,
        operation: Callable[[list[T]], list[T]],
        display_name: str | None = None,
    ):
        self._operation = operation

        self.display_name = (
            display_name if display_name is not None else operation.__name__
        )

    def __call__(self, tracks: list[T]) -> list[T]:
        return self._operation(tracks)

    def __and__(self, other: "CombinableListOperation") -> "CombinableListOperation":
        def chained_operation(tracks: list[T]) -> list[T]:
            return other(self(tracks))

        return type(self)(
            operation=chained_operation,
            display_name=f"{self.display_name} & {other.display_name}",
        )

    def __or__(self, other: "CombinableListOperation") -> "CombinableListOperation":
        def union(tracks: list[T]) -> list[T]:
            return list(set(self(tracks)) | set(other(tracks)))

        return type(self)(
            operation=union,
            display_name=f"({self.display_name} | {other.display_name})",
        )

    def __str__(self) -> str:
        return self.display_name


def combinable(func: Callable[[list[T]], list[T]]) -> CombinableListOperation[T]:
    return CombinableListOperation(operation=func)
