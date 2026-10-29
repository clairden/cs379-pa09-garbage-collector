"""
PA 9: The Garbage Collector -- starter.

Complete GCHeap below. See the assignment, Part B,
for the full requirements.

Use gc_heap.py as specified in the assignment and imported by the harness.

Design note: GCHeap.allocate(obj) takes exactly one argument per the
spec, so an allocated object that references OTHER heap handles must
expose them itself for decref's cascade to find -- via a
get_child_handles() -> list[int] method. HeapNode below is a given
example object shaped this way, used by the cyclic-structure test.
"""

from typing import Any, List


class HeapNode:
    """
    Given: a minimal heap object whose fields may hold OTHER handles
    (ints). get_child_handles() is what GCHeap.decref's cascade calls
    to find them -- it must reflect the CURRENT field values, not a
    snapshot taken at creation time.
    """

    def __init__(self, **fields: Any) -> None:
        self.fields = fields

    def get_child_handles(self) -> List[int]:
        return [v for v in self.fields.values() if isinstance(v, int)]


class GCHeap:
    def __init__(self) -> None:
        # TODO: internal storage -- e.g. {handle: (obj, refcount)} -- and a handle counter.
        self.heap = {}
        self.next_handle = 1

    def allocate(self, obj: Any) -> int:
        """Store obj, return a new handle. Initial refcount is 1 (the creating reference)."""
        # TODO
        handle = self.next_handle 
        self.heap[handle] = (obj, 1) #set heap as object and initial refcount as 1
        self.next_handle += 1 #increment handle 
        return handle

    def incref(self, handle: int) -> None:
        # TODO
        obj, count = self.heap[handle] #unpack tuple to increase the count 
        count += 1 #increase count int
        self.heap[handle] = (obj, count) #update tuple dict with new count

    def decref(self, handle: int) -> None:
        """
        Decrement the refcount. When it hits 0: free the object, AND
        cascade-decref every handle returned by the freed object's
        get_child_handles() (if it has that method), recursively.
        """
        # TODO
        obj, count = self.heap[handle]
        count -= 1
        if count > 0:
            self.heap[handle] = (obj, count)
        else:
            del self.heap[handle] 

        if hasattr(obj, "get_child_handles"):
            for child_handle in obj.get_child_handles():
                self.decref(child_handle)

    def is_alive(self, handle: int) -> bool:
        # TODO
        if handle in self.heap:
            return True
        else:
            return False

    def live_count(self) -> int:
        """Number of currently-alive (refcount > 0) handles."""
        # TODO
        return len(self.heap)
