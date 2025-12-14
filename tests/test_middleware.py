from app import create_app


def test_admin_redirects_when_not_logged():
    app = create_app()
    client = app.test_client()
    resp = client.get('/administrador/listar', follow_redirects=False)
    # Should redirect to login
    assert resp.status_code in (302, 301)


def test_admin_allows_when_admin_session():
    app = create_app()
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['user'] = {'id': 1, 'username': 'admin', 'tipo': 'ADMIN'}

    resp = client.get('/administrador/listar')
    assert resp.status_code == 200
