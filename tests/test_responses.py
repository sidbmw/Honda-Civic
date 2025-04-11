import glob
import os
import pytest
from pathlib import Path
from typing import Dict, Any

# These will be imported from the schemas repository
from schemas.python.can_frame import CANIDFormat
from schemas.python.json_formatter import format_file
from schemas.python.signals_testing import obd_testrunner_by_year

REPO_ROOT = Path(__file__).parent.parent.absolute()

TEST_CASES = [
    {
        "model_year": 2016,
        "tests": [
            # Ambient air temperature
            ("""
18DAF1601039627028F8F000
18DAF1602100000004040100
18DAF1602200000000004E00
18DAF160234C000000000000
18DAF1602400000000000000
18DAF1602500000000000000
18DAF1602600000000000000
18DAF1602700000000000000
18DAF1602800005555555555
""", {"CIVIC_AAT": 36}),
            ("""
18DAF1601039627028F8F000
18DAF1602100000004070101
18DAF1602200000000005800
18DAF1602357000000000000
18DAF1602400000000000000
18DAF1602500000000000000
18DAF1602600000000000000
18DAF1602700000000000000
18DAF1602800005555555555
""", {"CIVIC_AAT": 47}),

            # ODO + runtime
            ("""
18DAF1101039622660801FFF
18DAF11021F3FFF000000000
18DAF1102200000000000000
18DAF1102300002CD11B0201
18DAF1102400040040408300
18DAF1102501021D000005BD
18DAF110260150017035018F
18DAF110278500E500460000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 102277.0,
    "CIVIC_RUNTM": 229,
    }),
            ("""
18DAF1101039622660801FFF
18DAF11021F3FFF000000000
18DAF1102200000000000000
18DAF1102300002CFC1B0101
18DAF1102400040040408300
18DAF1102501021100000947
18DAF11026040504FD4B018F
18DAF11027B3063B02F00000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 102323.0,
    "CIVIC_RUNTM": 1595,
    }),
        ]
    },
    {
        "model_year": 2017,
        "tests": [
            # ODO + runtime
            ("""
18DAF1101039622660801FFF
18DAF11021F3F7F000000000
18DAF1102200000000000000
18DAF11023000023DE1B0101
18DAF1102400040040408300
18DAF110250100B8000005B8
18DAF11026022E022E000299
18DAF1102726037F005B0000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 170278,
    "CIVIC_RUNTM": 895,
    }),
            ("""
18DAF1101039622660801FFF
18DAF11021F3F7F000000000
18DAF1102200000000000000
18DAF11023000023E11B0101
18DAF1102400040040408300
18DAF110250100B800000E59
18DAF11026081507F6000299
18DAF1102729043301710000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 170281,
    "CIVIC_RUNTM": 1075,
}),
        ]
    },
    {
        "model_year": 2018,
        "tests": [
            # ODO + RUNTM
            ("""
18DAF1101039622660801FFF
18DAF11021F3F7F000000000
18DAF1102200000000000000
18DAF110230000042D1B0101
18DAF1102400040040008300
18DAF110250103840000082C
18DAF1102605D60547000143
18DAF1102796001500000000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 82838,
    "CIVIC_RUNTM": 21,
}),
            ("""
18DAF1101039622660801FFF
18DAF11021F3F7F000000000
18DAF1102200000000000000
18DAF11023000004D41B0201
18DAF1102400040040408300
18DAF110250103760000022B
18DAF11026017F017A000144
18DAF1102745014B01300000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 83013,
    "CIVIC_RUNTM": 331,
}),
            # AAT
            ("""
18DAF1601039627028F8F000
18DAF1602100000004020100
18DAF1602200000000002500
18DAF1602325000000000000
18DAF1602400000000000000
18DAF1602500000000000000
18DAF1602600000000000000
18DAF1602700000000000000
18DAF1602800005555555555
""", {"CIVIC_AAT": -3}),
            ("""
18DAF1601039627028F8F000
18DAF1602100000004020100
18DAF1602200000000004C00
18DAF160234C000000000000
18DAF1602400000000000000
18DAF1602500000000000000
18DAF1602600000000000000
18DAF1602700000000000000
18DAF1602800005555555555
""", {"CIVIC_AAT": 36}),
        ]
    },
    {
        "model_year": 2022,
        "tests": [
            # ODO + RUNTM
            ("""
18DAF1101039622660801FFF
18DAF11021F3FFF000000000
18DAF1102200000000000000
18DAF11023000023A53B0201
18DAF1102400040040408300
18DAF110250101AA00000372
18DAF110260137012D380067
18DAF110273300AC005B0000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 26419,
    "CIVIC_RUNTM": 172
}),
            ("""
18DAF1101039622660801FFF
18DAF11021F3FFF000000000
18DAF1102200000000000000
18DAF110230000330D3B2201
18DAF1102400040040008300
18DAF1102501012300000467
18DAF11026012F014C350140
18DAF110277D00C100000000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 82045,
    "CIVIC_RUNTM": 193
}),
            # AAT
            ("""
18DAF1601039627028F8F000
18DAF1602100000004070101
18DAF1602200000000005400
18DAF1602353000000000000
18DAF1602400000000000000
18DAF1602500000000000000
18DAF1602600000000000000
18DAF1602700000000000000
18DAF1602800005555555555
""", {"CIVIC_AAT": 43}),
            ("""
18DAF1601039627028F8F000
18DAF1602100000004040000
18DAF1602200000000000300
18DAF1602302000000000000
18DAF1602400000000000000
18DAF1602500000000000000
18DAF1602600000000000000
18DAF1602700000000000000
18DAF1602800005555555555
""", {"CIVIC_AAT": -38}),
        ]
    },
    {
        "model_year": 2023,
        "tests": [
            # ODO + RUNTM
            ("""
18DAF1101039622660801FFF
18DAF11021F3FFF000000000
18DAF1102200000000000000
18DAF11023000063643B0001
18DAF1102400040040008300
18DAF1102501039100000F4B
18DAF11026078A06E559008B
18DAF11027B5009F00000000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 35765,
    "CIVIC_RUNTM": 159,
}),
            ("""
18DAF1101039622660801FFF
18DAF11021F3FFF000000000
18DAF1102200000000000000
18DAF11023000064503B0201
18DAF1102400040040408300
18DAF1102501037C0000026C
18DAF1102600EC00E234008C
18DAF11027A507EC09930000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 36005,
    "CIVIC_RUNTM": 2028,
}),
            # AAT
            ("""
18DAF1601039627028F8F000
18DAF1602100000004020100
18DAF1602200000000002C00
18DAF160232D000000000000
18DAF1602400000000000000
18DAF1602500000000000000
18DAF1602600000000000000
18DAF1602700000000000000
18DAF1602800005555555555
""", {"CIVIC_AAT": 5}),
            ("""
18DAF1601039627028F8F000
18DAF1602100000004020100
18DAF1602200000000005C00
18DAF160235C000000000000
18DAF1602400000000000000
18DAF1602500000000000000
18DAF1602600000000000000
18DAF1602700000000000000
18DAF1602800005555555555
""", {"CIVIC_AAT": 52}),
        ]
    },
    {
        "model_year": 2024,
        "tests": [
            # ODO + RUNTM
            ("""
18DAF1101039622660801FFF
18DAF11021F3FFF000000000
18DAF1102200000000000000
18DAF110230000259B3B0101
18DAF1102400040040008300
18DAF110250103A000000543
18DAF110260216022C3F0025
18DAF11027FB00B900020000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 9723,
    "CIVIC_RUNTM": 185,
}),
            ("""
18DAF1101039622660801FFF
18DAF11021F3FFF000000000
18DAF1102200000000000000
18DAF11023000026AE3B0101
18DAF1102400040040008300
18DAF1102501038800000E24
18DAF11026087208045D0027
18DAF1102710014200730000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 10000,
    "CIVIC_RUNTM": 322,
}),
            # AAT
            ("""
18DAF1601039627028F8F000
18DAF1602100000004020100
18DAF1602200000000002200
18DAF1602322000000000000
18DAF1602400000000000000
18DAF1602500000000000000
18DAF1602600000000000000
18DAF1602700000000000000
18DAF1602800005555555555
""", {"CIVIC_AAT": -6}),
            ("""
18DAF1601039627028F8F000
18DAF1602100000004020100
18DAF1602200000000005200
18DAF1602352000000000000
18DAF1602400000000000000
18DAF1602500000000000000
18DAF1602600000000000000
18DAF1602700000000000000
18DAF1602800005555555555
""", {"CIVIC_AAT": 42}),
        ]
    },
    {
        "model_year": 2025,
        "tests": [
            # ODO + RUNTM
            ("""
18DAF1101039622660801FFF
18DAF11021F3FFF000000000
18DAF1102200000000000000
18DAF110230000372E3B0101
18DAF1102400040040008300
18DAF110250102F200000B0E
18DAF1102604CB06F44F0037
18DAF11027AB031F00350000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 14251,
    "CIVIC_RUNTM": 799,
}),
            ("""
18DAF1101039622660801FFF
18DAF11021F3FFF000000000
18DAF1102200000000000000
18DAF11023000037FD3B0101
18DAF1102400040040408300
18DAF110250102E600000562
18DAF11026018E0173370038
18DAF110277C0C5B13B00000
18DAF1102800005555555555
""", {
    "CIVIC_ODO": 14460,
    "CIVIC_RUNTM": 3163,
}),
            # AAT
            ("""
18DAF1601039627028F8F000
18DAF1602100000004020100
18DAF1602200000000003C00
18DAF160233C000000000000
18DAF1602400000000000000
18DAF1602500000000000000
18DAF1602600000000000000
18DAF1602700000000000000
18DAF1602800005555555555
""", {"CIVIC_AAT": 20}),
            ("""
18DAF1601039627028F8F000
18DAF1602100000004070101
18DAF1602200000000005500
18DAF1602351000000000000
18DAF1602400000000000000
18DAF1602500000000000000
18DAF1602600000000000000
18DAF1602700000000000000
18DAF1602800005555555555
""", {"CIVIC_AAT": 41}),
        ]
    },
]

def load_signalset(filename: str) -> str:
    """Load a signalset JSON file from the standard location."""
    signalset_path = REPO_ROOT / "signalsets" / "v3" / filename
    with open(signalset_path) as f:
        return f.read()

@pytest.mark.parametrize(
    "test_group",
    TEST_CASES,
    ids=lambda test_case: f"MY{test_case['model_year']}"
)
def test_signals(test_group: Dict[str, Any]):
    """Test signal decoding against known responses."""
    for response_hex, expected_values in test_group["tests"]:
        try:
            obd_testrunner_by_year(
                test_group['model_year'],
                response_hex,
                expected_values,
                can_id_format=CANIDFormat.TWENTY_NINE_BIT
            )
        except Exception as e:
            pytest.fail(
                f"Failed on response {response_hex} "
                f"(Model Year: {test_group['model_year']}: {e}"
            )

def get_json_files():
    """Get all JSON files from the signalsets/v3 directory."""
    signalsets_path = os.path.join(REPO_ROOT, 'signalsets', 'v3')
    json_files = glob.glob(os.path.join(signalsets_path, '*.json'))
    # Convert full paths to relative filenames
    return [os.path.basename(f) for f in json_files]

@pytest.mark.parametrize("test_file",
    get_json_files(),
    ids=lambda x: x.split('.')[0].replace('-', '_')  # Create readable test IDs
)
def test_formatting(test_file):
    """Test signal set formatting for all vehicle models in signalsets/v3/."""
    signalset_path = os.path.join(REPO_ROOT, 'signalsets', 'v3', test_file)

    formatted = format_file(signalset_path)

    with open(signalset_path) as f:
        assert f.read() == formatted

if __name__ == '__main__':
    pytest.main([__file__])
