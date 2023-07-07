export async function selectPackages(_client) {
    const query = {
        'text': 'SELECT package.id as id, brand.name as brand, package.type as type, package.price as price, package.chance_rare as chance_rare, package.chance_ultrarare as chance_ultrarare FROM package INNER JOIN brand ON package.brand = brand.id ORDER BY package.brand ASC, package.type DESC'
    };
    const res = await _client.query(query);
    return {'packages': res.rows, 'error': null};
};

export async function selectFilterPackages(_client, _filter) {
    const query = {
        'text': 'SELECT package.id as id, brand.name as brand, package.type as type, package.price as price, package.chance_rare as chance_rare, package.chance_ultrarare as chance_ultrarare FROM package INNER JOIN brand ON package.brand = brand.id WHERE brand.name ILIKE $1 ORDER BY package.brand ASC, package.type DESC',
        'values': [`%${_filter}%`]
    };
    const res = await _client.query(query);
    return {'packages': res.rows, 'error': null};
};

// Funções usuário admin criar novo Pacote

export async function filterPackages(_client, _brand, _type) {
    const query = {
        'text': 'SELECT id from package WHERE brand = $1 AND type = $2',
        'values': [_brand, _type]
    }
    const res = await _client.query(query);
    if (res.rows.length > 0) {
        throw new Error(`Não foi possível criar esse pacote pois ele já existe!`);
    }
    return {'error': null };
}

export async function insertPackage(_client, _brand, _type, _price, _chancerare, _chanceultrarare) {
    const query = {
        'text': 'INSERT INTO package (brand, type, price, copies_sold, chance_rare, chance_ultrarare) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id',
        'values': [_brand, _type, _price, 0, _chancerare, _chanceultrarare]
    }
    const res = await _client.query(query);
    return {'packageID': res.rows[0].id, 'error': null };
}

// Funções de transação de compra de card: findBrand, raffleCharacter, createNewCard, debitPriceFromUserCoins

export async function findBrand(_client, _packageID) {
    const query = {
        'text': 'UPDATE package SET copies_sold = copies_sold + 1, updated_at = NOW() WHERE id = $1 RETURNING brand AS brand_id,(SELECT name FROM brand WHERE package.brand = brand.id) AS brand_name, price AS card_price, chance_rare AS rare,chance_ultrarare AS ultra_rare;',
        'values': [_packageID]
    };
    const res = await _client.query(query);
    if (res.rows.length == 0) {
        throw new Error(`Houve um erro nesta solicitação!`);
    };
    return {'res': res.rows, 'error': null};
};

export async function raffleCharacter(_client, _brandID, _rarity) {
    const query = {
        'text': 'SELECT character.id as character_id, character.name as character_name FROM character WHERE brand = $1 AND rarity = $2 ORDER BY RANDOM() LIMIT 1;',
        'values': [_brandID, _rarity]
    };
    const res = await _client.query(query);
    if (res.rows.length == 0) {
        throw new Error(`Não há personagens desta marca com esta raridade!`);
    };
    return {'res': res.rows, 'error': null};
};

export async function createNewCard(_client, _userID, _characterID) {
    const query = {
        'text': 'INSERT INTO card (user_id,character_id) VALUES ($1,$2) RETURNING id as card_id;',
        'values': [_userID, _characterID]
    };
    const res = await _client.query(query);
    if (res.rows.length == 0) {
        throw new Error(`Não foi possível criar este card!`);
    };
    return {'res': res.rows, 'error': null};
};

export async function debitPriceFromUserCoins(_client, _userID, _cardPrice) {
    const query = {
        'text': 'UPDATE users SET coins = coins - $1, updated_at = NOW() WHERE id = $2 AND coins >= $1 RETURNING coins as user_coins;',
        'values': [_cardPrice, _userID]
    };
    const res = await _client.query(query);
    if (res.rows.length == 0) {
        throw new Error(`Não foi possível realizar o pagamento do card, saldo de coins insuficiente!`);
    };
    return {'res': res.rows, 'error': null};
};