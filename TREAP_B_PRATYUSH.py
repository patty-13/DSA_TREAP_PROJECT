from math import inf
import random
import time

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


# PART-B IMPLEMENTATION performance analysis

class MeasureTime:
  def __init__(self):
    self.startTime = 0
    self.cumulativeTime = 0
    self.stopTime = 0
    self.started = False

  def start(self):

    if not self.started:
      self.startTime = time.time_ns()
      self.started = True
    
  def stop(self):
    if self.started:
      self.stopTime  = time.time_ns()
      self.cumulativeTime += (self.stopTime - self.startTime)
      self.startTime = self.stopTime = 0
      self.started = False
  
  def reset(self):
    self.cumulativeTime = 0
    self.started = False

  def cumulative_Time(self):
    return self.cumulativeTime

# Function to populate the tree
def populate(treap, root,input_size, keys):
  for i in range(treap.size(root), input_size):
    root = treap.insert(root, keys[i])
  print(f"Treap populated to size: {treap.size(root)}") 

# Function to define successful keys
def key_for_successful_find(sorted_key_arr, sample_size):
  return random.sample(sorted_key_arr, sample_size)

# Function to define unsucessful keys
def keys_for_unsuccessful_find(sorted_key_arr, sample_size):

  lst = []
  while ( len(lst) <= sample_size):
    idx = random.randint(0, len(sorted_key_arr))
    if (idx == len(sorted_key_arr)):
      key = sorted_key_arr[-1] + 1
    else:
      key = sorted_key_arr[idx] -1
    
    if key not in lst:
      lst.append(key)
  return lst

# Disaply function for performance stats table
def performance_stats(cum_times, operation_names, input_size):
  operations = ["Insert", "Delete", "Find", "Split", "Join"]
  print(f"{'Operation':<10} | " + " | ".join([f"{size:<8}" for size in INPUT_SIZE]))
  print("-" * 10 + "+" + "-" * (9 * len(INPUT_SIZE) + len(INPUT_SIZE) - 1))
  for i, operation in enumerate(operations):
    times = [f"{cum_times[i][j]:<5.3f}" for j in range(len(INPUT_SIZE))]
    print(f"{operation:<10} | " + " | ".join(times))

# Function to measure time for find, insert, split, join, delete 
def measure_performance(treap, root, keys, input_size, NUM_TRIALS, cum_times):
  timer = MeasureTime()
  timer1 = MeasureTime()
  operation_names = ["Insert", "Delete","Find","Split","Join"]
  for i, size in enumerate(input_size):
    root = populate(treap, root, size, keys)
    start_idx = input_size[i - 1] if i > 0 else 0
    end_idx = size
    sub_arr = sorted(keys[start_idx : end_idx])
    successful_keys = key_for_successful_find(sub_arr, NUM_TRIALS)
    unsuccessful_keys = keys_for_unsuccessful_find(sub_arr, NUM_TRIALS)
    
    # FIND for successful keys
    timer.reset()
    for key in successful_keys:
      timer.start()
      treap.find(root,key)
      timer.stop()
    # avg of find on successful keys
    cum_times[2][i] += timer.cumulative_Time() / (2* NUM_TRIALS)
    
    # FIND for unsccessful keys
    timer.reset()
    for key in unsuccessful_keys:
      timer.start()
      treap.find(root,key)
      timer.stop()
    # avg of find on unsccessful keys
    cum_times[2][i] += timer.cumulative_Time() / (2* NUM_TRIALS)
    # avg of both successful and unsucessful keys
    cum_times[2][i] /= 2

    # SPLIT for success keys
    timer.reset()
    split_keys = successful_keys
    for key in split_keys:
      timer.start()
      left, right = treap.split(root,key)
      timer.stop()
    # JOIN for success keys
      timer1.start()
      treap.join(left, right)
      timer1.stop()
    # avg of split for success keys & join for sucess for keys
    cum_times[3][i] += timer.cumulative_Time()/ (2*NUM_TRIALS)
    cum_times[4][i] += timer1.cumulative_Time() / (2*NUM_TRIALS)

  # SPLIT for unsucess keys
    timer.reset()
    un_split_keys = unsuccessful_keys
    for key in un_split_keys:
      timer.start()
      left, right = treap.split(root, key)
      timer.stop()
  # JOIN for unsucess keys 
      timer1.start()
      treap.join(left, right)
      timer1.stop()
    # avg for split for unsucess keys
    cum_times[3][i] += timer.cumulative_Time() / (2*NUM_TRIALS)
    cum_times[4][i] += timer1.cumulative_Time() / (2*NUM_TRIALS)
    # avg for split sucess and unsucess keys
    cum_times[3][i] /= 2
    # avg for join sucess and unsucess keys
    cum_times[4][i] /= 2

# INSERT and REMOVE Keys
    timer.reset()
    for key in keys[size:size + NUM_TRIALS]:
      timer.start()
      # insert for keys
      root = treap.insert(root,key)
      timer.stop()
      timer1.start()
      # remove for keys
      root,_ = treap.remove(root,key)
      timer1.stop()
    cum_times[0][i] = timer.cumulative_Time() / (2*NUM_TRIALS)
    cum_times[1][i] = timer1.cumulative_Time() / (2*NUM_TRIALS)

  performance_stats(cum_times, operation_names, input_size)

# DRIVER FUNCTION
if __name__ == '__main__':
  treap = _Treap_()
  INPUT_SIZE = [5000, 10000, 15000, 20000, 30000]
  NUM_TRIALS = 1000
  cum_times = [[0 for _ in range(len(INPUT_SIZE))] for _ in range(5)]
  key_size = INPUT_SIZE[-1] + NUM_TRIALS
  key = [2*i for i in range(key_size)]  
  random.shuffle(key)
  keys = key[:]
  root = None
  measure_performance(treap, root, keys, INPUT_SIZE, NUM_TRIALS, cum_times)
  