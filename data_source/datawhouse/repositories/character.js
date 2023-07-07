// Funções usuário admin criar novo Personagem

export async function filterCharacter(_client, _brand, _name, _rarity) {
    const query = {
        'text': "SELECT id FROM character WHERE brand = $1 AND name = $2 AND rarity = $3",
        'values': [_brand, _name, _rarity]
    }
    const res = await _client.query(query);
    if (res.rows.length > 0) {
        throw new Error(`Não foi possível criar personagem pois ele já existe!`);
    }
    return { 'error': null } ;
}

export async function insertCharacter(_client, _brand, _name, _rarity) {
    const query = {
        'text': "INSERT INTO character (brand, name, rarity) VALUES ($1, $2, $3) RETURNING id",
        'values': [_brand, _name, _rarity]
    }
    const res = await _client.query(query);
    return { 'characterID': res.rows[0].id, 'error': null };
}