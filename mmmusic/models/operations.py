from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class CombinableListOperation(Generic[T]):
    def __init__(self, *, operation: Callable[[list[T]], list[T]]):
        self._operation = operation

    def __call__(self, tracks: list[T]) -> list[T]:
        return self._operation(tracks)

    def __and__(self, other: "CombinableListOperation") -> "CombinableListOperation":
        def chained_operation(tracks: list[T]) -> list[T]:
            return other(self(tracks))

        return type(self)(operation=chained_operation)

    def __or__(self, other: "CombinableListOperation") -> "CombinableListOperation":
        def union(tracks: list[T]) -> list[T]:
            return list(set(self(tracks)) | set(other(tracks)))

        return type(self)(operation=union)


def combinable(func: Callable[[list[T]], list[T]]) -> CombinableListOperation[T]:
    return CombinableListOperation(operation=func)
