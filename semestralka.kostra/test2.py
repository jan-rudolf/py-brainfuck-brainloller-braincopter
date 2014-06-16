import brainx

program = brainx.BrainFuck('[>+>+<<-]>>[<<+>>-]', memory=b'\x03\x03')

print(program.get_memory())