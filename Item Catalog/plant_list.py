from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from plants_db_setup import Family, Base, Plant, User

engine = create_engine('sqlite:///familywithplants.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# Create dummy user
User1 = User(name="Plant Afficionado", email="email@gmail.com",)
session.add(User1)
session.commit()

# Plants for Asparagaceae
family1 = Family(user_id=1, name="Asparagaceae", hemisphere="North",
                       picture="https://upload.wikimedia.org/wikipedia/commons/b/b4/Funkia_%27Wide_brim%27.jpg",
                       description="Asparagaceae is a family of flowering plants, placed in the order Asparagales of the monocots. In earlier classification systems, the species involved were often treated as belonging to the family Liliaceae.")

session.add(family1)
session.commit()

plant1 = Plant(user_id=1, name="Agave", description="Agave is a genus of monocots native to the hot and arid regions of Mexico and the southern United States.",
                    family=family1)

session.add(plant1)
session.commit()


plant2 = Plant(user_id=1, name="Aloe", description="Aloe, is a genus containing over 500 species of flowering succulent plants.",
                     family=family1)

session.add(plant2)
session.commit()

plant3 = Plant(user_id=1, name="Drimia", description="Drimia is a species of flowering plant in the Asparagaceae family, commonly known as squill.",
                     family=family1)

session.add(plant3)
session.commit()

plant4 = Plant(user_id=1, name="Semele", description="Semele is a genus of flowering plants native to the Canary Islands and Madeira.",
                     family=family1)

session.add(plant4)
session.commit()


# Plants for Cactaceae
family2 = Family(user_id=1, name="Cactaceae", hemisphere="Western",
                       picture="https://upload.wikimedia.org/wikipedia/commons/1/12/Singapore_Botanic_Gardens_Cactus_Garden_2.jpg",
                       description="A cactus is a member of the plant family Cactaceae, a family comprising ca 127 genera with some 1750 known species of the order Caryophyllales.")

session.add(family2)
session.commit()


plant1 = Plant(user_id=1, name="Cactus", description="The name Cactus derives, through Latin from the Ancient Greek kaktos, a name originally used by Theophrastus for a spiny plant whose identity is not certain.",
                     family=family2)

session.add(plant1)
session.commit()

plant2 = Plant(user_id=1, name="Denmoza", description="The name of this genus is an anagram of the western province of Mendoza.",
                     family=family2)

session.add(plant2)
session.commit()

plant3 = Plant(user_id=1, name="Leptocereus", description="Leptocereus is a genus of cacti native to the Greater Antilles.",
                     family=family2)

session.add(plant3)
session.commit()

plant4 = Plant(user_id=1, name="Rebutia", description="Rebutia is a genus in the family Cactaceae, native to Bolivia and Argentina.",
                     family=family2)

session.add(plant4)
session.commit()


# Plants for Compositae
family3 = Family(user_id=1, name="Compositae", hemisphere="Southern",
                       picture="https://upload.wikimedia.org/wikipedia/commons/9/95/Cladanthus_arabicus_(Compositae)_flower.JPG",
                       description="Asteraceae or Compositae is an exceedingly large and widespread family of flowering plants. The family has more than 23,600 currently accepted species, spread across 1,620 genera and 13 subfamilies.")

session.add(family3)
session.commit()


plant1 = Plant(user_id=1, name="Bellis Perennis", description="Bellis perennis is a common European species of daisy, often considered the archetypal species of that name.",
                     family=family3)

session.add(plant1)
session.commit()

plant2 = Plant(user_id=1, name="Crocidium multicaule", description="Crocidium multicaule is a species of plants in the daisy family known by the common name spring gold.",
                     family=family3)

session.add(plant2)
session.commit()

plant3 = Plant(user_id=1, name="Lactuca", description="Lactuca, commonly known as lettuce, is a genus of flowering plants in the daisy family.",
                     family=family3)

session.add(plant3)
session.commit()

plant4 = Plant(user_id=1, name="Psilocarphus", description="Psilocarphus is a genus of flowering plants in the pussy's-toes tribe within the daisy family.",
                     family=family3)

session.add(plant4)
session.commit()


# Plants for Ericaceae
family4 = Family(user_id=1, name="Ericaceae", hemisphere="Northern",
                       picture="https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Leptecophylla_juniperina.jpg/220px-Leptecophylla_juniperina.jpg",
                       description="The Ericaceae are a family of flowering plants, commonly known as the heath or heather family, found most commonly in acid and infertile growing conditions.")

session.add(family4)
session.commit()


plant1 = Plant(user_id=1, name="Diogenesia", description="The genus Diogenesia is in the Ericaceae family in the major group of Angiosperms- Flowering plants.",
                     family=family4)

session.add(plant1)
session.commit()

plant2 = Plant(user_id=1, name="Kalmia", description="Kalmia is a genus of about 8 species of evergreen shrubs from 0.2 m tall. They are native to North America and Cuba.",
                     family=family4)

session.add(plant2)
session.commit()

plant3 = Plant(user_id=1, name="Lyonia", description="Lyonia is a genus of shrubs and trees, deciduous or evergreen. Some have rhizomes.",
                     family=family4)

session.add(plant3)
session.commit()

plant4 = Plant(user_id=1, name="Oxycoccus", description="Oxycoccus is a small genus of trailing or prostrate shrubs consisting of the cranberries.",
                     family=family4)

session.add(plant4)
session.commit()


# Plants for Lycopodiaceae
family5 = Family(user_id=1, name="Lycopodiaceae", hemisphere="Northern",
                       picture="https://upload.wikimedia.org/wikipedia/commons/8/84/LycopodiumClavatum.jpg",
                       description="The Lycopodiaceae are a family of vascular plants, including all of the core clubmosses, comprising three accepted genera and ca 400 known species.")

session.add(family5)
session.commit()


plant1 = Plant(user_id=1, name="Astrocaryum urostachys", description="A species of flowering plant found only in Ecuador.",
                     family=family5)

session.add(plant1)
session.commit()

plant2 = Plant(user_id=1, name="Huperzia serrata", description="Huperzia Serrata is widely distributed over the counter as both an herbal Alzheimer's treatment and as a cognitive enhancement supplement.",
                     family=family5)

session.add(plant2)
session.commit()

plant3 = Plant(user_id=1, name="Lycopodium clavatum", description="The most widespread species in the clubmoss family, Lycopodium clavatum is a perennial evergreen plant.",
                     family=family5)

session.add(plant3)
session.commit()

plant4 = Plant(user_id=1, name="Spinulum annotinum", description="Commonly known as bristly clubmoss, or common interrupted-clubmoss.",
                     family=family5)

session.add(plant4)
session.commit()

print "added plants!"
