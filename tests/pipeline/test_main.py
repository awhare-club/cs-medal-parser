from cs_medal_parser.__main__ import _build_parser


def test_default_command_is_full_run() -> None:
    args = _build_parser().parse_args([])
    assert args.command is None


def test_inspect_command() -> None:
    args = _build_parser().parse_args(["inspect"])
    assert args.command == "inspect"
