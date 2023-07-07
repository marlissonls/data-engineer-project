export async function selectUserCards(_client, _userID) {
    const query = {
        'text': 'SELECT card.id as cardid, card.character_id as characterid, card.change_available as change_available, character.name as charactername, character.rarity as characterrarity, brand.name as brand_name, brand.series as brand_series FROM card INNER JOIN character ON card.character_id = character.id INNER JOIN brand ON character.brand = brand.id WHERE card.user_id = $1 AND card.deleted_at IS NULL ORDER BY character.rarity DESC',
        'values': [_userID]
    };
    const res = await _client.query(query);
    return {'cards': res.rows, 'error': null};
};

export async function filterUserCards(_client, _userID, _filter) {
    const query = {
        'text': 'SELECT card.id as cardid, card.character_id as characterid, card.change_available as change_available, character.name as charactername, character.rarity as characterrarity, brand.name as brand_name, brand.series as brand_series FROM card INNER JOIN character ON card.character_id = character.id INNER JOIN brand ON character.brand = brand.id WHERE card.user_id = $1 AND card.deleted_at IS NULL AND character.name ILIKE $2 ORDER BY character.rarity DESC',
        'values': [_userID, `%${_filter}%`]
    };
    const res = await _client.query(query);
    return {'cards': res.rows, 'error': null};
};

export async function selectChangeableCards(_client, _userID) {
    const query = {
        'text': 'SELECT card.id as card_id, card.character_id as character_id, character.name as character_name, character.rarity as character_rarity, brand.name as brand_name, brand.series as brand_series FROM card INNER JOIN character ON card.character_id = character.id INNER JOIN brand ON character.brand = brand.id WHERE card.change_available IS TRUE AND card.user_id <> $1 AND card.deleted_at IS NULL ORDER BY character.rarity DESC',
        'values': [_userID]
    };
    const res = await _client.query(query);
    return {'cards': res.rows, 'error': null};
}

export async function filterChangeableCards(_client, _userID, _filter) {
    const query = {
        'text': 'SELECT card.id as card_id, card.character_id as character_id, character.name as character_name, character.rarity as character_rarity, brand.name as brand_name, brand.series as brand_series FROM card INNER JOIN character ON card.character_id = character.id INNER JOIN brand ON character.brand = brand.id WHERE card.change_available IS TRUE AND card.user_id <> $1 AND card.deleted_at IS NULL AND character.name ILIKE $2 ORDER BY character.rarity DESC',
        'values': [_userID, `%${_filter}%`]
    };
    const res = await _client.query(query);
    return {'cards': res.rows, 'error': null};
}

export async function selectUserChangeableCards(_client, _userID) {
    const query = {
        'text': 'SELECT card.id as card_id, card.character_id, character.name, character.rarity, brand.name as brand_name, brand.series as brand_series FROM card INNER JOIN character ON card.character_id = character.id INNER JOIN brand ON character.brand = brand.id WHERE card.change_available IS TRUE AND card.user_id = $1 AND card.deleted_at IS NULL ORDER BY character.rarity DESC',
        'values': [_userID]
    };
    const res = await _client.query(query);
    return {'cards': res.rows, 'error': null};
}

export async function filterUserChangeableCards(_client, _userID, _filter) {
    const query = {
        'text': 'SELECT card.id as card_id, card.character_id, character.name, character.rarity, brand.name as brand_name, brand.series as brand_series FROM card INNER JOIN character ON card.character_id = character.id INNER JOIN brand ON character.brand = brand.id WHERE card.change_available IS TRUE AND card.user_id = $1 AND card.deleted_at IS NULL AND character.name ILIKE $2 ORDER BY character.rarity DESC',
        'values': [_userID, `%${_filter}%`]
    };
    const res = await _client.query(query);
    return {'cards': res.rows, 'error': null};
}

export async function toggleCardChangeable(_client, _cardID, _isAvailable) {
    const query = {
        'text': 'UPDATE card SET change_available = $2 WHERE id = $1 RETURNING change_available',
        'values': [_cardID, _isAvailable]
    };
    const res = await _client.query(query);
    return {'change_available': res.rows[0].change_available, 'error': null};
}