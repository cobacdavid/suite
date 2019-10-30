import dvtDecimal as dD


__author__ = "david cobac"
__date__ = 201910


class suite(object):
   
    def __init__(self,
                 p_terme=None,
                 rang_p_terme=0,
                 fonction=None,
                 rec=False,
                 use_dvtDecimal=True):
        self._rang_premier_terme = rang_p_terme
        self.termes_connus = []
        if p_terme is not None and rec:
            self.set_premier_terme_rec(p_terme)
        if fonction is not None:
            self.set_fonction(fonction)
        self._rec = rec

    def set_premier_terme_rec(self, nombre):
        if self._rang_premier_terme is not None:
            # reinitialisation si besoin
            self.termes_connus = []
            self.termes_connus += [None] * (self._rang_premier_terme + 1)
            if type(nombre) == tuple:
                self.termes_connus[self._rang_premier_terme] =\
                    dD.dvtDecimal(*nombre)
            else:
                self.termes_connus[self._rang_premier_terme] =\
                    dD.dvtDecimal(nombre)

    def set_rang_premier_terme(self, rang):
        self._rang_premier_terme = rang

    def set_fonction(self, fonction):
        self._fonction = fonction

    def __format_ecriture_dvtDecimal(objet_dvtDecimal, approx):
        if objet_dvtDecimal.simpValues[1] == 1:
            resultat = [str(objet_dvtDecimal.simpValues[0])]
        else:
            resultat = [str(objet_dvtDecimal.simpValues[0]) +
                        "/" + str(objet_dvtDecimal.simpValues[1])]
        if approx:
            if objet_dvtDecimal.repPart == [0]:
                ecriture = objet_dvtDecimal.intPart + \
                    objet_dvtDecimal.irrPart()
                ecriture = str(ecriture)
            else:
                ecriture = objet_dvtDecimal.dotWrite(15)
            resultat += [ecriture]
        return resultat

    def __renvoi_on_demand(terme, demande_approx):
        if isinstance(terme, dD.dvtDecimal):
            renvoi = suite.__format_ecriture_dvtDecimal(terme, demande_approx)
        else:
            renvoi = terme
        return renvoi

    def on_demand(self, n=None, approx=False):
        rang = self._rang_premier_terme
        ##
        terme = self.get_terme_rang(rang)
        yield rang, suite.__renvoi_on_demand(terme, approx)
        #
        j, b = 1, n is None
        rang += 1
        while b or j < n:
            terme = self.get_terme_rang(rang)
            yield rang, suite.__renvoi_on_demand(terme, approx)
            rang += 1
            j += 1

    def play(self, n=10):
        from midiutil import MIDIFile
        degrees = [60, 62, 64, 65, 67, 69, 71, 72]
        track = 0
        channel = 0
        time = 0   # In beats
        duration = 1  # In beats
        tempo = 160  # In BPM
        volume = 100 # 0-127, as per the MIDI standard
        morceau = MIDIFile(1)
        morceau.addTempo(track, time, tempo)
        #
        for i, terme in enumerate(self.on_demand(n)):
            note = terme % len(degrees)
            morceau.addNote(track, channel, note, time + i, duration, volume)
        #
        with open("temp.mid", "w") as sortie:
            morceau.writeFile(sortie)

    def get_terme_rang(self, rang):
        resultat = None
        # s'il existe, on le donne
        if len(self.termes_connus) >= rang + 1 and\
           self.termes_connus[rang] is not None:
            resultat = self.termes_connus[rang]
        elif rang >= self._rang_premier_terme:
            if not self._rec:
                # définition explicite
                nb_termes_a_ajouter = rang - (len(self.termes_connus) - 1)
                self.termes_connus += [None] * nb_termes_a_ajouter
                try:
                    resultat = self._fonction(dD.dvtDecimal(rang))
                except (AttributeError, TypeError):
                    resultat = self._fonction(rang)
                self.termes_connus[rang] = resultat
            else:
                # définition par récurrence
                # si on manque de termes
                rang_actuel = len(self.termes_connus) - 1
                while rang_actuel < rang:
                    self.termes_connus += \
                        [self._fonction(self.termes_connus[-1])]
                    rang_actuel += 1
                resultat = self.termes_connus[rang]
        return resultat

    def get_diff_succ(self):
        resultat = None
        if len(self.termes_connus) >= 2:
            resultat = []
            for i in range(len(self.termes_connus) - 1):
                if self.termes_connus[i + 1] is not None and\
                   self.termes_connus[i] is not None:
                    resultat.append(self.termes_connus[i + 1]
                                    - self.termes_connus[i])
                else:
                    resultat.append(None)
        return resultat

    def get_div_succ(self):
        resultat = None
        if len(self.termes_connus) >= 2 and \
           0 not in self.termes_connus:
            resultat = []
            for i in range(len(self.termes_connus) - 1):
                if self.termes_connus[i + 1] is not None and\
                   self.termes_connus[i] is not None:
                    resultat.append(self.termes_connus[i + 1]
                                    / self.termes_connus[i])
                else:
                    resultat.append(None)
        return resultat

    def get_somme_premiers(self, n):
        # on s'assure de tout avoir
        if not self._rec:
            for i in range(self._rang_premier_terme, n +
                           self._rang_premier_terme):
                self.get_terme_rang(i)
        else:
            self.get_terme_rang(self._rang_premier_terme + n - 1)
        # on somme
        return sum(self.termes_connus[self._rang_premier_terme:
                                      self._rang_premier_terme + n])

    def get_rep_exp(self, p):
        """représentation de p termes"""
        if self._rec:
            self.get_terme_rang(self._rang_premier_terme + p - 1)
        else:
            for i in range(self._rang_premier_terme,
                           self._rang_premier_terme + p):
                self.get_terme_rang(i)
        # la liste créée ne contient plus de None au départ
        termes_num = []
        for v in self.termes_connus[self._rang_premier_terme:
                                    self._rang_premier_terme + p]:
            termes_num.append(float(v))
        #
        return (range(self._rang_premier_terme,
                      self._rang_premier_terme + p), termes_num)

    def get_rep_rec(self, p):
        """représentation de p termes"""
        # on cherche les termes
        if self._rec:
            self.get_terme_rang(self._rang_premier_terme + p - 1)
        else:
            for i in range(self._rang_premier_terme,
                           self._rang_premier_terme + p):
                self.get_terme_rang(i)
        # on les met sous forme numérique
        # la liste créé ne contient plus de None au départ
        termes_num = []
        for v in self.termes_connus[self._rang_premier_terme:
                                    self._rang_premier_terme + p]:
            termes_num.append(float(v))
        #
        resultatX = []
        resultatY = []
        for i in range(len(termes_num) - 1):
            resultatX += [termes_num[i]]
            resultatY += [0]
            resultatX += [termes_num[i]]
            resultatY += [termes_num[i+1]]
            resultatX += [termes_num[i+1]]
            resultatY += [termes_num[i+1]]
        i = p - 1
        resultatX += [termes_num[i]]
        resultatY += [0]
        resultatX += [termes_num[i]]
        resultatY += [termes_num[i]]
        resultat = (resultatX, resultatY)
        #
        return resultat

    # def semble_arithmetique(self):
    #     resultat = None
    #     if None not in self.termes_connus and \
    #        len(self.termes_connus) >= 2:
    #         resultat = len(set(self.get_diff_succ())) == 1
    #     return resultat

    # def semble_geometrique(self):
    #     resultat = None
    #     if None not in self.termes_connus and \
    #        len(self.termes_connus) >= 2:
    #         if self.get_div_succ() is not None:
    #             resultat = len(set(self.get_div_succ())) == 1
    #     return resultat


if __name__ == "__main__":
    pass
