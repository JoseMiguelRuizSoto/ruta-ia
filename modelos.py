from llm import cliente

for m in cliente.models.list():
    if "flash" in m.name:
        print(m.name)