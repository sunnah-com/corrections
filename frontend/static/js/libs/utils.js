async function fetchJsonData(url, body) {
    let resp = await fetch(url, {
        method: body ? 'POST' : 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        body: body ? JSON.stringify(body) : null
    })
    if (resp.status == 204) {
        return null;
    }
    else if (resp.ok) {
        return resp.json();
    }
    throw new Error(`Http status ${resp.statusText}`);
}