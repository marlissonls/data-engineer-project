import db from '../config/db.js';

export async function connect() {
    const client = await db.connect();
    return client;
};

export async function release(client) {
    client.release();
    return;
};

export async function begin(client) {
    const begin = await client.query('BEGIN');
    return;
};

export async function commit(client) {
    const commit = await client.query('COMMIT');
    return { 'error' : null };
};

export async function rollback(client) {
    const rollback = await client.query('ROLLBACK');
    return;
}