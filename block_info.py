class BlockInfo:
    def __init__(self, data, index, previous_hash, difficulty, max_difficulty, fee_per_tx):
        self.data = data
        self.index = index
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.max_difficulty = max_difficulty
        self.fee_per_tx = fee_per_tx
