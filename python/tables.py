# Piece table classes

# First draft of piece tables are from the Chess Programming Wiki.
# See the "Simplified Evaluation Function" page here:
# https://www.chessprogramming.org/Simplified_Evaluation_Function

import matplotlib.pyplot as plt
import numpy as np
import tools

class PieceTable:
    def __init__(self):
        # Pawn table
        self.pawn_table = [
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [ 5,  5, 10, 25, 25, 10,  5,  5],
            [ 0,  0,  0, 20, 20,  0,  0,  0],
            [ 5, -5,-10,  0,  0,-10, -5,  5],
            [ 5, 10, 10,-20,-20, 10, 10,  5],
            [ 0,  0,  0,  0,  0,  0,  0,  0]
        ]
        # Knight table
        self.knight_table = [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ]
        # Bishop table
        self.bishop_table = [
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ]
        # Rook table
        self.rook_table = [
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 5, 10, 10, 10, 10, 10, 10,  5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [ 0,  0,  0,  5,  5,  0,  0,  0]
        ]
        # Queen table
        self.queen_table = [
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [ -5,  0,  5,  5,  5,  5,  0, -5],
            [  0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
        ]
        # King middle game table
        self.king_middle_game_table = [
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [ 20, 20,  0,  0,  0,  0, 20, 20],
            [ 20, 30, 10,  0,  0, 10, 30, 20]
        ]
        # King end game table
        self.king_end_game_table = [
            [-50,-40,-30,-20,-20,-30,-40,-50],
            [-30,-20,-10,  0,  0,-10,-20,-30],
            [-30,-10, 20, 30, 30, 20,-10,-30],
            [-30,-10, 30, 40, 40, 30,-10,-30],
            [-30,-10, 30, 40, 40, 30,-10,-30],
            [-30,-10, 20, 30, 30, 20,-10,-30],
            [-30,-30,  0,  0,  0,  0,-30,-30],
            [-50,-30,-30,-30,-30,-30,-30,-50]
        ]
        # Dictionary of tables
        self.tables = {
            "pawn"              : self.pawn_table,
            "knight"            : self.knight_table,
            "bishop"            : self.bishop_table,
            "rook"              : self.rook_table,
            "queen"             : self.queen_table,
            "king_middle_game"  : self.king_middle_game_table,
            "king_end_game"     : self.king_end_game_table
        }

    # Get dictionary of tables
    def GetTables(self):
        return self.tables

    # Return a table based on the table name
    def GetTable(self, table_name):
        result = None
        if table_name in self.tables:
            result = self.tables[table_name]
        else:
            print("ERROR: The table name '{0}' was not found.".format(table_name))
        return result

    # Plot tables
    def PlotTables(self, plot_dir):
        tables = self.GetTables()
        for table_name in tables:
            table = tables[table_name]
            self.PlotTable(plot_dir, table_name, table)

    # Plot a table
    def PlotTable(self, plot_dir, table_name, table):
        data = np.array(table)
        fig, ax = plt.subplots()
        
        print(table_name)
        print(data)
        
        ax.pcolormesh(data)
        
        #plt.show()
        
        output_pdf = "{0}/{1}.pdf".format(plot_dir, table_name)
        output_png = "{0}/{1}.png".format(plot_dir, table_name)

        plt.savefig(output_png, bbox_inches='tight')
        plt.savefig(output_pdf, bbox_inches='tight')
        
        plt.close('all')


def main():
    plot_dir = "plots"
    tools.makeDir(plot_dir)
    piece_table = PieceTable()
    piece_table.PlotTables(plot_dir)

if __name__ == "__main__":
    main()
