"""The `*Repo` abstract types which implement the "Repository" pattern."""

from __future__ import annotations

import abc
from typing import Generic, TypeVar

from eris import ErisResult


K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


class BasicRepo(Generic[K, V], abc.ABC):
    """The simplest possible Repository type."""

    @abc.abstractmethod
    def add(self, item: V, /, *, key: K = None) -> ErisResult[K]:
        """Add a new `item` to the repo and associsate it with `key`."""

    @abc.abstractmethod
    def get(self, key: K) -> ErisResult[V | None]:
        """Retrieve an item from the repo by key."""


class Repo(BasicRepo[K, V], Generic[K, V], abc.ABC):
    """A full-featured Repository

    Adds the ability to update and delete ontop of the BasicRepo type.
    """

    @abc.abstractmethod
    def remove(self, key: K) -> ErisResult[V | None]:
        """Remove an item from the repo by key."""

    @abc.abstractmethod
    def update(self, key: K, item: V, /) -> ErisResult[V]:
        """Update an item by key."""


class TaggedRepo(Repo[K, V], Generic[K, V, T], abc.ABC):
    """A Repository that is aware of some kind of "tags".

    Adds the ability to retrieve / delete a group of objects based off of some
    arbitrary "tag" type.

    NOTE: In general, K can be expected to be a primitive type, whereas T is
      often a custom user-defined type.
    """

    @abc.abstractmethod
    def get_by_tag(self, tag: T) -> ErisResult[list[V]]:
        """Retrieve a group of items that meet the given tag's criteria."""

    @abc.abstractmethod
    def remove_by_tag(self, tag: T) -> ErisResult[list[V]]:
        """Remove a group of items that meet the given tag's criteria."""
