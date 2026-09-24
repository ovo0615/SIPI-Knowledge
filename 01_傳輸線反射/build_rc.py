from ansys.aedt.core import settings
settings.release_on_exception = False
settings.pyedb_use_grpc = True
from ansys.aedt.core import Circuit

c = Circuit(project="SIPI_Basic_Reflection", design="Basic_RC_Transient", version="2026.1", non_graphical=False, new_desktop=False, port=50051)
s = c.modeler._schematic
v = s.create_voltage_pulse("V1", ["0V", "1V", "0s", "10ps", "10ps", "1ns", "3ns"], [0, 0], angle=90)
r = s.create_resistor("R1", 1e3, [0.005, 0], angle=0)
cap = s.create_capacitor("C1", 1e-9, [0.012, -0.005], angle=90)
g = s.create_gnd([0.012, -0.01])
for name, comp in [("V1", v), ("R1", r), ("C1", cap), ("GND", g)]:
    print(name, [(pin.name, pin.location) for pin in comp.pins])
