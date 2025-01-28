from src.Classes import WorkTree as WT

prova = WT()
prova.create_worktree()

path = getattr(prova, "path")
print(path)