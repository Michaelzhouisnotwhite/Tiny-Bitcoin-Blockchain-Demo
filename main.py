from blockchain import Chain, Block
from merkle_tree import *
from colorprt.default import success


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


def main():
    chain = Chain(20)  # difficulty is xx bits
    print_blocks(chain.blocks[0], is_first=True)
    tg1 = [Transaction('', 'A', 100)]
    tg2 = [Transaction('A', 'B', 100), Transaction('B', 'A', 25), Transaction('B', 'B', 75)]
    tg3 = [Transaction('B', 'C', 15), Transaction('B', 'B', 60)]
    tgs = [MerkleTree(tg1), MerkleTree(tg2), MerkleTree(tg3)]

    for i, tg in enumerate(tgs):
        data = tg
        chain.add_to_pool(data)
        chain.mine()
        # if i % 5 == 0:
        print_blocks(chain.blocks[i + 1], is_first=True)


if __name__ == "__main__":
    main()
