#!/usr/bin/env python3
"""Lock W12 product PositionTarget at 30 Hz. Planner and NMPC periods stay put."""
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
INCLUDE = PACKAGE / "include" / "px4_multirotor_controller"
TYPES = (INCLUDE / "common" / "types.h").read_text()
NMPC_YAML = (PACKAGE / "config" / "uav_nmpc.yaml").read_text()
STRATEGY = (PACKAGE / "src" / "tracking" / "px4_local_raw_strategy.cpp").read_text()
STATES = [
    INCLUDE / "uav" / "state_machine" / "custom1_state.h",
    INCLUDE / "uav" / "state_machine" / "hover_state.h",
    INCLUDE / "uav" / "state_machine" / "landing_state.h",
    INCLUDE / "uav" / "state_machine" / "takeoff_ascending_state.h",
    INCLUDE / "uav" / "state_machine" / "takeoff_init_state.h",
    INCLUDE / "uav" / "state_machine" / "takeoff_arm_request_state.h",
    INCLUDE / "uav" / "state_machine" / "takeoff_offboard_request_state.h",
]


def main() -> None:
    assert "constexpr double kLocalSetpointPublishHz = 30.0;" in TYPES
    assert "constexpr double kLocalSetpointPublishInterval = 1.0 / kLocalSetpointPublishHz;" in TYPES
    assert "double planning_period{0.1};" in TYPES
    assert "double control_period{0.01};" in TYPES
    assert "control_period: 0.01" in NMPC_YAML
    assert "return kLocalSetpointPublishInterval;" in STRATEGY
    assert "return config_.nmpc.control_period;" not in STRATEGY
    for path in STATES:
        text = path.read_text()
        assert "kLocalSetpointPublishInterval" in text, path
        assert "SETPOINT_PUBLISH_INTERVAL = 0.1" not in text, path
        assert "kPx4LocalSetpointPublishInterval = 0.1" not in text, path
    print("Product PositionTarget 30 Hz; planner 10 Hz; nmpc AttitudeTarget 100 Hz")


if __name__ == "__main__":
    main()
