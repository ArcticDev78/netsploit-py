"""
Tests for utils/secure_utils.py

Covers:
  - validate_ip_address
  - validate_ip_range
  - validate_port
  - validate_hostname
  - get_privilege_prefix
  - run_user_command
"""

import shlex
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from utils.secure_utils import (
    get_privilege_prefix,
    run_user_command,
    validate_hostname,
    validate_ip_address,
    validate_ip_range,
    validate_port,
)

# ---------------------------------------------------------------------------
# validate_ip_address
# ---------------------------------------------------------------------------


class TestValidateIpAddress:
    @pytest.mark.parametrize(
        "ip",
        [
            "192.168.1.1",
            "10.0.0.1",
            "255.255.255.255",
            "0.0.0.0",
        ],
    )
    def test_valid_ipv4(self, ip):
        assert validate_ip_address(ip) is True

    @pytest.mark.parametrize(
        "ip",
        [
            "::1",
            "2001:db8::1",
        ],
    )
    def test_valid_ipv6(self, ip):
        assert validate_ip_address(ip) is True

    @pytest.mark.parametrize(
        "ip",
        [
            "999.999.999.999",
            "not_an_ip",
            "",
            "192.168.1",
            "192.168.1.1.1",
        ],
    )
    def test_invalid_ip(self, ip):
        assert validate_ip_address(ip) is False


# ---------------------------------------------------------------------------
# validate_ip_range
# ---------------------------------------------------------------------------


class TestValidateIpRange:
    # --- CIDR ---

    @pytest.mark.parametrize(
        "cidr",
        [
            "192.168.0.0/24",
            "10.0.0.0/8",
        ],
    )
    def test_valid_private_cidr(self, cidr):
        assert validate_ip_range(cidr, restrict_to_private=True) is True

    def test_public_cidr_rejected_when_restricted(self):
        assert validate_ip_range("8.8.8.0/24", restrict_to_private=True) is False

    def test_public_cidr_accepted_when_unrestricted(self):
        assert validate_ip_range("8.8.8.0/24", restrict_to_private=False) is True

    # --- Dash range ---

    def test_valid_private_dash_range(self):
        assert (
            validate_ip_range("192.168.1.1-192.168.1.10", restrict_to_private=True)
            is True
        )

    @pytest.mark.parametrize(
        "ip_range",
        [
            "192.168.1.10-192.168.1.1",  # start > end
            "192.168.1.5-192.168.1.5",  # start == end
        ],
    )
    def test_invalid_dash_range_start_gte_end(self, ip_range):
        assert validate_ip_range(ip_range) is False

    @pytest.mark.parametrize(
        "ip_range",
        [
            "not_a_range",
            "192.168.1.1",
            "",
        ],
    )
    def test_invalid_range_format(self, ip_range):
        assert validate_ip_range(ip_range) is False

    def test_mixed_ip_version_dash_range(self):
        """An IPv4 start and IPv6 end must be rejected regardless of restrict flag."""
        assert validate_ip_range("192.168.1.1-::1", restrict_to_private=False) is False
        assert validate_ip_range("192.168.1.1-::1", restrict_to_private=True) is False


# ---------------------------------------------------------------------------
# validate_port
# ---------------------------------------------------------------------------


class TestValidatePort:
    @pytest.mark.parametrize("port", [1024, 8080, 65535])
    def test_valid_unprivileged(self, port):
        assert validate_port(port, allow_privileged=False) is True

    @pytest.mark.parametrize("port", [1, 80, 443, 1023])
    def test_invalid_unprivileged_too_low(self, port):
        assert validate_port(port, allow_privileged=False) is False

    @pytest.mark.parametrize("port", [1, 80, 443])
    def test_valid_privileged(self, port):
        assert validate_port(port, allow_privileged=True) is True

    @pytest.mark.parametrize("port", [0, 65536, -1])
    def test_out_of_range(self, port):
        assert validate_port(port, allow_privileged=True) is False

    def test_string_valid(self):
        assert validate_port("8080") is True

    def test_string_invalid(self):
        assert validate_port("abc") is False

    def test_none_invalid(self):
        assert validate_port(None) is False  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# validate_hostname
# ---------------------------------------------------------------------------


class TestValidateHostname:
    @pytest.mark.parametrize(
        "hostname",
        [
            "example.com",
            "sub.example.com",
            "my-host.local",
        ],
    )
    def test_valid_hostnames(self, hostname):
        assert validate_hostname(hostname) is True

    def test_valid_with_trailing_dot(self):
        assert validate_hostname("example.com.", allow_trailing_dot=True) is True

    def test_empty_string_returns_false(self):
        assert validate_hostname("") is False

    def test_label_too_long(self):
        long_label = "a" * 64  # 64 chars → exceeds 63-char max
        hostname = f"{long_label}.com"
        assert validate_hostname(hostname) is False

    def test_hostname_too_long(self):
        # Build a hostname that is 256 characters total
        label = "a" * 63  # 63 chars
        # "aaaa...aaa.aaaa...aaa.aaaa...aaa.aaaa...aaa" — 4×63 + 3 dots = 255, add one more char
        filler = ".".join(["a" * 63] * 3)  # 63+1+63+1+63 = 191 chars
        hostname = filler + "." + "b" * (256 - len(filler) - 1)
        assert len(hostname) > 255
        assert validate_hostname(hostname) is False

    def test_leading_hyphen_in_label(self):
        assert validate_hostname("-invalid.com") is False

    def test_trailing_hyphen_in_label(self):
        assert validate_hostname("invalid-.com") is False

    def test_underscore_rejected_by_default(self):
        assert validate_hostname("my_host.com", allow_underscores=False) is False

    def test_underscore_allowed_when_permitted(self):
        assert validate_hostname("my_host.com", allow_underscores=True) is True


# ---------------------------------------------------------------------------
# get_privilege_prefix
# ---------------------------------------------------------------------------


class TestGetPrivilegePrefix:
    def test_windows_returns_empty_list(self):
        with patch("utils.secure_utils.os.name", "nt"):
            result = get_privilege_prefix()
        assert result == []

    def test_posix_returns_sudo(self):
        with patch("utils.secure_utils.os.name", "posix"):
            result = get_privilege_prefix()
        assert result == ["sudo"]


# ---------------------------------------------------------------------------
# run_user_command
# ---------------------------------------------------------------------------


class TestRunUserCommand:
    def test_list_cmd_calls_subprocess_with_list_and_shell_false(self):
        """When cmd is a list, subprocess.run should be called with shell=False and the list."""
        cmd = ["echo", "hello"]
        mock_result = MagicMock(spec=subprocess.CompletedProcess)

        with patch(
            "utils.secure_utils.subprocess.run", return_value=mock_result
        ) as mock_run:
            result = run_user_command(cmd)

        mock_run.assert_called_once()
        call_args, call_kwargs = mock_run.call_args
        # First positional arg is the command list
        assert call_args[0] == ["echo", "hello"]
        assert call_kwargs.get("shell") is False
        assert result is mock_result

    def test_string_cmd_is_shlex_split_and_shell_false(self):
        """When cmd is a string and use_shell=False, it should be split via shlex."""
        cmd_str = "ping -c 1 192.168.1.1"
        expected_args = shlex.split(cmd_str)
        mock_result = MagicMock(spec=subprocess.CompletedProcess)

        with patch(
            "utils.secure_utils.subprocess.run", return_value=mock_result
        ) as mock_run:
            result = run_user_command(cmd_str, use_shell=False)

        mock_run.assert_called_once()
        call_args, call_kwargs = mock_run.call_args
        assert call_args[0] == expected_args
        assert call_kwargs.get("shell") is False
        assert result is mock_result

    def test_use_shell_true_with_list_raises_value_error(self):
        """Passing use_shell=True together with a list cmd must raise ValueError."""
        with pytest.raises(ValueError):
            run_user_command(["echo", "hello"], use_shell=True)
