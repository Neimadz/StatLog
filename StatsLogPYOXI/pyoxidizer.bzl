# Importez le module pyoxidizer
load("@pyoxidizer//pyoxidizer.bzl", "pyoxidizer")

# Définissez votre projet PyOxidizer
pyoxidizer.project(
    name = "mon_projet",
    srcs = ["main.py", "script.py"],
)

# Déclarez les dépendances et configurez l'interpréteur Python inclus si nécessaire
# Assurez-vous d'ajuster cette section en fonction de vos besoins spécifiques
pyoxidizer.project.add_deps([
    "pandas",
    "matplotlib",
    # Ajoutez d'autres dépendances selon vos besoins
])
