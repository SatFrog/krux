import pytest

TEST_QR = """
00000000000000000000000000000000000
01111111001110001000100110011111110
01000001010011001001011110010000010
01011101010011000010000010010111010
01011101000101010001100111010111010
01011101011010011100001010010111010
01000001010101001110111101010000010
01111111010101010101010101011111110
00000000011111011011011110000000000
01101001101011110100101101011101100
00011010001001110111011001010000010
00101011010101000000110001111101010
00011010101010101001111000100110010
00101101100101100110011000010000000
00111000110101000100101101010100010
01001101000011010111011010001101100
00001000010010110011101000100110110
00010111111001000110111100010100010
01111000111110100101000011100000000
00001111111100110000000100001101110
01011010001111001110011001010100010
01000101111001100101101001101000110
00110010110001100110010101110000110
01101111001101110101110001110001010
00110000001000111100111000011110010
01001011101011100110111111111100000
00000000010001010000111111000100010
01111111011111100100000101010101100
01000001001011101110111001000100110
01011101000100001010101101111100000
01011101011111010101001000011111110
01011101001000010000000101101100110
01000001010010000111101011001110000
01111111010000110100011011010110100
00000000000000000000000000000000000
""".strip()


@pytest.fixture
def mock_uart_cls(mocker):
    class MockUART(mocker.MagicMock):
        UART2 = 0

        def read(self, bytes):
            return 0b00000000.to_bytes(1, "big")

        def write(self, bytes):
            pass

    return MockUART


@pytest.fixture
def mock_uart_no_paper_cls(mocker):
    class MockUARTNoPaper(mocker.MagicMock):
        UART2 = 0

        def read(self, bytes):
            return 0b00000100.to_bytes(1, "big")

        def write(self, bytes):
            pass

    return MockUARTNoPaper


def test_init(mocker, m5stickv, mock_uart_cls):
    mocker.patch("krux.printers.thermal.UART", new=mock_uart_cls)
    from krux.printers.thermal import AdafruitPrinter

    p = AdafruitPrinter()

    assert isinstance(p, AdafruitPrinter)


def test_init_fails_when_no_paper(mocker, m5stickv, mock_uart_no_paper_cls):
    mocker.patch("krux.printers.thermal.UART", new=mock_uart_no_paper_cls)
    from krux.printers.thermal import AdafruitPrinter

    with pytest.raises(ValueError):
        AdafruitPrinter()


def test_clear(mocker, m5stickv, mock_uart_cls):
    mocker.patch("krux.printers.thermal.UART", new=mock_uart_cls)
    from krux.printers.thermal import AdafruitPrinter

    p = AdafruitPrinter()
    mocker.spy(p, "write_bytes")

    p.clear()

    assert p.write_bytes.call_count == 5


def test_print_qr_code(mocker, m5stickv, mock_uart_cls):
    mocker.patch("krux.printers.thermal.UART", new=mock_uart_cls)
    import krux
    from krux.printers.thermal import AdafruitPrinter

    p = AdafruitPrinter()
    mocker.spy(p, "write_bytes")
    mocker.spy(p, "feed")

    p.print_qr_code(TEST_QR)

    assert p.write_bytes.call_count == 701
    p.feed.assert_called_once()
    krux.printers.thermal.wdt.feed.assert_called()
