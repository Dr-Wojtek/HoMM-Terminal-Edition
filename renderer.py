class Renderer:
    def renderer(town):
        for i in range(8, 10):
            for j in range(5, 7):
                town.render.square[i][j].kind = "tavern"
                if i == 8:
                    town.render.square[i][j].placement[0] = 3
                else:
                    town.render.square[i][j].placement[0] = 1
                if j == 5:
                    town.render.square[i][j].placement[1] = 4
                else:
                    town.render.square[i][j].placement[1] = 3

        if town.hasdw1:
            for i in range(3, 5):
                for j in range(0, 1):
                    town.render.square[i][j].kind = town.dw_names[0]
            town.render.square[3][0].placement = [3, 4]
            town.render.square[4][0].placement = [1, 4]

        if town.hasdw2:
            for i in range(2, 5):
                for j in range(2, 3):
                    town.render.square[i][j].kind = town.dw_names[1]
            town.render.square[2][2].placement = [3, 4]
            town.render.square[3][2].placement = [2, 4]
            town.render.square[4][2].placement = [1, 4]

        if town.hasdw3:
            for i in range(0, 2):
                for j in range(0, 2):
                    town.render.square[i][j].kind = town.dw_names[2]
                    if i == 0:
                        town.render.square[i][j].placement[0] = 3
                    else:
                        town.render.square[i][j].placement[0] = 1
                    if j == 0:
                        town.render.square[i][j].placement[1] = 1
                    else:
                        town.render.square[i][j].placement[1] = 4
        if town.hasdw4:
            for i in range(3, 5):
                for j in range(3, 4):
                    town.render.square[i][j].kind = town.dw_names[3]
            town.render.square[3][3].placement = [3, 4]
            town.render.square[4][3].placement = [1, 4]

        if town.hasdw5:
            for i in range(8, 10):
                for j in range(1, 3):
                    town.render.square[i][j].kind = town.dw_names[4]
                    if i == 8:
                        town.render.square[i][j].placement[0] = 3
                    else:
                        town.render.square[i][j].placement[0] = 1
                    if j == 1:
                        town.render.square[i][j].placement[1] = 2
                    else:
                        town.render.square[i][j].placement[1] = 5
        if town.hasdw6:
            for i in range(6, 7):
                for j in range(2, 6):
                    town.render.square[i][j].kind = town.dw_names[5]
            town.render.square[6][2].placement = [4, 1]
            town.render.square[6][3].placement = [4, 2]
            town.render.square[6][4].placement = [4, 5]
            town.render.square[6][5].placement = [4, 3]
        if town.hasdw7:
            for i in range(0, 1):
                for j in range(4, 8):
                    town.render.square[i][j].kind = town.dw_names[6]
            town.render.square[0][4].placement = [4, 1]
            town.render.square[0][5].placement = [4, 4]
            town.render.square[0][6].placement = [4, 2]
            town.render.square[0][7].placement = [4, 3]

        if town.hall_lvl == 1:
            for i in range(9, 10):
                for j in range(8, 12):
                    town.render.square[i][j].kind = "VillageHll"
                    if i == 9:
                        town.render.square[i][j].placement[0] = 4
                    if j == 8:
                        town.render.square[i][j].placement[1] = 1
                    elif j == 9:
                        town.render.square[i][j].placement[1] = 2
                    elif j == 10:
                        town.render.square[i][j].placement[1] = 4
                    else:
                        town.render.square[i][j].placement[1] = 3
        elif town.hall_lvl == 2:
            for i in range(8, 10):
                for j in range(8, 12):
                    town.render.square[i][j].kind = "Town Hall"
                    if i == 8:
                        town.render.square[i][j].placement[0] = 3
                    else:
                        town.render.square[i][j].placement[0] = 1
                    if j == 8:
                        town.render.square[i][j].placement[1] = 1
                    elif j == 9:
                        town.render.square[i][j].placement[1] = 2
                    elif j == 10:
                        town.render.square[i][j].placement[1] = 4
                    else:
                        town.render.square[i][j].placement[1] = 3
        elif town.hall_lvl == 3:
            for i in range(7, 10):
                for j in range(8, 12):
                    town.render.square[i][j].kind = "City Hall"
                    if i == 7:
                        town.render.square[i][j].placement[0] = 3
                    elif i == 8:
                        town.render.square[i][j].placement[0] = 2
                    else:
                        town.render.square[i][j].placement[0] = 1
                    if j == 8:
                        town.render.square[i][j].placement[1] = 1
                    elif j == 9:
                        town.render.square[i][j].placement[1] = 2
                    elif j == 10:
                        town.render.square[i][j].placement[1] = 4
                    else:
                        town.render.square[i][j].placement[1] = 3
        elif town.hall_lvl == 4:
            for i in range(6, 10):
                for j in range(8, 12):
                    town.render.square[i][j].kind = "Capitol"
                    if i == 6:
                        town.render.square[i][j].placement[0] = 3
                    elif i == 9:
                        town.render.square[i][j].placement[0] = 1
                    else:
                        town.render.square[i][j].placement[0] = 2
                    if j == 8:
                        town.render.square[i][j].placement[1] = 1
                    elif j == 9:
                        town.render.square[i][j].placement[1] = 2
                    elif j == 10:
                        town.render.square[i][j].placement[1] = 4
                    else:
                        town.render.square[i][j].placement[1] = 3

        if town.guild_lvl == 1:
            for i in range(4, 5):
                for j in range(11, 12):
                    town.render.square[i][j].kind = "MageGuild1"
            town.render.square[4][11].placement = [4, 4]
        elif town.guild_lvl == 2:
            for i in range(3, 5):
                for j in range(11, 12):
                    town.render.square[i][j].kind = "MageGuild2"
            town.render.square[3][11].placement = [3, 4]
            town.render.square[4][11].placement = [1, 4]
        elif town.guild_lvl == 3:
            for i in range(2, 5):
                for j in range(11, 12):
                    town.render.square[i][j].kind = "MageGuild3"
            town.render.square[2][11].placement = [3, 4]
            town.render.square[3][11].placement = [2, 4]
            town.render.square[4][11].placement = [1, 4]
        elif town.guild_lvl == 4:
            for i in range(1, 5):
                for j in range(11, 12):
                    town.render.square[i][j].kind = "MageGuild4"
            town.render.square[1][11].placement = [3, 4]
            town.render.square[2][11].placement = [2, 4]
            town.render.square[3][11].placement = [2, 4]
            town.render.square[4][11].placement = [1, 4]
        elif town.guild_lvl == 5:
            for i in range(0, 5):
                for j in range(11, 12):
                    town.render.square[i][j].kind = "MageGuild5"
            town.render.square[0][11].placement = [3, 4]
            town.render.square[1][11].placement = [2, 4]
            town.render.square[2][11].placement = [2, 4]
            town.render.square[3][11].placement = [2, 4]
            town.render.square[4][11].placement = [1, 4]
        if town.town_lvl == 1:
            for i in range(4, 5):
                for j in range(5, 10):
                    town.render.square[i][j].kind = "Fort"
                    if i == 4:
                        town.render.square[i][j].placement[0] = 4
                    if j == 5:
                        town.render.square[i][j].placement[1] = 1
                    elif j == 7:
                        town.render.square[i][j].placement[1] = 4
                    elif j == 9:
                        town.render.square[i][j].placement[1] = 3
                    else:
                        town.render.square[i][j].placement[1] = 2
        elif town.town_lvl == 2:
            for i in range(3, 5):
                for j in range(5, 10):
                    town.render.square[i][j].kind = "Citadel"
                    if i == 3:
                        town.render.square[i][j].placement[0] = 3
                    elif i == 4:
                        town.render.square[i][j].placement[0] = 1
                    if j == 5:
                        town.render.square[i][j].placement[1] = 1
                    elif j == 7:
                        town.render.square[i][j].placement[1] = 4
                    elif j == 9:
                        town.render.square[i][j].placement[1] = 3
                    else:
                        town.render.square[i][j].placement[1] = 2

        elif town.town_lvl == 3:
            for i in range(2, 5):
                for j in range(5, 10):
                    town.render.square[i][j].kind = "Castle"
                    if i == 2:
                        town.render.square[i][j].placement[0] = 3
                    elif i == 4:
                        town.render.square[i][j].placement[0] = 1
                    else:
                        town.render.square[i][j].placement[0] = 2
                    if j == 5:
                        town.render.square[i][j].placement[1] = 1
                    elif j == 7:
                        town.render.square[i][j].placement[1] = 4
                    elif j == 9:
                        town.render.square[i][j].placement[1] = 3
                    else:
                        town.render.square[i][j].placement[1] = 2