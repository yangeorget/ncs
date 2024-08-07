from typing import List

from ncs.problems.problem import Problem
from ncs.propagators.propagators import ALG_AFFINE_EQ, ALG_ALLDIFFERENT

A = 0
B = 1
C = 2
D = 3
E = 4
F = 5
G = 6
H = 7
I = 8
J = 9
K = 10
L = 11
M = 12
N = 13
O = 14
P = 15
Q = 16
R = 17
S = 18
T = 19
U = 20
V = 21
W = 22
X = 23
Y = 24
Z = 25


class AlphaProblem(Problem):
    """
    This problem comes from the newsgroup rec.puzzle.
    The numbers from 1 to 26 are assigned to the letters of the alphabet.
    The numbers beside each word are the total of the values assigned to the letters in the word
    (e.g for LYRE: L,Y,R,E might be to equal 5,9,20 and 13 or any other combination that add up to 47).

    Find the value of each letter under the equations:
    BALLET  45     GLEE  66     POLKA      59     SONG     61
    CELLO   43     JAZZ  58     QUARTET    50     SOPRANO  82
    CONCERT 74     LYRE  47     SAXOPHONE 134     THEME    72
    FLUTE   30     OBOE  53     SCALE      51     VIOLIN  100
    FUGUE   50     OPERA 65     SOLO       37     WALTZ    34
    """

    def __init__(self) -> None:
        super().__init__(shr_domains=[(1, 26)] * 26, dom_indices=list(range(26)), dom_offsets=[0] * 26)
        self.set_propagators(
            [
                ([A, B, E, T, L], ALG_AFFINE_EQ, [45, 1, 1, 1, 1, 2]),
                ([C, E, O, L], ALG_AFFINE_EQ, [43, 1, 1, 1, 2]),
                ([E, O, N, R, T, C], ALG_AFFINE_EQ, [74, 1, 1, 1, 1, 1, 2]),
                ([E, F, L, U, T], ALG_AFFINE_EQ, [30, 1, 1, 1, 1, 1]),
                ([E, F, G, U], ALG_AFFINE_EQ, [50, 1, 1, 1, 2]),
                ([G, L, E], ALG_AFFINE_EQ, [66, 1, 1, 2]),
                ([A, J, Z], ALG_AFFINE_EQ, [58, 1, 1, 2]),
                ([E, L, R, Y], ALG_AFFINE_EQ, [47, 1, 1, 1, 1]),
                ([E, B, O], ALG_AFFINE_EQ, [53, 1, 1, 2]),
                ([A, E, P, O, R], ALG_AFFINE_EQ, [65, 1, 1, 1, 1, 1]),
                ([A, K, L, O, P], ALG_AFFINE_EQ, [59, 1, 1, 1, 1, 1]),
                ([A, E, Q, R, U, T], ALG_AFFINE_EQ, [50, 1, 1, 1, 1, 1, 2]),
                ([A, E, H, N, P, S, X, O], ALG_AFFINE_EQ, [134, 1, 1, 1, 1, 1, 1, 1, 2]),
                ([A, C, E, L, S], ALG_AFFINE_EQ, [51, 1, 1, 1, 1, 1]),
                ([L, S, O], ALG_AFFINE_EQ, [37, 1, 1, 2]),
                ([G, N, O, S], ALG_AFFINE_EQ, [61, 1, 1, 1, 1]),
                ([A, N, P, R, S, O], ALG_AFFINE_EQ, [82, 1, 1, 1, 1, 1, 2]),
                ([H, M, T, E], ALG_AFFINE_EQ, [72, 1, 1, 1, 2]),
                ([L, N, O, V, I], ALG_AFFINE_EQ, [100, 1, 1, 1, 1, 2]),
                ([A, L, T, W, Z], ALG_AFFINE_EQ, [34, 1, 1, 1, 1, 1]),
                ([A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z], ALG_ALLDIFFERENT, []),
            ]
        )

    def pretty_print_solution(self, solution: List[int]) -> None:
        print(
            {
                "A": solution[A],
                "B": solution[B],
                "C": solution[C],
                "D": solution[D],
                "E": solution[E],
                "F": solution[F],
                "G": solution[G],
                "H": solution[H],
                "I": solution[I],
                "J": solution[J],
                "K": solution[K],
                "L": solution[L],
                "M": solution[M],
                "N": solution[N],
                "O": solution[O],
                "P": solution[P],
                "Q": solution[Q],
                "R": solution[R],
                "S": solution[S],
                "T": solution[T],
                "U": solution[U],
                "V": solution[V],
                "W": solution[W],
                "X": solution[X],
                "Y": solution[Y],
                "Z": solution[Z],
            }
        )
