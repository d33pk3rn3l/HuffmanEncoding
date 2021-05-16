import heapq

"""
HuffmanNode for a HuffmanTree. Implements a comparator for building a minheap (or sorted list) based in frequency.
Also implements a representer to pretty print to console when calling the object (for debugging).
"""
class HuffmanNode:
    def __init__(self, freq, char = None):
      #character
      self.char = char
      #frequency of given character in plaintext
      self.freq = freq
      #pointers to next nodes
      self.left = self.right = None
      
    #comparator for heapq  
    def __lt__(self, other):
      return self.freq < other.freq
      
    #so I can see the freqs and chars when printing these node-objects
    def __repr__(self):
      return str(self.char) + ": " + str(self.freq) 
    
    #traverse the tree and add 0 / 1 for left / right edges to build the encoding (translation) bitseqs for the code dict
    def build_translation(self, code):
      #when node is a leaf, yield the char from leaf and the built bitseq
      if self.left is None and self.right is None:
        yield(self.char, code) # using yield to avoid passing the dictionary
      #else traverse the tree in both directions
      else:
        #on left edge call transl and add "0"
        for i in self.left.build_translation(code + "0"):
          yield i
        #on right edge call transl and add "1"
        for i in self.right.build_translation(code + "1"):
          yield i

"""
HuffmanTree gets initialized based on plaintext by creating an object. It calculates all the necessary steps to create a HuffmanTree.
You then call encode() / decode() with the plaintext to encode / decode to bitsequences / plaintext. 

The special case where the input text consists of a repetition of a single character (such as "aaaaaa") is not covered.
Also the returned bitsequence is as a string and not in bits. 
"""

class HuffmanTree:
  
  def __init__(self, text):
    self.text = text
    #count freqs
    freqs = self.count_characters(text)
    #make heap
    heap = self.build_heap(freqs)
    #make tree
    heap = self.build_tree(heap)
    #set root node
    self.root = heap[0]
    #build encoding dictionary for tree
    self.build_dict()
    
  #if HuffmanTree-Object is called, just print the encoding dict
  def __repr__(self):
    return str(self.code)
      
  #Pass a string and count characters (all of them, also spaces, commas etc.), passes a dic with char and occurrences
  def count_characters(self, string):
    counter = {}
    for char in string:
      if char in counter:
        counter[char] += 1
      else:
        counter[char] = 1
    print("Counter: ", counter)
    return counter
  
  def build_tree(self, heap):
    while len(heap) > 1:
      smol = heapq.heappop(heap)
      tol = heapq.heappop(heap)
      #print(smol.freq() + tol.freq()) #me dumb f*ck was calling ints ^^
      new = HuffmanNode(smol.freq + tol.freq)
      new.left = smol
      new.right = tol
      heapq.heappush(heap, new)
    return heap
  
  def build_dict(self):
    self.code = {}
    for char, bits in self.root.build_translation(""):
      self.code[char] = bits
    return 0
  
  def build_heap(self, freqs):
    heap = []
    for char in freqs:
      heap.append(HuffmanNode(freqs[char], char))
    heapq.heapify(heap)
    print("Heap: ", heap)
    return heap
    
  def encode(self, string):
    encoded = ""
    for char in string:
      encoded += self.code[char]
    return encoded
  
  def decode(self, cipher):
    node = self.root
    string = ""
    for char in cipher:
      if char == "0":
        node = node.left
      else:
        node = node.right
      if node.char:
        #add to string
        string += node.char
        #start from root again for next char
        node = self.root
    return string
