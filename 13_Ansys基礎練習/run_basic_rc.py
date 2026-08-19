"""Ansys AEDT 2026 R1：第一個 Circuit 暫態練習。

請先把專案與執行工作目錄放在純英文路徑，例如 D:\SIPI_Ansys_Basic。
"""

from ansys.aedt.core import settings

settings.release_on_exception = False
settings.pyedb_use_grpc = True

from ansys.aedt.core import Circuit


# 為避免 AEDT 受到中文路徑影響，這裡刻意使用純英文路徑。
PROJECT_PATH = r"D:\SIPI_Ansys_Basic\SIPI_Basic_RC_Practice.aedt"

circuit = Circuit(
    project=PROJECT_PATH,
    design="Basic_RC_Transient_Practice",
    version="2026.1",
    non_graphical=False,
    port=50051,
)
sch = circuit.modeler._schematic

source = sch.create_voltage_pulse(
    "V1", ["0V", "1V", "0s", "10ps", "10ps", "1ns", "3ns"], [0, 0], angle=90
)
resistor = sch.create_resistor("R1", 1e3, [0.005, 0], angle=0)
capacitor = sch.create_capacitor("C1", 1e-9, [0.012, -0.005], angle=90)
ground = sch.create_gnd([0.012, -0.01])

# 訊號路徑：脈衝源 → 1 kohm 電阻 → 1 nF 電容。
sch.create_line([source.pins[1].location, resistor.pins[1].location])
sch.create_line([resistor.pins[0].location, capacitor.pins[1].location])

# 回流路徑：電容另一端與脈衝源負端接到同一個 GND。
ground_pin = ground.pins[0].location
sch.create_line([capacitor.pins[0].location, ground_pin])
sch.create_line([ground_pin, [0.00508, -0.00762], source.pins[0].location])

setup = circuit.create_setup("TransientSetup", setup_type="NexximTransient")
setup.props["TransientData"] = ["10ps", "5ns"]
setup.update()

if not circuit.analyze_setup("TransientSetup"):
    raise RuntimeError("AEDT 無法完成 TransientSetup 求解，請檢查線路是否連接完整。")

circuit.save_project(PROJECT_PATH, overwrite=True)
print("SOLVE_OK=True")
