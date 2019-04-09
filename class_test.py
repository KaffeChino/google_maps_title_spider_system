class stack:
    """A list-based stack implementation."""

    def __init__(self, x_small, x_large, y_small, y_large, zoom):
        """
        _items is a list.
        _size is length of the list.
        You may ask, why not use list(_items)?
        No. In fact, I'm using space exchaging time.
        """
        self._items = []
        self._size = 0

        for i in range(x_small, x_large + 1):
            for j in range(y_small, y_large + 1):
                self.push(i, j, zoom)

    def isEmpty(self):
        """
        Check whether the stack is Empty.
        YOU MUST CHECK IT BEFORE YOU USE POP METHOD.
        DON'T FORGET! OR YOU MAY GET A KEYERROR!
        """
        # if len(self) == 0:
        if self._size == 0:
            return True
        else:
            return False

    def __len__(self):
        """
        Return the length of the stack.
        """
        return self._size

    def push(self, x, y, z):
        """
        Inserts items at top the stack
        -- and in fact that is the end of the list.
        """
        self._items.append([x, y, z])
        self._size += 1

    def pop(self):
        """
        Removes and returns the item at top the stack.
        New item append at the end of the list,
        when use pop method, it will return the end as the same.
        so I used list.pop().
        It will return the last item of the list and delete it.
        """
        if self.isEmpty():
            raise KeyError
        x, y, z = self._items.pop()
        self._size -= 1
        print(x, y, z)

    def peek(self):
        """
        This method seems no use,
        x, y will be transferd by spider_system when save images.
        but I defined it. May be used one day ^_^
        """
        if self.isEmpty():
            raise KeyError
        x, y, z = self._items[len(self) - 1]
        return x, y, z


def main():
    stack_test = stack(1, 3, 3, 10, 0)
    while stack_test.isEmpty() is False:
        stack_test.pop()


main()
