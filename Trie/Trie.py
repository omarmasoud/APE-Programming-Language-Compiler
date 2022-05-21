
keywords = [
        "new",
        "if",
        "else",
        "elseif",
        "return",
        "familyof",
        "inherit",
        "panic",
        "listen",
        "routine",
        "when",
        "break",
        "do",
        "within" ]

class TrieNode :
    def __init__(self,data:str) -> None:
        self.next = {}
        self.end = False
        self.data = data
    
    
class Trie:

    def __init__(self):
        self.head = TrieNode('')
        self.keywords = []
        self.addAll()

    def add(self,item:str):
        if item in self.keywords:
            return 
        pointer = self.head
        size = len(item) - 1
        item = item.lower()
        for index,char in enumerate(item):
            if char not in pointer.next:
                node = TrieNode(char)
                pointer.next[char] = node

            pointer = pointer.next[char]
          
        pointer.end = True
        self.keywords.append(item)
            
    def autoComplete(self,word:str):
        node = self.head
        res = []
        word = word.lower()
        for char in word:
            if char in node.next:
                node = node.next[char]
            else:
                return []
        self.DFS(res,node,word[:-1])
        return res

    def DFS(self,res:list,node,prefix:str):
        if node.end:
            res.append(prefix+node.data)
        for child in node.next.values():
            self.DFS(res,child,prefix+node.data)

    def addAll(self):
        for keyword in keywords:
            #print(keyword)
            self.add(keyword)

if __name__ == "__main__":
    x = "I"
    
    trie = Trie()
    print(trie.head.next)
    print(trie.autoComplete('List'))
    print(trie.autoComplete('R'))
    print(trie.autoComplete('els'))
    print(trie.autoComplete('whe'))

    
    