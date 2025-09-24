def word_exists(board, word):
    if not board or not word: return False
    m, n = len(board), len(board[0])
    def dfs(i, j, k, visited):
        if k == len(word): return True
        if i < 0 or i >= m or j < 0 or j >= n or (i,j) in visited or board[i][j] != word[k]: return False
        visited.add((i,j))
        found = any(dfs(i+di, j+dj, k+1, visited) for di, dj in [(-1,0),(1,0),(0,-1),(0,1)])
        visited.remove((i,j))
        return found
    return any(dfs(i, j, 0, set()) for i in range(m) for j in range(n) if board[i][j] == word[0])

board1 = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
print(word_exists(board1, "ABCCED"))  
print(word_exists(board1, "ABCB"))    