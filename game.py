import copy, random

class BattleshipAvioane:
    # functie care afiseaza tabla

    def afisare_tabla(self, s, tabla):
        player = "Computer"
        if s == "u":
            player = "Paul"
        print(" Tabla lui " + player + " arată cam așa: \n")

        # afiseaza numerele pe orizontala
        print(" ", end=' ')
        for i in range(10):
            print("  " + str(i + 1) + "  ", end=' ')
        print("\n")
        for i in range(10):
            # afiseaza numerele pe verticala
            if i != 9:
                print(str(i + 1) + "  ", end=' ')
            else:
                print(str(i + 1) + " ", end=' ')
            # afiseaza valorile de pe tablă
            for j in range(10):
                if tabla[i][j] == -1:
                    print(' ', end=' ')
                elif s == "u":
                    print(tabla[i][j], end=' ')
                elif s == "c":
                    if tabla[i][j] == "*" or tabla[i][j] == "$":
                        print(tabla[i][j], end=' ')
                    else:
                        print(" ", end=' ')
                if j != 9:
                    print(" | ", end=' ')
            print()
            # afiseaza o linie orizontala la finalul tablei
            if i != 9:
                print("   ----------------------------------------------------------")
            else:
                print()

    # functie care lasa userul să puna avioanele

    def user_place_ships(self, tabla, avioane):
        """
        lasa userul să își plaseze avioanele și verifică dacă sunt într-o poziție corectă
        """
        for avion in list(avioane.keys()):
            valid = False
            while (not valid):
                self.afisare_tabla("u", tabla)
                print("Plasăm un " + avion)
                x, y = self.get_coor()
                ori = self.v_or_h()
                valid = self.validate(tabla, avioane[avion], x, y, ori)
                if not valid:
                    print("Nu se poate pune un avion acolo.\nTe rog să te uiți la tablă și să încerci din nou.")
                    input("Apasă ENTER pentru a continua")
            # place the ship
            tabla = self.place_avion(tabla, avioane[avion], avion[0], ori, x, y)
            self.afisare_tabla("u", tabla)
        input("Am terminat de pus avioanele. Apasă ENTER pentru a continua")
        return tabla

    # lasă computerul să pună avioanele și să le verifice poziția
    def computer_place_ships(self, tabla, avioane):
        """
        computerul va folosi random pentru a genera locatia avioanelor
        """
        for avion in list(avioane.keys()):
            # genereaza coordonate random și validează poziția
            valid = False
            while (not valid):
                x = random.randint(1, 10) - 1
                y = random.randint(1, 10) - 1
                o = random.randint(0, 1)
                # vertical sau orizontala
                if o == 0:
                    ori = "v"
                else:
                    ori = "o"
                valid = self.validate(tabla, avioane[avion], x, y, ori)
            print("Computerul a pus un " + avion)
            tabla = self.place_avion(tabla, avioane[avion], avion[0], ori, x, y)
        return tabla

    # lasă userul să pună un avion
    def place_avion(self, tabla, avion, s, ori, x, y):
        
        # orientează avioanele
        if ori == "v":
            for i in range(avion):
                tabla[x + i][y] = s
        elif ori == "o":
            for i in range(avion):
                tabla[x][y + i] = s
        return tabla

    # verifică dacă avionul se potrivește poziției
    def validate(self, tabla, avion, x, y, ori):
        """
        verifică dacă avionul se potrivește poziției, în funcție de mărimea avionului, tablă, orientare și coordonate
        """
        if ori == "v" and x + avion > 10:
            return False
        elif ori == "o" and y + avion > 10:
            return False
        else:
            if ori == "v":
                for i in range(avion):
                    if tabla[x + i][y] != -1:
                        return False
            elif ori == "o":
                for i in range(avion):
                    if tabla[x][y + i] != -1:
                        return False
        return True

    # vede dacă avionul e vertical sau orizontal
    def v_or_h(self):
        # primește orientarea avionului de la user
        while (True):
            user_input = input("vertical sau orizontal (v,o) ? ")
            if user_input == "v" or user_input == "o":
                return user_input
            else:
                print("Intrare invalidă. Te rog să introduci v sau o")

    def get_coor(self):
        """
        userul va introduce coordonatele (rând și coloană) pentru avionul care va pleca
        """
        while (True):
            user_input = input("Te rog să introduci coordonatele (rând,coloană) ? ")
            try:
                # verifică dacă userul a introdus 2 coordonate separate prin virgulă
                coor = user_input.split(",")
                if len(coor) != 2:
                    raise Exception("Intrare invalidă, prea multe/puține coordonate.");
                # verfică dacă cele 2 valori sunt int
                coor[0] = int(coor[0]) - 1
                coor[1] = int(coor[1]) - 1
                # verifică dacă valorile lui int sunt între 1 și 10 a ambelor coordonate
                if coor[0] > 9 or coor[0] < 0 or coor[1] > 9 or coor[1] < 0:
                    raise Exception("Intrare invalidă. Te rog să folosești doar valori între 1 și 10.")
                # dacă totul e ok, returnează coordonatele
                return coor
            # dacă userul introduce ceva diferit
            except ValueError:
                print("Intrare invalidă. Te rog să introduci doar valori numerice pentru pentru coordonate.")
            except Exception as e:
                print(e)

    def make_move(self, tabla, x, y):
        """
        face mutarea pe tablă și afișeză tabla modificată
        """
        if tabla[x][y] == -1:
            return "miss"
        elif tabla[x][y] == '*' or tabla[x][y] == '$':
            return "try again"
        else:
            return "hit"

    def user_move(self, tabla):
        """
        continuă să primească coordonate de la user și verifică dacă e lovit, ratat sau scufundat 
        """
        while (True):
            x, y = self.get_coor()
            res = self.make_move(tabla, x, y)
            if res == "lovit":
                print("Lovit la " + str(x + 1) + "," + str(y + 1))
                self.check_sink(tabla, x, y)
                tabla[x][y] = '$'
                if self.check_win(tabla):
                    return "WIN"
            elif res == "ratat":
                print("Scuze, " + str(x + 1) + "," + str(y + 1) + " e o ratare.")
                tabla[x][y] = "*"
            elif res == "încearcă din nou":
                print("Scuze, coordonata aceea a fost deja lovită. Te rog să încerci din nou.")
            if res != "încearcă din nou":
                return tabla

    def computer_move(self, tabla):
        """
        generează coordonate random pentru care computerul încearcă să folosească random 
        la fel ca și funcția user_move și verifică dacă e lovit, ratat sau scufundat
        """
        while (True):
            x = random.randint(1, 10) - 1
            y = random.randint(1, 10) - 1
            res = self.make_move(tabla, x, y)
            if res == "lovit":
                print("Lovit la " + str(x + 1) + "," + str(y + 1))
                self.check_sink(tabla, x, y)
                tabla[x][y] = '$'
                if self.check_win(tabla):
                    return "WIN"
            elif res == "ratat":
                print("Scuze, " + str(x + 1) + "," + str(y + 1) + " e o ratare.")
                tabla[x][y] = "*"
            elif res == "încearcă din nou":
                return tabla


    def check_sink(self, tabla, x, y):
        """
        află dacă avionul este lovit, apoi verifică câte puncte mai sunt in avion, apoi vede dacă este scufundat.
        avionul este scufundat dacă nu mai sunt puncte rămase
        """
        if tabla[x][y] == "A":
            ship = "Avion"
        # mark cell as hit and check if sunk
        tabla[-1][ship] -= 1
        if tabla[-1][ship] == 0:
            print(ship + " Sunk")


    def check_win(self, tabla):
        """
        odată ce toate avioanele sunt scufundate, cineva câștigă și se încheie jocul
        """
        for i in range(10):
            for j in range(10):
                if tabla[i][j] != -1 and tabla[i][j] != '*' and tabla[i][j] != '$':
                    return False
        return True

    # function called to start program
    #all of us 
    def main(self):
        # types of ships
        avioane = {"Avion": 5}
        # setup blank 10x10 board
        tabla = []
        for i in range(10):
            board_row = []
            for j in range(10):
                board_row.append(-1)
            tabla.append(board_row)
        # setup user and computer boards
        user_board = copy.deepcopy(tabla)
        comp_board = copy.deepcopy(tabla)
        # add ships in array
        user_board.append(copy.deepcopy(avioane))
        comp_board.append(copy.deepcopy(avioane))
        # ship placement
        user_board = self.user_place_ships(user_board, avioane)
        comp_board = self.computer_place_ships(comp_board, avioane)
        # game main loop
        #owen
        while (1):
            # user move
            self.afisare_tabla("c", comp_board)
            comp_board = self.user_move(comp_board)
            # check if user won
            if comp_board == "VICTORIE":
                print("Paul a CÂȘTIGAT! :)")
                quit()
            # display current computer board
            self.afisare_tabla("c", comp_board)
            input("Pentru a finaliza rândul utilizatorului apasă ENTER")
            # computer move
            user_board = self.computer_move(user_board)
            # check if computer move
            if user_board == "VICTORIE":
                print("Computer a CÂȘTIGAT! :(")
                quit()
            # display user board
            input("Pentru a finaliza rândul computerului apasă ENTER")


root = BattleshipAvioane()
root.main()
