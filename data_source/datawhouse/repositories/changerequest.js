export async function selectCards(_client, _cardID) {
    const query = {
        'text': 'SELECT change_request.offeredcard_id, card.character_id, character.name, character.rarity, brand.name as brand_name, brand.series as brand_series FROM change_request INNER JOIN card ON change_request.offeredcard_id = card.id INNER JOIN character ON card.character_id = character.id INNER JOIN brand ON character.brand = brand.id WHERE change_request.requestcard_id = $1 AND change_request.finished_at IS NULL AND change_request.cancelled_at IS NULL',
        'values': [_cardID]
    };
    const res = await _client.query(query);
    return {'cards': res.rows, 'error': null};
};

export async function filterCards(_client, _cardID, _filter) {
    const query = {
        'text': 'SELECT change_request.offeredcard_id, card.character_id, character.name, character.rarity, brand.name as brand_name, brand.series as brand_series FROM change_request INNER JOIN card ON change_request.offeredcard_id = card.id INNER JOIN character ON card.character_id = character.id INNER JOIN brand ON character.brand = brand.id WHERE change_request.requestcard_id = $1 AND change_request.finished_at IS NULL AND change_request.cancelled_at IS NULL AND character.name ILIKE $2',
        'values': [_cardID, `%${_filter}%`]
    };
    const res = await _client.query(query);
    return {'cards': res.rows, 'error': null};
};

export async function checkChangeRequest(_client, _offeredcardID, _requestcardID) {
    const query = {
        'text': `SELECT * FROM change_request WHERE (requestcard_id, offeredcard_id) IN (($1, $2), ($2, $1));`,
        'values': [_requestcardID, _offeredcardID]
    }
    const res = await _client.query(query);
    if (res.rows.length > 0) {
        throw new Error('Esse pedido de troca já existe!')
    }
    return {'error': null};
}

export async function createChangeRequest(_client, _offeredcardID, _requestcardID) {
    const query = {
        'text': 'INSERT INTO change_request (requestcard_id,offeredcard_id) VALUES ($1,$2)',
        'values': [_requestcardID, _offeredcardID]
    }
    const res = await _client.query(query);
    return {'res': 'Pedido de troca realizado!', 'error': null};
}

export async function selectChangeRequest(_client, _reqcardID, _offcardID) {
    const query = {
        'text': 'SELECT cancelled_at FROM change_request WHERE requestcard_id = $1 AND offeredcard_id = $2',
        'values': [_reqcardID, _offcardID]
    };
    const res = await _client.query(query);
    if (res.rows[0].cancelled_at !== null) {
        throw new Error('Pedido de troca foi cancelado!')
    }
    return {'error': null}
}

export async function deleteCardFromOriginalUser(_client, _cardID) {
    const query = {
        'text': 'UPDATE card SET deleted_at = now() WHERE id = $1 RETURNING user_id, character_id',
        'values': [_cardID]
    };
    const res = await _client.query(query);
    return {'user_id': res.rows[0].user_id, 'character_id': res.rows[0].character_id, 'error': null}
}

export async function finishChangeRequest(_client, _reqcardID, _offcardID) {
    const query = {
        'text': 'UPDATE change_request SET finished_at = now() WHERE requestcard_id = $1 AND offeredcard_id = $2',
        'values': [_reqcardID, _offcardID]
    }
    const res = await _client.query(query);
    return {'error': null}
}

export async function cancelAnyOpenTrades(_client, _cardID) {
    const query = {
        'text': 'UPDATE change_request SET cancelled_at = now() WHERE (requestcard_id = $1 AND finished_at IS NULL) OR (offeredcard_id = $1 AND finished_at IS NULL)',
        'values': [_cardID]
    }
    const res = await _client.query(query);
    return {'error': null };
}

export async function reopenTrades(_client, _cardID) {
    const query = {
        'text': 'UPDATE change_request SET cancelled_at = NULL WHERE (requestcard_id = $1 AND finished_at IS NULL) OR (offeredcard_id = $1 AND finished_at IS NULL)',
        'values': [_cardID]
    }
    const res = await _client.query(query);
    return {'error': null };
}