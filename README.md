# Handle-duplicate-keys

Modify our implementation of the `BinarySearchTree` class so that it handles duplicate keys properly. That is, if a key is already in the tree then the new payload should replace the old rather than add another node with the same key.

Remember, one earlier example in class (the "Binary Search and AVL Trees" notebook), we attempted this on `wt`, which was a word tree we constructed. We could not update the definition of an already existing word:

```
>>> wt["abeam"]
'No definition available'
>>> wt["abeam"] = "A bright headlight"
>>> wt["abeam"]
'No definition available'
```
