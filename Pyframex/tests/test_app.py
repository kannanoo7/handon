def test_ap_run():
    from pyframex.app import App
    from pyframex.config import Config

    app = App(Config())
    app.run()