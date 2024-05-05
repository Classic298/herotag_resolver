document.getElementById('herotagForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const input = document.getElementById('herotagsInput').value;
    const herotags = input.split(/\n|;/).map(tag => tag.trim().endsWith('.elrond') ? tag : tag + '.elrond');

    fetch('https://index.multiversx.com/accounts/_search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            query: {
                bool: {
                    must: [
                        {
                            terms: {
                                "userName.keyword": herotags
                            }
                        }
                    ]
                }
            },
            size: 10000
        })
    })
    .then(response => response.json())
    .then(data => {
        const hits = data.hits.hits;
        const results = document.getElementById('results');
        const errors = document.getElementById('errors');
        results.innerHTML = '';
        errors.innerHTML = '';

        const resolved = {};
        hits.forEach(hit => {
            resolved[hit._source.userName] = hit._id;
        });

        herotags.forEach(tag => {
            if (tag in resolved) {
                results.innerHTML += `<p>${tag}: ${resolved[tag]}</p>`;
            } else {
                errors.innerHTML += `<p>Could not resolve herotag: ${tag}</p>`;
            }
        });
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('errors').textContent = 'Failed to fetch data';
    });
});
