from schroedinger.commands.status import create_server_embed, format_bool


def test_format_bool_returns_true_label():
    result = format_bool(True, "Ja", "Nein")

    assert result == "Ja"


def test_format_bool_returns_false_label():
    result = format_bool(False, "Ja", "Nein")

    assert result == "Nein"


def test_format_bool_returns_unknown_for_none():
    result = format_bool(None, "Ja", "Nein")

    assert result == "Unbekannt"


def test_create_server_embed_returns_embed(server_status):

    embed = create_server_embed(
        server_status,
        "Minecraft Server Status",
    )

    assert embed.title == "Minecraft Server Status"
    assert embed.description == "**Mein Server**"


def test_create_server_embed_contains_status_fields(server_status):
    embed = create_server_embed(server_status, "Server Status")

    fields = {field.name: field.value for field in embed.fields}

    assert fields["🟢 Status"] == "Online"
    assert fields["👥 Spieler"] == "3 / 20"
    assert fields["📡 Ping"] == "43 ms"
    assert fields["🏷️ Version"] == "1.21"


def test_create_server_embed_none_fields(empty_server_status):
    embed = create_server_embed(empty_server_status, "Server Status")

    fields = {field.name: field.value for field in embed.fields}

    assert embed.description == "Unknown"
    assert fields["🟢 Status"] == "Unbekannt"
    assert fields["👥 Spieler"] == "Unbekannt"
    assert fields["📡 Ping"] == "Unbekannt"
    assert fields["🏷️ Version"] == "Unbekannt"
