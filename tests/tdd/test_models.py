def test_model(db,member):
    assert member.id
    assert member.username
    assert not member.avatar_thumbnail