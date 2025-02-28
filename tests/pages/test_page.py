import pytest
from ..shared_mocks import snapshot_generator, MockQRPartParser, SNAP_SUCCESS


@pytest.fixture
def mock_page_cls(mocker):
    from krux.pages import Page, Menu

    class MockPage(Page):
        def __init__(self, ctx):
            Page.__init__(
                self,
                ctx,
                Menu(
                    ctx,
                    [
                        (("Test"), mocker.MagicMock()),
                    ],
                ),
            )

    return MockPage


def test_init(mocker, m5stickv, mock_page_cls):
    from krux.pages import Page

    page = mock_page_cls(mocker.MagicMock())

    assert isinstance(page, Page)


def test_capture_qr_code(mocker, m5stickv, mock_page_cls):
    mocker.patch(
        "krux.camera.sensor.snapshot", new=snapshot_generator(outcome=SNAP_SUCCESS)
    )
    mocker.patch("krux.camera.QRPartParser", new=MockQRPartParser)
    from krux.camera import Camera

    ctx = mocker.MagicMock(
        #  input=mocker.MagicMock(
        #      wait_for_button=mocker.MagicMock(side_effect=[BUTTON_PAGE, BUTTON_ENTER, BUTTON_PAGE]),
        #  ),
        camera=Camera(),
    )

    mocker.patch("time.ticks_ms", new=lambda: 0)

    page = mock_page_cls(ctx)

    qr_code, qr_format = page.capture_qr_code()
    assert qr_code == "12345678910"
    assert qr_format == MockQRPartParser.FORMAT

    ctx.display.to_landscape.assert_has_calls([mocker.call() for _ in range(10)])
    ctx.display.to_portrait.assert_has_calls([mocker.call() for _ in range(10)])
    ctx.display.draw_centered_text.assert_has_calls(
        [
            mocker.call("10%"),
            mocker.call("20%"),
            mocker.call("30%"),
            mocker.call("40%"),
            mocker.call("50%"),
            mocker.call("60%"),
            mocker.call("70%"),
            mocker.call("80%"),
            mocker.call("90%"),
        ]
    )
