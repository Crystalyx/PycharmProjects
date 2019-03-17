class Gamet:
    def __init__(self, snak):
        self.dna = snak.dna.mutated_copy()
        self.snak = snak
        self.timer = 20

    def activate(self, world, snak):
        snak.pregnant = True
        snak.partner_dna = self.dna
