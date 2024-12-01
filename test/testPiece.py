import pytest
from src.piece import Piece
import src.pieceForm as pf

@pytest.mark.parametrize(
    "pos_x,pos_y",
    [
        (5,4),
        (3,6)
    ],
)
def test_set_position(pos_x,pos_y):
    piece = Piece(pos_x,pos_y)

    assert (piece.x == pos_x and piece.y == pos_y)

@pytest.mark.parametrize(
    "piece,target",
    [
        (pf.PIECE_I, [True,False,True,True]),
        (pf.PIECE_L, [False,False,True]),
        (pf.PIECE_Z, [False, False, True])
    ],
)
def test_is_empty_row(piece,target):
    test_piece = Piece(0,0,piece)
    output =[]
    for i in range(test_piece.size()):
        output.append(test_piece.is_empty_row(i))

    assert output == target

@pytest.mark.parametrize(
    "piece,posx,posy,target",
    [
        (pf.PIECE_I,3,4,[1,2,3,4]),
        (pf.PIECE_I,3,2,[0,1,2]),
        (pf.PIECE_O,3,7,[6,7]),
    ],
)
def test_get_lines(piece,posx,posy,target):
    test_piece = Piece(posx,posy,piece)
    output= test_piece.get_lines()

    assert output == target

@pytest.mark.parametrize(
    "piece,posx,sizex,target",
    [
        (pf.PIECE_I,-2,5,0),
        (pf.PIECE_I,20,5,1),
        (pf.PIECE_O,3,10,3),
    ],
)
def test_adjust_pos(piece,posx,sizex,target):
    test_piece = Piece(posx,0,piece)

    test_piece.adjust_pos(sizex)

    assert test_piece.x == target

