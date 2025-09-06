data = ['a5', 'a2', 'b1', 'b3', 'c2']

sorted_data = sorted(data, key=lambda x: (x[0], int(x[1:])))
# x[0] → sorts by the letter (a, b, c).
# int(x[1:]) → sorts by the numeric part (5, 2, 1, 3, 2).
# 'a2' (a,2) → first among a.
# 'a5' (a,5) → next among a.
# 'b1' (b,1), 'b3' (b,3) → ordered numerically under b.
# 'c2' (c,2) → last group.

print(sorted_data)
#'a2' (a,2) → first among a.
#'a5' (a,5) → next among a.
#'b1' (b,1), 'b3' (b,3) → ordered numerically under b.
#'c2' (c,2) → last group.
#Final sorted result: ['a2', 'a5', 'b1', 'b3', 'c2']