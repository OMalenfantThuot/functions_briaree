class Psppar:
    """Une classe pour les fichiers pseudopotentiels"""

    def __init__(self, element):
        """
        :param element: élément de l'atome représenté par le pseudo
        """
        self.element = element.upper()
        if self.element not in ["C", "N"]:
            raise NameError("This element is not supported yet.")

    def create(self):
        """crée le fichier pseudopotential"""

        with open("psppar." + self.element, "w") as f:

            if self.element == "C":
                text = (
                    "HGH for Carbon (C) in PBE with NLCC,generated by Saha,2015\n"
                    "    6    4  20150303 zatom, zion, date (yymmdd)\n"
                    "   12   -101130  0 0 2002 0         pspcod, ixc, lmax, lloc, mmax, r2well\n"
                    "    0.41329225352  2 -5.729305064  0.874750285642 rloc nloc c1 .. cnloc\n"
                    "   1                                                      nsep\n"
                    "   0.4341053017   2   9.01955484658 -2.4185793675      s-projector\n"
                    "                       0.554729349186\n"
                    "    0.362404633914     0.60557630341      rcore, qcore (nlcc)"
                )
                f.write(text)

            elif self.element == "N":
                text = (
                    "HGH for Nitrogen (N) in PBE with NLCC,generated by Saha,2015\n"
                    "    7    5  20150407 zatom, zion, date (yymmdd)\n"
                    "   12   -101130  0 0 2002 0         pspcod, ixc, lmax, lloc, mmax, r2well\n"
                    "    0.40469225352    2 -8.10098063736025  1.294191224 rloc nloc c1 .. cnloc\n"
                    "   1                                                       nsep\n"
                    "   0.4256053017  2   9.2183335485526  -2.4905918767      s-projector\n"
                    "                       0.38356320566013\n"
                    "    0.3540622374     0.380004476133      rcore, qcore (nlcc)"
                )
                f.write(text)
