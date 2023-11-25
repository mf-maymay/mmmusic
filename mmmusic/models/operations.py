from functools import update_wrapper
from typing import Callable, Generic, TypeVar, overload

T = TypeVar("T")

ListOperation = Callable[[list[T]], list[T]]


class CombinableListOperation(Generic[T]):
    def __init__(
        self,
        *,
        operation: ListOperation[T],
        display_name: str | None = None,
    ):
        self._operation = operation

        update_wrapper(self, self._operation)

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


@overload
def combinable(
    func: ListOperation[T], *, display_name: str | None = None
) -> CombinableListOperation[T]:
    ...


@overload
def combinable(
    func: None, *, display_name: str | None = None
) -> Callable[[ListOperation[T]], CombinableListOperation[T]]:
    ...


def combinable(
    func: ListOperation[T] | None = None,
    *,
    display_name: str | None = None,
) -> (
    CombinableListOperation[T]
    | Callable[[ListOperation[T]], CombinableListOperation[T]]
):
    if func is not None:
        return CombinableListOperation(operation=func, display_name=display_name)

    def decorator(func: ListOperation) -> CombinableListOperation[T]:
        return CombinableListOperation(operation=func, display_name=display_name)

    return decorator
