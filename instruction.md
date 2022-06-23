# code running instructinos

使用Transaction类来定义交易的信息

example:`Transaction('A', 'B', 100)`表示A向B发送了100个币。

将同一时间产生的相关交易放入列表中，形成交易链。例如A有100，A向B购买一个价值50的物品，则需要这么使用：

```python
tg = [Transaction('A', 'B', 100), Transaction('A', 'A', 50)]
```

多个交易链需要经过默克尔树进行压缩，将交易列表放入MerkleTree中，将所有的默克尔根放入列表中模拟交易池，如下：

```python
tgs = [MerkleTree(tg1), MerkleTree(tg2), MerkleTree(tg3)]
```

使用Chain类来模拟产生区块和上链的过程，Chain中输入区块的工作量，如下：

```python
chain = Chain(20) # 代表这个区块链是20个比特的工作量

for i, tg in enumerate(tgs):
    data = tg
    chain.add_to_pool(data)
    chain.mine()
    print_blocks(chain.blocks[i + 1], is_first=False)
```

print_blocks函数是输出区块的信息，定义如下：

```python
def print_blocks(block: Block, is_first=False):
    print("Nonce:", block.nonce)
    print("Prev:", block.previous_hash.hexdigest())
    print("Hash:", block.hash.hexdigest())
    print("Data:", block.data)
    if not is_first:
        success("-----------------------------------")
        block.data.printTree()
        success("------------------------------------")
        
    print("")
```

![image-20220623194332174](C:\Users\michael\Pictures\typora-copy-image\image-20220623194332174.png)
