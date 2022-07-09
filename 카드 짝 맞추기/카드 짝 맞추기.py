import itertools
from collections import deque

INF = int(1e9)

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

def ctrl(graph, y, x, dy, dx):
    for i in range(1, 5):
        ny = y + dy * i
        nx = x + dx * i
        # 카드를 맞닥뜨리는 경우 정지
        if 0 <= ny < 4 and 0 <= nx < 4 and graph[ny][nx] != 0:
            return ny, nx
        # 카드가 벽에 부딪힌 경우 정지
        if 4 <= ny or ny < 0 or 4 <= nx or nx < 0:
            return ny - dy, nx - dx


def bfs(graph, y, x):
    q = deque()
    distance = [[INF for _ in range(4)] for _ in range(4)]
    distance[y][x] = 0

    visited = [[False for _ in range(4)] for _ in range(4)]
    
    q.append((0, y, x))
    visited[y][x] = True

    while q:
        dist, y, x = q.popleft()
        for i in range(4):
            ny = y + dy[i]
            nx = x + dx[i]
            if 0 <= ny < 4 and 0 <= nx < 4 and not visited[ny][nx]:
                # 상, 하, 좌, 우 1칸 씩 움직일 경우
                q.append((dist + 1, ny, nx))
                visited[ny][nx] = True
                distance[ny][nx] = dist + 1
                # Ctrl + 방향키를 사용한 경우
            ny, nx = ctrl(graph, y, x, dy[i], dx[i])
            if not visited[ny][nx]:
                q.append((dist + 1, ny, nx))
                visited[ny][nx] = True
                distance[ny][nx] = dist + 1

    return distance


def get_dist(graph, location, r, c, dist):
    # 첫번째 그림 -> 두번째 그림
    distance = bfs(graph, r, c)
    y, x = location[0][0], location[0][1]
    dist_first = dist + distance[y][x]
    graph[y][x] = 0
    distance = bfs(graph, y, x)
    y, x = location[1][0], location[1][1]
    dist_first = dist_first + distance[y][x]
    y, x = location[0][0], location[0][1]
    graph[y][x] = location[0][2]

    # 두번째 그림 -> 첫번째 그림
    distance = bfs(graph, r, c)
    y, x = location[1][0], location[1][1]
    dist_second = dist + distance[y][x]
    graph[y][x] = 0
    distance = bfs(graph, y, x)
    y, x = location[0][0], location[0][1]
    dist_second = dist_second + distance[y][x]
    y, x = location[1][0], location[1][1]
    graph[y][x] = location[0][2]

    return dist_first, dist_second


def get_dists(graph, locations, d, r, c):

    for i in range(len(locations)):
        location = locations[i]
        if i == 0:
            dist_first, dist_second = get_dist(graph, location, r, c, 0)
            y, x = location[0][0], location[0][1]
            graph[y][x] = 0
            d[y][x] = dist_second
            y, x = location[1][0], location[1][1]
            graph[y][x] = 0
            d[y][x] = dist_first
        else:
            start = locations[i - 1]
            r, c = start[0][0], start[0][1]
            dist_first, dist_second = get_dist(graph, location, r, c, d[r][c])
            y, x = location[0][0], location[0][1]
            d[y][x] = dist_second
            y, x = location[1][0], location[1][1]
            d[y][x] = dist_first

            r, c = start[1][0], start[1][1]
            dist_first, dist_second = get_dist(graph, location, r, c, d[r][c])
            y, x = location[0][0], location[0][1]
            d[y][x] = min(d[y][x], dist_second)
            y, x = location[1][0], location[1][1]
            d[y][x] = min(d[y][x], dist_first)
            
            y, x = location[0][0], location[0][1]
            graph[y][x] = 0
            y, x = location[1][0], location[1][1]
            graph[y][x] = 0
    
    for location in locations:
        for i, j, target in location:
            graph[i][j] = target

    return


def solution(board, r, c):
    
    cards = []
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                card = board[i][j]
                if cards.count(card) == 0:
                    cards.append(card)

    combs = list(itertools.permutations(cards))

    dist = INF
    for comb in combs:
        d = [[INF for _ in range(4)] for _ in range(4)]
        locations = []
        for target in comb:
            location = []
            for i in range(4):
                for j in range(4):
                    if target == board[i][j]:
                        location.append((i, j, target))
            locations.append(location)
        get_dists(board, locations, d, r, c)
        y, x = location[0][0], location[0][1]
        dist = min(dist, d[y][x])
        y, x = location[1][0], location[1][1]
        dist = min(dist, d[y][x])
    
    # 엔터키 조작 횟수 더하기
    dist = dist + len(comb)*2
    
    return dist


board = [[1,0,0,3],[2,0,0,0],[0,0,0,2],[3,0,1,0]]
r = 1
c = 0
solution(board, r, c)