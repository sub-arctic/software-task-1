from typing import Iterator

from rigidbody import RigidBody

type ObjectsMap = dict[int, RigidBody]


class Bodies:
    """Manages a collection of RigidBody objects with unique IDs.

    Used in Engine to allow more effective pairing of canvas IDs and
    RigidBodies.

    Attributes:
        objects: A dictionary mapping of IDs to RigidBody objects.
        next_id: The next available ID for a new RigidBody.
        iter_index: An index for dereferencing the objects for iteration.
    """

    def __init__(self):
        """Initializes an empty Bodies collection."""
        self._objects: ObjectsMap = {}
        self._next_id: int = 0
        self._iter_index: int = 0

    @property
    def objects(self) -> ObjectsMap:
        """Gets the dictionary of RigidBody objects."""
        return self._objects

    def add(self, new_body: RigidBody, id: int | None = None) -> int:
        """Adds a new RigidBody to the collection.

        If no ID is provided, a new unique ID is generated.
        Typically a provided canvas ID would be provided to allow
        analogous canvas and engine objects.

        Args:
            new_body: The RigidBody to add.
            id: The ID to assign to the new RigidBody.
                If it is none next_id is assigned and
                then incremented.

        Returns:
            The ID assigned to the new RigidBody.
        """
        if id is None:
            id = self.next_id
            self.next_id = 1
        self.objects[id] = new_body
        return id

    @property
    def next_id(self) -> int:
        """Gets the next available ID for a new RigidBody."""
        return self._next_id

    @next_id.setter
    def next_id(self, increment: int = 1) -> int:
        """Sets the next available ID for a new RigidBody.

        Args:
            increment: The amount to increment the next ID by.

        Returns:
            The new next ID after incrementing.
        """
        new_id = self.next_id + increment
        self._next_id = new_id
        return new_id

    def __iter__(self) -> Iterator:
        """Initializes the iterator for the Bodies collection."""
        self._iter_index = 0
        self._keys = list(self.objects.keys())
        return self

    def __next__(self) -> tuple[int, RigidBody]:
        """Returns the next (ID, RigidBody) pair in the iteration.

        Raises:
            StopIteration: If there are no more items to iterate over.

        Returns:
            The next ID and corresponding RigidBody as a tuple.
        """
        if self._iter_index < len(self._keys):
            key = self._keys[self._iter_index]
            self._iter_index += 1
            return key, self.objects[key]
        else:
            raise StopIteration

    def __getitem__(self, index: int) -> RigidBody:
        """Gets the RigidBody at the specified index.

        Args:
            index: The index of the RigidBody to retrieve.

        Returns:
            The RigidBody at the specified index.
        """
        items = list(self.objects.items())
        return items[index][1]

    def __len__(self) -> int:
        """Returns the number of RigidBody objects in the collection."""
        return len(self.objects)

    def delete(self, id: int) -> None:
        """Deletes a RigidBody from the collection by its ID.

        Args:
            id: The ID of the RigidBody to delete.
        """
        if id in self.objects:
            del self.objects[id]

    def get(self, id: int) -> RigidBody | None:
        """Gets a RigidBody by its ID.

        Args:
            id: The ID of the RigidBody to retrieve.

        Returns:
            The RigidBody if found, otherwise None.
        """
        return self.objects.get(id)

    def items(self):
        """Returns an iterator over the (ID, RigidBody)
            pairs in the collection.

        Returns:
            An iterator of (ID, RigidBody) pairs.
        """
        return self.objects.items()
