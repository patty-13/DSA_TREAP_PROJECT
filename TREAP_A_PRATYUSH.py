from math import inf
import random

# Treap_Node defination
class Treap_Node:
  def __init__(self, key_value, priority = None):
    self.key_value = key_value
    self.left = None
    self.right = None
    self.priority = priority if priority is not None else random.randint(50, 200)


# Treap Class
class _Treap_:
  
  # Right rotation to balance the tree
  def right_rotate(self, y):
    x = y.left
    temp = x.right
    # y.left = x.right
    x.right = y
    y.left = temp
    return x

  # Left rotation to balance the tree
  def left_rotate(self, x):
    y = x.right
    temp = y.left

    # x.right = y.left
    y.left = x
    x.right = temp
    return y

# RESTRUCTER the nodes
  def _rotation_(self, node):
    if (node == None):
      return None

    # checking if the priority of left is less than root priority then right rotate
    if node.left and node.left.priority > node.priority:
      node = self.right_rotate(node)

    # checking if the priority of right is less than root priority then left rotate
    elif node.right and node.right.priority > node.priority:
      node = self.left_rotate(node)

    return node

# INSERT Function
  def insert(self, node, key_value, priority = None):

    # check if it is integer
    key_value = int(key_value) if isinstance(key_value, str) and key_value.isdigit() else key_value
    # if node is none, create a new node with key_value and priority
    # if priority is not defined by user it takes random value from (1, 100000)
    if (node == None):
      return Treap_Node(key_value, priority)

    # if the key value already exists, we return node with updated priority
    if (key_value == node.key_value):
      if(priority != None):
        node.priority = priority
      else:
        node.priority = random.randint(50, 200)
      node = self._rotation_(node)
      return node

    # if new value is less than node value
    if (key_value <= node.key_value):
       node.left = self.insert( node.left, key_value, priority)

    # if new value is more than node value
    else:
      node.right = self.insert( node.right, key_value, priority)

    # return the rotation if imbalanced after addition of new value
    node = self._rotation_(node)
    return node

  
# REMOVE FUNCTION
  def remove(self, node, key_value):
    # node is none return none
    if node is None:
        return None, None

    # setting delete priority as none
    del_priority = None

    # if key value is less than root node then traverse left tree
    if (key_value < node.key_value):
      node.left, deleted_priority = self.remove(node.left, key_value)
    # if key value is greater than root node then traverse right tree
    elif (key_value > node.key_value):
        node.right, deleted_priority = self.remove(node.right, key_value)
    else:

      del_priority = node.priority
      # if left node is none return right node
      if (node.left == None):
        return node.right, del_priority
      
      # if right node is none return left node
      elif (node.right == None):
        return node.left, del_priority
      
      # rotation to keep it balanced
      elif(node.left.priority < node.right.priority):
        node = self.right_rotate(node)
        node.right, _ = self.remove(node.right, key_value)
      else:
        node = self.left_rotate(node)
        node.left, _ = self.remove(node.left, key_value)

    if (node != None):
      node = self._rotation_(node)
    return node, del_priority


# FIND Function

  def find(self, node, key_value):

    # if node value is None or null then return error
    if (node == None):
      return 0

    # if node value is key_value itself return node
    if (node.key_value == key_value):
      return node.priority

    # if node value is > key_value traverse left subtree else right subtree
    if (node.key_value > key_value):
      return self.find(node.left, key_value)
    else:
      return self.find(node.right, key_value)

# SPLIT Function
  def split(self, node, key_value):
    if (node == None):
      return None, None

    # checking if the current split key is less the current node.key_value
    if (key_value < node.key_value):
      left, node.left = self.split(node.left, key_value)
      return left, node
    else:
      node.right, right = self.split(node.right, key_value)
      return node, right

# JOIN Function
  def join(self, left, right):

    if (left == None or right == None):
      if(left == None):
        return right
      else:
        return left

    if(left.priority > right.priority):
      left.right = self.join(left.right, right)
      return left
    else:
      right.left = self.join(left, right.left)
      return right


# SIZE Function
  def size(self, node):
    if (node == None):
      return 0
    else:
      return 1 + self.size(node.left) + self.size(node.right)

# DISPLAY FUNCTION
  def display(self, node, depth=0):
    if node is not None:
      self.display(node.left, depth + 1)
      print(" " * 4 * depth + f"{node.key_value}({node.priority})")
      self.display(node.right, depth + 1)


# PART-1 IMPLEMENTATION
if __name__ == '__main__':
  treap = _Treap_()
  root = None
  while(True):
    print("1.-- insertWithPriority, 2.-- insertWithRandom, 3.-- remove, 4.-- find, 5.-- split, 6.-- join, 7.-- Display, 8.-- Exit")
    choice = input('Enter Operation ')

    # INSERT WITH PRIORITY
    if(choice == '1'):
      key_priority = input("Enter key and priority: ")
      key, priority = key_priority.split(" ")
      root = treap.insert(root, key, priority)
      treap_size = treap.size(root)
      print(f"Printing treap of size: {treap_size}")
      print("\n")
      treap.display(root)
      print("\n")

    # INSERT RANDOMLY
    elif (choice == '2'):
      key = input("Enter key: ")
      root = treap.insert(root, key, None)
      treap_size = treap.size(root)
      print(f"Printing treap of size: {treap_size}")
      print("\n")
      treap.display(root)
      print("\n")

    # REMOVE
    elif (choice == '3'):
      del_key = input("Enter key to remove: ")
      root, deleted_priority = treap.remove(root, del_key)
      if(deleted_priority == None):
        print(f"Removed {del_key} not found in treap")
      else:
        print(f"Removed key: {del_key}, priority value: {deleted_priority}")
      treap_size = treap.size(root)
      print(f"Printing treap of size: {treap_size}")
      print("\n")
      treap.display(root)
      print("\n")
    
      # FIND
    elif (choice == '4'):
      find_key = input("Enter key to find")
      priority_found = treap.find(root, find_key)
      if(priority_found == 0):
        print(f"Key {find_key} not exists")
      else:
        print(f"key: {find_key}, priority: {priority_found} found")
      treap_size = treap.size(root)
      print(f"Printing treap of size: {treap_size}") 
      print("\n")
      treap.display(root)
      print("\n")

    #SPLIT
    elif (choice == '5'):
      split_key = input("Enter split key: ")
      print("\n")
      left_side, right_side = treap.split(root, split_key)
      print("Left split: ")
      left_size = treap.size(left_side)
      print(f"Printing treap of size: {left_size}")
      treap.display(left_side)

      print("\nRight split: ")
      print("\n")
      right_size = treap.size(right_side)
      print(f"Printing treap of size: {right_size}")
      treap.display(right_side)
      print("\n")

    # JOIN
    elif (choice == '6'):
      root = treap.join(left_side, right_side)
      print("After join:")
      treap_size = treap.size(root)
      print(f"Printing treap of size: {treap_size}")
      print("\n")
      treap.display(root)
      print("\n")

    # DISPLAY
    elif(choice == '7'):
      treap.display(root)
    
    # EXIT
    elif (choice == '8'):
      break
    else:
      print("Invalid choice")