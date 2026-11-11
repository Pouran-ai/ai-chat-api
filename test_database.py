import database
def test_save_and_get_message(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_NAME", str(test_db))
    database.init_db()
    database.save_message("user_1", "user", "Hello")
    history = database.get_chat_history("user_1")
    assert history == [
      {"role": "user", "content": "Hello"}
    ]
def test_users_have_separate_histories(tmp_path, monkeypatch):
    test_db = tmp_path / "test_users.db"
    monkeypatch.setattr(database, "DB_NAME", str(test_db))
    database.init_db()
    database.save_message("user_1", "user", "Hello from user 1")
    database.save_message("user_2", "user", "Hello from user 2")
    history_1 = database.get_chat_history("user_1")
    history_2 = database.get_chat_history("user_2")
    assert history_1 == [
    {"role": "user", "content": "Hello from user 1"}
    ]

    assert history_2 == [
    {"role": "user", "content": "Hello from user 2"}
    ]
def test_delete_user_history(tmp_path, monkeypatch):
    test_db = tmp_path / "test_delete.db"
    monkeypatch.setattr(database, "DB_NAME", str(test_db))
    database.init_db()
    database.save_message("user_1", "user", "Hello from user 1")
    database.save_message("user_2", "user", "Hello from user 2")
    deleted_count = database.delete_user_history("user_1")
    assert deleted_count == 1
    history_1 = database.get_chat_history("user_1")
    history_2 = database.get_chat_history("user_2")
    assert history_1 == []
    assert history_2 == [
    {"role": "user", "content": "Hello from user 2"}
    ]
    