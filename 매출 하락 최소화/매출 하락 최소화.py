
INF = (2 ** 31) - 1

def dfs(sales, links, graph, d, n):
    # 자식 노드가 없는 경우
    if len(graph[n]) == 0:
        d[n] = [0, sales[n - 1]]
        return d[n]

    sum_child = 0
    # d[k][0] > d[k][1]의 여부
    member_join = False
    for i in range(len(graph[n])):
        # 자식 노드 k
        k = graph[n][i]
        d[k] = dfs(sales, links, graph, d, graph[n][i])
        sum_child = sum_child + min(d[k])

        if d[k][0] > d[k][1]:
            member_join = True
    
    # 팀장이 참석하는 경우의 최적해
    d[n][1] = sales[n - 1] + sum_child

    # 팀장이 불참하는 경우의 최적해
    # 팀원이 무조건 참석하는 경우
    if member_join:
        d[n][0] = sum_child
    # 팀원이 무조건 불참하는 경우
    else:
        # 팀원이 한명 참석 시 매출 하락 최소값
        member_join_min_value = INF
        for i in range(len(graph[n])):
            k = graph[n][i]
            member_join_min_value = min(member_join_min_value, d[k][1] - d[k][0])
        d[n][0] = sum_child + member_join_min_value
    
    return d[n]

# 두 원소가 속한 집합을 합치기
def union_parent(parent, a, b):
    parent[a].append(b)

    
def solution(sales, links):
    v = len(sales)

    # d[i][0] = i 번 노드가 불참하는 경우의 최적해
    # d[i][1] = i 번 노드가 참석하는 경우의 최적해
    d = [[INF, INF] for _ in range(v + 1)]
    
    parents = [[] for _ in range((v + 1))]
    for a, b in links:
        union_parent(parents, a, b)

    result = dfs(sales, links, parents, d, 1)
    
    return min(result)