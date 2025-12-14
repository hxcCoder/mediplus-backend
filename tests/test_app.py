from app import create_app


def test_app_creation():
    app = create_app()
    assert app is not None
    # Comprobar rutas básicas registradas
    rules = {r.endpoint for r in app.url_map.iter_rules()}
    assert 'login.login_form' in rules
    assert 'login.login_action' in rules
    assert 'login.logout' in rules
