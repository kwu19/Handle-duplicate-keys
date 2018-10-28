#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 17:32:35 2018

@author: kefei
"""

class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0
        
    def length(self):
        return self.size
    
    def __len__(self):
        return self.length()
    
    def __iter__(self):
        return self.root.__iter__()
    
    def put(self, key, val):
        if self.root:
            self.__put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
            
        self.size += 1
   
    def __put(self, key, val, current_node):
        """BinarySearchTree class handles duplicate keys properly. 
        That is, if a key is already in the tree then the new payload should replace the old 
        rather than add another node with the same key."""
        #print("Called from BinarySearchTree class")
        if key == current_node.key:  # check if a key is already in the tree
            current_node.payload = val  # replace previous value
            
        elif key < current_node.key:        
            if current_node.has_left_child():
                self.__put(key, val, current_node.left_child)
            else:
                current_node.left_child = TreeNode(key, val, parent=current_node)  # base case 
        else: # key is >= than current_node.key
            if current_node.has_right_child():
                self.__put(key, val, current_node.right_child)
            else:
                current_node.right_child = TreeNode(key, val, parent=current_node)  # base case
                
    def __setitem__(self, k, v):
        self.put(k, v)
        
    def get(self, key):
        if self.root:
            res = self.__get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None
        
    def __get(self, key, current_node):
        if not current_node:
            return None
        elif current_node.key == key:
            return current_node
        elif key < current_node.key:
            return self.__get(key, current_node.left_child)
        else:
            return self.__get(key, current_node.right_child)
        
    def __getitem__(self, key):
        return self.get(key)
    
    
    def __contains__(self, key):
        if self.__get(key, self.root):
            return True
        else:
            return False
        
        #return bool(self.__get(key, self.root))
        #return True if self.__get(key, self.root) else False
        
    def delete(self, key):
        if self.size > 1:
            node_to_remove = self.__get(key, self.root)
            if node_to_remove:
                self.remove(node_to_remove)  # TODO: 'remove' needs to be defined!
                self.size -= 1
            else:
                raise KeyError('Key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -=1
        else:
            raise KeyError('Key not in tree')
            
    def __delitem__(self, key):
        self.delete(key)
        
    def splice_out(self):
        if self.is_leaf():
            if self.is_left_child():
                self.parent.left_child = None
            else:
                self.parent_right_child = None
        elif self.has_any_children():
            
            if self.has_left_child():
                if self.is_left_child():
                    self.parent.left_child = self.left_child
                else:
                    self.parent_right_child = self.left_child
                    
                self.left_child.parent = self.parent
            else:
                if self.is_left_child():
                    self.parent.left_child = self.right_child
                else:
                    self.parent.right_child = self.right_child
                    
                self.right_child.parent = self.parent
                
                
    def find_successor(self):
        succ = None
        if self.has_right_child():
            succ = self.right_child.find_min()
        else:
            if self.parent:
                if self.is_left_child():
                    succ = self.parent
                else:
                    self.parent.right_child = None
                    succ = self.parent.find_successor()
                    self.parent.right_child = self
                    
        return succ
    
    def find_min(self):
        current = self
        
        while current.has_left_child():
            current = current.left_child
            
        return current
    
    
    def remove(self, current_node):
        if current_node.is_leaf():  # leaf
            if current_node == current_node.parent.left_child:
                current_node.parent.left_child = None
            else:
                current_node.parent.right_child = None
        elif current_node.has_both_children():  # interior
            succ = current_node.find_successor()
            succ.splice_out()
            current_node.key = succ.key
            current_node.payload = succ.payload

        else:  # this node has one child
            if current_node.has_left_child():
                if current_node.is_left_child():
                    current_node.left_child.parent = current_node.parent
                    current_node.parent.left_child = current_node.left_child
                elif current_node.is_right_child():
                    current_node.left_child.parent = current_node.parent
                    current_node.parent.right_child = current_node.left_child
                else:
                    current_node.replace_node_data(current_node.left_child.key,
                                                   current_node.left_child.payload,
                                                   current_node.left_child.left_child,
                                                   current_node.left_child.right_child)
            else:
                if current_node.is_left_child():
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.left_child = current_node.right_child
                elif current_node.is_right_child():
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.right_child = current_node.right_child
                else:
                    current_node.replace_node_data(current_node.right_child.key,
                                                   current_node.right_child.payload,
                                                   current_node.right_child.left_child,
                                                   current_node.right_child.right_child)
                    
class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.left_child = left
        self.right_child = right
        self.parent = parent
        
    def has_left_child(self):
        return self.left_child
    
    def has_right_child(self):
        return self.right_child
    
    def is_left_child(self):
        return self.parent and self.parent.left_child == self
    
    def is_right_child(self):
        return self.parent and self.parent.right_child == self

    def is_root(self):
        return not self.parent
    
    def is_leaf(self):
        return not (self.right_child or self.left_child)
    
    def has_any_children(self):
        return self.right_child or self.left_child
    
    def has_both_children(self):
        return self.right_child and self.left_child
        
    def replace_node_data(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.left_child = lc
        self.right_child = rc
        
        if self.has_left_child():
            self.left_child.parent = self
            
        if self.has_right_child():
            self.right_child.parent = self
            
    def __iter__(self):
        # inorder traversal of (sub-)tree
        # left children, root (self), right children
        if self:
            if self.has_left_child():
                for elem in self.left_child:
                    yield elem
                    
            yield self.key
            
            if self.has_right_child():
                for elem in self.right_child:
                    yield elem
                    
# Test out the BinarySearchTree class to show it works as advertised.
wt = BinarySearchTree()
wt["abeam"] = "None"
wt["abeam"]

wt["abeam"] = "A bright headlight"
wt["abeam"]